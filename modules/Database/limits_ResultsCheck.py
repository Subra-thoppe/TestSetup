import pandas as pd
import time
from datetime import datetime
import numpy as np

#database connection
# working 
import pyodbc as odbc


def Connect_SQLdb():
    #import pyodbc as odbc
    #import sqlite3
    DRIVER_NAME='SQL SERVER'
    SERVER_NAME='SQL04'
    DABASE_NAME='ProdDB'

    Connection_string=f""" 

    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABSE={DABASE_NAME};
    Trust_connection=yes
    uid='jetsub'
    pwd='Laget2501!'
    """
    cnxn=odbc.connect(Connection_string)
    cursor=cnxn.cursor()
    #print(cursor)
    return cnxn,cursor
#cnxn, cursor=Connect_SQLdb()

##WO details

""" SensorElements=[88542,88534,88523,88522,88551,88536,88544,88526,88548,88545,88546,88529]

SerialNos=[19311,19327,19325,19319,19299,19309,19301, 19317,19303,19315,19321,19305]
#channelno=[0,1]


ProdOrderx=223340
ProdNox=124179
Station='DESKTOP-EUTQFRK'
Prosess='Test&Setup'
#SADC,#LoggElTest #IrTest,#TempChk
sw='python'
Batch='K22-0108'
Operator_ID=314
Recipe_ID=405
DateTime= datetime.now().replace(microsecond=0)
"""
#Create ProcessID for TSEtof setup tests

#print(DateTime)

#limits read and Tests


Limitfile="C:\AM5000\python-libTestsetup-nysw\modules\LimitSetting\TestSetup_limits_STW_AM5000.txt"

df2=pd.read_csv(Limitfile, sep="\t", header=None)
#print(df2)

#print(df2.iloc[[1][0]])
#current row 1,IR row 2, PADC row 3, TADC row 4, low limit col1, upper limit col 2 
#print(float(df2.iat[1,1]))
""" 
ChannelNo=0
data=3.9
ResultDisp='xx'
Resultdb='xx'
Overstyr='FALSE'
 """

#Limitfile="C:\Scansense\jeya\AM5000\TestSetup_limits_STW_AM5000.txt"
def CurrentLimitAccep(ChannelNo,data):
    df2=pd.read_csv(Limitfile, sep="\t", header=None)
    LowerLimit=float(df2.iat[1,1])
    UpperLimit=float(df2.iat[1,2])
    if data<LowerLimit or data>UpperLimit:
        ResultDisp='FAIL_CurrentLimit'
        Resultdb='FAILED'
    else:
        ResultDisp='PASS_current'
        Resultdb='PASSED'
    return ResultDisp, Resultdb, ChannelNo
    

def IRLimitAccep(ChannelNo,data,Testtime):
    df2=pd.read_csv(Limitfile, sep="\t", header=None)
    LowerLimit=float(df2.iat[2,1])
    UpperLimit=float(df2.iat[2,2])
    print("limtis",UpperLimit,LowerLimit)
    if data<LowerLimit or data>UpperLimit:
        ResultDisp='FAIL_IRLimit'
        Resultdb='FAILED'
    else:
        ResultDisp='PASS_IR'
        Resultdb='PASSED'
    return ResultDisp, Resultdb, Testtime,ChannelNo

def OffsetLimitAccep(ChannelNo,data,Overstyr):
    df2=pd.read_csv(Limitfile, sep="\t", header=None)
    LowerLimit= float(df2.iat[3,1])
    UpperLimit= float(df2.iat[3,2])
    if Overstyr=='TRUE':
        ResultDisp='PASS_Offset'
        Resultdb='PASSED'   
    else:
        if data<=LowerLimit:
            ResultDisp=' STW MEMBRANE WIREBOND FEIL. (BONDEPAD NO.4 ELLER  NO.6 PÅ STW MEMBRANE ) SJEKK HVIS ALLE BONDEPADER ER WIREBONDET. KONTAKT PROSSESS ANSVARLIG HVIS ALLE WIREBOND ER PÅ PLASS'
            Resultdb='FAILED'
        else:
            if data>=UpperLimit:
                ResultDisp=' STW MEMBRANE WIREBOND FEIL. ( BONDEPAD NO. 3 ELLER 5 PÅ STW MEMBRANE ).SJEKK HVIS ALLE BONDEPADER ER WIREBONDET. KONTAKT PROSSESS ANSVARLIG HVIS ALLE WIREBOND ER PÅ PLASS'
                Resultdb='FAILED'
            else:
                ResultDisp='PASS_Offset'
                Resultdb='PASSED'
         
    return ResultDisp, Resultdb,ChannelNo


def innerOffsetLimitAccep(ChannelNo,data,Overstyr):
    df2=pd.read_csv(Limitfile, sep="\t", header=None)
    LowerLimit= float(df2.iat[5,1])
    UpperLimit= float(df2.iat[5,2])
    if Overstyr=='TRUE':
        ResultDisp='PASS_Offset'
        Resultdb='PASSED'   
    else:
        if abs(data)<=LowerLimit:
            ResultDisp=' STW MEMBRANE WIREBOND FEIL. (BONDEPAD NO.4 ELLER  NO.6 PÅ STW MEMBRANE ) SJEKK HVIS ALLE BONDEPADER ER WIREBONDET. KONTAKT PROSSESS ANSVARLIG HVIS ALLE WIREBOND ER PÅ PLASS'
            Resultdb='FAILED'
        else:
            if abs(data)<=UpperLimit:
                ResultDisp=' STW MEMBRANE WIREBOND FEIL. ( BONDEPAD NO. 3 ELLER 5 PÅ STW MEMBRANE ).SJEKK HVIS ALLE BONDEPADER ER WIREBONDET. KONTAKT PROSSESS ANSVARLIG HVIS ALLE WIREBOND ER PÅ PLASS'
                Resultdb='FAILED'
            else:
                ResultDisp='PASS_Offset'
                Resultdb='PASSED'
         
    return ResultDisp, Resultdb,ChannelNo

def TempLimitAccep(ChannelNo,data):
    df2=pd.read_csv(Limitfile, sep="\t", header=None)
    LowerLimit=float(df2.iat[4,1])
    UpperLimit=float(df2.iat[4,2])
    if data<LowerLimit or data>UpperLimit:
        ResultDisp='FAIL_Offset_TADCLimit'
        Resultdb='FAILED'
    else:
        ResultDisp='PASS_Temp_TADC'
        Resultdb='PASSED'
    return ResultDisp, Resultdb,ChannelNo


def EEPROMcheck(ChannelNo):
    # read EEProm 
   """  config for nordbit
    read serial number of elektronic
    read eeprom values 
    if serial no is not correct or empty eeprom , then error 

    write standard confog to electronic """
   return ChannelNo


""" Resultdisplay,Resulttodatabase=CurrentLimitAccep(data,float(df2.iat[1,1]), float(df2.iat[1,2]), ResultDisp,Resultdb)
Resultdisplay,Resulttodatabase=IRLimitAccep(data,float(df2.iat[2,1]), float(df2.iat[2,2]), ResultDisp,Resultdb)
Resultdisplay,Resulttodatabase=OffsetLimitAccep(abs(data),Overstyr, float(df2.iat[3,1]), float(df2.iat[3,2]), ResultDisp, Resultdb)
#if offset is failed and all are o.k. , need to run with Oversytr as 'TRUE' again to get PASSED
Resultdisplay,Resulttodatabase=TempLimitAccep(data,float(df2.iat[4,1]), float(df2.iat[4,2]), ResultDisp,Resultdb)
print(Resultdisplay,Resulttodatabase) """


# writing result to SQL database

#get processid for ch 0 or 1 
 #use ChannelNo
 #CurrentSQLdb_Process(SensorElement_ID,channel)
def CurrentSQLdb_Process(SensorElement_ID, channel, Prosess,ProdOrderx,ProdNox,Station,ProsessType,sw,Batch, Operator_ID, Recipe_ID):
    cnxn,cursor=Connect_SQLdb()
   # inserts new row in prosess table and gets the prosess ID
    Prosess='mAtest'
    ProsessType='Test&Setup'
    Timenow = datetime.now().replace(microsecond=0)
    DateTime=Timenow
    cursor.execute("INSERT INTO ProdDB.dbo.Prosess( SensorElement_ID,ProdOrder,ProdNo, Station, Prosess,ProsessType, Channel, SW,Batch,Operator_ID,DateTime,Recipe_ID) values (?,?,?,?,?,?,?,?,?,?,?,?)", SensorElement_ID, ProdOrderx, ProdNox, Station, Prosess, ProsessType, channel,sw,Batch,Operator_ID,DateTime,Recipe_ID)
    cnxn.commit()
    #return process ID
    query="SELECT  TOP (1) Prosess_ID FROM   ProdDB.dbo.Prosess WHERE (ProdOrder =? )AND (SensorElement_ID =?) AND (channel=?) AND (Prosess=?) ORDER BY DateTime DESC"
    parameter=[ProdOrderx,SensorElement_ID,channel,Prosess]
    df = pd.read_sql(query, cnxn, params=parameter)
    print(df)
    Curr_Prosess_ID=df.iat[0,0]
    print(Curr_Prosess_ID)
    if Curr_Prosess_ID  == "" or np.isnan(df.iat[0,0]) == 'True':
        print("Processid error")
        exit()
    cursor.close()
    cnxn.close()
    return Curr_Prosess_ID
#working
#Current_Prosess_ID=CurrentSQLdb_Process(88542,0)
""" Current_Prosess_ID=CurrentSQLdb_Process(88542,0,'IR',224288,124189,'pc','Test&Setup','v1','jk22',324, 1)
print(Current_Prosess_ID) """

def IRSQLdb_Process(SensorElement_ID, channel, Prosess,ProdOrderx,ProdNox,Station,ProsessType,sw,Batch, Operator_ID, Recipe_ID):
    # inserts new row in prosess table and gets the prosess ID
    cnxn,cursor=Connect_SQLdb()
    #Prosess='IrTest'  # got from calling funciton 
    #ProsessType='Test&Setup'
    Timenow = datetime.now().replace(microsecond=0)
    DateTime=Timenow
    cursor.execute("INSERT INTO ProdDB.dbo.Prosess( SensorElement_ID,ProdOrder,ProdNo, Station, Prosess,ProsessType, Channel, SW,Batch,Operator_ID,DateTime,Recipe_ID) values (?,?,?,?,?,?,?,?,?,?,?,?)", SensorElement_ID, ProdOrderx, ProdNox, Station, Prosess, ProsessType, channel,sw,Batch,Operator_ID,DateTime,Recipe_ID)
    cnxn.commit()
    #return process ID
    query="SELECT  TOP (1) Prosess_ID FROM   ProdDB.dbo.Prosess WHERE (ProdOrder =? )AND (SensorElement_ID =?) AND (channel=?) AND (Prosess=?) ORDER BY DateTime DESC"
    parameter=[ProdOrderx,SensorElement_ID,channel,Prosess]
    df = pd.read_sql(query, cnxn, params=parameter)
    print(df)
    IR_Prosess_ID=df.iat[0,0]
    print(IR_Prosess_ID)
    if IR_Prosess_ID  == "" or np.isnan(df.iat[0,0]) == 'True':
        print("Processid error")
        exit()
    cursor.close()
    cnxn.close()
    return IR_Prosess_ID
#working
#IR_Prosess_ID=IRSQLdb_Process(88542,0,'IR',224288,124189,'pc','Test&Setup','v1','jk22',324, 1)
#print("hh",IR_Prosess_ID)

def offsetSQLdb_Process(SensorElement_ID, channel, Prosess,ProdOrderx,ProdNox,Station,ProsessType,sw,Batch, Operator_ID, Recipe_ID):
    # inserts new row in prosess table and gets the prosess ID
    cnxn,cursor=Connect_SQLdb()
    """ Prosess='SADC'
    ProsessType='Test&Setup' """
    Timenow = datetime.now().replace(microsecond=0)
    DateTime=Timenow
    print("all print",SensorElement_ID, channel, Prosess,ProdOrderx,ProdNox,Station,ProsessType,sw,Batch, Operator_ID, Recipe_ID, DateTime)
    cursor.execute("INSERT INTO ProdDB.dbo.Prosess( SensorElement_ID,ProdOrder,ProdNo, Station, Prosess,ProsessType, Channel, SW,Batch,Operator_ID,DateTime,Recipe_ID) values (?,?,?,?,?,?,?,?,?,?,?,?)", SensorElement_ID, ProdOrderx, ProdNox, Station, Prosess, ProsessType, channel,sw,Batch,Operator_ID,DateTime,Recipe_ID)
    cnxn.commit()
    #return process ID
    query="SELECT  TOP (1) Prosess_ID FROM   ProdDB.dbo.Prosess WHERE (ProdOrder =? )AND (SensorElement_ID =?) AND (channel=?) AND (Prosess=?) ORDER BY DateTime DESC"
    parameter=[ProdOrderx,SensorElement_ID,channel,Prosess]
    df = pd.read_sql(query, cnxn, params=parameter)
    print(df)
    offset_Prosess_ID=df.iat[0,0]
    print(offset_Prosess_ID)
    if offset_Prosess_ID  == "" or np.isnan(df.iat[0,0]) == 'True':
        print("Processid error")
        exit()
    cursor.close()
    cnxn.close()
    return offset_Prosess_ID
#working
""" offset_Prosess_ID=offsetSQLdb_Process(88542,0,'IR',224288,124189,'pc','Test&Setup','v1','jk22',324, 1)
print(offset_Prosess_ID) """


def ElectronicSQLdb_Process(SensorElement_ID, ProdOrderx,ProdNox,Serialno,Elekslno,ElekBatchno,Operator_ID,Comments,DateTime,ch,Bootloader,application,Kommenter):
    # inserts new row in prosess table and gets the prosess ID
    cnxn,cursor=Connect_SQLdb()
    """ Prosess='SADC'
    ProsessType='Test&Setup' """
    Timenow = datetime.now().replace(microsecond=0)
    DateTime=Timenow
    #Kommenter=' '
    #Comments=' '
    #¤Bootloader=1
    #application=1

    #print("all print",SensorElement_ID, channel, Prosess,ProdOrderx,ProdNox,Station,ProsessType,sw,Batch, Operator_ID, Recipe_ID, DateTime)
    cursor.execute("INSERT INTO ProdDB.dbo. Electronic( SensorElement_ID, ProdOrder, ProdNo, SerialNum, ElSerial, ElBatch, Operator_ID, Comments, DateTime, Channel, Bootloader, Application, Kommentar) values (?,?,?,?,?,?,?,?,?,?,?,?,?)", SensorElement_ID, ProdOrderx, ProdNox,Serialno,Elekslno,ElekBatchno,Operator_ID,Comments,DateTime,ch,Bootloader,application,Kommenter)
    cnxn.commit()
    #return process ID
    query="SELECT  TOP (1) Electronic_ID FROM   ProdDB.dbo.Electronic WHERE (ProdOrder =? )AND (SensorElement_ID =?) AND (channel=?) AND (SerialNum=?) ORDER BY DateTime DESC"
    parameter=[ProdOrderx,SensorElement_ID,ch,str(Serialno)]
    df = pd.read_sql(query, cnxn, params=parameter)
    #print(df)
    Elec_Prosess_ID=df.iat[0,0]
    print(Elec_Prosess_ID)
    if Elec_Prosess_ID  == "" or np.isnan(df.iat[0,0]) == 'True':
        print("Processid error")
        exit()
    cursor.close()
    cnxn.close()
    return Elec_Prosess_ID

""" SensorElement_ID=88542
ProdOrderx=224505
ProdNox=124170
Serialno=19311
Elekslno=10000
ElekBatchno=79833
Operator_ID=214
Comments=' '
DateTime=datetime.now().replace(microsecond=0)
ch=0
Bootloader=1
application=1
Kommenter=' '


ElectronicSQLdb_Process(SensorElement_ID, ProdOrderx,ProdNox,Serialno,Elekslno,ElekBatchno,Operator_ID,Comments,DateTime,ch,Bootloader,application,Kommenter)
 """

def PIH_PHT_SQLdb_Process(SensorElement_ID, channel, Prosess,ProdOrderx,ProdNox,Station,ProsessType,sw,Batch, Operator_ID, Recipe_ID):
    # inserts new row in prosess table and gets the prosess ID
    cnxn,cursor=Connect_SQLdb()
    """ Prosess='SADC'
    ProsessType='Test&Setup' """
    Timenow = datetime.now().replace(microsecond=0)
    DateTime=Timenow
    print("all print",SensorElement_ID, channel, Prosess,ProdOrderx,ProdNox,Station,ProsessType,sw,Batch, Operator_ID, Recipe_ID, DateTime)
    cursor.execute("INSERT INTO ProdDB.dbo.Prosess( SensorElement_ID,ProdOrder,ProdNo, Station, Prosess,ProsessType, Channel, SW,Batch,Operator_ID,DateTime,Recipe_ID) values (?,?,?,?,?,?,?,?,?,?,?,?)", SensorElement_ID, ProdOrderx, ProdNox, Station, Prosess, ProsessType, channel,sw,Batch,Operator_ID,DateTime,Recipe_ID)
    cnxn.commit()
    #return process ID
    query="SELECT  TOP (1) Prosess_ID FROM   ProdDB.dbo.Prosess WHERE (ProdOrder =? )AND (SensorElement_ID =?) AND (channel=?) AND (Prosess=?) ORDER BY DateTime DESC"
    parameter=[ProdOrderx,SensorElement_ID,channel,Prosess]
    df = pd.read_sql(query, cnxn, params=parameter)
    print(df)
    offset_Prosess_ID=df.iat[0,0]
    print(offset_Prosess_ID)
    if offset_Prosess_ID  == "" or np.isnan(df.iat[0,0]) == 'True':
        print("Processid error")
        exit()
    cursor.close()
    cnxn.close()
    return offset_Prosess_ID
#all print 95119 0 EBW-PIH 224504 124170 HPSHAKER01 Work 1 100 229 1 2024-09-23 14:49:21
#pih_Prosess_ID=PIH_PHT_SQLdb_Process(88542,0,'IR',224288,124189,'pc','Test&Setup','v1','jk22',324, 1)
""" elementid=95119
channel=int(0)
Prosess='EBW-PIH'
#ProsessType='EBW-PIH-PYTHON-V1'
ProdOrderx=224504
ProdNox=124170
print(ProdNox,ProdOrderx)
Station='HPSHAKER01'
sw='1'
Batch='100'
Recipe_ID=1
ProsessType='Work' """
""" pih_Prosess_ID=PIH_PHT_SQLdb_Process(elementid,channel,Prosess,ProdOrderx,ProdNox,Station,ProsessType,sw,Batch,324, 1)
print(pih_Prosess_ID)  """

def adctest_Process(SensorElement_ID, channel, Prosess,ProdOrderx,ProdNox,Station,ProsessType,sw,Batch, Operator_ID, Recipe_ID):
    # inserts new row in prosess table and gets the prosess ID
    cnxn,cursor=Connect_SQLdb()
    """ Prosess='SADC'
    ProsessType='Test&Setup' """
    Timenow = datetime.now().replace(microsecond=0)
    DateTime=Timenow
    print("all print",SensorElement_ID, channel, Prosess,ProdOrderx,ProdNox,Station,ProsessType,sw,Batch, Operator_ID, Recipe_ID, DateTime)
    cursor.execute("INSERT INTO ProdDB.dbo.Prosess( SensorElement_ID,ProdOrder,ProdNo, Station, Prosess,ProsessType, Channel, SW,Batch,Operator_ID,DateTime,Recipe_ID) values (?,?,?,?,?,?,?,?,?,?,?,?)", SensorElement_ID, ProdOrderx, ProdNox, Station, Prosess, ProsessType, channel,sw,Batch,Operator_ID,DateTime,Recipe_ID)
    cnxn.commit()
    #return process ID
    query="SELECT  TOP (1) Prosess_ID FROM   ProdDB.dbo.Prosess WHERE (ProdOrder =? )AND (SensorElement_ID =?) AND (channel=?) AND (Prosess=?) ORDER BY DateTime DESC"
    parameter=[ProdOrderx,SensorElement_ID,channel,Prosess]
    df = pd.read_sql(query, cnxn, params=parameter)
    print(df)
    adctest_Prosess_ID=df.iat[0,0]
    print(adctest_Prosess_ID)
    if adctest_Prosess_ID  == "" or np.isnan(df.iat[0,0]) == 'True':
        print("Processid error")
        exit()
    cursor.close()
    cnxn.close()
    return adctest_Prosess_ID

def FAT_calver_Process(SensorElement_ID, channel, Prosess,ProdOrderx,ProdNox,Station,ProsessType,sw,Batch, Operator_ID, Recipe_ID):
    # inserts new row in prosess table and gets the prosess ID
    cnxn,cursor=Connect_SQLdb()
    """ Prosess='SADC'
    ProsessType='Test&Setup' """
    Timenow = datetime.now().replace(microsecond=0)
    DateTime=Timenow
    print("all print",SensorElement_ID, channel, Prosess,ProdOrderx,ProdNox,Station,ProsessType,sw,Batch, Operator_ID, Recipe_ID, DateTime)
    cursor.execute("INSERT INTO ProdDB.dbo.Prosess( SensorElement_ID,ProdOrder,ProdNo, Station, Prosess,ProsessType, Channel, SW,Batch,Operator_ID,DateTime,Recipe_ID) values (?,?,?,?,?,?,?,?,?,?,?,?)", SensorElement_ID, ProdOrderx, ProdNox, Station, Prosess, ProsessType, channel,sw,Batch,Operator_ID,DateTime,Recipe_ID)
    cnxn.commit()
    #return process ID
    query="SELECT  TOP (1) Prosess_ID FROM   ProdDB.dbo.Prosess WHERE (ProdOrder =? )AND (SensorElement_ID =?) AND (channel=?) AND (Prosess=?) ORDER BY DateTime DESC"
    parameter=[ProdOrderx,SensorElement_ID,channel,Prosess]
    df = pd.read_sql(query, cnxn, params=parameter)
    print(df)
    FAT_calver_Prosess_ID=df.iat[0,0]
    print(FAT_calver_Prosess_ID)
    if FAT_calver_Prosess_ID == "" or np.isnan(df.iat[0,0]) == 'True':
        print("Processid error")
        exit()
    cursor.close()
    cnxn.close()
    return FAT_calver_Prosess_ID

""" elementid=97388
channel=int(0)
Prosess='CalibrationVerification'
ProsessType='FAT'
ProdOrderx=224600
ProdNox=124170
print(ProdNox,ProdOrderx)
Station='HPSHAKER01'
sw='v9'
Batch='100'
Recipe_ID=1

FAT_calver_Prosess_ID=FAT_calver_Process(elementid,channel,Prosess,ProdOrderx,ProdNox,Station,ProsessType,sw,Batch,324, 1)
print(FAT_calver_Prosess_ID)  """


""" skaptemp=20.1
trykksigpr=8.3679535
ReadmA=4.207020675
ExpectedmA=4.194039501
FSerror=0.012
Result='PASS'
Prosess_ID=int(FAT_calver_Prosess_ID)
 """

def FATcalver_WriteResulttoSQLdb_ProcessData(Prosess_ID,skaptemp, trykksigpr, readma, expectedma,FSerror, result ):
    #Writes process esults
    cnxn,cursor=Connect_SQLdb()
    #ProcessID=df.iat[0,0] # get process ifd for ch 0 or 1 
    ResultType='mA'
    Max=0
    Min=0
    #KeyValue=curr_value
    Unit='mA'
    Timenow = datetime.now().replace(microsecond=0)
    DateTime=Timenow
    #SELECT        TOP (200) ProsessData_ID, Prosess_ID, SetT, SetL, RefT, RefL, SigT, SigL, Unit, DateTime, Data3, Data4
    cursor.execute("INSERT INTO ProdDB.dbo.ProsessData(Prosess_ID,RefT, RefL, ReadmA, ExpectedmA, FullScaleError, Result,Unit,DateTime) values (?,?,?,?,?,?,?,?,?)",Prosess_ID,skaptemp, trykksigpr, readma, expectedma,FSerror, result ,Unit,DateTime )
    cnxn.commit()
    cursor.close()
    cnxn.close()

#FATcalver_WriteResulttoSQLdb_ProcessData(Prosess_ID,skaptemp, trykksigpr, ReadmA, ExpectedmA,FSerror, Result )

""" def FATcalver_WritetoSQLdb_ProcessData(Prosess_ID,RefT, RefL, ReadmA, ExpectedmA, FullScaleError, Result,Unit, DateTime):
    #Writes process esults
    cnxn,cursor=Connect_SQLdb()
    #ProcessID=df.iat[0,0] # get process ifd for ch 0 or 1 
    SetT, SetL, SigT, SigL, Data3, Data4,=0
    Unit='mA'
    Timenow = datetime.now().replace(microsecond=0)
    DateTime=Timenow
    cursor.execute("INSERT INTO ProdDB.dbo.ProsessData(Prosess_ID,RefT, RefL, ReadmA, ExpectedmA, FullScaleError, Result,Unit,DateTime) values (?,?,?,?,?,?,?,?,?)", Prosess_ID,ResultType,Resultdb,Max,Min,KeyValue,Unit,DateTime )
    cnxn.commit()
    cursor.close()
    cnxn.close()
 """

def TempSQLdb_Process(SensorElement_ID, channel, Prosess,ProdOrderx,ProdNox,Station,ProsessType,sw,Batch, Operator_ID, Recipe_ID):
    # inserts new row in prosess table and gets the prosess ID
    cnxn,cursor=Connect_SQLdb()
    """ Prosess='TempChk'
    ProsessType='Test&Setup' """
    Timenow = datetime.now().replace(microsecond=0)
    DateTime=Timenow
    cursor.execute("INSERT INTO ProdDB.dbo.Prosess( SensorElement_ID,ProdOrder,ProdNo, Station, Prosess,ProsessType, Channel, SW,Batch,Operator_ID,DateTime,Recipe_ID) values (?,?,?,?,?,?,?,?,?,?,?,?)", SensorElement_ID, ProdOrderx, ProdNox, Station, Prosess, ProsessType, channel,sw,Batch,Operator_ID,DateTime,Recipe_ID)
    cnxn.commit()
    #return process ID
    query="SELECT  TOP (1) Prosess_ID FROM   ProdDB.dbo.Prosess WHERE (ProdOrder =? )AND (SensorElement_ID =?) AND (channel=?) AND (Prosess=?) ORDER BY DateTime DESC"
    parameter=[ProdOrderx,SensorElement_ID,channel,Prosess]
    df = pd.read_sql(query, cnxn, params=parameter)
    print(df)
    Temp_Prosess_ID=df.iat[0,0]
    print(Temp_Prosess_ID)
    if Temp_Prosess_ID  == "" or np.isnan(df.iat[0,0]) == 'True':
        print("Processid error")
        exit()
    cursor.close()
    cnxn.close()
    return Temp_Prosess_ID
#working
""" Temp_Prosess_ID=offsetSQLdb_Process(88542,0,'IR',224288,124189,'pc','Test&Setup','v1','jk22',324, 1)
print(Temp_Prosess_ID) """

# process Result Table
def CurrentWriteResulttoSQLdb_ProcessRes(Prosess_ID,Resultdb,curr_value):
    #Writes process esults
    cnxn,cursor=Connect_SQLdb()
    #ProcessID=df.iat[0,0] # get process ifd for ch 0 or 1 
    ResultType='mA'
    Max=0
    Min=0
    KeyValue=curr_value
    Unit='mA'
    Timenow = datetime.now().replace(microsecond=0)
    DateTime=Timenow
    cursor.execute("INSERT INTO ProdDB.dbo.ProsessRes(Prosess_ID,ResultType,Result, Max, Min,KeyValue,Unit,DateTime) values (?,?,?,?,?,?,?,?)", Prosess_ID,ResultType,Resultdb,Max,Min,KeyValue,Unit,DateTime )
    cnxn.commit()
    cursor.close()
    cnxn.close()
curr_value=3.93
#working
#CurrentWriteResulttoSQLdb_ProcessRes(int(Current_Prosess_ID),Resultdb,curr_value)

def IRWriteResulttoSQLdb_ProcessRes(ProsessID,Resultdb, IRValue,IRTestTime):
    cnxn,cursor=Connect_SQLdb()
    ResultType='IR'
    Max=0
    Min=IRTestTime
    KeyValue=IRValue
    Unit='MOhm'
    Timenow = datetime.now().replace(microsecond=0)
    DateTime=Timenow
    cursor.execute("INSERT INTO ProdDB.dbo.ProsessRes(Prosess_ID,ResultType,Result, Max, Min,KeyValue,Unit,DateTime) values (?,?,?,?,?,?,?,?)", ProsessID,ResultType,Resultdb,Max,Min, KeyValue,Unit, DateTime )
    cnxn.commit()
    cursor.close()
    cnxn.close()



""" def IRWriteResult_v2toSQLdb_ProcessRes(ProsessID,Resultdb, IRValue,IRTestTime,allvaluestillpass):
    cnxn,cursor=Connect_SQLdb()
    ResultType='IR'
    Max=0
    Min=IRTestTime
    KeyValue=IRValue
    Unit='MOhm'
    Kommentar=allvaluestillpass
    Timenow = datetime.now().replace(microsecond=0)
    DateTime=Timenow
    cursor.execute("INSERT INTO ProdDB.dbo.ProsessRes(Prosess_ID,ResultType,Result, Max, Min,KeyValue,Unit,DateTime,Kommentar) values (?,?,?,?,?,?,?,?,?)", ProsessID,ResultType,Resultdb,Max,Min, KeyValue,Unit,DateTime,Kommentar )
    cnxn.commit()
    cursor.close()
    cnxn.close() """

def IRWriteResult_v2toSQLdb_ProcessRes(ProsessID,Resultdb, IRValue,IRTestTime,allvaluestillpass):
    cnxn,cursor=Connect_SQLdb()
    ResultType='IR'
    Max=0
    Min=IRTestTime
    KeyValue=IRValue
    Unit='MOhm'
    Kommentar=allvaluestillpass
    Timenow = datetime.now().replace(microsecond=0)
    DateTime=Timenow
    cursor.execute("INSERT INTO ProdDB.dbo.ProsessRes(Prosess_ID,ResultType,Result, Max, Min,KeyValue,Unit,DateTime,Kommentar) values (?,?,?,?,?,?,?,?,?)", ProsessID,ResultType,Resultdb,Max,Min, KeyValue,Unit,DateTime,Kommentar )
    cnxn.commit()
    cursor.close()
    cnxn.close()

def eepromWritetoSQLdb(Prosess_ID,EEPType,EEPdata):
    cnxn,cursor=Connect_SQLdb()
    #Writes process esults
    #ProcessID=df.iat[0,0] # get process ifd for ch 0 or 1 
    ResultType='Offset'
    
    Timenow = datetime.now().replace(microsecond=0)
    DateTime=Timenow
    cursor.execute("INSERT INTO ProdDB.dbo.EEProm(Prosess_ID,EEPType,EEPdata,DateTime) values (?,?,?,?)", Prosess_ID,EEPType,EEPdata,DateTime )
    cnxn.commit()
    cursor.close()
    cnxn.close()
#offset_value=3.93
#working
#OffsetWriteResulttoSQLdb_ProcessRes(int(Current_Prosess_ID),Resultdb,offset_value)

""" elementid=93855
channel=int(0)
Prosess='EEPROM'
ProsessType='FAT'
ProdOrderx=224719
ProdNox=124170
print(ProdNox,ProdOrderx)
Station='HPSHAKER01'
sw='v9'
Batch='100'
Recipe_ID=1

EEPROM_Prosess_ID=FAT_calver_Process(elementid,channel,Prosess,ProdOrderx,ProdNox,Station,ProsessType,sw,Batch,324, 1)
print(EEPROM_Prosess_ID) 







EEPType='AM5000'
eepromvalues=['4A', 'BA', '07', '00', '00', '00', '00', '00', '00', '00', '00', '00', 'B3', 'F8', 'FE', '00', '00', '00', '00', '00', '00', '00', '00', '00', 'EF', '2D', '01', '00', '00', '00', '00', '00', '00', '00', '00', '00', '68', '1A', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '66', '01', '00', '08', '01', '1C', '03', '20', '00', '01', '00', '00', '66', '06', '99', '39', '33', '03', 'CC', '3C', '01', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '66', '55', 'FF', '3F', 'FF', '3F', '01', '00', '00', '00', '00', '00', '00', '00', '69', '46', '01', '00', '01', '37', 'D9', 'FF', 'FF', 'FF', 'FF', 'FF', 'FF', 'FF', 'FF', 'FF', 'FF', 'FF', 'FF', 'FF', 'FF', 'FF', 'FF', 'FF', 'FF', '08']
EEPdata= ','.join(eepromvalues)

eepromWritetoSQLdb(int(EEPROM_Prosess_ID),EEPType,EEPdata)
 """
def Electronic_writedb(Electronic_ID, SensorElement_ID, ProdOrder, ProdNo, SerialNum, ElSerial, ElBatch, Operator_ID, Comments, DateTime, Channel, Bootloader, Application):
    cnxn,cursor=Connect_SQLdb()
    #Writes process esults
    #ProcessID=df.iat[0,0] # get process ifd for ch 0 or 1 
    Comments=' '
    Bootloader=1
    Application=1
    Timenow = datetime.now().replace(microsecond=0)
    DateTime=Timenow
    cursor.execute("INSERT INTO ProdDB.dbo.Electronic(Prosess_ID,ResultType,Result, Max, Min,KeyValue,Unit,DateTime) values (?,?,?,?,?,?,?,?)", Electronic_ID,SensorElement_ID, ProdOrder, ProdNo, SerialNum, ElSerial, ElBatch, Operator_ID, Comments, DateTime, Channel,Bootloader, Application)
    cnxn.commit()
    cursor.close()
    cnxn.close()

def OffsetWriteResulttoSQLdb_ProcessRes(Prosess_ID,Resultdb,Temp_value):

    #Writes process esults
    cnxn,cursor=Connect_SQLdb()
    #ProcessID=df.iat[0,0] # get process ifd for ch 0 or 1 
    ResultType='PADC'
    Max=0
    Min=0
    KeyValue=Temp_value
    Unit='ADC'
    Timenow = datetime.now().replace(microsecond=0)
    DateTime=Timenow
    cursor.execute("INSERT INTO ProdDB.dbo.ProsessRes(Prosess_ID,ResultType,Result, Max, Min,KeyValue,Unit,DateTime) values (?,?,?,?,?,?,?,?)", Prosess_ID,ResultType,Resultdb,Max,Min,KeyValue,Unit,DateTime )
    cnxn.commit()
    cursor.close()
    cnxn.close()

def TempWriteResulttoSQLdb_ProcessRes(Prosess_ID,Resultdb,Temp_value):

    #Writes process esults
    cnxn,cursor=Connect_SQLdb()
    #ProcessID=df.iat[0,0] # get process ifd for ch 0 or 1 
    ResultType='TADC'
    Max=0
    Min=0
    KeyValue=Temp_value
    Unit='ADC'
    Timenow = datetime.now().replace(microsecond=0)
    DateTime=Timenow
    cursor.execute("INSERT INTO ProdDB.dbo.ProsessRes(Prosess_ID,ResultType,Result, Max, Min,KeyValue,Unit,DateTime) values (?,?,?,?,?,?,?,?)", Prosess_ID,ResultType,Resultdb,Max,Min,KeyValue,Unit,DateTime )
    cnxn.commit()
    cursor.close()
    cnxn.close()
#Temp_value=3.93
#working
#TempWriteResulttoSQLdb_ProcessRes(int(Current_Prosess_ID),Resultdb,Temp_value)
# Close the cursor and connection
""" cursor.close()
cnxn.close() """

def CombinedResult_v2toSQLdb_ProcessRes(ProsessID,Resultdb):
    cnxn,cursor=Connect_SQLdb()
    ResultType='IR'
    Max=0
    Min=0
    KeyValue=0
    Unit='0'
    Kommentar='0'
    Timenow = datetime.now().replace(microsecond=0)
    DateTime=Timenow
    cursor.execute("INSERT INTO ProdDB.dbo.ProsessRes(Prosess_ID,ResultType,Result, Max, Min,KeyValue,Unit,DateTime,Kommentar) values (?,?,?,?,?,?,?,?,?)", ProsessID,ResultType,Resultdb,Max,Min, KeyValue,Unit,DateTime,Kommentar )
    cnxn.commit()
    cursor.close()
    cnxn.close()
