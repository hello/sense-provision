import serial
from serial.tools import list_ports
from logger import loge, logi


sig_abort = False
def serial_abort():
    sig_abort = True
    
def get_port():
    ports = list_ports.comports()
    if len(ports) > 0:
        try:
            dev = ports[0].device
            logi("Opening port %s"%(dev))
            port = serial.Serial(port = dev,
                                 baudrate = 115200,
                                 parity = serial.PARITY_NONE,
                                 bytesize=serial.EIGHTBITS,
                                 stopbits=serial.STOPBITS_ONE,
                                 timeout = 1)
            return port
        except Exception as e:
            loge("Unable to Open Com Port, Error %s"%(e))

def read_line(p):
    global sig_abort
    line = []
    while True:
        c = p.read()
        if len(c) is 0:
            if sig_abort:
                return
            else:
                continue
        if ord(c) is not ord('\n'):
            line.append(c)
        else:
            return "".join(line).rstrip()
            
def test_port():
    import signal
    def signal_handler(signal, frame):
        global sig_abort
        sig_abort = True
    p = get_port()
    if p:
        while True and not sig_abort:
            logi(read_line(p))
        p.close()

test_port()
        
    
