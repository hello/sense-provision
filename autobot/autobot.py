from serial_io import SenseIO
from logger import loge, logi
import re
import time
import requests
import json

class AutobotCommand(object):
    def __init__(self, name = ""):
        self.completed = False #True if command has finished
        self.status = "FAIL"
        self.name = name

    def finish(self, status = "PASS"):
        self.completed = True
        self.status = status

    def execute(self, io, context):
        raise Exception("execute function not implemented")

    def get_status_string(self):
        if self.completed:
            return "%s\t- %s"%(self.status, self.name)
        else:
            return "FAIL\t- (Incomplete)%s"%(self.name)

    def did_pass(self):
        return self.status == "PASS"

class Text(AutobotCommand):
    def __init__(self, command, expected="", timeout=5, fuzzy=False):
        super(Text, self).__init__(name=command)
        self.command = command
        self.expected =  []
        if isinstance(expected, list) or isinstance(expected, tuple):
            self.expected.extend(expected)
        else:
            self.expected.append(expected)
        if expected == "":
            self.no_rx = True
        else:
             self.no_rx = False   
        self.timeout = timeout
        self.fuzzy = fuzzy

    def match(self, expected_line, actual_line):
        if self.fuzzy:
            if expected_line.lower() in actual_line.lower():
                return True
        else:
            if expected_line == actual_line:
                return True
        return False
    
    def intersect(self, line):
        for expected in self.expected:
            if self.match(expected, line):
                self.expected.remove(expected)
                return True
        return False
            
    def execute(self, io, context):
        io.write_command(str(self.command))
        if self.no_rx:
            self.finish()
            return True
        while True:
            try:
                line = io.read_line(self.timeout)
                self.intersect(line)
                if len(self.expected) == 0:
                    self.finish()
                    return True
            except Exception as e:
                for item in self.expected:
                    loge("Missing: %s"%(item))
                raise e
        return False
    
class Repeat(AutobotCommand):
    def __init__(self, times = 1, commands = []):
        super(Repeat, self).__init__(name="Repeat %d"%(repeat))
        self.commands = commands
        self.repeat = times

    def execute(self, io, context):
        while self.repeat != 0:
            for command in self.commands:
                if not command.execute(io, context):
                    return False
            self.repeat -= 1
        self.finish()
        return True

class Search(AutobotCommand):
    class PrintHandler:
        def on_match(self, match): #match is the regex match object
            logi(match.string)
        
    def __init__(self, regex, handler = PrintHandler(),  timeout = 60):
        super(Search, self).__init__(name="%s"%(regex))
        self.pattern = re.compile(regex)
        self.timeout = timeout
        self.handler = handler

    def execute(self, io, context):
        while True:
            try:
                line = io.read_line(self.timeout)
                result = self.pattern.match(line)
                if result:
                    self.handler.on_match(result)
                    self.finish()
                    return True
                    break
            except Exception as e:
                print e
                return False
            

class Delay(AutobotCommand):
    def __init__(self, delay):
        super(Delay, self).__init__(name="Delay %ss"%str(delay))
        self.delay = delay

    def execute(self, io, context):
        time.sleep(self.delay)
        self.finish()
        return True
           
class DeviceInfo(AutobotCommand):
    def __init__(self, color="B"):
        super(DeviceInfo, self).__init__(name="Get ID & SN")
        
        self.color = color

    def __color_code_to_num(self, code):
        if code == "B":
            return "1"
        elif code == "W":
            return "0"
        else:
            #prompt user for color
            return "1"
        
        
    def __parse_id(self, line):
        pattern = u"^got id from top ([0-9a-f:]*)"
        match = re.search(pattern, line)
        if match:
            raw = match.group(1)
            raw = raw.replace(":","").upper()
            self.id = raw
            return True
        return False
    
    def __get_id(self, io):
        while True:
            line = io.read_line(10)
            if self.__parse_id(line):
                return True
            
    def __gen_sn(self):
        template = "9100010%s%sRefurb"%(self.__color_code_to_num(self.color),
                                        self.id)
        logi("SN: %s"%(template))
        self.sn =  template
        
    def __get_auth_token(self):
        with open("auth.txt", "rU") as fr:
            return fr.readline().strip()
    
    def __get_sn(self):
        auth = self.__get_auth_token()
        logi("Getting SN from server...")
        r = requests.get("https://admin-api.hello.is/v1/key_store/sense/%s"%(self.id),
                         headers = {"Authorization": "Bearer %s"%(auth)})
        if r.status_code == 200:
            meta = json.loads(r.text)["metadata"]
            if "Refurb" not in meta:
                meta = meta + "Refurb"
            logi("SN is %s"%(meta))
            self.sn = meta
            return True
        elif r.status_code == 404:
            logi("SN not found... generating new SN")
            self.__gen_sn()
            return True
        else:
            loge(r.text)
            return False
        
    def execute(self, io, context):
        if not self.__get_id(io):
            return False
        if not self.__get_sn():
            return False
        context["id"] = self.id
        context["sn"] = self.sn
        self.finish()
        return True

class Terminal(AutobotCommand):
    def __init__(self):
        super(Terminal, self).__init__(name="Console")

    def execute(self, io, context):
        if io.terminal():
            self.finish()
            return True
        return False


        
class Provision(AutobotCommand):
    def __init__(self):
        super(Provision, self).__init__(name="Provision")
        
    def __parse_key(self, line, context):
        pattern = u"^factory key:\s*([A-F0-9]{256})"
        match = re.search(pattern, line)
        if match:
            self.key = match.group(1)
            return True            
        return False

    def genkey(self, io, context):
        io.write_command("genkey")
        while True:
            line = io.read_line(10)
            if self.__parse_key(line, context):
                context["key"] = self.key
                self.finish()
                return True
        return False
    
    def __post_key(self, sn, key):
        try:
            res = requests.post("https://provision.hello.is/v1/provision/%s"%(sn), data = key)	
            if res.status_code == 200:
                logi("Provision Status %d"%(res.status_code))
                return True
            loge("Provision failed %d"%(res.status_code))
        except Exception as e:
            loge("Connection Error %s"%(str(e)))
        return False
    
    def execute(self, io, context):
        self.genkey(io, context)
        if self.__post_key(context["sn"], context["key"]):
            self.finish()
            return True
        return False
        
         
class Autobot:
    def __init__(self, io, commands, verbose = False):
        self.io = io
        self.sig_abort = False
        self.error = None
        self.commands = commands
        self.verbose = verbose
        
    def run(self):
        context = {}
        try:
            for command in self.commands:
                if not command.execute(self.io, context):
                    break
        except Exception as e:
            loge("Command Error %s"%(e))
        return self.report_status()

    def report_status(self):
        logi("Result:")
        allpass = True
        for command in self.commands:
            logi("%s"%(command.get_status_string()))
            if not command.did_pass():
                allpass = False
        if allpass:
            logi("!!!PASS!!!")
        else:
            logi("!!!FAIL!!!")
        return allpass

"""
demo mode
"""
if __name__ == "__main__":
    logi("Tests Relocated")
  
