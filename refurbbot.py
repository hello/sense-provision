from serial_io import SenseIO
from logger import loge, logi
import re
from autobot import *

class RefurbCommand(AutobotCommand):
    def __init__(self):
        super(RefurbCommand, self).__init__(name="Refurb")

    def __get_id(self, io):
        io.write_command("^ id")
        while True:
            line = io.read_line(60)
            logi(line)
            
        
    def execute(self, io):
        self.__get_id(io)
        

if __name__ == "__main__":
    commands = [
        RefurbCommand(),
        ]
    bot = Autobot(SenseIO(), commands, verbose = True)
    bot.run()
  
