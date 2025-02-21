# driver for Agilent 34970A , RElay card 34903A and MUX card 34901A 
import pyvisa
import time
import sys
#sys.path.append("C:/Scansense/jeya/AM5000/python-lib")
#sys.path.append("C:/Scansense/jeya/AM5000/python-lib/modules/Insulation_Resistance")
#C:\Scansense\jeya\AM5000\python-lib\modules\Insulation_Resistance
#from main import *

# 25.10.24 - relay switch delay decreased from 0.5
def test():
    print("Working")
def Connect_agilent34970A():
    rm = pyvisa.ResourceManager()

    agilent34970A = rm.open_resource("ASRL5::INSTR")
    agilent34970A.read_termination = "\n"
    agilent34970A.baud_rate = 9600
    return agilent34970A 

#print(Connect_agilent34970A())
""" agilent34970A.write("ROUT:CLOSE (@101)") # done code 19/18, fail code 12
time.sleep(2)
agilent34970A.write(("ROUT:OPEN (@101:120)")) """
#ir.write(("ROUT:OPEN (@201)"))

def openallchannels():
    agilent34970A =Connect_agilent34970A()
    print(agilent34970A.query("*IDN?"))
    agilent34970A.write("*CLS")
    agilent34970A.write("ROUT:OPEN (@101:120)")

#openallchannels()
def CloseOneChannel(ch):
    #ch1=str(ch)
    agilent34970A =Connect_agilent34970A()
    agilent34970A.write(f"ROUT:CLOSE (@{ch})")

def CommunicateChA():
    openallchannels()
    #time.sleep(0.5)
    time.sleep(0.2)
    CloseOneChannel('101')
    time.sleep(0.2)
    CloseOneChannel('104')
    time.sleep(0.2)
    CloseOneChannel('105')
    time.sleep(0.2)
    CloseOneChannel('109')

def CommunicateChB():
    openallchannels()
    time.sleep(0.2)
    CloseOneChannel('101')
    time.sleep(0.2)
    CloseOneChannel('106')
    time.sleep(0.2)
    CloseOneChannel('107')
    time.sleep(0.2)
    CloseOneChannel('109')
    time.sleep(0.2)
    CloseOneChannel('110')
    time.sleep(0.2)
    CloseOneChannel('113')
    time.sleep(0.2)

def mAtestChA():
    openallchannels()
    time.sleep(0.15)
    CloseOneChannel('101')
    time.sleep(0.15)
    CloseOneChannel('104')
    time.sleep(0.15)
    CloseOneChannel('105')
    time.sleep(0.15)
    CloseOneChannel('109')


def mAtestChB():
    openallchannels()
    time.sleep(0.15)
    CloseOneChannel('101')
    time.sleep(0.15)
    CloseOneChannel('106')
    time.sleep(0.15)
    CloseOneChannel('107')
    time.sleep(0.15)
    CloseOneChannel('109')
    time.sleep(0.15)
    CloseOneChannel('110')
    time.sleep(0.15)
    CloseOneChannel('113')
    time.sleep(0.15)

def IRtestChAandbody():
    openallchannels()
    time.sleep(0.3)
    CloseOneChannel('103')
    time.sleep(0.3)
    CloseOneChannel('104')
    time.sleep(0.3)
    CloseOneChannel('105')
    time.sleep(0.3)
    CloseOneChannel('111')
    time.sleep(0.3)



def IRtestChBandbody():
    openallchannels()
    time.sleep(0.3)
    CloseOneChannel('103')
    time.sleep(0.3)
    CloseOneChannel('106')
    time.sleep(0.3)
    CloseOneChannel('107')
    time.sleep(0.3)
    CloseOneChannel('112')
    time.sleep(0.3)
    CloseOneChannel('113')
    time.sleep(0.3)

def IRtestChAandChB():
    openallchannels()
    time.sleep(0.3)
    CloseOneChannel('103')
    time.sleep(0.3)
    CloseOneChannel('104')
    time.sleep(0.3)
    CloseOneChannel('105')
    time.sleep(0.3)
    CloseOneChannel('106')
    time.sleep(0.3)
    CloseOneChannel('107')
    time.sleep(0.3)
    CloseOneChannel('108')
    time.sleep(0.3)
    CloseOneChannel('111')
    time.sleep(0.3)
    CloseOneChannel('112')
    time.sleep(0.3)


#open all cahnnels
#openallchannels()

#time.sleep(2)

""" #PGA 305 communciation ChA
CommunicateChA()
time.sleep(2)
sn = PGA305.Connect()[0]
print("Connect:\t\t", sn)
#print(PGA305.Connect())
print("Activate:\t\t", PGA305.Activate(sn))
serialnumber = PGA305.ReadICSerial(sn) #1
print("Read serial:\t\t",serialnumber ) #
#PGA305.Activate """

#CommunicateChA()


#CommunicateChB()

#mAtestChA()

#mAtestChB()

#openallchannels()
  
#IRtestChAandbody()
#IRtestChBandbody()
#IRtestChAandChB()

""" openallchannels()
IRtestChAandChB() """

""" TO open or close Relay channels  give channel no. with slot no . slot 1 is relay card 34903A
ir.write("ROUT:CLOSE (@101)") # done code 19/18, fail code 12
time.sleep(2)
ir.write(("ROUT:OPEN (@101)")

TO open or close Mux channels  give channel no. with slot no . slot 2 is MUX card 34901A 
ir.write("ROUT:CLOSE (@201)") # done code 19/18, fail code 12
time.sleep(2)
ir.write(("ROUT:OPEN (@201)") """

