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

    def ReadICSerial(self):
        h = self.Read(5, [0x64, 0x65, 0x66, 0x67])
        return int("".join(h), 16)
    
    def WriteICSerial(self, serialnumber: int):
        util.typeCheck("serialnumber", serialnumber, int)
        util.minMaxCheck("serialnumber", serialnumber, 0, 0xFFFFFFFF)

        h = hex(serialnumber).replace("0x", "").zfill(8).upper()
        self.WritePage(12, [None, None, None, None, int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(h[6:8], 16)])

        return self.ReadICSerial()

    def ReadICBatch(self):
        h = self.Read(5, [0x6A, 0x6B, 0x6C])
        return int("".join(h), 16)
    
    def WriteICBatch(self, batchnumber: int):
        util.typeCheck("batchnumber", batchnumber, int)
        util.minMaxCheck("batchnumber", batchnumber, 0, 0xFFFFFF)

        h = hex(batchnumber).replace("0x", "").zfill(6).upper()
        self.WritePage(13, [None, None, int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), None, None, None])

        return self.ReadICBatch()

    def ReadPadc(self, count = 10, drop = 2):
        util.typeCheck("count", count, int)

        for ii in range(5):

            Padc = []
            for _ in range(5):
                self.Read(2, [0x22, 0x21, 0x20])
                time.sleep(0.3)  #added this jeya 27,09,24

            for i in range(count):
                util.White(["Reading Padc:", f"{i+1}/{count}"], end="\r")
                r = "".join(self.Read(2, [0x22, 0x21, 0x20]))
                h = util.HexToInt2s(r)
                Padc.append(h)
                time.sleep(0.3)  #added this jeya 27,09,24


            Padc2 = Padc.copy()
            Padc2.sort()

            for _ in range(drop):
                Padc2.pop(0)
                Padc2.pop(-1)

            Pavg = round(np.median(Padc2))
            diff = max(Padc2) - min(Padc2)

            if diff > 20_000:
                util.Red(f"Retrying to read Padc, diff out of range: {diff}\tattempt: {ii+1}/5")
                continue

            util.White([f"Reading Padc: {diff}", f"{Pavg} = {round(util.MapRange(Pavg), 3)}V"])
            return Padc, Pavg, diff, "Passed"
        
        return Padc, Pavg, diff, "Failed"
    
    def ReadTadc(self, count = 10, drop = 2):
        util.typeCheck("count", count, int)

        for ii in range(5):

            Tadc = []
            for _ in range(5):
                self.Read(2, [0x26, 0x25, 0x24])
                time.sleep(0.3)  #added this jeya 27,09,24
        
            for i in range(count):
                util.White(["Reading Tadc:", f"{i+1}/{count}"], end="\r")
                r = "".join(self.Read(2, [0x26, 0x25, 0x24]))
                h = util.HexToInt2s(r)
                Tadc.append(h)
                time.sleep(0.3)  #added this jeya 27,09,24


            Tadc2 = Tadc.copy()
            Tadc2.sort()

            for _ in range(drop):
                Tadc2.pop(0)
                Tadc2.pop(-1)

            Tavg = round(np.median(Tadc2))
            diff = max(Tadc2) - min(Tadc2)
            
            if diff > 30_000:
                util.Red(f"Retrying to read Tadc, diff out of range: {diff}\tattempt: {ii+1}/5")
                continue

            util.White([f"Reading Tadc: {diff}", f"{Tavg} = {round(util.MapRange(Tavg), 3)}V"])
            return Tadc, Tavg, diff, "Passed"
        
        return Tadc, Tavg, diff, "Failed"
    
    def ReadEEPROM(self):
        return self.Read(5, list(range(0, 128)), print="Reading EEPROM: ")        

    def UploadDefaultConfig(self):
        p0 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]   # H0_LSB,           H0_MID,          H0_MSB,             H1_LSB,             H1_MID,              H1_MSB,              H2_LSB,              H2_MID
        p1 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]   # H2_MSB,           H3_LSB,          H3_MID,             H3_MSB,             G0_LSB,              G0_MID,              G0_MSB,              G1_LSB
        p2 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]   # G1_MID,           G1_MSB,          G2_LSB,             G2_MID,             G2_MSB,              G3_LSB,              G3_MID,              G3_MSB
        p3 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]   # N0_LSB,           N0_MID,          N0_MSB,             N1_LSB,             N1_MID,              N1_MSB,              N2_LSB,              N2_MID
        p4 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]   # N2_MSB,           N3_LSB,          N3_MID,             N3_MSB,             M0_LSB,              M0_MID,              M0_MSB,              M1_LSB
        p5 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]   # M1_MID,           M1_MSB,          M2_LSB,             M2_MID,             M2_MSB,              M3_LSB,              M3_MID,              M3_MSB
        p6 = [0x66, 0x01, 0x00, 0x08, 0x01, 0x1C, 0x03, 0x20]   # DIG_IF_CTRL,      DAC_CTRL_STATUS, DAC_CONFIG,         OP_STAGE_CTRL,      BRDG_CTRL,           P_GAIN_SELECT,       T_GAIN_SELECT,       TEMP_CTRL
        p7 = [0x00, 0x01, 0x00, 0x00, 0x66, 0x06, 0x99, 0x39]   # **,               **,              TEMP_SE,            **,                 NORMAL_LOW_LSB,      NORMAL_LOW_MSB,      NORMAL_HIGH_LSB,     NORMAL_HIGH_MSB
        p8 = [0x33, 0x03, 0xCC, 0x3C, 0x01, 0x00, 0x00, 0x00]   # LOW_CLAMP_LSB,    LOW_CLAMP_MSB,   HIGH_CLAMP_LSB,     HIGH_CLAMP_MSB,     PADC_GAIN_LSB,       PADC_GAIN_MID,       PADC_GAIN_MSB,       PADC_OFFSET_LSB
        p9 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]   # PADC_GAIN_MID,    PADC_OFFSET_MSB, A0_LSB,             A0_MSB,             A1_LSB,              A1_MSB,              A2_LSB,              A2_MSB
        pA = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]   # B0_LSB,           B0_MSB,          B1_LSB,             B1_MSB,             B2_LSB,              B2_MSB,              DIAG_ENABLE,         EEPROM_LOCK
        pB = [0x66, 0x55, 0xFF, 0x3F, 0xFF, 0x3F, 0x01, 0x00]   # AFEDIAG_CFG,      AFEDIAG_MASK,    **,                 **,                 FAULT_LSB,           FAULT_MSB,           TADC_GAIN_LSB,       TADC_GAIN_MID
        pC = [0x00, 0x00, 0x00, 0x00, 0x49, 0x96, 0x02, 0xD2]   # TADC_GAIN_MSB,    TADC_OFFSET_LSB, TADC_OFFSET_MID,    TADC_OFFSET_MSB,    SERIAL_NUMBER_BYTE0, SERIAL_NUMBER_BYTE1, SERIAL_NUMBER_BYTE2, SERIAL_NUMBER_BYTE3
        pD = [0x01, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]   # ADC_24BIT_ENABLE, OFFSET_ENABLE,   BATCH_NUMBER_BYTE0, BATCH_NUMBER_BYTE1, BATCH_NUMBER_BYTE2,  **,                  **,                  **
        pE = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]   # **,               **,              **,                 **,                 **,                  **,                  **,                  **
        pF = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x80]   # **,               **,              **,                 **,                 **,                  **,                  **,                  EEPROM_CRC _VALUE

        pages = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, pA, pB, pC, pD, pE, pF]

        for i, data in enumerate(pages):
            util.White(["Writing config:", f"{i+1}/16"], end="\r")
            self.WritePage(i, data)
        
        util.White(["Writing config:", "OK"])
        return "Uploaded"

    def CalcCoeff(self, Padc: list, Tadc: list, Dac: list, grade=2):
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

        h0, h1, h2, h3, g0, g1, g2, g3, n0, n1, n2, n3, m0, m1, m2, m3 = Coeff
        z = f"z = ({h0} + {h1}*y + {h2}*y^2 + {h3}*y^3) + ({g0} + {g1}*y + {g2}*y^2 + {g3}*y^3)*x + ({n0} + {n1}*y + {n2}*y^2 + {n3}*y^3)*x^2 + ({m0} + {m1}*y + {m2}*y^2 + {m3}*y^3)*x^3"
        util.Grey(z)

        util.Cyan(["Calculate coeff:", Coeff, Offset])
        return Coeff, Offset
    
    def UploadCoeff(self, coeff: list, offset: list, hex=False):
        util.typeCheck("coeff", coeff, list)
        util.typeCheck("offset", offset, list)

        if not hex:
            coeff = list(map(lambda c: util.Int2sToHex(c*2**22), coeff))
            offset = list(map(lambda o: util.Int2sToHex(o), offset))
            util.Cyan(["Uploading coeff:", coeff, offset])
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
            util.White(["Writing page:", f"{i+1}/10"], end="\r")
            self.WritePage(i, list(map(lambda a: int(a, 16), d)))
        
        util.White(["Writing page:", f"7/10"], end="\r")
        self.WritePage(8, [None, None, None, None, int(offset[2][4:6], 16), int(offset[2][2:4], 16), int(offset[2][0:2], 16), int(offset[3][4:6], 16)])

        util.White(["Writing page:", f"8/10"], end="\r")
        self.WritePage(9, [int(offset[3][2:4], 16), int(offset[3][0:2], 16), None, None, None, None, None, None])

        util.White(["Writing page:", f"9/10"], end="\r")
        self.WritePage(11, [None, None, None, None, None, None, int(offset[0][4:6], 16), int(offset[0][2:4], 16)])

        util.White(["Writing page:", f"10/10"], end="\r")
        self.WritePage(12, [int(offset[0][0:2], 16), int(offset[1][4:6], 16), int(offset[1][2:4], 16), int(offset[1][0:2], 16), None, None, None, None])

        return "Uploaded"

    def UploadDummyData(self, target: int | float, mm):
        util.typeCheck("target", target, int | float)

        Padc = self.ReadPadc(10)[1]
        Dac = self.DacCalibrate(target, mm)[0]

        coeff, offset = self.CalcCoeff([Padc, Padc*2], [0, 0], [Dac, Dac*2], grade=1)
        self.UploadCoeff(coeff, offset)
        self.CalcCRC()

        return "Uploaded"

    def CalcCRC(self):
        EEPROM = self.ReadEEPROM()
        EEPROM.pop()
        EEPROM_bytes = bytes.fromhex("".join(EEPROM))

        crc = int(crc8(EEPROM_bytes, 0xFF).hexdigest(), 16)

        data = [None, None, None, None, None, None, None, crc]
        self.WritePage(15, data)

        read = f"0x{self.Read(5, 0x7F)[0]}"

        util.Cyan(["Calculated CRC:", read])
        return read

    def DacCalibrate(self, target: int | float, mm):
        util.typeCheck("target", target, int | float)

        self.WriteControl(2, [0x30, 0x31, 0x67], [0x00, 0x00, 0x07])

        for v in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            self.SetAdditionalVoltage(v/10)
            low = 1000
            high = 11000
            i = 0
            while low < high:
                i += 1
                mid = (low + high) // 2
                h = hex(mid).replace("0x", "").zfill(4).upper()
                self.WriteControl(2, [0x30, 0x31],  [int(h[2:4], 16), int(h[0:2], 16)])
                time.sleep(0.5)
                mA = mm.readCurrentDC() * 1000
                util.White([f"Calculating DAC: {v/10}v", f"{target} mA = {mid} = {mA} mA"], end="\r")
                
                if mA < target:
                    low = mid + 1
                else:
                    high = mid - 1

            if abs(mA - target) > 0.01:
                continue

            print()
            self.WriteControl(2, [0x30, 0x31, 0x67], [0x00, 0x00, 0x06])
            self.SetAdditionalVoltage(0)
            return [mid, mA]
        
        raise ValueError("Dac is out of range")

if __name__ == "__main__":
    util.setColor()

    pga = PGA305()
    pga.Activate()
    util.Green(["Connected to:", pga.serialnumber])
    e=pga.ReadEEPROM()
    print(e)
    """ 
    util.Cyan(["Firmware version:", pga.GetDeviceFirmwareVersions()])
    #pga.UploadDefaultConfig()
    #util.Cyan(["Writing serial:", pga.WriteICSerial(12345)])
    util.Cyan(["Reading serial:", pga.ReadICSerial()])
    util.Cyan(["Reading batch:", pga.ReadICBatch()])
    #util.Cyan(["Writing batch:", pga.WriteICBatch(54321)]) """