import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

from modules import util
import time
from protocols.Scpi import Scpi

class Keithley_2750(Scpi):

    def __init__(self, port: str) -> None:
        util.typeCheck("port", port, str)
        self.timeout = 5000
        super().__init__(port)

        self.format()
        self.mode = self.readMode()

    def readMode(self) -> str:
        read = self.__read__("CONF?")   # "VOLT:DC"
        self.mode = read.replace('"', '') # VOLT
        return self.mode.strip()
    
    def readVoltDC(self) -> float:
        self.setMode("VOLT")
        read = self.__read__("READ?")
        return float(read)
    
    def readVoltAC(self) -> float:
        self.setMode("VOLT:AC")
        read = self.__read__("READ?")
        return float(read)
    
    def readCurrentDC(self) -> float:
        self.setMode("CURR")
        read = self.__read__("READ?")
        return float(read)
    
    def readCurrentAC(self) -> float:
        self.setMode("CURR:AC")
        read = self.__read__("READ?")
        return float(read)
    
    def readResistance(self) -> float:
        self.setMode("RES")
        read = self.__read__("READ?")
        return float(read)
    
    def readContinuity(self) -> float:
        self.setMode("CONT")
        read = self.__read__("READ?")
        return float(read)
    
    def setMode(self, mode: str) -> None:
        util.typeCheck("mode", mode, str)
        
        if self.mode != mode:
            self.__write__(f"CONF:{mode}")
            self.mode = self.readMode()

    def openAllPorts(self) -> None:
        self.__write__("ROUTe:OPEN:ALL")

    def closeOnePort(self, channel: int) -> None:
        util.typeCheck("channel", channel, int)
        util.minMaxCheck("channel", channel, 1, 200)
        self.openAllPorts()
        time.sleep(0.20)

        if channel > 0 and channel <= 40:
            card = 1
            ch = channel
        elif channel > 40 and channel <= 80:
            card = 2
            ch = channel-40
        elif channel > 80 and channel <= 120:
            card = 3
            ch = channel-80
        elif channel > 120 and channel <= 160:
            card = 4
            ch = channel-120
        elif channel > 160 and channel <= 200:
            card = 5
            ch = channel-160

        self.__write__("ROUTe:CLOSe (@<slot><channel>)".replace("<slot>", str(card)).replace("<channel>", str(ch).zfill(2)))

    def readOnePort(self, channel: int) -> int:
        util.typeCheck("channel", channel, int)
        util.minMaxCheck("channel", channel, 1, 200)

        if channel > 0 and channel <= 40:
            card = 1
            ch = channel
        elif channel > 40 and channel <= 80:
            card = 2
            ch = channel-40
        elif channel > 80 and channel <= 120:
            card = 3
            ch = channel-80
        elif channel > 120 and channel <= 160:
            card = 4
            ch = channel-120
        elif channel > 160 and channel <= 200:
            card = 5
            ch = channel-160
        
        read = self.__read__("ROUTe:CLOSe:STATe? (@<slot><channel>)".replace("<slot>", str(card)).replace("<channel>", str(ch).zfill(2)))
        return int(read.strip())

    def format(self) -> None:
        self.__write__("FORMat:ELEMents READing")

if __name__ == "__main__":
    import time
    util.setColor()

    if util.config["instruments"]["sw"]["module"] != "Keithley_2750":
        raise Exception(util.Red("The switch 'Keithley_2750' is not defined in config"))

    sw = Keithley_2750(util.config["instruments"]["sw"]["port"])
    util.Purple(sw)

    sw.closeOnePort(int(input("CLose channel? ")))
    time.sleep(1)