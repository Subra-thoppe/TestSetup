import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

import time
from modules import util
from protocols.Scpi import Scpi

class Kikusui_TOS7200(Scpi):

    def __init__(self, port: str) -> None:
        util.typeCheck("port", port, str)
        super().__init__(port)

    def readTestVoltage(self) -> int:
        read = self.__read__("TES?")
        return int(read)
    
    def readTestTime(self) -> tuple[float, int]:
        timer, state = self.__read__("TIMER?").split(",")
        return float(timer), int(state)
    
    def readLowerLimit(self) -> tuple[float, int]:
        lower, state = self.__read__("LOW?").split(",")
        return float(lower.replace("E6", "")), int(state)
    
    def readUpperLimit(self) -> tuple[float, int]:
        upper, state = self.__read__("UPP?").split(",")
        return float(upper.replace("E6", "")), int(state)

    def readBuzzerVolume(self) -> int:
        read = self.__read__("BVOL?")
        return int(read)

    def readPassHold(self) -> int:
        read = self.__read__("PHOL?")
        return int(read)

    def readWaitTime(self) -> float:
        read = self.__read__("WTIM?")
        return float(read)

    def readMeasuredValue(self) -> int:
        read = self.__read__("MON?").split(",")
        return int(read[0]), float(read[1].replace("E6", "")), float(read[2])

    def setTestVoltage(self, volt: int) -> None:
        util.typeCheck("volt", volt, int)
        util.minMaxCheck("volt", volt, 10, 1020)

        self.__read__(f"TES {volt}")

    def setTestTime(self, time: int | float, state: int) -> None:
        util.typeCheck("time", time, int | float)
        util.minMaxCheck("time", time, 0.5, 999)
        util.typeCheck("state", state, int)
        util.minMaxCheck("state", state, 0, 1)

        self.__read__(f"TIMER {time},{state}")

    def setLowerLimit(self, volt: int | float, state: int) -> None:
        util.typeCheck("volt", volt, int | float)
        util.typeCheck("state", state, int)
        util.minMaxCheck("volt", volt, 0.01, 5000)
        util.minMaxCheck("state", state, 0, 1)

        self.__read__(f"LOW {volt}E6,{state}")

    def setUpperLimit(self, volt: int | float, state: int) -> None:
        util.typeCheck("volt", volt, int | float)
        util.typeCheck("state", state, int)
        util.minMaxCheck("volt", volt, 0.01, 5000)
        util.minMaxCheck("state", state, 0, 1)

        self.__read__(f"UPP {volt}E6,{state}")

    def setBuzzerVolume(self, volume: int) -> None:
        util.typeCheck("volume", volume, int)
        util.minMaxCheck("volume", volume, 0, 9)

        self.__read__(f"BVOL {volume}")

    def setPassHold(self, state: int) -> None:
        util.typeCheck("state", state, int)
        util.minMaxCheck("state", state, 0, 1)

        self.__read__(f"PHOL {state}")

    def setWaitTime(self, waittime: int | float) -> None:
        util.typeCheck("waittime", waittime, int | float)
        util.minMaxCheck("waittime", waittime, 0.3, 10)

        self.__read__(f"WTIM {waittime}")

    def stopTest(self) -> None:
        self.__read__("STOP")

    def startTest(self) -> None:
        self.__read__("START")
        time.sleep(0.5)

    def __read__(self, command: str) -> str:
        read = super().__read__(command)
        
        if read == "ERROR":
            util.errorCheck("CommandInvalid", "read", read)
        return read

if __name__ == "__main__":
    util.setColor()

    if util.config["instruments"]["it"]["module"] != "Kikusui_TOS7200":
        raise Exception(util.Red("The insulation tester 'Kikusui_TOS7200' is not defined in config"))

    it = Kikusui_TOS7200(util.config["instruments"]["it"]["port"])
    util.Purple(it)

    #ir.setLowerLimit(10.00, 0)
    #print(ir.readLowerLimit())

    #ir.setUpperLimit(5000, 0)
    #print(ir.readUpperLimit())

    #ir.setTestVoltage(1000)
    #print(ir.readTestVoltage())

    #ir.setTestTime(1.3, 0)
    #print(ir.readTestTime())

    #ir.setBuzzerVolume(9)
    #print(ir.readBuzzerVolume())

    #ir.setPassHold(1)
    #print(ir.readPassHold())

    #ir.setWaitTime(1)
    #print(ir.readWaitTime())

    it.startTest()
    for _ in range(100):
        print(it.readMeasuredValue())
    it.stopTest()