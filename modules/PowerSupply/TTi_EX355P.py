import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

import time
from modules import util
from protocols.Scpi import Scpi

class TTi_EX355P(Scpi):

    def __init__(self, port: str) -> None:
        util.typeCheck("port", port, str)
        super().__init__(port)

    def readSetVoltage(self) -> float:
        read = self.__read__("V?").replace("V", "")
        return float(read)
    
    def readSetCurrent(self) -> float:
        read = self.__read__("I?").replace("I", "")
        return float(read)
    
    def readMeasuredVoltage(self) -> float:
        read = self.__read__("VO?").replace("V", "")
        return float(read)
    
    def readMeasuredCurrent(self) -> float:
        read = self.__read__("IO?").replace("I", "")
        return float(read)
    
    def readState(self) -> int:
        read = self.__read__("OUT?").replace("OUT OFF", "0").replace("OUT ON", "1")
        return int(read)
    
    def setVoltage(self, volt: int | float) -> None:
        util.typeCheck("volt", volt, int | float)

        minVoltage = 0.0
        maxVoltage = 30.8
        
        util.minMaxCheck("volt", volt, minVoltage, maxVoltage)
        self.__write__("V <volt>".replace("<volt>", str(volt)))

    def setCurrent(self, current: int | float) -> None:
        util.typeCheck("current", current, int | float)

        minCurrent = 0.0
        maxCurrent = 2.06
        
        util.minMaxCheck("current", current, minCurrent, maxCurrent)
        self.__write__("I <current>".replace("<current>", str(current)))

    def setState(self, state: int) -> None:
        util.typeCheck("state", state, int)
        util.minMaxCheck("state", state, 0, 1)

        self.__write__(["OFF", "ON"][state])

    def local(self) -> None:
        pass

if __name__ == "__main__":
    util.setColor()

    if util.config["instruments"]["ps"]["module"] != "TTi_EX355P":
        raise Exception(util.Red("The power supply 'TTi_EX355P' is not defined in config"))

    ps = TTi_EX355P(util.config["instruments"]["ps"]["port"])
    util.Purple(ps)
    
    ps.setVoltage(2)
    ps.setCurrent(0.02)
    ps.setState(1)
    time.sleep(1)
    util.White(ps.readSetVoltage(), ps.readMeasuredVoltage())
    util.White(ps.readSetCurrent(), ps.readMeasuredCurrent())
    util.White(ps.readState())
    ps.setState(0)
    ps.local()