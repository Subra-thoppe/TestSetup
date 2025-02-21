import sys
#print(sys.path)
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
    timer=10
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
    return ir

def IRinitrun(x):
    ir=IRTestOneCh(x)

    ir.write("*CLS") # this is need to get 32 in Measvalue
    time.sleep(2)
    ir.write("START")
    return ir

def IRdataread(x,ir,DSR1,MeasValue, timer ,stop):
    #print("timer",timer)
    # Read data from the instrument
    """ data = ir.read_bytes(num_bytes_to_read)
    print(f"Read {len(data)} bytes from the instrument: {data}")
    """
    # Print the read data
    #print(ir.read())
    
    #print("ir read)")
    print(ir.read())
    #if ir.read()=='OK':
    starttime=time.time()
    while stop=='FALSE':
            #print("stop",stop)     
            #for i in range(10):
            #print("vent")
            #print(i)
            """ ir.write("MON?")
            print("mon",ir.read()) """
           
            ir.write("DSR?")
            time.sleep(0.05)
            l=ir.read()
            #print("l",l)
            #print(type(l))
            #exit()
            time.sleep(0.05)
            DSR1.append(l)
            
            #DSR.append(ir.query("DSR?"))
            #print(ir.query("DSR?"))
            #DSR only works with query command , START commnad has to precced DSR commnad , then only we get 16 for PASS and 12 for fail output
            #if display shows PASS then DSR op 16, else DSR op1
            
            ir.write("MON?")
            time.sleep(0.05)
            m=ir.read()
            #print("m",m)
            MeasValue.append(m)
            #MeasValue.append(ir.query("MON?"))
            #print(ir.query("MON?"))
            #print("dsr",ir.read())
            stoptime=time.time()
            #print("time",stoptime-starttime)
            #print("DSR,MEASVALUE",DSR1,MeasValue)
           
            
            
            #print("l",l, "sp[1]", sp[1])
            if l=='12' or l=='16':
                #print("in if case l")
                #print(type(m))
                if (m.find(",")) !=-1:
                    sp=m.split(",")
                    #print("sp",sp)
                    if len(sp)>=2:
                        if sp[1]=='5000E6':
                            stop='TRUE'
                            #print(stop)
                            Result='PASSED'
                            ir.write("STOP")
                        else:
                            stop='FALSE'
                            Result='FAILED'
                else:
                            stop='FALSE'
                
            else:
                if stoptime-starttime>=timer :
                    stop='TRUE'
                    #print(stop)
                    Result='FAILED'
                    ir.write("STOP")
                else:
                    stop='FALSE'
    
    #print("error")
    ir.write("STOP")
    #exit()
        
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
    #print(DSR1,MeasValue)
    #exit()
    #print(MeasValue[0:14])
    """ print(MeasValue[5])
    print(type(MeasValue[5]))
    Resultcalc=MeasValue[7]
    R=(Resultcalc.split(","))
    Res_TestVolt=R[0]
    Res_IRvalue=R[1]
    Res_TestTime=R[2] """
    print("RESULT- ir VALUE, TIME(S),VOLT(DCV)",DSR1,MeasValue,m ) #Res_IRvalue,#Res_TestTime,Res_TestVolt,)

    #exit()

    """ if MeasValue[5]=='0':
        Result="PASS"
        
    elif MeasValue[5]=='1':
        Result="FAIL"
    
  
   
    
    else:
        Result="Contact Process ansvar "
    print(f"result of Channel  {x}",Result) """
    #return Result, Res_IRvalue,Res_TestTime,Res_TestVolt
    return DSR1,MeasValue,m ,Result

""" for i in range(3):
    Result, Res_IRvalue,Res_TestTime,Res_TestVolt=IRTestOneCh('AB') 
    print(Result, Res_IRvalue,Res_TestTime,Res_TestVolt) """

"""
ir=IRinitrun('A')
DSR1=[]
MeasValue=[]
timer=10
stop='FALSE'
DSR1,MeasValue,m=IRdataread('A',ir,DSR1,MeasValue, timer,stop)
print("all result", DSR1,MeasValue,m)
print(m[-1])
sp=m[-1].split(",")
IRtid=10 - float(sp[2])
IRtid= round(IRtid,4)
IRvalue=sp[1]
IRvolt=sp[0]
print(IRtid,IRvalue, IRvolt)
s3 = ' ,'.join(s[4:-1])
print(s3) # Output: Hello World

"""
#IRTestOneCh('A')
#IRTestOneCh('B')
#IRTestOneCh('AB')