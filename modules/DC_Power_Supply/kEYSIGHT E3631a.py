#kEYSIGHT E3631a
""" SYST:REM; # TO SET TO REMOTE
SYST:RWL; # REMOTE AND LOCK FRONT PANEL KEY S """
#JUST TO CHECK
import pyvisa
import time


rm = pyvisa.ResourceManager()
dc = rm.open_resource("ASRL9::INSTR")
dc.read_termination = "\n"

print(dc.query("*IDN?")) #working

dc.write("*CLS")

dc.write("OUTPut:STATe 0")
time.sleep(2)

""" CH=2 # Positive24V
CH=3 #Negative24V
voltage= flaot (voltage)
opstate = 1 ON , 0 OFF
"""
def P24VSET(ch,voltage,opstate):
    dc.write(f"INST:NSEL {ch};")
    dc.write(f"VOLT {voltage};") 
    dc.write(f"OUTPut:STATe {opstate}")
    
    time.sleep(2)

P24VSET(2,24.00,1)
time.sleep(2)

def outputoff():
    dc.write("OUTPut:STATe 0")
#outputoff()

def outputon():
     dc.write("OUTPut:STATe 1")
#outputon()
    
""" P24VSET(3,-24.00,1)
time.sleep(2) """

""" dc.write("INST:NSEL 2;")
dc.write("VOLT 20.00;") 
dc.write("OUTPut:STATe 1")
time.sleep(2)

dc.write("INST:NSEL 3;")
dc.write("VOLT -20.00;") 
dc.write("OUTPut:STATe 1")
time.sleep(2) """


""" print(dc.query("SOUR:VOLT?")) # working
print(dc.query("SOUR:CURR?")) # working
print(dc.query("CURR?")) # working """

#print(dc.read())
#print(curr)

"""
#CH 3 is -ve volt supply. set -20 til den

dc.write("INST:NSEL 3;")
dc.write("VOLT -20.00;") 
dc.write("OUTPut:STATe 1") """

""" # finding error

dc.write("SYST:ERR?")
time.sleep(2)
errormsg=dc.read
print(errormsg)
print(type(errormsg)) """


""" 
error messages
+0,"No error"
-410,"Query INTERRUPTED"
 """

