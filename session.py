from serial_io import SenseIO
from logger import loge, logi
import re
import requests
class ProvisionSession:
    def __init__(self, io):
        self.io = io
        self.sig_abort = False
        self.error = None
        self.conditions = {
            "booted":None,
            "id":None,
            "key":None
            }

    def print_conditions(self):
        for key in self.conditions:
            status = self.conditions[key]
            if status is None:
                logi("Condition (%s) not met"%key)
            else:
                logi("Condition (%s) is"%(key, self.conditions[key]))
                
    def is_complete(self):
        ret = True
        for key in self.conditions:
            status = self.conditions[key]
            if status is None:
                ret = False
        if self.error:
            ret = False
        if self.sig_abort:
            ret = False
        return ret

    def abort(self, err = "Abort"):
        self.io.abort()
        self.sig_abort = True
        self.error = err
        loge(self.error)

    def parse(self):
        while not self.is_complete():
            try:
                line = self.io.read_line(1)
            except Exception as e:
                self.abort("Serial Timeout")
                break
            #print line
            self.__parse_boot(line)
            self.__parse_id(line)
            self.__try_genkey(line)
            self.__parse_key(line)
        
        logi("Session Exit")
        return self.is_complete()

    def __parse_boot(self, line):
        if "Boot" in line:
            if self.conditions["booted"] is None:
                self.conditions["booted"] = "PASS"

    def __try_genkey(self, line):
        if "Top Board Version" in line and self.conditions["key"] is None:
             if not self.io.write_command("genkey"):
                self.abort("Unable to genkey")
                
    def __parse_id(self, line):
        pattern = u"^got id from top ([0-9a-f:]*)"
        match = re.search(pattern, line)
        if match:
            raw = match.group(10)
            raw = raw.replace(":","").upper()
            logi("found %s"%(raw))
            if self.conditions["id"] is None:
                self.conditions["id"] = raw
            
    def __parse_key(self, line):
        pattern = u"^factory key:\s*([A-F0-9]{256})"
        match = re.search(pattern, line)
        if match:
            if self.conditions["key"] is None:
                self.conditions["key"] = match.group(1)
                logi("Found Key %s"%(self.conditions["key"]))
            else:
                self.abort("Double Key")
                
def provision(sn, key):
    res = requests.post("https://provision.hello.is/v1/provision/%s"%(sn), data = key)	
    if res.status_code == 200:
        logi("Status %d"%(res.status_code))
        return True
    loge("Provision failed %d"%(res.status_code))
    return False
    
def try_provision(serial):
    session = ProvisionSession(SenseIO())
    session.print_conditions()
    if session.parse():
        print provision(serial, session.conditions["key"])

if __name__ == "__main__":
    try_provision("xxx")
  
