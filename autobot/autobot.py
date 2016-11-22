from serial_io import SenseIO
from logger import loge, logi
import re
import time
import requests
import json
import pyaudio
import wave
import os


PROJECT_ROOT = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        ".."
        )
class AutobotCommand(object):
    def __init__(self, name = ""):
        self.name = name

    def execute(self, io, context):
        raise Exception("execute function not implemented")

    def get_status_string(self, passed):
        if passed:
            return "PASS\t- %s"%(self.name)
        else:
            return "FAIL\t- %s"%(self.name)

class Text(AutobotCommand):
    def __init__(self, command, expected="", timeout=5, fuzzy=True):
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
            return True

        while True:
            line = io.readline(self.timeout)
            if line == None:
                return

            self.intersect(line)
            if len(self.expected) == 0:
                return True

        for item in self.expected:
            loge("Missing: %s"%(item))
    
class Repeat(AutobotCommand):
    def __init__(self, times, *args):
        super(Repeat, self).__init__(name="Repeat %d"%(int(times)))
        self.commands = args
        self.repeat = int(times)

    def execute(self, io, context):
        while self.repeat != 0:
            for command in self.commands:
                res = command.execute(io, context)
                # logi("%s"%(command.get_status_string(res)))
                if not res:
                    return False
            self.repeat -= 1

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
        start_time = time.time()
        while True:
            line = io.readline(self.timeout)
            if line == None:
                break
            if self.timeout > 0 and (time.time() - start_time > self.timeout):
                break
            result = self.pattern.match(line)
            if result:
                self.handler.on_match(result)
                return True

class Conditional(AutobotCommand):
    NONE = 0
    ANY = 1
    ALL = 2

    def __init__(self, conditional_type, *args):
        super(Conditional, self).__init__(name="Conditional")
        self.cond = conditional_type
        self.commands = args

    def execute(self, io, context):
        pass_num = 0
        total_commands = len(self.commands)
        for command in self.commands:
            res = command.execute(io, context)
            logi("%s"%(command.get_status_string(res)))
            if res:
                pass_num += 1
            elif self.cond == self.ALL:
                break

        #any returns true if any condition is true
        if self.cond == self.NONE:
            return True
        elif self.cond == self.ANY and pass_num > 0:
            return True
        elif self.cond == self.ALL and pass_num == total_commands:
            return True
        else:
            return False
            

class Delay(AutobotCommand):
    def __init__(self, delay):
        super(Delay, self).__init__(name="Delay %ss"%str(delay))
        self.delay = delay

    def execute(self, io, context):
        time.sleep(self.delay)
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
            line = io.readline(10)
            if line == None:
                return False
            if self.__parse_id(line):
                return True
            
    def __gen_sn(self):
        template = "9100010%s%sRefurb"%(self.__color_code_to_num(self.color),
                                        self.id)
        logi("SN: %s"%(template))
        return template
        
    def __get_auth_token(self):
        with open(os.path.join(PROJECT_ROOT, "assets", "cred", "auth.txt"), "rU") as fr:
            return fr.readline().strip()
    
    def __get_sn(self):
        auth = self.__get_auth_token()
        logi("Getting SN from server...")
        r = requests.get("https://admin-api.hello.is/v1/key_store/sense/%s"%(self.id),
                         headers = {"Authorization": "Bearer %s"%(auth)})
        if r.status_code == 200:
            meta = json.loads(r.text)["metadata"]
            template = "9100"
            if "Refurb" not in meta:
                meta = meta + "Refurb"
                self.sn = meta
            elif template not in meta:
                self.sn = self.__gen_sn()
            else:
                logi("SN is %s"%(meta))
                self.sn = meta
            return True
        elif r.status_code == 404:
            logi("SN not found... generating new SN")
            self.sn = self.__gen_sn()
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
        return True

class Terminal(AutobotCommand):
    def __init__(self):
        super(Terminal, self).__init__(name="Console")

    def execute(self, io, context):
        if io.terminal():
            return True

        
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
            line = io.readline(10)
            if line == None:
                return False

            if self.__parse_key(line, context):
                context["key"] = self.key
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
            return True
        return False
        
class Sound(AutobotCommand):
    def __init__(self, aud, verbose = False):
        super(Sound, self).__init__(name="Sound")
        self.aud = aud

    def play_audio(self):
        CHUNK = 1024
        try:
            f = str(self.aud)
            player = pyaudio.PyAudio()
            logi("Playing %s"%(f))
            wf = wave.open(f, 'rb')
            stream = player.open(
                    format = player.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)
            data = wf.readframes(CHUNK)
            while data != '':
                stream.write(data)
                data = wf.readframes(CHUNK)

            stream.stop_stream()
            stream.close()
            player.terminate()
            return True
        except Exception as e:
            return False

    def execute(self, io, context):
        if self.play_audio():
            return True
        else:
            return False
         
class Autobot:
    def __init__(self, io, commands, verbose = False):
        self.io = io
        self.sig_abort = False
        self.error = None
        self.commands = commands
        self.verbose = verbose
        self.all_pass = False
        
    def run(self):
        context = {}
        tests_passed = 0
        total_tests = len(self.commands)
        try:
            for command in self.commands:
                res = command.execute(self.io, context)
                if self.verbose:
                    logi("%s"%(command.get_status_string(res)))
                if res:
                    tests_passed += 1
                else:
                    break

            if tests_passed == total_tests:
                self.app_pass = True

        except Exception as e:
            loge("Command Error %s"%(e))
        return self.report_status()

    def report_status(self):
        logi("=============Result=============")
        if self.all_pass:
            logi("!!!PASS!!!")
        else:
            logi("!!!FAIL!!!")
        return self.all_pass

"""
demo mode
"""
if __name__ == "__main__":
    logi("Tests Relocated")
  
