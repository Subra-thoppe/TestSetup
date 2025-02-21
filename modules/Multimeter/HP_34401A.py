import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

import time
from modules import util
from protocols.Scpi import Scpi

class HP_34401A(Scpi):

    def __init__(self, port: str) -> None:
        util.typeCheck("port", port, str)
        super().__init__(port)
        
        self.reset()
        self.remote()
        time.sleep(0.5)
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
    
    def readError(self) -> str:
        read = self.__read__("SYSTem:ERRor?")
        self.reset()
        return read.strip()
    
    def setMode(self, mode: str) -> None:
        util.typeCheck("mode", mode, str)
        
        if self.mode != mode:
            self.__write__(f"CONF:{mode}")
            time.sleep(0.5)
            self.mode = self.readMode()

    def reset(self) -> None:
        self.__write__("*CLS")
        time.sleep(0.5)

    def remote(self) -> None:
        self.__write__("SYST:REM")

if __name__ == "__main__":
    util.setColor()

    if util.config["instruments"]["mm"]["module"] != "HP_34401A":
        raise Exception(util.Red("The multimeter 'HP_34401A' is not defined in config"))

    mm = HP_34401A(util.config["instruments"]["mm"]["port"])
    util.Purple(mm)
    
    while True:
        try:
            util.White("Read mA:", mm.readCurrentDC() * 1000, end="\r")
        except KeyboardInterrupt:
            break
    print()