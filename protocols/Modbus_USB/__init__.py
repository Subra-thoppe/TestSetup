import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

import time
from modules import util
from minimalmodbus import Instrument

class Modbus_USB:

    def __init__(self, port: str, address: int) -> None:
        util.typeCheck("port", port, str)
        util.typeCheck("address", address, int)
        
        try:
            self.instrument = Instrument(port, address)
            self.instrument.serial.baudrate = self.baud_rate if hasattr(self, "baud_rate") else 9600
        except Exception:
            util.errorCheck("VisaIOError", "port", port)
    
    def __readFloat__(self, registeraddress: int, functioncode: int, number_of_registers: int) -> float:
        util.typeCheck("registeraddress", registeraddress, int)
        util.typeCheck("functioncode", functioncode, int)
        util.typeCheck("number_of_registers", number_of_registers, int)

        try:
            for _ in range(10):
                read = self.instrument.read_float(registeraddress, functioncode, number_of_registers)
                if read:
                    return float(read)
        except Exception:
            util.errorCheck("VisaReadError", "Modbus_USB", registeraddress)
            time.sleep(0.5)

    def __repr__(self) -> str:
        return "Modbus USB Connection"