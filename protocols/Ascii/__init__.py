import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

import pyvisa, time
from modules import util

class Ascii:

    def __init__(self, port: str):
        util.typeCheck("port", port, str)

        try:
            rm = pyvisa.ResourceManager()
            self.instrument: pyvisa.resources.SerialInstrument = rm.open_resource(port)
        except pyvisa.VisaIOError:
            util.errorCheck("VisaIOError", "port", port)
        
        self.instrument.baud_rate = 9600
        self.instrument.read_termination = "\r"

    def __read__(self, command: str):
        util.typeCheck("command", command, str)

        try:
            for _ in range(10):
                read = str(self.instrument.query(command))
                if read:
                    return read.replace("\x00", "").strip()
        except Exception:
            util.errorCheck("VisaReadError", "Ascii", command)
            time.sleep(0.5)
    
    def __write__(self, command: str):
        util.typeCheck("command", command, str)

        write = self.instrument.write(command)
        return str(write).strip()
    
    def __repr__(self) -> str:
        return "Ascii Connection"