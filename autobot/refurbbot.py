#!/usr/local/bin/python
from autobot import *
import sys
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "new":
        commands = [
            TextCommand("^ bounce", "", 10),
            IDSNCommand(color = "B"),
            DelayCommand(2),
            GenKeyCommand(),
            ProvisionCommand(),
            TextCommand("^ dfu", "got SYNC_DEVICE_ID", 60, fuzzy = True),
            TextCommand("^ bounce", "", 10),
            MinitermCommand()
            ]
    else:
        commands = [
            MinitermCommand()
            ]
            
    bot = Autobot(SenseIO(), commands, verbose = True)
    if bot.run():
        sys.exit(0)
    sys.exit(1)
  
