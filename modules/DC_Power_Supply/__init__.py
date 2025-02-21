import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

from modules import util
from protocols.Scpi import Scpi

def init(*params):

    if not isinstance(params[0], DC_Power_Supply):
        return DC_Power_Supply(params[0])

    else:
        f = getattr(params[0], params[1])
        return f(*params[2:])

class DC_Power_Supply(Scpi):

    def __init__(self, port: str, configPath: str = __file__):
        util.typeCheck("port", port, str)
        util.typeCheck("configPath", configPath, str)

        self.read_termination = "\n"
        self.baud_rate = 9600
        super().__init__(port, configPath)

    def setVoltage(self, channel: int, volt: int | float):
        util.typeCheck("channel", channel, int)
        util.typeCheck("volt", volt, int | float)
        util.configCheck("setVoltage", self.config, True)
        util.configCheck(str(channel), self.config["setVoltage"]["channels"], True)

        minVoltage = self.config["setVoltage"]["channels"][str(channel)]["minVoltage"]
        maxVoltage = self.config["setVoltage"]["channels"][str(channel)]["maxVoltage"]

        util.minMaxCheck("volt", volt, minVoltage, maxVoltage)

        write = self.__write__(self.config["setVoltage"]["command"].replace("<channel>", str(channel)).replace("<volt>", str(volt)))
        return write
    
    def setCurrent(self, channel: int, current: int | float):
        util.typeCheck("channel", channel, int)
        util.typeCheck("current", current, int | float)
        util.configCheck("setCurrent", self.config, True)
        util.configCheck(str(channel), self.config["setCurrent"]["channels"], True)

        minCurrent = self.config["setCurrent"]["channels"][str(channel)]["minCurrent"]
        maxCurrent = self.config["setCurrent"]["channels"][str(channel)]["maxCurrent"]

        util.minMaxCheck("current", current, minCurrent, maxCurrent)

        write = self.__write__(self.config["setCurrent"]["command"].replace("<channel>", str(channel)).replace("<current>", str(current)))
        return write
    
    def setState(self, channel: int, state: int):
        util.typeCheck("channel", channel, int)
        util.typeCheck("state", state, int)
        util.configCheck("setState", self.config, True)
        util.configCheck(str(channel), self.config["setState"]["channels"], True)

        state = self.config["setState"]["channels"][str(channel)][str(state)]
        write = self.__write__(self.config["setState"]["command"].replace("<channel>", str(channel)).replace("<state>", str(state)))
        return write
    
    def readVoltage(self, channel: int):
        util.typeCheck("channel", channel, int)
        util.configCheck("readVoltage", self.config, True)
        util.configCheck(str(channel), self.config["readVoltage"]["channels"], True)

        read = self.__read__(self.config["readVoltage"]["command"].replace("<channel>", str(channel))).replace("V", "")
        return float(read)
    
    def readCurrent(self, channel: int):
        util.typeCheck("channel", channel, int)
        util.configCheck("readCurrent", self.config, True)
        util.configCheck(str(channel), self.config["readCurrent"]["channels"], True)

        read = self.__read__(self.config["readCurrent"]["command"].replace("<channel>", str(channel))).replace("A", "")
        return float(read)

    def readState(self, channel: int):
        util.typeCheck("channel", channel, int)
        util.configCheck("readState", self.config, True)
        util.configCheck(str(channel), self.config["readState"]["channels"], True)

        read = self.__read__(self.config["readState"]["command"].replace("<channel>", str(channel)))
        return {"OFF": 0, "ON": 1, "0": 0, "1": 1}[read]

    def close(self):
        util.configCheck("setLocal", self.config, True)

        write = self.__write__(self.config["setLocal"])
        return write

if __name__ == "__main__":
    util.setColor()
    
    import pyvisa

    """ rm = pyvisa.ResourceManager()
    dc = rm.open_resource("ASRL7::INSTR")
    dc.read_termination = "\n"
    print(dc.query("OUTPut:STATe 0")) """
    
    dc = DC_Power_Supply("ASRL7::INSTR")
    util.Purple(dc)
    
    """ print(dc.setVoltage(1, 24))
    print(dc.setVoltage(2, 0.1))
    print(dc.setCurrent(1, 0.1))
    print(dc.setCurrent(2, 0.05))
    print(dc.setState(1, 0))
    print(dc.setState(2, 0))
    print(dc.readVoltage(1))
    print(dc.readCurrent(1)) """
    dc.setState(2, 1)
    dc.close()
