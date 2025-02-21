import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

from modules import util
import pyvisa

class Scpi:

    def __init__(self, port: str) -> None:
        util.typeCheck("port", port, str)
        self.port = port

        try:
            rm = pyvisa.ResourceManager()
            self.instrument: pyvisa.resources.SerialInstrument = rm.open_resource(port)
            self.instrument.read_termination = self.read_termination if hasattr(self, "read_termination") else "\n"
            self.instrument.baud_rate = self.baud_rate if hasattr(self, "baud_rate") else 9600
            self.instrument.timeout = self.timeout if hasattr(self, "timeout") else 2000

        except pyvisa.VisaIOError:
            util.errorCheck("VisaIOError", "port", port)

    def __read__(self, command: str) -> str:
        util.typeCheck("command", command, str)

        try:
            for _ in range(10):
                read = self.instrument.query(command)
                if read:
                    return str(read).strip()
        except Exception:
            util.errorCheck("VisaReadError", "Scpi", command)
    
    def __write__(self, command: str) -> str:
        util.typeCheck("command", command, str)

        write = self.instrument.write(command)
        return str(write).strip()
    
    def __repr__(self) -> str | None:
        if hasattr(self, "idn"):
            return self.idn
        
        try:
            self.idn = self.__read__("*IDN?")
            return self.idn
        except Exception:
            util.errorCheck("IdnError", "port", self.port)