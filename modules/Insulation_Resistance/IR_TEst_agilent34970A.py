import sys
print(sys.path)
#sys.path.append("C:/Scansense/jeya/AM5000/python-lib")
#sys.path.append("C:/Scansense/jeya/AM5000/python-lib/modules/Insulation_Resistance")
#sys.path.append("C:\Scansense\jeya\AM5000\python-lib_020524\modules\Insulation_Resistance\agilent34970a.py")
#sys.path.append("C:/Scansense/jeya/AM5000/python-lib_020524/modules/Insulation_Resistance/agilent34970a.py") 
#import modules.Insulation_Resistance.IR_Setup
import pyvisa
import time

#DualChannelSensor='TRUE'
DualChannelSensor='FALSE'


def IRTestOneCh(x):
    rm = pyvisa.ResourceManager()

    ir = rm.open_resource("ASRL7::INSTR") # on new pc
    ir.read_termination = "\r\n"
    ir.baud_rate = 38400
  
    print(ir.query("*IDN?"))

    #IRTest(RelayHw,0)  # OPEN ALL RELAYS FIRST
    time.sleep(2)
    ir.write("*CLS") # this is need to get 32 in Measvalue
    time.sleep(2)
    ir.write("START")
    
    # Read data from the instrument
    """ data = ir.read_bytes(num_bytes_to_read)
    print(f"Read {len(data)} bytes from the instrument: {data}")
    """
    # Print the read data
    #print(ir.read())
    DSR=[]
    MeasValue=[]
    if ir.read()=='OK':

        for i in range(6):
            print(i)
            """ ir.write("MON?")
            print("mon",ir.read()) """
            time.sleep(2)
            ir.write("DSR?")
            l=ir.read()
            DSR.append(l)
            
            #DSR.append(ir.query("DSR?"))
            #print(ir.query("DSR?"))
            #DSR only works with query command , START commnad has to precced DSR commnad , then only we get 16 for PASS and 12 for fail output
            #if display shows PASS then DSR op 16, else DSR op1
            time.sleep(.3)
            ir.write("MON?")
            m=ir.read()
            MeasValue.append(m)
            #MeasValue.append(ir.query("MON?"))
            #print(ir.query("MON?"))
            #print("dsr",ir.read())
            ir.write("STOP")
    else:
        print("error")
        ir.write("STOP")
        exit()
    ir.write("STOP")
    print(DSR,MeasValue)
    print("measvalue")
    #print(MeasValue[0:3])

    Resultcalc=MeasValue[2]
    R=(Resultcalc.split(","))
    Res_TestVolt=R[0]
    Res_IRvalue=R[1]
    Res_TestTime=R[2]
    print("RESULT- ir VALUE, TIME(S),VOLT(DCV)",Res_IRvalue,Res_TestTime,Res_TestVolt)
    if MeasValue[0]=='16':
        Result="PASS"
        
    elif MeasValue[0]=='32':
        Result="FAIL"
    
    elif MeasValue[0]=='12' and Res_IRvalue=='5000E6':
        Result="PASS"
        
    elif MeasValue[0]=='12' and Res_IRvalue!='5000E6':
        Result="FAIL"
    
    else:
        Result="Contact Process ansvar "
    print(f"result of Channel  {x}",Result)
    return Result, Res_IRvalue,Res_TestTime,Res_TestVolt


""" Result, Res_IRvalue,Res_TestTime,Res_TestVolt=IRTestOneCh('A')
print(Result, Res_IRvalue,Res_TestTime,Res_TestVolt) """

#IRTestOneCh('A')
#IRTestOneCh('AB')