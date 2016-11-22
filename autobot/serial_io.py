import serial
from serial.tools import list_ports
from serial.tools import miniterm
from logger import loge, logi, logs
import os
import sys
import time


class SenseIO:
    def __init__(self, verbose = False):
        self.sig_abort = False
        self.verbose = verbose
        try:
            self.__get_port()
        except:
            raise
        
    def __del__(self):
        self.close()
            
    def close(self):
        self.port.close()
            
    def abort(self):
        self.sig_abort = True
        
    def filter_ports(self, ports):
        if os.name == "nt":
            return [port for port in ports if "COM" in port.device]
        elif os.name == "posix":
            return [port for port in ports if "serial" in port.device]
        else:
            return []

    def select_device(self, ports):
        if len(ports) == 0:
            return None
        elif len(ports) == 1:
            return ports[0].device
        else:
            while True:
                for i,d in enumerate(ports):
                    print "%d : %s"%(i, d)
                port = raw_input("Which Device?")
                try:
                    index = int(port)
                    if not 0 <= index < len(ports):
                        continue
                    else:
                        return ports[index].device
                except ValueError:
                    return None
            
        
    def __get_port(self):
        ports = list_ports.comports()
        filtered_ports = self.filter_ports(ports)
        dev = self.select_device(filtered_ports)
        if dev is None:
            raise Exception("No Serial Port Detected")
        else:
            try:
                logi("Opening port %s"%(dev))
                self.port = serial.Serial(port = dev,
                                     baudrate = 115200,
                                     parity = serial.PARITY_NONE,
                                     bytesize=serial.EIGHTBITS,
                                     stopbits=serial.STOPBITS_ONE,
                                     timeout = 1) 
                self.port.write("\r\n")
            except Exception as e:
                loge("Unable to Open Com Port, Error %s"%(e))
                raise e

    def readline(self, timeout = 0):
        line = []
        start_time = time.time()
        while True:
            if timeout > 0 and (time.time() - start_time > timeout):
                return None
            c = self.port.read()
            if len(c) is 0:
                if self.sig_abort:
                    return
                else:
                    continue
            if ord(c) is not ord('\n'):
                line.append(c)
            else:
                return "".join(line).strip()

    def write_command(self, cmd):
        fmt_cmd = cmd.rstrip()+"\r\n"
        try:
            if len(fmt_cmd) == self.port.write(fmt_cmd):
                if self.verbose:
                    logi(">%s"%cmd.rstrip())
                return True           
        except:
            pass
        loge("Input command (%s) Failure"%cmd.rstrip())
        return False

    def terminal(self):
        ok = True
        term = miniterm.Miniterm(self.port)
        term.set_rx_encoding("UTF-8")
        term.set_tx_encoding("UTF-8")
        term.exit_character = unichr(0x1d) #ctrl ]
        term.menu_character = unichr(0x14) #ctrl T
        try:
            term.start()
            term.join(True)
        except KeyboardInterrupt:
            ok = False
            pass
        term.join()
        return ok

    

def test_port():
    import signal
    sig_abort = False
    p = SenseIO()
    def signal_handler(signal, frame):
        sig_abort = True
        p.abort()

    while True and not sig_abort:
        line = p.readline()
        logs(line)
        if "SYNC_DEVICE_ID" in line:
            p.write_command("genkey")

if __name__ == "__main__":
    test_port()
        
    
