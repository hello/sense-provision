from autobot import *
import sys
if __name__ == "__main__":
    commands = [
        TextCommand("^ bounce", "", 30),
        IDSNCommand(),
        DelayCommand(2),
        GenKeyCommand(),
        ProvisionCommand(),
        ]
    bot = Autobot(SenseIO(), commands, verbose = True)
    if bot.run():
        sys.exit(0)
    sys.exit(1)
  
