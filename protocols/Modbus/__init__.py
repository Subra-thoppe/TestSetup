import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

from modules import util
from minimalmodbus import Instrument

class Modbus:

    def __init__(self, port: str, address: int, baudrate = 9600):
        util.typeCheck("port", port, str)
        util.typeCheck("address", address, int)
        
        try:
            self.instrument = Instrument(port, address)
            self.instrument.serial.baudrate = baudrate
        except Exception:
            raise ConnectionError(util.Red(f"Can not connect to Instrument on {port}", True))

    def __repr__(self):
        return "Precise 2"
    
    def __read_float__(self, registeraddress: int, functioncode: int, number_of_registers: int):
        util.typeCheck("registeraddress", registeraddress, int)
        util.typeCheck("functioncode", functioncode, int)
        util.typeCheck("number_of_registers", number_of_registers, int)

        read = self.instrument.read_float(registeraddress, functioncode, number_of_registers)
        return float(read)