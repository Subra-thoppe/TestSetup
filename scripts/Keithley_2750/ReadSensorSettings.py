import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

from main import *
util.setColor()

sw = Switch()
util.Purple(sw)

pga = PGA305()
util.Purple(pga)

channels = 2

for channel in range (1, channels+1):
    sw.closeOnePort(channel)
    time.sleep(1)

    pga.Activate()

    """ Pg, Tg = pga.ReadEEPROM([(6, 5), (6, 6)])
    util.Cyan(f"{channel}/{channels}", pga.ReadScanSenseSerial(), pga.ReadFullScaleRange(), Pg, Tg) """


    util.White("ScanSense Serial:", pga.ReadScanSenseSerial())
    util.White("ScanSense Test", str(pga.ReadScanSenseTestStatus()))
    util.White("ScanSense partnumber", pga.ReadScanSensePartNumber())
    util.White("Supplier Serial:", pga.ReadSupplierSerial())
    util.White("Supplier Batch:", pga.ReadSupplierBatch())
    util.White("Supplier Ess:", pga.ReadSupplierEss())
    util.White("FullScale range:", pga.ReadFullScaleRange())