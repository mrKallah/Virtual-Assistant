import os
import time
import re

#.replace("\t", "").replace(" ", "").replace("index:", "").replace("[!0-9]", "")
devices = os.popen("pacmd list-sinks | grep index:").read()
devices = re.sub(r"[^(0-9\n)]", "", devices)
devices = devices.split("\n")[0:-1]

def to_volume_value(value):
    return hex(int(0x10000/100*value))


for i in devices:
    os.system('pacmd set-default-sink {}'.format(i))

    # current volume is
    volume = os.popen("amixer -c 1 -M -D pulse get Master | grep -m 1 -o -E [[:digit:]]+% | tr -d '%'").read()
    print("Volume is {}".format(volume))
    os.system("pacmd set-sink-volume {}".format(to_volume_value(50)))
    volume = os.popen("amixer -c 1 -M -D pulse get Master | grep -m 1 -o -E [[:digit:]]+% | tr -d '%'").read()
    print("Volume is {}".format(volume))
    # maybe change volume to 50 then 100 percent?
    time.sleep(3)

volume = os.popen("amixer -c 1 -M -D pulse get Master | grep -m 1 -o -E [[:digit:]]+% | tr -d '%'").read()
print("Volume is {}".format(volume))