import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

import time
import numpy as np
from modules.PGA305.PGA305EVM import PGA305EVM
from modules import util
from crc8 import crc8

class PGA305(PGA305EVM):

    def SetPin(self, pin: int, state: int):
        util.typeCheck("pin", pin, int)
        util.typeCheck("state", state, int)
        util.minMaxCheck("state", state, 0, 1)

        if not(pin == 2 or pin == 6): # J28 = GPIO 2, J24 = GPIO 6
            util.errorCheck("PinError", "pin", pin)

        self.GPIO_WritePort(pin, state + 1)

    def ReadScanSenseSerial(self):
        h = self.ReadEEPROM([(12, 7), (12, 6), (12, 5), (12, 4)])
        return int("".join(h))
    
    def ReadScanSenseSerial_prev(self):
        h =  int("".join("".join(self.ReadEEPROM([(12, 4), (12, 5), (12, 6), (12, 7)]))), 16)
        return h

    def WriteScanSenseSerial(self, ScanSenseSerial: int):
        util.typeCheck("ScanSenseSerial", ScanSenseSerial, int)
        util.minMaxCheck("ScanSenseSerial", ScanSenseSerial, 1, 99999999)

        h = str(ScanSenseSerial).zfill(8)
        self.WriteEEPROM(12, [None, None, None, None, int(h[6:8], 16), int(h[4:6], 16), int(h[2:4], 16), int(h[0:2], 16)])
        return self.ReadScanSenseSerial()
    
    def ReadSupplierSerial(self):
        h = self.ReadEEPROM([(14, 0), (14, 1), (14, 2)])
        return int("".join(h), 16)
    
    def WriteSupplierSerial(self, SupplierSerial: int):
        util.typeCheck("SupplierSerial", SupplierSerial, int)
        util.minMaxCheck("SupplierSerial", SupplierSerial, 1, 0xFFFFFF)

        h = hex(SupplierSerial).replace("0x", "").zfill(6)
        self.WriteEEPROM(14, [int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), None, None, None, None, None])
        return self.ReadSupplierSerial()
    
    def ReadSupplierBatch(self):
        h = self.ReadEEPROM([(14, 3), (14, 4), (14, 5)])
        return int("".join(h), 16)
    
    def ReadSupplierBatch_prev(self):
        h= int("".join("".join(self.ReadEEPROM([(13, 2), (13, 3), (13, 4)]))), 16)
        return h
    
    def WriteSupplierBatch(self, SupplierBatch: int):
        util.typeCheck("SupplierBatch", SupplierBatch, int)
        util.minMaxCheck("SupplierBatch", SupplierBatch, 1, 0xFFFFFF)

        h = hex(SupplierBatch).replace("0x", "").zfill(6)
        self.WriteEEPROM(14, [None, None, None, int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), None, None])
        return self.ReadSupplierBatch()
    
    def ReadSupplierEss(self):
        h = self.ReadEEPROM([(14, 6), (14, 7)])
        return int("".join(h), 16)
    
    def WriteSupplierEss(self, essNumber: int):
        util.typeCheck("essNumber", essNumber, int)
        util.minMaxCheck("essNumber", essNumber, 1, 0xFFFF)

        h = hex(essNumber).replace("0x", "").zfill(4)
        self.WriteEEPROM(14, [None, None, None, None, None, None, int(h[0:2], 16), int(h[2:4], 16)])
        return self.ReadSupplierEss()
    
    def ReadScanSenseTestStatus(self):
        h = self.ReadEEPROM((13, 2))
        B = list(str(bin(int("".join(h), 16))).replace("0b", "").zfill(8))
        return {
            "essTest": B[0],
            "testSetup": B[1],
            "vibrationTest": B[2],
            "calibrationTest": B[3],
            "verificationTest": B[4],
            "finalTest": B[5]
        }
    
    def WriteScanSenseTestStatus(self, essTest = None, testSetup = None, vibrationTest = None, calibrationTest = None, verificationTest = None, finalTest = None):
        B = self.ReadScanSenseTestStatus()
        
        B["essTest"] = "1" if essTest else "0"
        B["testSetup"] = "1" if testSetup else "0"
        B["vibrationTest"] = "1" if vibrationTest else "0"
        B["calibrationTest"] = "1" if calibrationTest else "0"
        B["verificationTest"] = "1" if verificationTest else "0"
        B["finalTest"] = "1" if finalTest else "0"
        
        I = int("".join(B.values()).ljust(8, "0"), 2)
        self.WriteEEPROM(13, [None, None, I, None, None, None, None, None])

    def ReadFullScaleRange(self):
        h = self.ReadEEPROM([(7, 0), (7, 1)])
        return int("".join(h), 16)
    
    def WriteFullScaleRange(self, fullScale: int):
        util.typeCheck("fullScale", fullScale, int)
        util.minMaxCheck("fullScale", fullScale, 1, 0xFFFF)

        h = hex(fullScale).replace("0x", "").zfill(4)
        self.WriteEEPROM(7, [int(h[0:2], 16), int(h[2:4], 16), None, None, None, None, None, None])
        return self.ReadFullScaleRange()

    def ReadScanSensePartNumber(self):
        h = self.ReadEEPROM([(13, 3), (13, 4), (13, 5)])
        return int("".join(h), 16)
    
    def WriteScanSensePartNumber(self, partNumber: int):
        util.typeCheck("partNumber", partNumber, int)
        util.minMaxCheck("partNumber", partNumber, 1, 0xFFFFFF)

        h = hex(partNumber).replace("0x", "").zfill(6)
        self.WriteEEPROM(13, [None, None, None, int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), None, None])
        return self.ReadScanSensePartNumber()

    def ReadPadc(self, count = 10):
        util.typeCheck("count", count, int)
        
        for _ in range(5):
            self._ReadPadc()

        Padc = []
        for i in range(count):
            util.White("Reading Padc:", f"{i+1}/{count}", end="\r")
            r = self.Retry(lambda: self._ReadPadc(), "_ReadPadc()", "!None", "Can not read Padc")
            h = util.HexToInt2s(r)
            Padc.append(h)

        Pavg = round(np.median(Padc))
        Pdiff = max(Padc) - min(Padc)

        if Pdiff < 10_000:
            util.White(f"Reading Padc: {Pdiff}", f"{Pavg} = {'%.6f' % util.MapRange(Pavg)} V")
        else:
            util.Red(f"Reading Padc: {Pdiff}", f"{Pavg} = {'%.6f' % util.MapRange(Pavg)} V")

        return [Padc, Pavg, Pdiff]
    
    def ReadTadc(self, count = 10):
        util.typeCheck("count", count, int)

        for _ in range(5):
            self._ReadTadc()

        Tadc = []       
        for i in range(count):
            util.White("Reading Tadc:", f"{i+1}/{count}", end="\r")
            r =  self.Retry(lambda: self._ReadTadc(), "_ReadTadc()", "!None", "Can not read Tadc")
            h = util.HexToInt2s(r)
            Tadc.append(h)

        Tavg = round(np.median(Tadc))
        Tdiff = max(Tadc) - min(Tadc)
        
        if Tdiff < 10_000:
            util.White(f"Reading Tadc: {Tdiff}", f"{Tavg} = {'%.6f' % util.MapRange(Tavg)}V")
        else:
            util.Red(f"Reading Tadc: {Tdiff}", f"{Tavg} = {'%.6f' % util.MapRange(Tavg)}V")

        return [Tadc, Tavg, Tdiff]
    
    def ReadAllEEPROM(self):
        EEPROM = []
        for i in range(16):
            for ii in range(8):
                EEPROM.append((i, ii))
        return self.ReadEEPROM(EEPROM, print="Reading EEPROM: ")

    def UploadDefaultConfig(self):
        p0 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # 00   H0_LSB,             H0_MID,             H0_MSB,                 H1_LSB,            H1_MID,              H1_MSB,              H2_LSB,              H2_MID
        p1 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # 01   H2_MSB,             H3_LSB,             H3_MID,                 H3_MSB,            G0_LSB,              G0_MID,              G0_MSB,              G1_LSB
        p2 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # 02   G1_MID,             G1_MSB,             G2_LSB,                 G2_MID,            G2_MSB,              G3_LSB,              G3_MID,              G3_MSB
        p3 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # 03   N0_LSB,             N0_MID,             N0_MSB,                 N1_LSB,            N1_MID,              N1_MSB,              N2_LSB,              N2_MID
        p4 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # 04   N2_MSB,             N3_LSB,             N3_MID,                 N3_MSB,            M0_LSB,              M0_MID,              M0_MSB,              M1_LSB
        p5 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # 05   M1_MID,             M1_MSB,             M2_LSB,                 M2_MID,            M2_MSB,              M3_LSB,              M3_MID,              M3_MSB
        p6 = [0x66, 0x01, 0x00, 0x08, 0x01, 0x1D, 0x02, 0x20]  # 06   DIG_IF_CTRL,        DAC_CTRL_STATUS,    DAC_CONFIG,             OP_STAGE_CTRL,     BRDG_CTRL,           P_GAIN_SELECT,       T_GAIN_SELECT,       TEMP_CTRL
        p7 = [0x27, 0x0F, 0x00, 0xFF, 0x66, 0x06, 0x99, 0x39]  # 07   *FullScale_Range_1, *FullScale_Range_2, TEMP_SE,                **,                NORMAL_LOW_LSB,      NORMAL_LOW_MSB,      NORMAL_HIGH_LSB,     NORMAL_HIGH_MSB
        p8 = [0x33, 0x03, 0xCC, 0x3C, 0x00, 0x00, 0x00, 0x00]  # 08   LOW_CLAMP_LSB,      LOW_CLAMP_MSB,      HIGH_CLAMP_LSB,         HIGH_CLAMP_MSB,    PADC_GAIN_LSB,       PADC_GAIN_MID,       PADC_GAIN_MSB,       PADC_OFFSET_LSB
        p9 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # 09   PADC_OFFSET_MID,    PADC_OFFSET_MSB,    A0_LSB,                 A0_MSB,            A1_LSB,              A1_MSB,              A2_LSB,              A2_MSB
        pA = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # 10   B0_LSB,             B0_MSB,             B1_LSB,                 B1_MSB,            B2_LSB,              B2_MSB,              DIAG_ENABLE,         EEPROM_LOCK
        pB = [0x66, 0x55, 0xFF, 0xFF, 0xFF, 0x3F, 0x00, 0x00]  # 11   AFEDIAG_CFG,        AFEDIAG_MASK,       **,                     **,                FAULT_LSB,           FAULT_MSB,           TADC_GAIN_LSB,       TADC_GAIN_MID
        pC = [0x00, 0x00, 0x00, 0x00, 0x99, 0x99, 0x99, 0x99]  # 12   TADC_GAIN_MSB,      TADC_OFFSET_LSB,    TADC_OFFSET_MID,        TADC_OFFSET_MSB,   *ScanSense_Serial_1, *ScanSense_Serial_2, *ScanSense_Serial_3, *ScanSense_Serial_4
        pD = [0x01, 0x00, 0x00, 0x0F, 0x42, 0x3F, 0xFF, 0xFF]  # 13   ADC_24BIT_ENABLE,   OFFSET_ENABLE,      *ScanSense_Test_Status, *ScanSense_Part_1, *ScanSense_Part_2,   *ScanSense_Part_3    **,                  **
        pE = [0x0F, 0x42, 0x3F, 0x0F, 0x42, 0x3F, 0x27, 0x0F]  # 14   *Supplier_Serial_1, *Supplier_Serial_2, *Supplier_Serial_3      *Supplier_Batch_1, *Supplier_Batch_2,   *Supplier_Batch_3    *Supplier_Ess_1,     *Supplier_Ess_2
        pF = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x42]  # 15   **,                 **,                 **,                     **,                **,                  **,                  **,                  EEPROM_CRC_VALUE
        #                                                        register nomencalture not correct . 
        
        pages = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, pA, pB, pC, pD, pE, pF]


        for i, data in enumerate(pages):
            util.White("Writing config:", f"{i+1}/16", end="\r")
            self.WriteEEPROM(i, data)
        
        util.White("Writing config:", "OK")
        return "Uploaded"

    def CalcCoeff(self, Padc: list, Tadc: list, Dac: list, grade=2, print=True):
        util.typeCheck("Padc", Padc, list)
        util.typeCheck("Tadc", Tadc, list)
        util.typeCheck("Dac", Dac, list)

        if not (len(Padc) == len(Tadc) and len(Tadc) == len(Padc)):
            util.errorCheck("ListLengthError", "Padc, Tadc, Dac", f"{len(Padc)}, {len(Tadc)}, {len(Dac)}")

        Pgain = 1
        Poffset = (max(Padc) + min(Padc)) / -2
        Tgain = 1
        Toffset = (max(Tadc) + min(Tadc)) / -2

        Padc = list(map(lambda p: (p+Poffset)/2**22, Padc))
        Tadc = list(map(lambda t: (t+Toffset)/2**22, Tadc))
        Dac  = list(map(lambda d: (d)/2**14, Dac))

        if print:
            util.Grey("https://www.desmos.com/3d")
            for i, (p, t, d) in enumerate(zip(Padc, Tadc, Dac)):
                util.Grey(f"{chr(i+65)} = ({p}, {t}, {d})")  

        A = []
        for T, P in zip(Tadc, Padc):
            if grade == 1:
                A.append([
                    1, T, T**2, T**3,
                    P, P*T, P*(T**2), P*(T**3),
                    #P**2, P**2*T, P**2*(T**2), P**2*(T**3),
                    #P**3, P**3*T, P**3*(T**2), P**3*(T**3)
                ])
            elif grade == 2:
                A.append([
                    1, T, T**2, T**3,
                    P, P*T, P*(T**2), P*(T**3),
                    P**2, P**2*T, P**2*(T**2), P**2*(T**3),
                    #P**3, P**3*T, P**3*(T**2), P**3*(T**3)
                ])
            elif grade == 3:
                A.append([
                    1, T, T**2, T**3,
                    P, P*T, P*(T**2), P*(T**3),
                    P**2, P**2*T, P**2*(T**2), P**2*(T**3),
                    P**3, P**3*T, P**3*(T**2), P**3*(T**3)
                ])
        A = np.array(A)

        Coeff = list(np.linalg.lstsq(A, Dac, rcond=None)[0])
        Offset = [Tgain, Toffset, Pgain, Poffset]

        while len(Coeff) < 16:
            Coeff.append(0)

        if print:
            h0, h1, h2, h3, g0, g1, g2, g3, n0, n1, n2, n3, m0, m1, m2, m3 = Coeff
            z = f"z = ({h0} + {h1}*y + {h2}*y^2 + {h3}*y^3) + ({g0} + {g1}*y + {g2}*y^2 + {g3}*y^3)*x + ({n0} + {n1}*y + {n2}*y^2 + {n3}*y^3)*x^2 + ({m0} + {m1}*y + {m2}*y^2 + {m3}*y^3)*x^3"
            util.Grey(z)
            util.White("Calculated polynomial:", f"{Coeff} {Offset}")
        else:
            util.White("Calculated polynomial:", "OK")

        return Coeff, Offset
    
    def UploadCoeff(self, coeff: list, offset: list, hex=False, print=True):
        util.typeCheck("coeff", coeff, list)
        util.typeCheck("offset", offset, list)

        if not hex:
            coeff = list(map(lambda c: util.Int2sToHex(c*2**22), coeff))
            offset = list(map(lambda o: util.Int2sToHex(o), offset))
            if print:
                util.White("Uploading polynomial:", f"{coeff} {offset}")
            else:
                util.White("Uploading polynomial:", "OK")
        else:
            coeff = list(map(lambda c: str(c).zfill(6), coeff))
            offset = list(map(lambda o: str(o).zfill(6), offset))

        data = []
        for c in coeff:
            data.append(c[4:6])
            data.append(c[2:4])
            data.append(c[0:2])

        for i, p in enumerate(range(0, 48, 8)):
            d = data[p:p+8]
            util.White("Writing page:", f"{i+1}/10", end="\r")
            self.WriteEEPROM(i, list(map(lambda a: int(a, 16), d)))
        
        util.White("Writing page:", f"7/10", end="\r")
        self.WriteEEPROM(8, [None, None, None, None, int(offset[2][4:6], 16), int(offset[2][2:4], 16), int(offset[2][0:2], 16), int(offset[3][4:6], 16)])

        util.White("Writing page:", f"8/10", end="\r")
        self.WriteEEPROM(9, [int(offset[3][2:4], 16), int(offset[3][0:2], 16), None, None, None, None, None, None])

        util.White("Writing page:", f"9/10", end="\r")
        self.WriteEEPROM(11, [None, None, None, None, None, None, int(offset[0][4:6], 16), int(offset[0][2:4], 16)])

        util.White("Writing page:", f"10/10", end="\r")
        self.WriteEEPROM(12, [int(offset[0][0:2], 16), int(offset[1][4:6], 16), int(offset[1][2:4], 16), int(offset[1][0:2], 16), None, None, None, None])

        return "Uploaded"

    def UploadDummyData(self, target: int | float, mm, print=True):
        util.typeCheck("target", target, int | float)

        Padc = self.ReadPadc(10)[1]
        Dac = self.DacCalibrate(target, mm)[0]

        coeff, offset = self.CalcCoeff([Padc-1_000_000, Padc, Padc+1_000_000], [0, 0, 0], [Dac-4000, Dac, Dac+4000], grade=3, print=print)
        self.UploadCoeff(coeff, offset, print=print)
        self.CalcCRC(print=print)

        return "Uploaded"

    def CalcCRC(self, print=True):
        EEPROM = self.ReadAllEEPROM()
        EEPROM.pop()
        EEPROM_bytes = bytes.fromhex("".join(EEPROM))

        crc = int(crc8(EEPROM_bytes, 0xFF).hexdigest(), 16)

        data = [None, None, None, None, None, None, None, crc]
        self.WriteEEPROM(15, data)

        read = f"0x{self.ReadEEPROM((15, 7))[0]}"

        if print:
            util.White("Calculated CRC:", read)
        else:
            util.White("Calculated CRC:", "OK")
        return read

    def DacCalibrate(self, target: int | float, mm):
        util.typeCheck("target", target, int | float)

        self.WriteControl([0x30, 0x31, 0x67], [0x00, 0x00, 0x07])

        if target == 12:
            r = [3, 4, 5, 6, 7, 8, 9, 10]
        else:
            r = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        for v in r:
            self.SetAdditionalVoltage(v/10)

            if abs(4 - target) < 0.5:
                low = 1900
                high = 2400
            elif abs(12 - target) < 0.5:
                low = 5500
                high = 7000
            elif abs(20 - target) < 0.5:
                low = 9500
                high = 12000
            else:
                low = 2000
                high = 12000

            i = 0
            while low < high:
                i += 1
                mid = (low + high) // 2
                h = hex(mid).replace("0x", "").zfill(4).upper()
                self.WriteControl([0x30, 0x31],  [int(h[2:4], 16), int(h[0:2], 16)])
                time.sleep(0.5)
                mA = mm.readCurrentDC() * 1000
                util.White(f"Calculating DAC: {v/10}v", f"{target} mA: {mid} = {'%.6f' % mA} mA", end="\r")
                
                if mA < target:
                    low = mid + 1
                else:
                    high = mid - 1

            if abs(mA - target) > 0.01:
                continue

            print()
            self.WriteControl([0x30, 0x31, 0x67], [0x00, 0x00, 0x06])
            self.SetAdditionalVoltage(0)
            return [mid, mA]
        
        raise ValueError(f"Dac is out of range = {mid}, mA = {mA}")

if __name__ == "__main__":
    util.setColor()

    pga = PGA305()
    pga.Activate()
    util.Cyan("Connected to:", pga.serialnumber)
    util.Cyan("Firmware version:", pga.GetDeviceFirmwareVersions())
    #pga.UploadDefaultConfig()
    util.White("ScanSense SerialPREV:", pga.ReadScanSenseSerial_prev())
    util.White("Supplier Batch:", pga.ReadSupplierBatch_prev())
    
    util.White("ScanSense Serial:", pga.ReadScanSenseSerial())
    util.White("ScanSense SerialPREV:", pga.ReadScanSenseSerial_prev())
    #pga.WriteScanSenseSerial(29017)
    exit()
    util.White("ScanSense Test", str(pga.ReadScanSenseTestStatus()))
    util.White("ScanSense partnumber", pga.ReadScanSensePartNumber())
    util.White("Supplier Serial:", pga.ReadSupplierSerial())
    util.White("Supplier Batch:", pga.ReadSupplierBatch())
    util.White("Supplier Ess:", pga.ReadSupplierEss())
    util.White("FullScale range:", pga.ReadFullScaleRange())

    #util.White("ScanSense Serial:", pga.WriteScanSenseSerial(1234))
    #util.White("ScanSense Test", pga.WriteScanSenseTestStatus(123))
    #util.White("ScanSense partnumber", pga.WriteScanSensePartNumber(1234))
    #util.White("Supplier Serial:", pga.WriteSupplierSerial(1234))
    #util.White("Supplier Batch:", pga.WriteSupplierBatch(1234))
    #util.White("Supplier Ess:", pga.WriteSupplierEss(1234))
    #util.White("FullScale range:", pga.WriteFullScaleRange(1234))