import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

import pyvisa, time
from modules import util

class HW_034:

    def __init__(self, port: str):
        util.typeCheck("port", port, str)

        try:
            rm = pyvisa.ResourceManager()
            self.instrument: pyvisa.resources.SerialInstrument = rm.open_resource(port)
        except pyvisa.VisaIOError:
            util.errorCheck("VisaIOError", "port", port)
        
        self.instrument.baud_rate = 9600
        self.instrument.read_termination = ""
        self.instrument.write_termination = ""
        self.instrument.timeout = 10000

        self.instrument.write(chr(0x50))
        try:
            self.instrument.timeout = 10
            self.instrument.read_bytes(1)
            self.instrument.timeout = 10000
        except Exception:
            pass

        self.instrument.write(chr(0x51))
        time.sleep(0.01)
        self.instrument.write(chr(0xF))
        time.sleep(0.01)
        self.instrument.write(chr(0xF))
        time.sleep(0.1)
    
    def __repr__(self) -> str:
        return "HW-034"
    
    def setPort(self, state: str):
        util.typeCheck("state", state, str)
        util.minMaxCheck("state", int(state, 2), 0, 0xF)

        self.instrument.write(chr(0xF - int(state, 2)))

if __name__ == "__main__":
    util.setColor()

    if util.config["instruments"]["rb"]["module"] != "HW_034":
        raise Exception(util.Red("The relay board 'HW_034' is not defined in config"))

    rb = HW_034(util.config["instruments"]["rb"]["port"])
    util.Purple(rb)
    
    rb.setPort("0011")