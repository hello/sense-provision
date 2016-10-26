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
"STAR005.raw ",
"TONE.raw"
]
ringtone48 = [
"DIG101.raw",
"DIG102.raw",
"DIG103.raw",
"DIG104.raw",
"DIG105.raw",
"NEW101.raw",
"NEW102.raw",
"NEW103.raw",
"NEW104.raw",
"NEW105.raw",
"NEW106.raw",
"ORG101.raw",
"ORG102.raw",
"ORG103.raw",
"ORG104.raw",
"ORG105.raw",
"PINK1.raw",
"STAR101.raw",
"STAR102.raw",
"STAR103.raw",
"STAR104.raw",
"STAR105.raw ",
"TONE1.raw"
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
slptone48 = [
"ST101.raw",
"ST102.raw",
"ST103.raw",
"ST104.raw",
"ST106.raw",
"ST107.raw",
"ST108.raw",
"ST109.raw",
"ST110.raw",
"ST111.raw",
"ST112.raw",
]
voice32 = [
"VUI001.raw",
"VUI002.raw",
"VUI003.raw",
"VUI004.raw",
"VUI005.raw",
]
voice48 = [
"VUI101.raw",
"VUI102.raw",
"VUI103.raw",
"VUI104.raw",
"VUI105.raw",
]
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "new":
        commands = [
            TextCommand("^ bounce", "", 10),
            #32
            TextCommand("cd /RINGTONE", "", 5),
            TextCommand("ls", ringtone32, 2, fuzzy = True),
            TextCommand("cd /SLPTONES", "", 5),
            TextCommand("ls", slptone32, 2, fuzzy = True),
            TextCommand("cd /VOICEUI", "", 5),
            TextCommand("ls", voice32, 2, fuzzy = True),
            #48
            TextCommand("cd /RINGTO48", "", 5),
            TextCommand("ls", ringtone48, 2, fuzzy = True),
            TextCommand("cd /SLPTON48", "", 5),
            TextCommand("ls", slptone48, 2, fuzzy = True),
            TextCommand("cd /VOICE48", "", 5),
            TextCommand("ls", voice48, 2, fuzzy = True),
            #the rest
            TextCommand("^ bounce", "", 10),
            IDSNCommand(color = "B"),
            DelayCommand(2),
            GenKeyCommand(),
            ProvisionCommand(),
            TextCommand("^ dfu", "got SYNC_DEVICE_ID", 60, fuzzy = True),
            ]
    else:
        commands = [
            MinitermCommand()
            ]
            
    bot = Autobot(SenseIO(), commands, verbose = True)
    if bot.run():
        sys.exit(0)
    sys.exit(1)
  
