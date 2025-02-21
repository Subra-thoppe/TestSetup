import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

from modules import util
from protocols.Scpi import Scpi

class GW_4323(Scpi):

    def __init__(self, port: str) -> None:
        util.typeCheck("port", port, str)
        super().__init__(port)

    def readSetVoltage(self, channel: int) -> float:
        util.typeCheck("channel", channel, int)
        util.minMaxCheck("channel", channel, 1, 4)

        read = self.__read__("VSET<channel>?".replace("<channel>", str(channel)))
        return float(read)
    
    def readSetCurrent(self, channel: int) -> float:
        util.typeCheck("channel", channel, int)
        util.minMaxCheck("channel", channel, 1, 4)

        read = self.__read__("ISET<channel>?".replace("<channel>", str(channel)))
        return float(read)

    def readMeasuredVoltage(self, channel: int) -> float:
        util.typeCheck("channel", channel, int)
        util.minMaxCheck("channel", channel, 1, 4)

        read = self.__read__("MEAS<channel>:VOLT?".replace("<channel>", str(channel)))
        return float(read)

    def readMeasuredCurrent(self, channel: int) -> float:
        util.typeCheck("channel", channel, int)
        util.minMaxCheck("channel", channel, 1, 4)

        read = self.__read__("MEAS<channel>:CURR?".replace("<channel>", str(channel)))
        return float(read)
    
    def readState(self, channel: int) -> int:
        util.typeCheck("channel", channel, int)
        util.minMaxCheck("channel", channel, 1, 4)

        read = self.__read__("OUTP<channel>:STAT?".replace("<channel>", str(channel)))
        return int({"OFF": 0, "ON": 1}[read])

    def setVoltage(self, channel: int, volt: int | float) -> None:
        util.typeCheck("channel", channel, int)
        util.minMaxCheck("channel", channel, 1, 4)
        util.typeCheck("volt", volt, int | float)

        minVoltage = [0.0, 0.0, 0.0, 0.0][channel-1]
        maxVoltage = [32.0, 32.0, 5.0, 15.0][channel-1]
        
        util.minMaxCheck("volt", volt, minVoltage, maxVoltage)
        self.__write__("VSET<channel>:<volt>".replace("<channel>", str(channel)).replace("<volt>", str(volt)))

    def setCurrent(self, channel: int, current: int | float) -> None:
        util.typeCheck("channel", channel, int)
        util.minMaxCheck("channel", channel, 1, 4)
        util.typeCheck("current", current, int | float)

        minCurrent = [0.0, 0.0, 0.0, 0.0][channel-1]
        maxCurrent = [3.0, 3.0, 1.0, 1.0][channel-1]
        
        util.minMaxCheck("current", current, minCurrent, maxCurrent)
        self.__write__("ISET<channel>:<current>".replace("<channel>", str(channel)).replace("<current>", str(current)))

    def setState(self, channel: int, state: int) -> None:
        util.typeCheck("channel", channel, int)
        util.minMaxCheck("channel", channel, 1, 4)
        util.typeCheck("state", state, int)
        util.minMaxCheck("state", state, 0, 1)

        self.__write__("OUTP<channel>:STAT <state>".replace("<channel>", str(channel)).replace("<state>", str(state)))

    def local(self) -> None:
        self.__write__("LOCAL")

if __name__ == "__main__":
    util.setColor()

    if util.config["instruments"]["ps"]["module"] != "GW_4323":
        raise Exception(util.Red("The power supply 'GW_4323' is not defined in config"))

    ps = GW_4323(util.config["instruments"]["ps"]["port"])
    util.Purple(ps)

    ps.setVoltage(1, 10)
    ps.setCurrent(1, 0.02)
    ps.setState(1, 1)
    util.White(ps.readSetVoltage(1), ps.readMeasuredVoltage(1))
    util.White(ps.readSetCurrent(1) * 1000, ps.readMeasuredCurrent(1) * 1000)
    util.White(ps.readState(1))
    ps.setState(1, 0)
    ps.local()