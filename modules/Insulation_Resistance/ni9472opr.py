import nidaqmx
import time
from nidaqmx.constants import LineGrouping
"""
no. 32 for channel A
no. 64 for ch B
no. 224 mellom ch A & B 
no.0 for open all

"""

RelayHw='cDAQ5Mod1/port0/line0:7'

def IRTest(RelayHw,Channel):
    if Channel=='A':
        Relay=32
    elif Channel=='B':
        Relay=64
    elif Channel=='AB':
        Relay=224
    elif Channel=='OPEN' :
        Relay=0
    else:
        Relay=0
    
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(
            #"Dev1/port0/line0:3", line_grouping=LineGrouping.CHAN_FOR_ALL_LINES
            #'5V_24V_NI9472/port0/line0:3', line_grouping=LineGrouping.CHAN_FOR_ALL_LINES
            RelayHw)
        task.start()
        task.write(Relay)
        time.sleep(.002)
    return Channel
        
def mATest(RelayHw,Channel):
    if Channel=='A':
        Relay=2
    elif Channel=='B':
        Relay=4
    elif Channel=='OPEN' :
        Relay=0
    else:
        Relay=0
    
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(
            #"Dev1/port0/line0:3", line_grouping=LineGrouping.CHAN_FOR_ALL_LINES
            #'5V_24V_NI9472/port0/line0:3', line_grouping=LineGrouping.CHAN_FOR_ALL_LINES
            RelayHw)
        task.start()
        task.write(Relay)
        time.sleep(.002)
    return Channel

def RevmATest(RelayHw,Channel):
    if Channel=='A':
        Relay=3
    elif Channel=='B':
        Relay=5
    elif Channel=='OPEN' :
        Relay=0
    else:
        Relay=0
    
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan(
            #"Dev1/port0/line0:3", line_grouping=LineGrouping.CHAN_FOR_ALL_LINES
            #'5V_24V_NI9472/port0/line0:3', line_grouping=LineGrouping.CHAN_FOR_ALL_LINES
            RelayHw)
        task.start()
        task.write(Relay)
        time.sleep(.002)
    return Channel


""" with nidaqmx.Task() as task:
            task.do_channels.add_do_chan(
                #"Dev1/port0/line0:3", line_grouping=LineGrouping.CHAN_FOR_ALL_LINES
                #'5V_24V_NI9472/port0/line0:3', line_grouping=LineGrouping.CHAN_FOR_ALL_LINES
                'cDAQ5Mod1/port0/line0:7')
            task.start()
            task.write(32) # FOR 5 v
            time.sleep(.002) """



""" #mA test '1' for ch A , '2' for ch 2 , 'OPEN' for open all
mATest(RelayHw,'A')
time.sleep(2) """

mATest(RelayHw,'OPEN')
time.sleep(2)


""" #RevmA test '1' for ch A , '2' for ch 2 , 'OPEN' for open all
RevmATest(RelayHw,'B')
time.sleep(2)  """
 
""" #IR test 'A' for ch A , 'B' for ch B , 'AB' for between ch A & B , 'OPEN' for open all 
IRTest(RelayHw,'A') 
mATest(RelayHw,'OPEN')
time.sleep(2) """