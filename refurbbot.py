from serial_io import SenseIO
from logger import loge, logi
import re
from autobot import *
import requests


        
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
            print "FFFFF"
            return False
        elif r.status_code == 404:
            print "Still 404"
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
        
        

if __name__ == "__main__":
    commands = [
        TextCommand("^ bounce", "", 30),
        IDSNCommand(),
        DelayCommand(2),
        GenKeyCommand(),
        ProvisionCommand(),
        ]
    bot = Autobot(SenseIO(), commands, verbose = True)
    bot.run()
  
