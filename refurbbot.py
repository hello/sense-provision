from autobot import *

if __name__ == "__main__":
    commands = [
        TextCommand("^ bounce", "", 30),
        IDSNCommand(),
        DelayCommand(2),
        GenKeyCommand(),
        ProvisionCommand(),
        ]
    bot = Autobot(SenseIO(), commands, verbose = True)
    bot.run()
  
