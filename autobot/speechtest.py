#!/usr/bin/python
from autobot import *
from serial_io import *
import os

class FolderWalker():
    def __init__(self, root):
        self.root_files =  iter([os.path.join(root, f) for f in os.listdir(root) if "wav" in f.lower()])

    def __str__(self):
        name = self.root_files.next()
        return name

class OKCounter:
    def __init__(self):
        self.passcount = 0

    def on_match(self, match): #match is the regex match object
        self.passcount += 1

class Counter(AutobotCommand):
    def __init__(self):
        super(Counter, self).__init__(name="Counter")
        self.count = 0

    def execute(self, io, context):
        self.count += 1
        return True

def test_external():
    okcounter = OKCounter()
    totalcounter = Counter()

    external_test = [
            Text("boot"),
            Text("loglevel 0x100"),
            Repeat( -1,
                Flush(),
                Sound(FolderWalker( os.path.join(PROJECT_ROOT, "assets", "audio", "oksense"))),
                Conditional(Conditional.ANY,
                    totalcounter,
                    Search("OKAY SENSE", handler = okcounter, timeout = 4),
                    Delay(2.0),
                    ),
                ),
            ]

    Autobot(SenseIO(), external_test).run()

    if totalcounter.count == 0:
        totalcounter.count = 1
    msg = "Autobot voice passed %d Out of %d tests, %f %%"%(okcounter.passcount, totalcounter.count, okcounter.passcount * 1.0/totalcounter.count * 100)
    logi(msg)
    slack(msg)

class ServerWalker():
    def __init__(self, root):
        l = ["x http://"+str(Server.ip()) + "/a/" + f +" $r x" for f in os.listdir(root) if "wav" in f.lower()]
        self.root_files =  iter(l)

    def __str__(self):
        name = self.root_files.next()
        return name

def test_internal():
    totalcounter = Counter()
    okcounter = OKCounter()
    w = ServerWalker(os.path.join(PROJECT_ROOT, "assets", "audio", "oksense"))
    internal_test = [
            Text("^ bounce", "Freertos", timeout = 10),
            Text("connect Hello godsavethequeen 2", "IPV4"),
            Text("loglevel 0x100"),
            Repeat( -1,
                Text("x %s $r x"%(w)),
                Conditional(Conditional.ANY,
                    totalcounter,
                    Search("OKAY SENSE", handler = okcounter, timeout = 4),
                )
            ),
        ]
    Autobot(SenseIO(), internal_test).run()

if __name__ == "__main__":
    # test_internal()
    test_external()
