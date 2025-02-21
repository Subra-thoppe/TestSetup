import pyvisa
import time

rm = pyvisa.ResourceManager()

ir = rm.open_resource("ASRL14::INSTR") # on new pc
ir.read_termination = "\r\n"
ir.baud_rate = 38400

print(ir.query("*IDN?"))

#IRTest(RelayHw,0)  # OPEN ALL RELAYS FIRST
time.sleep(2)
ir.write("*CLS") # this is need to get 32 in Measvalue
time.sleep(2)
ir.write("START")
    