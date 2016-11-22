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
"STAR005.raw",
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
"STAR105.raw",
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
            Text("^ bounce", "freertos", 10, fuzzy = True),
            DeviceInfo(color = "B"),
            #32
            Text("cd /RINGTONE", ""),
            Text("ls", ringtone32, 5, fuzzy = True),
            Delay(1.5),
            Text("cd /SLPTONES", ""),
            Text("ls", slptone32, 5, fuzzy = True),
            Delay(1.5),
            Text("cd /VOICEUI", ""),
            Text("ls", voice32, 5, fuzzy = True),
            Delay(1.5),
            #48
            Text("cd /RINGTO48", ""),
            Text("ls", ringtone48, 5, fuzzy = True),
            Delay(1.5),
            Text("cd /SLPTON48", ""),
            Text("ls", slptone48, 5, fuzzy = True),
            Delay(1.5),
            Text("cd /VOICE48", ""),
            Text("ls", voice48, 5, fuzzy = True),
            Delay(1.5),
            #the rest
            Delay(1.5),
            Provision(),
            Text("^ dfu", "got SYNC_DEVICE_ID", 60, fuzzy = True),
            ]
    else:
        commands = [
            Terminal()
            ]
            
    bot = Autobot(SenseIO(verbose = True), commands, verbose = True)
    if bot.run():
        sys.exit(0)
    sys.exit(1)
  
