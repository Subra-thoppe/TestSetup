import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

import time
from modules import util
from protocols.Scpi import Scpi

class HP_E3631A(Scpi):

    def __init__(self, port: str) -> None:
        util.typeCheck("port", port, str)
        super().__init__(port)

        self.remote()
        self.mode = self.readMode()

    def readMode(self) -> str:
        self.mode = self.__read__("INST?")   # "P6V", "P25V", "N25V"
        return self.mode.strip()

    def readSetVoltage(self, channel: int) -> float:
        util.typeCheck("channel", channel, int)
        util.minMaxCheck("channel", channel, 1, 3)

        self.setMode(["P6V", "P25V", "N25V"][channel-1])
        read = self.__read__("VOLT?")
        return float(read)
    
    def readSetCurrent(self, channel: int) -> float:
        util.typeCheck("channel", channel, int)
        util.minMaxCheck("channel", channel, 1, 3)

        self.setMode(["P6V", "P25V", "N25V"][channel-1])
        read = self.__read__("CURR?")
        return float(read)
    
    def readMeasuredVoltage(self, channel: int) -> float:
        util.typeCheck("channel", channel, int)
        util.minMaxCheck("channel", channel, 1, 3)

        self.setMode(["P6V", "P25V", "N25V"][channel-1])
        read = self.__read__("MEAS:VOLT?")
        return float(read)
    
    def readMeasuredCurrent(self, channel: int) -> float:
        util.typeCheck("channel", channel, int)
        util.minMaxCheck("channel", channel, 1, 3)

        self.setMode(["P6V", "P25V", "N25V"][channel-1])
        read = self.__read__("MEAS:CURR?")
        return float(read)
    
    def readState(self, channel: int) -> int:
        util.typeCheck("channel", channel, int)
        util.minMaxCheck("channel", channel, 1, 3)

        self.setMode(["P6V", "P25V", "N25V"][channel-1])
        read = self.__read__("OUTP?")
        return int(read)
    
    def setMode(self, mode: str) -> None:
        util.typeCheck("mode", mode, str)

        if self.mode != mode:
            self.__write__(f"INST {mode}")
            time.sleep(0.5)
            self.mode = self.readMode()

    def setVoltage(self, channel: int, volt: int | float) -> None:
        util.typeCheck("channel", channel, int)
        util.minMaxCheck("channel", channel, 1, 3)
        util.typeCheck("volt", volt, int | float)

        minVoltage = [0.0, 0.0, -25.0][channel-1]
        maxVoltage = [6.0, 25.0, 0.0][channel-1]
        
        self.setMode(["P6V", "P25V", "N25V"][channel-1])
        util.minMaxCheck("volt", volt, minVoltage, maxVoltage)
        self.__write__("VOLT <volt>".replace("<volt>", str(volt)))

    def setCurrent(self, channel: int, current: int | float) -> None:
        util.typeCheck("channel", channel, int)
        util.minMaxCheck("channel", channel, 1, 3)
        util.typeCheck("current", current, int | float)

        minCurrent = [0.0, 0.0, 0.0][channel-1]
        maxCurrent = [5.0, 1.0, 1.0][channel-1]
        
        self.setMode(["P6V", "P25V", "N25V"][channel-1])
        util.minMaxCheck("current", current, minCurrent, maxCurrent)
        self.__write__("CURR <current>".replace("<current>", str(current)))

    def setState(self, channel: int, state: int) -> None:
        util.typeCheck("channel", channel, int)
        util.minMaxCheck("channel", channel, 1, 3)
        util.typeCheck("state", state, int)
        util.minMaxCheck("state", state, 0, 1)

        self.setMode(["P6V", "P25V", "N25V"][channel-1])
        self.__write__("OUTP <state>".replace("<state>", str(state)))
        time.sleep(0.5)

    def remote(self) -> None:
        self.__write__("SYST:REM")
        time.sleep(0.5)

    def local(self) -> None:
        self.__write__("SYST:LOC")

if __name__ == "__main__":
    util.setColor()

    if util.config["instruments"]["ps"]["module"] != "HP_E3631A":
        raise Exception(util.Red("The power supply 'HP_E3631A' is not defined in config"))

    ps = HP_E3631A(util.config["instruments"]["ps"]["port"])
    util.Purple(ps)
    
    ps.setVoltage(1, 10)
    ps.setCurrent(1, 0.02)
    ps.setState(1, 1)
    util.White(ps.readSetVoltage(1), ps.readMeasuredVoltage(1))
    util.White(ps.readSetCurrent(1) * 1000, ps.readMeasuredCurrent(1) * 1000)
    util.White(ps.readState(1))
    ps.setState(1, 0)
    ps.local()