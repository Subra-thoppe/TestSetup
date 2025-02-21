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
    import sys
    #print(sys.path)
    #sys.path.append("C:/AM5000/python-libTestsetup/")
    #sys.path.append("C:/AM5000/python-lib")
    #import modules.Insulation_Resistance.IR_Setup_function as IRsetup
    #IRsetup.IR_Setupfunction()
    

    rm = pyvisa.ResourceManager()
    ir = rm.open_resource("ASRL7::INSTR")
    ir.read_termination = "\r\n"
    ir.write_termination= "\r\n"
    ir.baud_rate = 38400
    ir.timeout=5000
    # all setting
    print(ir.query("*IDN?"))
    #exit()
    #ir.clear()
    ir.write("LOWER 200E6,ON")  # setting resistance lower limit 
    time.sleep(1)
    ir.write("UPPER 5000E6,OFF") # setting resistance upper limit , OFF sets the "upper ON" light off 
    time.sleep(1)
    ir.write("TESTV 50") # setting test voltage to 50 V
    time.sleep(1)
    #ir.write("TIMER 1.5,ON") # setting testing time   #30,09,24
    #ir.write("TIMER 20,ON") # setting testing time  # minimum 10 sec 
    ir.write("TIMER 10,ON") # setting testing time  # minimum 10 sec 14,oct,24
    time.sleep(1)
    #ir.write("PASSHOLD ON") # SETTING PASS HOLD ON / OFF  #30,09,24

    ir.write("PASSHOLD ON") # SETTING PASS HOLD ON / OFF 
    time.sleep(1)
    ir.write("BVOL 10") # BUZZER VOLUME  MINIMUM 0 , MAXIMUM 5000
    time.sleep(1)

    ir.write("WAITTIME 1.2") # waititme .. waitime should be less than test time  wait ime 1.2 , test time 1.5 seems tio be optimal to show pass fail result
    #ir.write("WAITTIME 1.2") # waititme .. waitime should be less than test time  wait ime 1.2 , test time 1.5 seems tio be optimal to show pass fail result
    time.sleep(1)
    #ir.close()




    #ir.write("*CLS") # this is need to get 32 in Measvalue
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

        for i in range(10):
            print("vent")
            #print(i)
            """ ir.write("MON?")
            print("mon",ir.read()) """
           
            ir.write("DSR?")
            time.sleep(0.2)
            l=ir.read()
            time.sleep(.1)
            DSR.append(l)
            
            #DSR.append(ir.query("DSR?"))
            #print(ir.query("DSR?"))
            #DSR only works with query command , START commnad has to precced DSR commnad , then only we get 16 for PASS and 12 for fail output
            #if display shows PASS then DSR op 16, else DSR op1
            time.sleep(.1)
            ir.write("MON?")
            time.sleep(0.2)
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
        
    #print("#first")
    #print(DSR,MeasValue)
    ir.write("STOP")
    time.sleep(1)
    ir.write("MON?")
    time.sleep(1)
    m=ir.read()
    #print("m",m)
   
    time.sleep(1)
    #print("measvalue -second")
    print(DSR,MeasValue)
    #exit()
    #print(MeasValue[0:14])
    print(MeasValue[5])
    print(type(MeasValue[5]))
    Resultcalc=MeasValue[7]
    R=(Resultcalc.split(","))
    Res_TestVolt=R[0]
    Res_IRvalue=R[1]
    Res_TestTime=R[2]
    print("RESULT- ir VALUE, TIME(S),VOLT(DCV)",Res_IRvalue,Res_TestTime,Res_TestVolt)

    #exit()

    if MeasValue[5]=='0':
        Result="PASS"
        
    elif MeasValue[5]=='1':
        Result="FAIL"
    
  
   
    
    else:
        Result="Contact Process ansvar "
    print(f"result of Channel  {x}",Result)
    return Result, Res_IRvalue,Res_TestTime,Res_TestVolt

for i in range(3):
    Result, Res_IRvalue,Res_TestTime,Res_TestVolt=IRTestOneCh('AB') 
    print(Result, Res_IRvalue,Res_TestTime,Res_TestVolt)

#IRTestOneCh('A')
#IRTestOneCh('B')
#IRTestOneCh('AB')