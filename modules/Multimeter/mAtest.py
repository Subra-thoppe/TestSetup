import pyvisa
import time
import sys
#sys.path.append("C:/Scansense/jeya/AM5000/python-lib")
#sys.path.append("C:/Scansense/jeya/AM5000/python-lib/modules/Multimeter")
#sys.path.append("C:/Scansense/jeya/AM5000/python-lib_020524 – Kopi/")
#C:\Scansense\jeya\AM5000\python-lib\modules\Insulation_Resistance

Multimeterresource = None


def measurecurrentDCmANew():
    global Multimeterresource

    if not Multimeterresource:
        rm = pyvisa.ResourceManager()
        Multimeterresource = rm.open_resource("USB0::0x0957::0x0607::MY47013873::INSTR")
        #dc = rm.open_resource("ASRL7::INSTR")
        Multimeterresource.read_termination = "\n"
        print(Multimeterresource.query("*IDN?"))
        time.sleep(1)
        Multimeterresource.write("*CLS")
        time.sleep(1)
        Multimeterresource.write("CONF:CURR")
        time.sleep(1)

    CurrentinmA = float(Multimeterresource.query("READ?")) * 1000
    return CurrentinmA

def measurecurrentDCmA():
    rm = pyvisa.ResourceManager()
    Multimeterresource = rm.open_resource("USB0::0x0957::0x0607::MY47013873::INSTR")
    #dc = rm.open_resource("ASRL7::INSTR")
    Multimeterresource.read_termination = "\n"
    print(Multimeterresource.query("*IDN?"))
    time.sleep(1)
    Multimeterresource.write("*CLS")
    time.sleep(1)
    CurrentinmA=float(Multimeterresource.query("MEASure:CURRent:DC?"))*1000
    Multimeterresource.close()
    return CurrentinmA
""" curr_value=measurecurrentDCmA()
print(curr_value) """