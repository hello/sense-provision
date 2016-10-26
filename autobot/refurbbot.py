#!/usr/local/bin/python
from autobot import *
import sys

ringtone32 = [
"DIG001.raw",
"DIG002.raw",
"DIG003.raw",
"DIG004.raw",
"DIG005.raw",
"NEW001.raw",
"NEW002.raw",
"NEW003.raw",
"NEW004.raw",
"NEW005.raw",
"NEW006.raw",
"ORG001.raw",
"ORG002.raw",
"ORG003.raw",
"ORG004.raw",
"PINK.raw",
"STAR001.raw",
"STAR002.raw",
"STAR003.raw",
"STAR004.raw",
#"STAR005.raw ",
"TONE.raw"
]
slptone32 = [
"ST001.raw",
"ST002.raw",
"ST003.raw",
"ST004.raw",
"ST006.raw",
"ST007.raw",
"ST008.raw",
"ST009.raw",
"ST010.raw",
"ST011.raw",
"ST012.raw",
]
voice32 = [
"VUI001.raw",
"VUI002.raw",
"VUI003.raw",
"VUI004.raw",
"VUI005.raw",
]
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
  
