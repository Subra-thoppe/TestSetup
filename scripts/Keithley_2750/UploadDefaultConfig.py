import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

from main import *
util.setColor()

channels = None

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
            prevSerial = pga.ReadScanSenseSerial()
            util.Cyan("Reading sensor:", prevSerial, f"{channel}/{channels}")

            pga.UploadDefaultConfig()
            pga.WriteScanSenseSerial(prevSerial)

            util.Yellow("Reading serial:", pga.ReadScanSenseSerial())

        except Exception as e:
            util.Red(e)
    else:
        util.Red("Nothing connected on:", f"{channel}/{channels}", f"{mA} mA")