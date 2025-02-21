import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))
print((os.path.abspath(".")))
exit()

from main import *
util.setColor()

channels = 4
fullScale = 690

mm = Multimeter()
util.Purple(mm)

""" sw = Switch()
util.Purple(sw) """

pga = PGA305()
util.Purple(pga)
for i in range(1):
#for channel in range(1, channels+1):
#for channel in range(2):
    #sw.closeOnePort(channel)
    #sw.closeOnePort(59)
    #exit()
    time.sleep(1)

    mA = mm.readCurrentDC() * 1000
    print(mA)
    #exit()
    if mA > 1:
        try:
            pga.Activate()
            #exit()
            """ elecslno=pga.ReadScanSenseSerial()
            print("elecsl.no",elecslno) """
           
            


            prevSerial = int("".join("".join(pga.ReadEEPROM([(12, 4), (12, 5), (12, 6), (12, 7)]))), 16)
            print(prevSerial)
            
            batchno= int("".join("".join(pga.ReadEEPROM([(13, 2), (13, 3), (13, 4)]))), 16)
            print("batchno",batchno)
            #exit()
            #decimal_value = int('137d9', 16)
            #print("decivalue",decimal_value)
            Padc, Pavg, Pdiff = pga.ReadPadc(10)
            #print("Padc, Pavg, Pdiff" ,Padc, Pavg, Pdiff)
            print(Pavg)
            Tadc, Tavg, Tdiff = pga.ReadTadc(10)
            #print("Tadc, Tavg, Tdiff",Tadc, Tavg, Tdiff)
            print(Tavg)
            #Dac = [pga.DacCalibrate(4, mm)[0]]
            #print("Dac",Dac)
            #exit()
            pga.UploadDummyData(4, mm, print=False)
            #exit()
            """ loc=list(range(0, 128))
            print(loc) """
            location_list = [(j, i) for j in range(16) for i in range(8)]
            #print(tuple_list)
            e=pga.ReadEEPROM(location_list,type_="hex",print="Reading EEPROM: ")
       
            print(e)
           
            exit()
            



            """ 
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
             """
        except Exception as e:
            util.Red(e)
            continue

        except KeyboardInterrupt:
            continue
    else:
        util.Red(f"Nothing connected on:", f"{channel}/{channels}", f"{mA} mA")