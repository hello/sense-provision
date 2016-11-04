#!/usr/local/bin/python
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

okcounter = OKCounter()
testcount = 3

commands = [
        Text("boot"),
        Repeat( testcount,
            Conditional(Conditional.ANY,
                Sound(FolderWalker( os.path.join(PROJECT_ROOT, "assets", "audio", "oksense"))),
                Search("OKAY SENSE", handler = okcounter, timeout = 1),
                ),
            )
        ]

Autobot(SenseIO(), commands).run()
logi("Passed %d Out of %d tests, %f"%(okcounter.passcount, testcount, okcounter.passcount * 1.0/testcount * 100))



