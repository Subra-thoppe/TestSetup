import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

from main import *
import pathlib
util.setColor()

sw = Switch()
util.Purple(sw)

mm = Multimeter()
util.Purple(mm)

pga = PGA305()
util.Purple(pga)

tg = Telegram()
util.Purple(tg)

channels = 1

path = f"scripts/Keithley_2750/log/AdcTest_{util.date()}.csv"
pathlib.Path("scripts/Keithley_2750/log/").mkdir(parents=True, exist_ok=True)
util.writeCsv(path, ["Channel", "Date", "Time", "Serial", "Pdiff", "Tdiff", "Padc", "Tadc", "Ptime", "Ttime", *[f"Padc {i}" for i in range(1, 11)], *[f"Tadc {i}" for i in range(1, 11)]])

for channel in range(1, channels+1):
    sw.closeOnePort(channel)
    mA = mm.readCurrentDC() * 1000
    if mA > 1:
        try:
            pga.Activate()
            serial = str(pga.ReadScanSenseSerial())
            util.Cyan(f"Reading sensor: {serial}", f"{channel}/{channels}")

            t1 = time.time()
            Padc, Pavg, Pdiff = pga.ReadPadc(10)
            t2 = time.time()
            t3 = time.time()
            Tadc, Tavg, Tdiff = pga.ReadTadc(10)
            t4 = time.time()

            util.writeCsv(path, [channel, util.date(), util.time(), serial, Pdiff, Tdiff, Pavg, Tavg, t2-t1, t4-t3, *Padc, *Tadc])

        except Exception as e:
            util.writeCsv(path, [channel, f"Error {channel}: {e}"])
            util.Red(e)
            continue

        except KeyboardInterrupt:
            continue
    else:
        util.Red(f"Nothing connected on:", f"{channel}/{channels}", f"{mA} mA")