import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))
sys.path.append("T:/ProdSW_AM5000/CommonTestSetupProgram_AM5000/python-libTestsetup-nysw")
import time
import numpy as np
from modules.PGA305.PGA305EVM_git import PGA305EVM
#from modules.PGA305.CoeffCalc import CalculateCoefficientsTi
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

    def ReadFullScaleRangeMinimum(self):
        h = self.ReadEEPROM([(7, 0), (7, 1)])
        return int("".join(h), 16) - 32767

    def WriteFullScaleRangeMinimum(self, fullScaleMin: int):
        util.typeCheck("fullScaleMin", fullScaleMin, int)
        util.minMaxCheck("fullScaleMin", fullScaleMin, -32767, 32767)

        h = hex(fullScaleMin + 32767).replace("0x", "").zfill(4)
        self.WriteEEPROM(7, [int(h[0:2], 16), int(h[2:4], 16), None, None, None, None, None, None])

    def ReadFullScaleRangeMaximum(self):
        h = self.ReadEEPROM([(11, 2), (11, 3)])
        return int("".join(h), 16) - 32767

    def WriteFullScaleRangeMaximum(self, fullScaleMax: int):
        util.typeCheck("fullScaleMax", fullScaleMax, int)
        util.minMaxCheck("fullScaleMax", fullScaleMax, -32767, 32767)

        h = hex(fullScaleMax + 32767).replace("0x", "").zfill(4)
        self.WriteEEPROM(11, [None, None, int(h[0:2], 16), int(h[2:4], 16), None, None, None, None])

    def ReadFullScaleRangeUnit(self):
        h = self.ReadEEPROM((7, 3))
        c = chr(int("".join(h), 16))

        units = {
            "B": "Bar",
            "t": "Metric Ton",
            "T": "Imperial Ton",
            "N": "Kilo Newton",
            "P": "Psi",
            "ÿ": "Undefined",
            "\x00": "Undefined"
        }

        return units[c]

    def ReadFullScaleRange(self):
        return self.ReadFullScaleRangeMaximum() - self.ReadFullScaleRangeMinimum()

    def WriteFullScaleRangeUnit(self, fullScaleUnit: str):
        util.typeCheck("fullScaleUnit", fullScaleUnit, str)

        units = {
            "Bar": "B",
            "Metric Ton": "t",
            "Imperial Ton": "T",
            "Kilo Newton": "N",
            "Psi": "P"
        }

        if fullScaleUnit not in units:
            raise ValueError(util.Red(f"fullScaleUnit can only be: [Bar, Metric Ton, Imperial Ton, Kilo Newton, Psi] = {fullScaleUnit}", ret=True))

        self.WriteEEPROM(7, [None, None, None, ord(units[fullScaleUnit]), None, None, None, None])

    def ReadScanSenseSerial(self):
        h = self.ReadEEPROM([(12, 7), (12, 6), (12, 5), (12, 4)])
        return int("".join(h))

    def WriteScanSenseSerial(self, ScanSenseSerial: int):
        util.typeCheck("ScanSenseSerial", ScanSenseSerial, int)
        util.minMaxCheck("ScanSenseSerial", ScanSenseSerial, 1, 99999999)

        h = str(ScanSenseSerial).zfill(8)
        self.WriteEEPROM(12, [None, None, None, None, int(h[6:8], 16), int(h[4:6], 16), int(h[2:4], 16), int(h[0:2], 16)])

    def ReadScanSenseTestStatus(self):
        h = self.ReadEEPROM((13, 2))
        B = list(str(bin(int("".join(h), 16))).replace("0b", "").zfill(8))

        return {
            "AoiPcbaStatus": B[0],
            "EssTemperatureCyclingAndBurnInStatus": B[1],
            "TestAndSetupStatus": B[2],
            "EssVibrationStatus": B[3],
            "CalibrationStatus": B[4],
            "ProofPressureStatus": B[5],
            "VerificationStatus": B[6],
            "FinalControl": B[7]
        }

    def WriteScanSenseTestStatus(self, AoiPcbaStatus = None, EssTemperatureCyclingAndBurnInStatus = None, TestAndSetupStatus = None, EssVibrationStatus = None, CalibrationStatus = None, ProofPressureStatus = None, VerificationStatus = None, FinalControl = None):
        B = self.ReadScanSenseTestStatus()

        B["AoiPcbaStatus"] = "1" if AoiPcbaStatus else "0"
        B["EssTemperatureCyclingAndBurnInStatus"] = "1" if EssTemperatureCyclingAndBurnInStatus else "0"
        B["TestAndSetupStatus"] = "1" if TestAndSetupStatus else "0"
        B["EssVibrationStatus"] = "1" if EssVibrationStatus else "0"
        B["CalibrationStatus"] = "1" if CalibrationStatus else "0"
        B["ProofPressureStatus"] = "1" if ProofPressureStatus else "0"
        B["VerificationStatus"] = "1" if VerificationStatus else "0"
        B["FinalControl"] = "1" if FinalControl else "0"

        I = int("".join(B.values()).ljust(8, "0"), 2)
        self.WriteEEPROM(13, [None, None, I, None, None, None, None, None])

    def ReadScanSensePartNumber(self):
        h = self.ReadEEPROM([(13, 3), (13, 4), (13, 5)])
        return int("".join(h), 16)

    def WriteScanSensePartNumber(self, partNumber: int):
        util.typeCheck("partNumber", partNumber, int)
        util.minMaxCheck("partNumber", partNumber, 1, 0xFFFFFF)

        h = hex(partNumber).replace("0x", "").zfill(6)
        self.WriteEEPROM(13, [None, None, None, int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), None, None])

    def ReadScanSenseProductionDate(self):
        h = self.ReadEEPROM([(13, 6), (13, 7)])

        return {
            "week": int(h[0], 16),
            "year": int(h[1], 16)
        }

    def WriteScanSenseProductionDate(self, week: int, year: int):
        util.typeCheck("week", week, int)
        util.typeCheck("year", year, int)
        util.minMaxCheck("week", week, 1, 55)
        util.minMaxCheck("year", year, 10, 99)

        self.WriteEEPROM(13, [None, None, None, None, None, None, week, year])

    def ReadSupplierSerial(self):
        h = self.ReadEEPROM([(14, 0), (14, 1), (14, 2)])
        return int("".join(h), 16)

    def WriteSupplierSerial(self, supplierSerial: int):
        util.typeCheck("supplierSerial", supplierSerial, int)
        util.minMaxCheck("supplierSerial", supplierSerial, 1, 0xFFFFFF)

        h = hex(supplierSerial).replace("0x", "").zfill(6)
        self.WriteEEPROM(14, [int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), None, None, None, None, None])

    def ReadSupplierBatch(self):
        h = self.ReadEEPROM([(14, 3), (14, 4), (14, 5)])
        return int("".join(h), 16)

    def WriteSupplierBatch(self, supplierBatch: int):
        util.typeCheck("supplierBatch", supplierBatch, int)
        util.minMaxCheck("supplierBatch", supplierBatch, 1, 0xFFFFFF)

        h = hex(supplierBatch).replace("0x", "").zfill(6)
        self.WriteEEPROM(14, [None, None, None, int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), None, None])

    def ReadSupplierEss(self):
        h = self.ReadEEPROM([(14, 6), (14, 7)])
        return int("".join(h), 16)

    def WriteSupplierEss(self, essNumber: int):
        util.typeCheck("essNumber", essNumber, int)
        util.minMaxCheck("essNumber", essNumber, 1, 0xFFFF)

        h = hex(essNumber).replace("0x", "").zfill(4)
        self.WriteEEPROM(14, [None, None, None, None, None, None, int(h[0:2], 16), int(h[2:4], 16)])

    def ReadTemperatureRangeMinimum(self):
        h = self.ReadEEPROM([(15, 0), (15, 1)])
        return int("".join(h), 16) - 32767

    def WriteTemperatureRangeMinimum(self, temperatureMinimum: int):
        util.typeCheck("temperatureMinimum", temperatureMinimum, int)
        util.minMaxCheck("temperatureMinimum", temperatureMinimum, -32767, 32767)

        h = hex(temperatureMinimum + 32767).replace("0x", "").zfill(4)
        self.WriteEEPROM(15, [int(h[0:2], 16), int(h[2:4], 16), None, None, None, None, None, None])

    def ReadTemperatureRangeMaximum(self):
        h = self.ReadEEPROM([(15, 3), (15, 4)])
        return int("".join(h), 16) - 32767

    def WriteTemperatureRangeMaximum(self, temperatureMaximum: int):
        util.typeCheck("temperatureMaximum", temperatureMaximum, int)
        util.minMaxCheck("temperatureMaximum", temperatureMaximum, -32767, 32767)

        h = hex(temperatureMaximum + 32767).replace("0x", "").zfill(4)
        self.WriteEEPROM(15, [None, None, None, int(h[0:2], 16), int(h[2:4], 16), None, None, None])

    def ReadTemperatureRangeUnit(self):
        h = self.ReadEEPROM((15, 2))
        c = chr(int("".join(h), 16))

        units = {
            "C": "Celsius",
            "K": "Kelvin",
            "F": "Farenheit",
            "ÿ": "Undefined",
            "\x00": "Undefined"
        }

        return units[c]

    def WriteTemperatureRangeUnit(self, temperatureUnit: str):
        util.typeCheck("temperatureUnit", temperatureUnit, str)

        units = {
            "Celsius": "C",
            "Kelvin": "K",
            "Farenheit": "F"
        }

        if temperatureUnit not in units:
            raise ValueError(util.Red(f"temperatureUnit can only be: [Celsius, Kelvin, Farenheit] = {temperatureUnit}", ret=True))

        self.WriteEEPROM(15, [None, None, ord(units[temperatureUnit]), None, None, None, None, None])

    def ReadScanSenseEX(self):
        h = self.ReadEEPROM((15, 5))
        return int("".join(h), 16)

    def WriteScanSenseEX(self, ex: int):
        util.typeCheck("ex", ex, int)
        util.minMaxCheck("ex", ex, 0, 1)

        self.WriteEEPROM(15, [None, None, None, None, None, ex, None, None])

    def ReadCustomerSpecificRequirements(self):
        h = self.ReadEEPROM((15, 5))
        return int("".join(h), 16)

    def WriteCustomerSpecificRequirements(self, specificRequirements: int):
        util.typeCheck("specificRequirements", specificRequirements, int)
        util.minMaxCheck("specificRequirements", specificRequirements, 0, 1)

        self.WriteEEPROM(15, [None, None, None, None, None, specificRequirements, None, None])

    def ReadPgain(self):
        i = self.ReadEEPROM((6, 5), type_="int")[0]
        Pgains = [5, 5.48, 5.97, 6.56, 7.02, 8, 9.09, 10, 10.53, 11.11, 12.5, 13.33, 14.29, 16, 17.39, 18.18, 19.05, 20, 22.22, 25, 30.77, 36.36, 40, 44.44, 50, 57.14, 66.67, 80, 100, 133.33, 200, 400]
        return Pgains[i]

    def WritePgain(self, Pgain: int | float):
        util.typeCheck("Pgain", Pgain, int | float)

        Pgains = [5, 5.48, 5.97, 6.56, 7.02, 8, 9.09, 10, 10.53, 11.11, 12.5, 13.33, 14.29, 16, 17.39, 18.18, 19.05, 20, 22.22, 25, 30.77, 36.36, 40, 44.44, 50, 57.14, 66.67, 80, 100, 133.33, 200, 400]

        if Pgain not in Pgains:
            raise ValueError(f"Pgain is not in the list: {Pgains} = {Pgain}")

        i = Pgains.index(Pgain)
        self.WriteEEPROM(6, [None, None, None, None, None, i, None, None])

    def ReadTgain(self):
        i = self.ReadEEPROM((6, 6), type_="int")[0]
        Tgain = [1.33, 2, 5, 20]
        return Tgain[i]

    def WriteTgain(self, Tgain: int | float):
        util.typeCheck("Tgain", Tgain, int | float)

        Tgains = [1.33, 2, 5, 20]

        if Tgain not in Tgains:
            raise ValueError(f"Tgain is not in the list: {Tgains} = {Tgain}")

        i = Tgains.index(Tgain)
        self.WriteEEPROM(6, [None, None, None, None, None, None, i, None])

    def ReadCRC(self):
        h = self.ReadEEPROM((15, 7))[0]
        return h

    def WriteCRC(self, crc: int):
        util.typeCheck("crc", crc, int)
        util.minMaxCheck("crc", crc, 0, 255)

        self.WriteEEPROM(15, [None, None, None, None, None, None, None, crc], verify=False)

    def ReadPadc(self, count = 10):
        util.typeCheck("count", count, int)

        for ii in range(10):
            Padc = []
            for i in range(count):
                util.White("Reading Padc:", f"{i+1}/{count}", end="\r")
                r = self.Retry(lambda: self._ReadPadc(), "_ReadPadc()", "$000000", "Can not read Padc")
                h = util.HexToInt2s(r)
                Padc.append(h)

            Pmed = round(np.median(Padc))
            Pdiff = max(Padc) - min(Padc)

            if Pmed != 0 and Pdiff < 10_000:
                util.White(f"Reading Padc:", f"{Pmed} = {'%.8f' % util.MapRange(Pmed)} V", Pdiff)
                break
            else:
                util.Red(f"Reading Padc: {ii+1}/10:", f"{Pmed} = {'%.8f' % util.MapRange(Pmed)} V", Pdiff)

        return [Padc, Pmed, Pdiff]

    def ReadTadc(self, count = 10):
        util.typeCheck("count", count, int)

        for ii in range(10):
            Tadc = []
            for i in range(count):
                util.White("Reading Tadc:", f"{i+1}/{count}", end="\r")
                r = self.Retry(lambda: self._ReadTadc(), "_ReadTadc()", "$000000", "Can not read Tadc")
                h = util.HexToInt2s(r)
                Tadc.append(h)

            Tmed = round(np.median(Tadc))
            Tdiff = max(Tadc) - min(Tadc)

            if Tmed != 0 and Tdiff < 10_000:
                util.White(f"Reading Tadc:", f"{Tmed} = {'%.8f' % util.MapRange(Tmed)} V", Tdiff)
                break
            else:
                util.Red(f"Reading Tadc: {ii+1}/10:", f"{Tmed} = {'%.8f' % util.MapRange(Tmed)} V", Tdiff)

        return [Tadc, Tmed, Tdiff]

    def ReadFullEEPROM(self):
        EEPROM = []
        for i in range(16):
            for ii in range(8):
                EEPROM.append((i, ii))
        return self.ReadEEPROM(EEPROM, print="Reading EEPROM: ")

    def UploadDefaultConfig(self):
        p0 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # 00   H0_LSB,                 H0_MID,                 H0_MSB,                 H1_LSB,                   H1_MID,                  H1_MSB,                  H2_LSB,                H2_MID
        p1 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # 01   H2_MSB,                 H3_LSB,                 H3_MID,                 H3_MSB,                   G0_LSB,                  G0_MID,                  G0_MSB,                G1_LSB
        p2 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # 02   G1_MID,                 G1_MSB,                 G2_LSB,                 G2_MID,                   G2_MSB,                  G3_LSB,                  G3_MID,                G3_MSB
        p3 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # 03   N0_LSB,                 N0_MID,                 N0_MSB,                 N1_LSB,                   N1_MID,                  N1_MSB,                  N2_LSB,                N2_MID
        p4 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # 04   N2_MSB,                 N3_LSB,                 N3_MID,                 N3_MSB,                   M0_LSB,                  M0_MID,                  M0_MSB,                M1_LSB
        p5 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # 05   M1_MID,                 M1_MSB,                 M2_LSB,                 M2_MID,                   M2_MSB,                  M3_LSB,                  M3_MID,                M3_MSB
        p6 = [0x66, 0x01, 0x00, 0x08, 0x01, 0x1D, 0x02, 0x20]  # 06   DIG_IF_CTRL,            DAC_CTRL_STATUS,        DAC_CONFIG,             OP_STAGE_CTRL,            BRDG_CTRL,               P_GAIN_SELECT,           T_GAIN_SELECT,         TEMP_CTRL
        p7 = [0x58, 0xF0, 0x00, 0xFF, 0x66, 0x06, 0x99, 0x39]  # 07   *FullScale_Range_Min_1, *FullScale_Range_Min_2, TEMP_SE,                *FullScale_Range_Unit,    NORMAL_LOW_LSB,          NORMAL_LOW_MSB,          NORMAL_HIGH_LSB,       NORMAL_HIGH_MSB
        p8 = [0x33, 0x03, 0xCC, 0x3C, 0x00, 0x00, 0x00, 0x00]  # 08   LOW_CLAMP_LSB,          LOW_CLAMP_MSB,          HIGH_CLAMP_LSB,         HIGH_CLAMP_MSB,           PADC_GAIN_LSB,           PADC_GAIN_MID,           PADC_GAIN_MSB,         PADC_OFFSET_LSB
        p9 = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # 09   PADC_OFFSET_MID,        PADC_OFFSET_MSB,        A0_LSB,                 A0_MSB,                   A1_LSB,                  A1_MSB,                  A2_LSB,                A2_MSB
        pA = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]  # 10   B0_LSB,                 B0_MSB,                 B1_LSB,                 B1_MSB,                   B2_LSB,                  B2_MSB,                  DIAG_ENABLE,           EEPROM_LOCK
        pB = [0x66, 0x55, 0xA7, 0x0E, 0xFF, 0x3F, 0x00, 0x00]  # 11   AFEDIAG_CFG,            AFEDIAG_MASK,           *FullScale_Range_Max_1, *FullScale_Range_Max_2,   FAULT_LSB,               FAULT_MSB,               TADC_GAIN_LSB,         TADC_GAIN_MID
        pC = [0x00, 0x00, 0x00, 0x00, 0x99, 0x99, 0x99, 0x99]  # 12   TADC_GAIN_MSB,          TADC_OFFSET_LSB,        TADC_OFFSET_MID,        TADC_OFFSET_MSB,          *ScanSense_Serial_1,     *ScanSense_Serial_2,     *ScanSense_Serial_3,   *ScanSense_Serial_4
        pD = [0x01, 0x00, 0x00, 0x0F, 0x42, 0x3F, 0x63, 0x63]  # 13   ADC_24BIT_ENABLE,       OFFSET_ENABLE,          *ScanSense_Test_Status, *ScanSense_Partnumber_1,  *ScanSense_Partnumber_2, *ScanSense_Partnumber_3, *Production_Date_Week, *Production_Date_Year
        pE = [0x0F, 0x42, 0x3F, 0x0F, 0x42, 0x3F, 0x27, 0x0F]  # 14   *Supplier_Serial_1,     *Supplier_Serial_2,     *Supplier_Serial_3      *Supplier_Batch_1,        *Supplier_Batch_2,       *Supplier_Batch_3,       *Supplier_Ess_1,       *Supplier_Ess_2
        pF = [0x58, 0xF0, 0xFF, 0xA7, 0x0E, 0x63, 0x63, 0x42]  # 15   *Temp_Min_Range_1,      *Temp_Min_Range_2,      *Temp_Range_Unit,       *Temp_Max_Range_1,        *Temp_Max_Range_2,       *ScanSense_EX,           *CustomerSpecific,     EEPROM_CRC_VALUE

        pages = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, pA, pB, pC, pD, pE, pF]

        for i, data in enumerate(pages):
            util.White("Writing config:", f"{i+1}/16", end="\r")
            self.WriteEEPROM(i, data)

        util.White("Writing config:", "OK")
        return "Uploaded"

    def CalculateCoefficients(self, Padc: list, Tadc: list, Dac: list):
        util.typeCheck("Padc", Padc, list)
        util.typeCheck("Tadc", Tadc, list)
        util.typeCheck("Dac", Dac, list)

        if not (len(Padc) == len(Tadc) and len(Tadc) == len(Dac)):
            util.errorCheck("ListLengthError", "Padc, Tadc, Dac", f"{len(Padc)}, {len(Tadc)}, {len(Dac)}")

        coefficients = CalculateCoefficientsTi(Padc, Tadc, Dac)
        return coefficients

    def UploadCoefficients(self, coefficients: list):
        util.typeCheck("coefficients", coefficients, list)

        data = []
        for c in list(map(lambda a: str(a).zfill(6), coefficients)):
            data.append(c[4:6])
            data.append(c[2:4])
            data.append(c[0:2])

        for i, p in enumerate(range(0, 48, 8)):
            d = data[p:p+8]
            util.White("Uploading polynomial:", f"{i+1}/10", end="\r")
            self.WriteEEPROM(i, list(map(lambda a: int(a, 16), d)))

        util.White("Uploading polynomial:", f"7/10", end="\r")
        self.WriteEEPROM(8, [None, None, None, None, int(data[54], 16), int(data[55], 16), int(data[56], 16), int(data[57], 16)])

        util.White("Uploading polynomial:", f"8/10", end="\r")
        self.WriteEEPROM(9, [int(data[58], 16), int(data[59], 16), None, None, None, None, None, None])

        util.White("Uploading polynomial:", f"9/10", end="\r")
        self.WriteEEPROM(11, [None, None, None, None, None, None, int(data[48], 16), int(data[49], 16)])

        util.White("Uploading polynomial:", f"10/10", end="\r")
        self.WriteEEPROM(12, [int(data[50], 16), int(data[51], 16), int(data[52], 16), int(data[53], 16), None, None, None, None])

        util.White("Uploaded polynomial:", str(coefficients))

    def ReadCoefficients(self):
        h0 = "".join(self.ReadEEPROM([(0, 2), (0, 1), (0, 0)]))
        h1 = "".join(self.ReadEEPROM([(0, 5), (0, 4), (0, 3)]))
        h2 = "".join(self.ReadEEPROM([(0, 8), (0, 7), (0, 6)]))
        h3 = "".join(self.ReadEEPROM([(0, 11), (0, 10), (0, 9)]))
        g0 = "".join(self.ReadEEPROM([(0, 14), (0, 13), (0, 12)]))
        g1 = "".join(self.ReadEEPROM([(0, 17), (0, 16), (0, 15)]))
        g2 = "".join(self.ReadEEPROM([(0, 20), (0, 19), (0, 18)]))
        g3 = "".join(self.ReadEEPROM([(0, 23), (0, 22), (0, 21)]))
        n0 = "".join(self.ReadEEPROM([(0, 26), (0, 25), (0, 24)]))
        n1 = "".join(self.ReadEEPROM([(0, 29), (0, 28), (0, 27)]))
        n2 = "".join(self.ReadEEPROM([(0, 32), (0, 31), (0, 30)]))
        n3 = "".join(self.ReadEEPROM([(0, 35), (0, 34), (0, 33)]))
        m0 = "".join(self.ReadEEPROM([(0, 38), (0, 37), (0, 36)]))
        m1 = "".join(self.ReadEEPROM([(0, 41), (0, 40), (0, 39)]))
        m2 = "".join(self.ReadEEPROM([(0, 44), (0, 43), (0, 42)]))
        m3 = "".join(self.ReadEEPROM([(0, 47), (0, 46), (0, 45)]))

        Pg = "".join(self.ReadEEPROM([(8, 6), (8, 5), (8, 4)]))
        Po = "".join(self.ReadEEPROM([(9, 1), (9, 0), (8, 7)]))
        Tg = "".join(self.ReadEEPROM([(12, 0), (11, 7), (11, 6)]))
        To = "".join(self.ReadEEPROM([(12, 3), (12, 2), (12, 1)]))

        return [h0, h1, h2, h3, g0, g1, g2, g3, n0, n1, n2, n3, m0, m1, m2, m3, Tg, To, Pg, Po]

    def UploadDummyData(self, target: int | float, mm, print=True):
        util.typeCheck("target", target, int | float)

        Padc = self.ReadPadc(20)[1]
        Dac = self.DacCalibrate(target, mm)[0]

        coefficients = self.CalculateCoefficients([Padc, Padc+3_000_000, Padc+4_000_000], [0, 0, 0], [Dac, Dac+4000, Dac+8000])

        self.UploadCoefficients(coefficients)
        self.CalcCRC(print=print)

        return "Uploaded"

    def CalcCRC(self, print=True):
        EEPROM = self.ReadFullEEPROM()
        EEPROM.pop()
        EEPROM_bytes = bytes.fromhex("".join(EEPROM))

        crc = int(crc8(EEPROM_bytes, 0xFF).hexdigest(), 16)
        self.WriteCRC(crc)
        read = self.ReadCRC()

        if print:
            util.White("Calculated CRC:", read)
        else:
            util.White("Calculated CRC:", "OK")

        return read, EEPROM

    def DacAdjust(self, target: int | float, mm, fullRange: bool):
        util.typeCheck("target", target, int | float)

        self.WriteControl([0x30, 0x31, 0x67], [0x00, 0x00, 0x07])

        if target == 12:
            r = [3, 4, 5, 6]
        else:
            r = [0, 1, 2, 3, 4, 5, 6]

        for v in r:
            self.SetAdditionalVoltage(v/10)

            low = 1800
            high = 13000

            if not fullRange:
                if abs(4 - target) < 0.5:
                    low = 1900
                    high = 2400
                elif abs(12 - target) < 0.5:
                    low = 5500
                    high = 7000
                elif abs(20 - target) < 0.5:
                    low = 9500
                    high = 12000

            i = 0
            while low < high:
                i += 1
                mid = (low + high) // 2
                h = hex(mid).replace("0x", "").zfill(4).upper()
                self.WriteControl([0x30, 0x31],  [int(h[2:4], 16), int(h[0:2], 16)])
                time.sleep(0.5)
                mA = mm.readmA()
                util.White(f"Calculating DAC: {v/10}v", target, f"{mid} = {'%.8f' % mA} mA", end="\r")

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

        self.SetAdditionalVoltage(0)
        raise ValueError(util.Red(f"Dac is out of range = {mid}, {target} != {mA}", ret=True))

    def DacCalibrate(self, target: int | float, mm):
        util.typeCheck("target", target, int | float)

        DacFullRange = False
        for i in range(10):
            try:
                DacValue, DacMeasured = self.DacAdjust(target, mm, DacFullRange)
                return DacValue, DacMeasured
            except Exception as e:
                DacFullRange = True
                util.Red(f"Dac calibration failed: {e}, retrying: attempt: {i+1}/10")

        return 0, 0

if __name__ == "__main__":
    util.setColor()

    pga = PGA305()
    pga.Activate()
    util.Cyan("Connected to:", pga.serialnumber)
    util.Cyan("Firmware version:", pga.GetDeviceFirmwareVersions())
    #pga.UploadDefaultConfig()

    #pga.WriteScanSenseSerial(12345678)
    #pga.WriteFullScaleRangeMinimum(-1000)
    #pga.WriteFullScaleRangeMaximum(1000)
    #pga.WriteFullScaleRangeUnit("Bar")
    #pga.WriteScanSenseTestStatus(1, 0, 1, 0, 1, 0, 1, 0)
    #pga.WriteScanSensePartNumber(2345678)
    #pga.WriteScanSenseProductionDate(10, 20)
    #pga.WriteSupplierSerial(123456)
    pga.WriteSupplierBatch(80353)
    #pga.WriteSupplierEss(20)
    #pga.WriteTemperatureRangeMinimum(-100)
    #pga.WriteTemperatureRangeMaximum(100)
    #pga.WriteTemperatureRangeUnit("Kelvin")
    #pga.WriteScanSenseEX(1)
    #pga.WriteCustomerSpecificRequirements(1)

    util.White("ScanSense Serial:", pga.ReadScanSenseSerial())
    util.White("FullScale range:", f"{pga.ReadFullScaleRangeMinimum()} to {pga.ReadFullScaleRangeMaximum()} {pga.ReadFullScaleRangeUnit()} = {pga.ReadFullScaleRange()}")
    util.White("ScanSense testStatus:", str(pga.ReadScanSenseTestStatus()))
    util.White("ScanSense partnumber:", pga.ReadScanSensePartNumber())
    util.White("ScanSense production:", pga.ReadScanSenseProductionDate())
    util.White("Supplier Serial:", pga.ReadSupplierSerial())
    util.White("Supplier Batch:", pga.ReadSupplierBatch())
    util.White("Supplier Ess:", pga.ReadSupplierEss())
    util.White("Temperature range:", f"{pga.ReadTemperatureRangeMinimum()} to {pga.ReadTemperatureRangeMaximum()} {pga.ReadTemperatureRangeUnit()}")
    util.White("ScanSense EX:", pga.ReadScanSenseEX())
    util.White("Customer Specific:", pga.ReadCustomerSpecificRequirements())
    util.White("Pgain:", pga.ReadPgain())
    util.White("Tgain:", pga.ReadTgain())
    util.White("CRC:", pga.ReadCRC())