import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

import time
from modules import util
from pyModbusTCP.client import ModbusClient

class Modbus_TCP:

    def __init__(self, ip: str, port: int) -> None:
        util.typeCheck("ip", ip, str)
        util.typeCheck("port", port, int)
        
        try:
            self.instrument = ModbusClient(ip, port, auto_open=False, auto_close=False, timeout=5)
        except Exception:
            util.errorCheck("VisaIOError", "ip", ip)
    
    def __open__(self):
        i = 0
        
        while True:
            i += 1
            if self.instrument.is_open:
                break

            self.instrument.open()
            util.Yellow(f"Waiting on pressure controller, attempt: {i}", end="\r")
            time.sleep(1) 

    def __close__(self):
        if self.instrument.is_open:
            self.instrument.close()

    def __read__(self, register: int, count: int) -> int:
        util.typeCheck("register", register, int)
        util.typeCheck("count", count, int)

        self.__open__()
        try:
            for _ in range(10):
                read = self.instrument.read_holding_registers(register, count)
                if read:
                    return read[0]
        except Exception:
            util.errorCheck("VisaReadError", "Modbus_TCP", register)
            time.sleep(0.5)

    def __readBits__(self, register, count) -> str:
        util.typeCheck("register", register, int)
        util.typeCheck("count", count, int)

        return bin(self.__read__(register, count)).replace("0b", "").zfill(16)
    
    def __write__(self, register, data):
        util.typeCheck("register", register, int)
        util.typeCheck("data", data, int)

        self.__open__()
        write = self.instrument.write_single_register(register, data)
        time.sleep(0.1)
        return write

    def __repr__(self) -> str:
        return "Modbus TCP Connection"