from serial_io import SenseIO
from logger import loge, logi
import re

"""
autobot takes a list of tuples as commands
[
("command", "expected", "timeout"),
...
]

"""
class AutobotCommand:
    def __init__(self, command, expected, timeout):
        self.completed = False
        self.command = command
        self.expected = expected
        self.timeout = timeout
        self.status = "Incomplete"

    def complete(self, status = "Completed"):
        self.completed = True
        self.status = status
        
class Autobot:
    def __init__(self, io, commands, verbose = False):
        self.io = io
        self.sig_abort = False
        self.error = None
        self.commands = commands
        self.verbose = verbose
        
    def run(self):
        for command in commands:
            if not self.execute(command):
                break
        self.print_status()

    def execute(self, command):
        try:
            self.io.write_command(command.command)
            while True:
                line = self.io.read_line(command.timeout)
                if self.verbose:
                    logi(line)
                if line == command.expected:
                    command.complete()
                    return True
        except Exception as e:
            loge("Command Error %s"%(e))
            pass 
        return False

    def print_status(self):
        logi("Result:")
        allpass = True
        for command in commands:
            logi("Command %s Status %s"%(command.command, command.status))
            if not command.completed:
                allpass = False
        if allpass:
            logi("PASS")
        else:
            logi("FAIL")



if __name__ == "__main__":
    commands = [
        AutobotCommand("connect Hello godsavethequeen 2", "SL_NETAPP_IPV4_ACQUIRED", 10),
        AutobotCommand("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/SLPTONES/ST007.raw $f/SLPTONES/ST007.raw", "Cmd Stream transfer exited with code -2", 30),
        AutobotCommand("disconnect", "SL_WLAN_DISCONNECT_EVENT", 10)
        ]
    bot = Autobot(SenseIO(), commands, verbose = True)
    bot.run()
  
