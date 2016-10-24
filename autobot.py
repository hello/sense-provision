from serial_io import SenseIO
from logger import loge, logi
import re

"""
autobot runs a list of AutobotCommand as commands
[
AutobotCommand("command", "expected", tieout),
...
]

"""
class AutobotCommand(object):
    def __init__(self, name = ""):
        self.completed = False #True if command has finished
        self.status = "FAIL"
        self.name = name

    def finish(self, status = "PASS"):
        self.completed = True
        self.status = status

    def execute(self, io):
        raise Exception("execute function not implemented")

    def get_status_string(self):
        if self.completed:
            return "%s - %s"%(self.name, self.status)
        else:
            return "%s - FAIL(Incomplete)"%(self.name)

    def did_pass(self):
        return self.status == "PASS"

class TextCommand(AutobotCommand):
    def __init__(self, command, expected, timeout):
        super(TextCommand, self).__init__(name=command)
        self.command = command
        self.expected = expected
        self.timeout = timeout
        
    def execute(self, io):
        io.write_command(self.command)
        while True:
            line = io.read_line(self.timeout)
            if line == self.expected:
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
        try:
            for command in commands:
                if not command.execute(self.io):
                    break
        except Exception as e:
            loge("Command Error %s"%(e))
        self.print_status()


    def print_status(self):
        logi("Result:")
        allpass = True
        for command in commands:
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
  
