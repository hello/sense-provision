from serial_io import SenseIO
from logger import loge, logi
import re

"""
autobot runs a list of Text as commands
[
Text("command", "expected", tieout),
...
]

"""
from autobot import *


if __name__ == "__main__":
    commands = [
#        Text("connect Hello godsavethequeen 2", "status: http/1.1 200 ok", 10),
        Text("disconnect", "Command returned code 0", 5),
        Text("connect sensor machinesarefriends 2", "SL_NETAPP_IPV4_ACQUIRED", 30),
        Text("rm /ringtone/dig001.raw", "Command returned", 10),
        Text("rm /ringtone/dig002.raw", "Command returned", 10),
        Text("rm /ringtone/dig003.raw", "Command returned", 10),
        Text("rm /ringtone/dig004.raw", "Command returned", 10),
        Text("rm /ringtone/dig005.raw", "Command returned", 10),
        Text("rm /ringtone/new001.raw", "Command returned", 10),
        Text("rm /ringtone/new002.raw", "Command returned", 10),
        Text("rm /ringtone/new003.raw", "Command returned", 10),
        Text("rm /ringtone/new004.raw", "Command returned", 10),
        Text("rm /ringtone/new005.raw", "Command returned", 10),
        Text("rm /ringtone/new006.raw", "Command returned", 10),
        Text("rm /ringtone/org001.raw", "Command returned", 10),
        Text("rm /ringtone/org002.raw", "Command returned", 10),
        Text("rm /ringtone/org003.raw", "Command returned", 10),
        Text("rm /ringtone/org004.raw", "Command returned", 10),
        Text("rm /ringtone/org005.raw", "Command returned", 10),
        Text("rm /ringtone/star001.raw", "Command returned", 10),
        Text("rm /ringtone/star002.raw", "Command returned", 10),
        Text("rm /ringtone/star003.raw", "Command returned", 10),
        Text("rm /ringtone/star004.raw", "Command returned", 10),
        Text("rm /ringtone/star005.raw", "Command returned", 10),
        Text("rm /ringtone/pink.raw", "Command returned", 10),
        Text("rm /ringtone/tone.raw", "Command returned", 10),
        Text("rm /slptones/st001.raw", "Command returned", 10),
        Text("rm /slptones/st002.raw", "Command returned", 10),
        Text("rm /slptones/st003.raw", "Command returned", 10),
        Text("rm /slptones/st004.raw", "Command returned", 10),
        Text("rm /slptones/st006.raw", "Command returned", 10),
        Text("rm /slptones/st007.raw", "Command returned", 10),
        Text("rm /slptones/st008.raw", "Command returned", 10),
        Text("rm /slptones/st009.raw", "Command returned", 10),
        Text("rm /slptones/st010.raw", "Command returned", 10),
        Text("rm /slptones/st011.raw", "Command returned", 10),
        Text("rm /slptones/st012.raw", "Command returned", 10),
        Text("mkdir VOICEUI", "Command returned", 30),

        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/RINGTONE/DIG001.raw $f/RINGTONE/DIG001.raw", "GET returned code 200", 300),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/RINGTONE/DIG002.raw $f/RINGTONE/DIG002.raw", "GET returned code 200", 300),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/RINGTONE/DIG003.raw $f/RINGTONE/DIG003.raw", "GET returned code 200", 300),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/RINGTONE/DIG004.raw $f/RINGTONE/DIG004.raw", "GET returned code 200", 300),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/RINGTONE/DIG005.raw $f/RINGTONE/DIG005.raw", "GET returned code 200", 300),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/RINGTONE/NEW001.raw $f/RINGTONE/NEW001.raw", "GET returned code 200", 300),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/RINGTONE/NEW002.raw $f/RINGTONE/NEW002.raw", "GET returned code 200", 300),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/RINGTONE/NEW003.raw $f/RINGTONE/NEW003.raw", "GET returned code 200", 300),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/RINGTONE/NEW004.raw $f/RINGTONE/NEW004.raw", "GET returned code 200", 300),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/RINGTONE/NEW005.raw $f/RINGTONE/NEW005.raw", "GET returned code 200", 300),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/RINGTONE/NEW006.raw $f/RINGTONE/NEW006.raw", "GET returned code 200", 300),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/RINGTONE/ORG001.raw $f/RINGTONE/ORG001.raw", "GET returned code 200", 300),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/RINGTONE/ORG002.raw $f/RINGTONE/ORG002.raw", "GET returned code 200", 300),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/RINGTONE/ORG003.raw $f/RINGTONE/ORG003.raw", "GET returned code 200", 300),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/RINGTONE/ORG004.raw $f/RINGTONE/ORG004.raw", "GET returned code 200", 300),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/RINGTONE/STAR001.raw $f/RINGTONE/STAR001.raw", "GET returned code 200", 300),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/RINGTONE/STAR002.raw $f/RINGTONE/STAR002.raw", "GET returned code 200", 300),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/RINGTONE/STAR003.raw $f/RINGTONE/STAR003.raw", "GET returned code 200", 300),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/RINGTONE/STAR004.raw $f/RINGTONE/STAR004.raw", "GET returned code 200", 300),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/RINGTONE/STAR005.raw $f/RINGTONE/STAR005.raw", "GET returned code 200", 300),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/RINGTONE/pink.raw $f/RINGTONE/PINK.raw", "GET returned code 200", 300),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/RINGTONE/tone.raw $f/RINGTONE/TONE.raw", "GET returned code 200", 300),
        Text("^ bounce", "SL_NETAPP_IPV4_ACQUIRED", 60),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/SLPTONES/ST001.raw $f/SLPTONES/ST001.raw", "GET returned code 200", 200),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/SLPTONES/ST002.raw $f/SLPTONES/ST002.raw", "GET returned code 200", 200),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/SLPTONES/ST003.raw $f/SLPTONES/ST003.raw", "GET returned code 200", 200),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/SLPTONES/ST004.raw $f/SLPTONES/ST004.raw", "GET returned code 200", 200),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/SLPTONES/ST005.raw $f/SLPTONES/ST005.raw", "GET returned code 200", 200),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/SLPTONES/ST006.raw $f/SLPTONES/ST006.raw", "GET returned code 200", 200),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/SLPTONES/ST007.raw $f/SLPTONES/ST007.raw", "GET returned code 200", 200),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/SLPTONES/ST008.raw $f/SLPTONES/ST008.raw", "GET returned code 200", 200),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/SLPTONES/ST009.raw $f/SLPTONES/ST009.raw", "GET returned code 200", 500),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/SLPTONES/ST010.raw $f/SLPTONES/ST010.raw", "GET returned code 200", 400),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/SLPTONES/ST011.raw $f/SLPTONES/ST011.raw", "GET returned code 200", 400),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/SLPTONES/ST012.raw $f/SLPTONES/ST012.raw", "GET returned code 200", 400),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/VOICEUI/VUI001.raw $f/VOICEUI/VUI001.raw", "GET returned code 200", 100),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/VOICEUI/VUI002.raw $f/VOICEUI/VUI002.raw", "GET returned code 200", 100),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/VOICEUI/VUI003.raw $f/VOICEUI/VUI003.raw", "GET returned code 200", 100),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/VOICEUI/VUI004.raw $f/VOICEUI/VUI004.raw", "GET returned code 200", 100),
        Text("x $is3-us-west-1.amazonaws.com/hello-firmware-public/Rev5/VOICEUI/VUI005.raw $f/VOICEUI/VUI005.raw", "GET returned code 200", 100)



#        Text("disconnect", "SL_WLAN_DISCONNECT_EVENT", 10)
        ]
    bot = Autobot(SenseIO(verbose=True), commands, verbose = True)
    bot.run()
  
