from autobot import *
import sys
if __name__ == "__main__":
    commands = [
        TextCommand("^ bounce", "", 30),
        IDSNCommand(),
        DelayCommand(2),
        GenKeyCommand(),
        ProvisionCommand(),
        TextCommand("^ dfu", "got SYNC_DEVICE_ID", 60, fuzzy = True)
        ]
    bot = Autobot(SenseIO(), commands, verbose = True)
    if bot.run():
        sys.exit(0)
    sys.exit(1)
  
