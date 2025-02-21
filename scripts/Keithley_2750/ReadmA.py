import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

from main import *
util.setColor()

fullScale = 690
channels = 2

mm = Multimeter()
util.Purple(mm)

sw = Switch()
util.Purple(sw)

pga = PGA305()
util.Purple(pga)

pr = PressureReference()
util.Purple(pr)

for channel in range(1, channels+1):
#for channel in range(13,19):
#for channel in range(53,61):
    sw.openAllPorts()
    sw.closeOnePort(channel)
    time.sleep(1)

    mA = mm.readCurrentDC() * 1000
    Pr = pr.readMeasuredPressure()
    m = util.MapRange(Pr, 0, fullScale, 4, 20)
    
    if mA > 1:
        try:
            pga.Activate()
            serial = str(pga.ReadScanSenseSerial())

            Pr = pr.readMeasuredPressure()
            m = util.MapRange(Pr, 0, fullScale, 4, 20)

            if m-0.056 <= mA and mA <= m+0.056:
                util.Green(f"Reading mA:", f"{channel}/{channels}", serial, mA, m, Pr)
            else:
                util.Red(f"Reading mA:", f"{channel}/{channels}", serial, mA, m, Pr)
            
        except Exception as e:
            util.Red(e)
            continue

        except KeyboardInterrupt:
            continue
    else:
        util.Red(f"Nothing connected on:", f"{channel}/{channels}", f"{mA} mA")