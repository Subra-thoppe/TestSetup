import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))
#import util
from modules import util
from protocols.Scpi import Scpi

class Agilent_34410A(Scpi):

    def __init__(self, port: str) -> None:
        util.typeCheck("port", port, str)
        super().__init__(port)
        
        self.mode = self.readMode()
    
    def readMode(self) -> str:
        read = self.__read__("CONF?")   # "VOLT +1.00000000E-01,+3.00000000E-08"
        self.mode = read.split(" ")[0].replace("'", "").replace('"', '') # "VOLT"
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
        read = float(self.__read__("READ?"))
        return read if read > 0.0001 else 0
    
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
    
    def reset(self) -> None:
        self.__write__("*RST")

    def __write__(self, command: str) -> None:
        super().__write__(command)
        self.instrument.clear()

if __name__ == "__main__":
    util.setColor()
    print(util.config["instruments"]["mm"]["module"])
    if util.config["instruments"]["mm"]["module"] != "Agilent_34410A":
        raise Exception(util.Red("The multimeter 'Agilent_34410A' is not defined in config"))

    mm = Agilent_34410A(util.config["instruments"]["mm"]["port"])
    util.Purple(mm)

    while True:
        try:
            util.White("Read mA:", mm.readCurrentDC() * 1000, end="\r")
        except KeyboardInterrupt:
            break
    print()