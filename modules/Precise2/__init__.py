import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

from modules import util
from protocols.Modbus import Modbus
from datetime import datetime
from pathlib import Path

def init(*params):

    if not isinstance(params[0], Precise2):
        return Precise2(params[0], params[1])

    else:
        f = getattr(params[0], params[1])
        return f(*params[2:])

class Precise2(Modbus):

    def __init__(self, port: str, address: int):
        util.typeCheck("port", port, str)
        util.typeCheck("address", address, int)
        
        super().__init__(port, address)

    def readPressure(self):
        error = None

        for _ in range(10):
            try:
                pressure = self.__read_float__(registeraddress=0, functioncode=4, number_of_registers=2)
                return pressure
            except Exception as e:
                error = e
                continue
        
        raise ConnectionError(util.Red(f"Can not read pressure from the device: {error}", True))
    
    def readTemperature(self):
        error = None

        for _ in range(10):
            try:
                temperature = self.__read_float__(registeraddress=2, functioncode=4, number_of_registers=2)
                return temperature
            except Exception as e:
                error = e
                continue
        
        raise ConnectionError(util.Red(f"Can not read temperature from the device: {error}", True))
    
    def log(self, ids: list, pressure: list, temperature: list):
        util.typeCheck("ids", ids, list)
        util.typeCheck("pressure", pressure, list)
        util.typeCheck("temperature", temperature, list)
        
        number = datetime.now().strftime("%d")
        date = datetime.now().strftime("%d.%m.%Y")
        time = datetime.now().strftime("%H:%M:%S")

        Path("log/").mkdir(parents=True, exist_ok=True)

        data = ""
        for i in range(len(ids)):
            data = data + str(ids[i]) + "\t" + format(pressure[i], '.16f') + "\t" + format(temperature[i], '.16f') + "\t"

        with open(f"log/{number}. {date}.log", "a+") as f:
            f.write(f"{date}\t{time}\t{data}\n")
            f.seek(0)
            return f.read() + "\n"
    
if __name__ == "__main__":
    util.setColor()

    ps = Precise2("COM9", 2)
    util.Purple(ps)

    while True:
        pressure = ps.readPressure()
        temperature = ps.readTemperature()
        print(ps.log([2,2], [pressure, temperature], [temperature, pressure]))