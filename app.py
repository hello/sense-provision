from logger import *
from Tkinter import *
from session import provision
import time

class LOLGUI():
    def __init__(self):
        self.root = Tk()
        self.__setup()

    def __disable(self, item):
        item['state'] = 'disabled'

    def __enable(self, item):
        item['state'] = 'normal'

    def __update_result(self, res, opt_result=""):
        if res:
            self.label['text'] = "PASS"
            self.label['bg'] = 'green'
            logi("Provision PASS")
        else:
            self.label['text'] = "FAIL, %s"%opt_result
            self.label['bg'] = 'red'
            loge("Provision FAIL")

    def __do_provision(self):
        try:
            serial = self.serial_entry.get().strip()
            if serial == "":
                self.__do_reset()
                return
        except:
            self.__do_reset()
            return
        self.__disable(self.ok_button)
        self.__disable(self.reset_button)
        self.root.update()
        logi("Got Serial %s"%serial)
        try:
            res = provision(serial)
            self.__update_result(res)
        except:
            pass
        self.__bind_default_action(self.__do_reset)
        self.__enable(self.reset_button)
        self.root.update()
        
    def __bind_default_action(self, function):
        self.root.bind('<Return>', lambda event: function())
        self.root.bind('<space>', lambda event: function())
        
    def __do_connect_sense(self):
        self.__disable(self.serial_entry)
        #self.ok_button.configure(command = self.__do_provision)
        self.label['text'] = "Connect Sense"
        self.label['bg'] = 'yellow'
        #self.root.bind('<Return>', lambda event: self.__do_provision())
        #self.__bind_default_action(self.__do_provision)
        self.__do_provision()
        
    def __do_reset(self):
        self.__enable(self.ok_button)
        self.__enable(self.serial_entry)
        self.__enable(self.reset_button)
        self.label['text'] = "Please Enter Serial"
        self.label['bg'] = "white"
        self.serial_entry.delete(0, END)
        self.ok_button.configure(command = self.__do_connect_sense)
        self.serial_entry.focus_set()
        #self.root.bind('<Return>', lambda event: self.__do_connect_sense())
        self.__bind_default_action(self.__do_connect_sense)
        
    def run(self):
        self.root.mainloop()
    
    def __setup(self):
        global label
        self.root.title("SenseProvision v1")
        self.label = Label(self.root, text = "Please Enter Serial", bg="white", width=70)
        self.serial_entry = Entry(self.root, width = 80)
        self.ok_button = Button(self.root, text = "OK", command=self.__do_connect_sense, width = 30)
        self.reset_button = Button(self.root, text = "Reset", command=self.__do_reset, width = 30)
        
        self.label.pack()
        self.serial_entry.pack()
        self.ok_button.pack(side = LEFT)
        self.reset_button.pack(side = RIGHT)

        self.__do_reset()
        

    
if __name__ == "__main__":
    with open("./logs/%s.log"%(str(time.time())).split('.')[0], "w+") as fw:
        setlog(fw)
        LOLGUI().run()
