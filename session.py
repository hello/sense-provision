from serial_io import SenseIO
from logger import loge, logi
import re
import requests
class ProvisionSession:
    def __init__(self, io):
        self.io = io
        self.sig_abort = False
        self.error = None
        #to make provisioning modifications, add more conditions here
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
                line = self.io.read_line(10)
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
        if "Top Board Version" in line and self.conditions["key"] is None \
        and self.conditions["booted"] is not None:
             if not self.io.write_command("genkey"):
                self.abort("Unable to genkey")
                
    def __parse_id(self, line):
        pattern = u"^got id from top ([0-9a-f:]*)"
        match = re.search(pattern, line)
        if match:
            raw = match.group(1)
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
                
def post_key(sn, key):
    try:
        res = requests.post("https://provision.hello.is/v1/provision/%s"%(sn), data = key)	
        if res.status_code == 200:
            logi("Status %d"%(res.status_code))
            return True
        loge("Provision failed %d"%(res.status_code))
    except Exception as e:
        loge("Connection Error %s"%(str(e)))
    return False
    
def provision(serial):
    try:
        session = ProvisionSession(SenseIO())
    except Exception as e:
        loge("Serial Error %s"%(str(e)))
        return False
    if session.parse():
        logi("Got Serial %s"%(serial))
        return post_key(serial, session.conditions["key"])
    else:
        session.print_conditions()
        return False

if __name__ == "__main__":
    provision("91000101BD01163400197")
  
