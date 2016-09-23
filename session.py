from serial_io import SenseIO
from logger import loge, logi
import re
from timeout import timeout
class ProvisionSession:
    def __init__(self, io):
        self.io = io
        self.abort = False
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
        return ret

    def abort(self, err = "Abort"):
        self.io.abort()
        self.abort = True
        self.error = err
        loge(self.error)

    def parse(self):
        while not self.abort and not self.is_complete():
            line = self.io.read_line()
            #print line
            self.__parse_boot(line)
            self.__parse_id(line)
            self.__try_genkey(line)
            self.__parse_key(line)
        logi("Session Complete")
        return self.is_complete and not self.abort and self.error is None

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
        
            

if __name__ == "__main__":
    session = ProvisionSession(SenseIO())
    session.print_conditions()
    print session.parse()
