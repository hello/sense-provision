import serial
from serial.tools import list_ports
from logger import loge, logi


class SerialIO:
    def __init__(self):
        self.abort = False
        try:
            self.__get_port()
        except:
            raise
        
    def __del__(self):
        self.close()
            
    def close(self):
        self.port.close()
            
    def abort(self):
        self.abort = True

    def __get_port(self):
        ports = list_ports.comports()
        if len(ports) > 0:
            try:
                dev = ports[0].device
                logi("Opening port %s"%(dev))
                self.port = serial.Serial(port = dev,
                                     baudrate = 115200,
                                     parity = serial.PARITY_NONE,
                                     bytesize=serial.EIGHTBITS,
                                     stopbits=serial.STOPBITS_ONE,
                                     timeout = 1) 
            except Exception as e:
                loge("Unable to Open Com Port, Error %s"%(e))
                raise e

    def read_line(self):
        line = []
        while True:
            c = self.port.read()
            if len(c) is 0:
                if self.abort:
                    return
                else:
                    continue
            if ord(c) is not ord('\n'):
                line.append(c)
            else:
                return "".join(line).rstrip()

    def write_command(self, cmd):
        fmt_cmd = cmd.rstrip()+"\r\n"
        try:
            if len(fmt_cmd) == p.write(fmt_cmd):
                #logi("Input command %s Success"%cmd.rstrip())
                return True           
        except:
            pass
        loge("Input command %s Failure"%cmd.rstrip())
        return False

    

def test_port():
    import signal
    sig_abort = False
    def signal_handler(signal, frame):
        sig_abort = True
    p = SerialIO()
    while True and not sig_abort:
        line = p.read_line()
        logi(line)
        if "SYNC_DEVICE_ID" in line:
            p.write_command("genkey")

test_port()
        
    
