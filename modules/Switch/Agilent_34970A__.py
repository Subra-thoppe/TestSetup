import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

from modules import util
import time
from protocols.Scpi import Scpi

class Agilent_34970A(Scpi):

    def __init__(self, port: str) -> None:
        util.typeCheck("port", port, str)
        self.timeout = 5000
        super().__init__(port)

    def openAllPorts(self) -> None:
        self.__write__("ROUTe:OPEN (@101:120)")

    def closeOnePort(self, channel: int) -> None:
        util.typeCheck("channel", channel, int)
        util.minMaxCheck("channel", channel, 1, 60)

        self.openAllPorts()
        time.sleep(0.20)

        if channel > 0 and channel <= 20:
            card = 1
            ch = channel
        elif channel > 20 and channel <= 40:
            card = 2
            ch = channel-20
        elif channel > 40 and channel <= 60:
            card = 3
            ch = channel-40 

        
        self.__write__("ROUTe:CLOSe:EXCLusive (@<slot><channel>)".replace("<slot>", str(card)).replace("<channel>", str(ch).zfill(2)))

    def readOnePort(self, channel: int) -> int:
        util.typeCheck("channel", channel, int)
        util.minMaxCheck("channel", channel, 1, 60)

        if channel > 0 and channel <= 20:
            card = 1
            ch = channel
        elif channel > 20 and channel <= 40:
            card = 2
            ch = channel-20
        elif channel > 40 and channel <= 60:
            card = 3
            ch = channel-40
        
        read = self.__read__("ROUTe:CLOSe? (@<slot><channel>)".replace("<slot>", str(card)).replace("<channel>", str(ch).zfill(2)))
        return int(read.strip())

if __name__ == "__main__":
    util.setColor()

    if util.config["instruments"]["sw"]["module"] != "Agilent_34970A":
        raise Exception(util.Red("The switch 'Agilent_34970A' is not defined in config"))

    sw = Agilent_34970A(util.config["instruments"]["sw"]["port"])
    util.Purple(sw)

    sw.closeOnePort(int(input("Open channel? ")))