import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

from main import *
util.setColor()

channels = 60
fullScale = 690

mm = Multimeter()
util.Purple(mm)

sw = Switch()
util.Purple(sw)

pga = PGA305()
util.Purple(pga)

for channel in range(1, channels+1):
#for channel in range(2):
    sw.closeOnePort(channel)
    #sw.closeOnePort(59)
    #exit()
    time.sleep(1)

    mA = mm.readCurrentDC() * 1000
    print(mA)
    #exit()
    if mA > 1:
        try:
            pga.Activate()
            prevSerial = int("".join("".join(pga.ReadEEPROM([(12, 4), (12, 5), (12, 6), (12, 7)]))), 16)
            
            #prevSerial=28097
            pga.WriteScanSenseSerial(prevSerial)
            pga.WriteFullScaleRange(fullScale)
            pga.WriteEEPROM(6, [None, None, None, None, None, 0x1D, 0x02, None])   # Pgain = 133, Tgain = 5
            #pga.WriteEEPROM(15, [None, None, None, None, None, None, None, 0x00]) # CRC off

            serial = str(pga.ReadScanSenseSerial())
            fullScale = pga.ReadFullScaleRange()
            util.White(channel, (channel+1)//2, f"{channel}/{channels}", serial, fullScale)
            pga.CalcCRC(False)
            
        except Exception as e:
            util.Red(e)
            continue

        except KeyboardInterrupt:
            continue
    else:
        util.Red(f"Nothing connected on:", f"{channel}/{channels}", f"{mA} mA")