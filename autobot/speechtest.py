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

okcounter = OKCounter()
totalcounter = Counter()

commands = [
        Text("boot"),
        Repeat( -1,
            Sound(FolderWalker( os.path.join(PROJECT_ROOT, "assets", "audio", "oksense"))),
            Conditional(Conditional.ANY,
                totalcounter,
                Search("OKAY SENSE", handler = okcounter, timeout = 4),
                Search("stop speech", timeout = 8),
                # Delay(3.0),
                ),
            ),
        ]

# Autobot(SenseIO(), commands).run()

if totalcounter.count == 0:
    totalcounter.count = 1
msg = "Autobot voice passed %d Out of %d tests, %f %%"%(okcounter.passcount, totalcounter.count, okcounter.passcount * 1.0/totalcounter.count * 100)
logi(msg)
import json
import requests
j = json.dumps({"text":msg})
print requests.post("https://hooks.slack.com/services/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", data = j)



