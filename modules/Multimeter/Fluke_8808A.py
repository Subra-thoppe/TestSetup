import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

from modules import util
from protocols.Scpi import Scpi

class Fluke_8808A(Scpi):

    def __init__(self, port: str) -> None:
        util.typeCheck("port", port, str)
        self.read_termination = "=>"
        self.timeout = 5000
        super().__init__(port)
        
        self.remote()
        self.mode = self.readMode()
        self.format()
        self.rate()

    def readMode(self) -> str:
        self.mode = self.__read__("FUNC1?")   # "VDC"
        return self.mode.strip()
    
    def readVoltDC(self) -> float:
        self.setMode("VDC")
        read = self.__read__("VAL1?")
        return float(read)
    
    def readVoltAC(self) -> float:
        self.setMode("VAC")
        read = self.__read__("VAL1?")
        return float(read)

    def readCurrentDC(self) -> float:
        self.setMode("ADC")
        read = float(self.__read__("VAL1?"))
        return read if read > 0.0001 else 0
    
    def readCurrentAC(self) -> float:
        self.setMode("AAC")
        read = self.__read__("VAL1?")
        return float(read)
    
    def readResistance(self) -> float:
        self.setMode("OHMS")
        read = self.__read__("VAL1?")
        return float(read)
    
    def readContinuity(self) -> float:
        self.setMode("CONT")
        read = self.__read__("VAL1?")
        return float(read)
    
    def setMode(self, mode: str) -> None:
        util.typeCheck("mode", mode, str)
        
        if self.mode != mode:
            self.__read__(mode)
            self.mode = self.readMode()

    def reset(self) -> None:
        self.__read__("*RST")
    
    def format(self) -> None:
        self.__read__("FORMAT 1")
    
    def rate(self) -> None:
        self.__read__("RATE S")
    
    def remote(self) -> None:
        self.__read__("REMS")
    
    def local(self) -> None:
        self.__read__("LOCS")

if __name__ == "__main__":
    util.setColor()

    if util.config["instruments"]["mm"]["module"] != "Fluke_8808A":
        raise Exception(util.Red("The multimeter 'Fluke_8808A' is not defined in config"))

    mm = Fluke_8808A(util.config["instruments"]["mm"]["port"])
    util.Purple(mm)

    while True:
        try:
            util.White("Read mA:", mm.readCurrentDC() * 1000, end="\r")
        except KeyboardInterrupt:
            break
    print()