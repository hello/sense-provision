#!/usr/local/bin/python
from autobot import *
from serial_io import *
import os

class FolderWalker():
    def __init__(self, root):
        self.root = root
        self.root_files = os.listdir(self.root)

    def __str__(self):
        f = os.path.join(self.root, "oksense_1.wav")
        return f

commands = [
        Text("boot"),
        Repeat( 2,
            Conditional(Conditional.ALL,
                Sound(FolderWalker( os.path.join(PROJECT_ROOT, "assets", "audio", "oksense"))),
                Search("OKAY_SENSE", timeout = 1),
                ),
            )
        ]

Autobot(SenseIO(), commands).run()
