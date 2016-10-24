from serial_io import SenseIO
from logger import loge, logi
import re
import time
import requests

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
            return "%s\t\t- %s"%(self.name, self.status)
        else:
            return "%s\t\t- FAIL(Incomplete)"%(self.name)

    def did_pass(self):
        return self.status == "PASS"

class TextCommand(AutobotCommand):
    def __init__(self, command, expected, timeout):
        super(TextCommand, self).__init__(name=command)
        self.command = command
        self.expected = expected
        self.timeout = timeout
        
    def execute(self, io, context):
        io.write_command(self.command)
        while True:
            line = io.read_line(self.timeout)
            if line == self.expected:
                self.finish()
                return True
        return False

class DelayCommand(AutobotCommand):
    def __init__(self, delay):
        super(DelayCommand, self).__init__(name="Delay %ss"%str(delay))
        self.delay = delay

    def execute(self, io, context):
        time.sleep(self.delay)
        self.finish()
        return True
    
class GenKeyCommand(AutobotCommand):
    def __init__(self):
        super(GenKeyCommand, self).__init__(name="Genkey")
        
    def __parse_key(self, line, context):
        pattern = u"^factory key:\s*([A-F0-9]{256})"
        match = re.search(pattern, line)
        if match:
            self.key = match.group(1)
            return True            
        return False
    
    def execute(self, io, context):
        io.write_command("genkey")
        while True:
            line = io.read_line(10)
            if self.__parse_key(line, context):
                context["key"] = self.key
                self.finish()
                return True
        return False

        
class IDSNCommand(AutobotCommand):
    def __init__(self, color="B"):
        super(IDSNCommand, self).__init__(name="Get ID & SN")
        
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
        self.sn =  template
        
    def __get_sn(self):
        r = requests.get("https://admin-api.hello.is/v1/key_store//sense/%s"%(self.id))
        if r.status_code == 200:
            print r.text
            return False
        elif r.status_code == 404:
            logi("SN not found... generating new SN")
            self.__gen_sn()
            return True
        
    def execute(self, io, context):
        if not self.__get_id(io):
            return False
        if not self.__get_sn():
            return False
        context["id"] = self.id
        context["sn"] = self.sn
        self.finish()
        return True
        
class ProvisionCommand(AutobotCommand):
    def __init__(self):
        super(ProvisionCommand, self).__init__(name="Provision")
        
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
        self.print_status()


    def print_status(self):
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

"""
demo mode
"""
if __name__ == "__main__":
    commands = [
        TextCommand("connect Hello godsavethequeen 2", "SL_NETAPP_IPV4_ACQUIRED", 10),
        #TextCommand("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/SLPTONES/ST007.raw $f/SLPTONES/ST007.raw", "Cmd Stream transfer exited with code -2", 30),
        TextCommand("disconnect", "SL_WLAN_DISCONNECT_EVENT", 10)
        ]
    bot = Autobot(SenseIO(), commands, verbose = True)
    bot.run()
  
