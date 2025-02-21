import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

from main import *
util.setColor()

channels = None
target = 12

sw = Switch()
util.Purple(sw)

mm = Multimeter()
util.Purple(mm)

pga = PGA305()
util.Purple(pga)

for channel in range(1, channels+1):
    sw.closeOnePort(channel)
    time.sleep(1)

    mA = mm.readCurrentDC() * 1000
    if mA > 1:
        try:
            pga.Activate()
            serial = str(pga.ReadScanSenseSerial())
            util.Yellow("Writing dummy data:", serial, f"{channel}/{channels}")

            pga.UploadDummyData(target, mm, print=False)

            sw.openAllPorts()
            time.sleep(0.25)
            sw.closeOnePort(channel)
            time.sleep(0.25)

            mA = [mm.readCurrentDC() * 1000 for _ in range(10)]

            if min(mA) >= 11.9 and max(mA) <= 12.1:
                util.Green("mA test:", serial, f"min: {min(mA)}", f"max: {max(mA)}", f"{channel}/{channels}")
            else:
                util.Red("mA test:", serial, f"min: {min(mA)}", f"max: {max(mA)}", f"{channel}/{channels}")

        except Exception as e:
            util.Red(e)
    else:
        util.Red("Nothing connected on:",  f"{channel}/{channels}", f"{mA} mA")