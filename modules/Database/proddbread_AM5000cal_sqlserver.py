
import pyodbc as odbc
from datetime import datetime
import numpy as np

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

def operatornumber_Operdb(oprname):
    cnxn, cursor=Connect_SQLdb()
    query="SELECT TOP (1) OperNum FROM   ProdDB.dbo. Oper WHERE  (OperName = ?)"
    #parameter='Ann Kristin Johnsen'
    parameter=oprname
    ans=cursor.execute(query,parameter)
   
    oprinfo={}
    if ans.rowcount!=0:
        for row in ans:
            #print (row.OperNum)
            oprinfo["OperNum"]=row.OperNum
        
        cursor.close()
        cnxn.close()
        return  oprinfo['OperNum']
""" rowl=operatornumber_Operdb('Ann Kristin Johnsen')
print(rowl) """





def serialdetail_thru_serialno_SERIALdb(SerialNumber):
    cnxn, cursor=Connect_SQLdb()
    
    query="SELECT TOP (1) SensorElement_ID, SerialNum FROM  ProdDB.dbo.Serial WHERE  (SerialNum = ?) order by datetime desc"
    parameter=str(SerialNumber)
    serialinfo={}
    Registered_status='FALSE'
    Error_status='FALSE'
    serialinfo['SensorElement_ID']=10000
    ans=cursor.execute(query,parameter)
    
    #print(ans)
    #print(type(ans))
    
    #exit() 
    try:
        if ans.rowcount!=0:     
            for row in ans:
                
                serialinfo['SensorElement_ID']=row.SensorElement_ID
                Registered_status='TRUE'
                Error_status='FALSE'
                
        else:   
            
            Registered_status='FALSE'
            Error_status='FALSE'
            serialinfo['SensorElement_ID']=10000

    except TypeError or KeyError as e:
        dummy=0
        """ Registered_status='FALSE'
        Error_status='FALSE'
        serialinfo['SensorElement_ID']=10000

        print(f"Error: {e}") """

    #exit()
    
    cursor.close()
    cnxn.close()
    return serialinfo['SensorElement_ID'],Registered_status,Error_status

""" seriallist,Registered_status,Error_status=serialdetail_thru_serialno_SERIALdb(28525)
#seriallist,Registered_status,Error_status=serialdetail_thru_serialno_SERIALdb(10746)
print(seriallist,Registered_status,Error_status) """


def FATcalver_WriteResulttoSQLdb_ProcessData(Prosess_ID,pressureset,Tempset, DateTime,skaptemp, trykksigpr, Data3,Data4,readma, expectedma,FSerror, result):
    #Writes process esults
    cnxn,cursor=Connect_SQLdb()
    ResultType='mA'
    Unit='mA'
    Timenow = datetime.now().replace(microsecond=0)
    #DateTime=Timenow
    cursor.execute("INSERT INTO ProdDB.dbo.ProsessData(Prosess_ID,SetL,SetT,RefT, RefL, ReadmA, ExpectedmA, FullScaleError, Result,Unit,DateTime,Data3,Data4) values (?,?,?,?,?,?,?,?,?,?,?,?,?)",int(Prosess_ID),pressureset,Tempset,skaptemp, trykksigpr, readma, expectedma,FSerror, result ,Unit,DateTime,Data3,Data4 )
    cnxn.commit()
    cursor.close()
    cnxn.close()

def FAT_calver_Process(SensorElement_ID, channel, Prosess,ProdOrderx,ProdNox,Station,ProsessType,sw,Batch, Operator_ID, Recipe_ID,Kommentar):
    # inserts new row in prosess table and gets the prosess ID
    cnxn,cursor=Connect_SQLdb()
    Timenow = datetime.now().replace(microsecond=0)
    DateTime=Timenow
    cursor.execute("INSERT INTO ProdDB.dbo.Prosess( SensorElement_ID,ProdOrder,ProdNo, Station, Prosess,ProsessType, Channel, SW,Batch,Operator_ID,DateTime,Recipe_ID,Kommentar) values (?,?,?,?,?,?,?,?,?,?,?,?,?)", SensorElement_ID, ProdOrderx, ProdNox, Station, Prosess, ProsessType, channel,sw,Batch,Operator_ID,DateTime,Recipe_ID,Kommentar)
    cnxn.commit()
    query="SELECT  TOP (1) Prosess_ID FROM   ProdDB.dbo.Prosess WHERE (ProdOrder =? )AND (SensorElement_ID =?) AND (channel=?) AND (Prosess=?) ORDER BY DateTime DESC"
    parameter=[ProdOrderx,SensorElement_ID,channel,Prosess]
    ans=cursor.execute(query,parameter)
    FAT_calver_proceddiddetail={}
    for row in ans:
        #print(row)
        FAT_calver_proceddiddetail['Prosess_ID']=row.Prosess_ID
   
    FAT_calver_Prosess_ID=FAT_calver_proceddiddetail['Prosess_ID']
    #print(FAT_calver_Prosess_ID)
    if FAT_calver_Prosess_ID == "" or np.isnan(FAT_calver_proceddiddetail['Prosess_ID']) == 'True':
        print("Processid error")
        exit()
    cursor.close()
    cnxn.close()
    return FAT_calver_Prosess_ID



""" Prosess_ID=2693600
pressureset=10
Tempset=40
skaptemp=40
trykksigpr=2
readma=4.0
expectedma=4.1
FSerror=0.12
result='dummy'

FATcalver_WriteResulttoSQLdb_ProcessData(Prosess_ID,pressureset,Tempset,skaptemp, trykksigpr, readma, expectedma,FSerror, result) """

""" elementid=93832
channel=int(0)
ProdOrderx=int(224837)
Prosess='dummy'
ProsessType='dummy'
ProdNox='124721'


Station='ggh'

sw='1'
Batch='dummy'
Operator_ID=int(229)
Recipe_ID=int(1)
Kommentar='dummy' """

""" op=FAT_calver_Process(int(elementid), channel, Prosess,ProdOrderx,ProdNox,Station,ProsessType,sw,Batch, int(Operator_ID), Recipe_ID,Kommentar)
print(op) """

def Calibration_WriteResulttoSQLdb_ProcessData(Prosess_ID,pressureset,Tempset,skaptemp, trykksigpr,Data3,Data4, readma, expectedma,FSerror, result):
    #Writes process esults
    cnxn,cursor=Connect_SQLdb()
    ResultType='mA'
    Unit='mA'
    Timenow = datetime.now().replace(microsecond=0)
    DateTime=Timenow
    cursor.execute("INSERT INTO ProdDB.dbo.ProsessData(Prosess_ID,SetL,SetT,RefT, RefL, Data3,Data4, ReadmA, ExpectedmA, FullScaleError, Result,Unit,DateTime) values (?,?,?,?,?,?,?,?,?,?,?,?,?)",int(Prosess_ID),pressureset,Tempset,skaptemp, trykksigpr, Data3,Data4,readma, expectedma,FSerror, result ,Unit,DateTime )
    cnxn.commit()
    cursor.close()
    cnxn.close()

def SensorSlnofraRisting_onlyPASSEDSensors(ProdOrderx):
    serialinfo=[]
    cnxn,cursor=Connect_SQLdb()
    query="SELECT  TOP (200) Prosess.Prosess_ID, Prosess.SensorElement_ID, Prosess.ProdOrder, Prosess.ProdNo, Prosess.Prosess, Prosess.ProsessType, Prosess.Channel, Prosess.DateTime, Serial.SerialNum, ProsessRes.Result FROM ProdDB.dbo.Prosess INNER JOIN  ProdDB.dbo.Serial ON Prosess.SensorElement_ID = Serial.SensorElement_ID INNER JOIN  ProdDB.dbo.ProsessRes ON Prosess.Prosess_ID = ProsessRes.Prosess_ID WHERE        (Prosess.ProsessType = N'FAT') AND (Prosess.Prosess = N'Vibration') AND (Prosess.Channel = 0) AND (ProsessRes.Result = N'PASSED') AND (Prosess.ProdOrder =?) ORDER BY Serial.SerialNum"
    parameter=[ProdOrderx]
    ans=cursor.execute(query,parameter)
    try:
        if ans.rowcount!=0:     
            for row in ans:
                
                serialinfo.append(int(row.SerialNum))
                #print(int(row.SerialNum))
                
        else:   
            print("Fail i Serilano")
           
            #serialinfo['SensorElement_ID']=10000

    except TypeError or KeyError as e:
        dummy=0
        """ Registered_status='FALSE'
        Error_status='FALSE'
        serialinfo['SensorElement_ID']=10000

        print(f"Error: {e}") """

    #exit()
    
    cursor.close()
    cnxn.close()
    return serialinfo

def SensorSlnofraRisting_all(ProdOrderx):
    serialinfo=[]
    cnxn,cursor=Connect_SQLdb()
    query="SELECT  TOP (200) Prosess.Prosess_ID, Prosess.SensorElement_ID, Prosess.ProdOrder, Prosess.ProdNo, Prosess.Prosess, Prosess.ProsessType, Prosess.Channel, Prosess.DateTime, Serial.SerialNum, ProsessRes.Result FROM ProdDB.dbo.Prosess INNER JOIN  ProdDB.dbo.Serial ON Prosess.SensorElement_ID = Serial.SensorElement_ID INNER JOIN  ProdDB.dbo.ProsessRes ON Prosess.Prosess_ID = ProsessRes.Prosess_ID WHERE        (Prosess.ProsessType = N'FAT') AND (Prosess.Prosess = N'Vibration') AND (Prosess.Channel = 0) AND (Prosess.ProdOrder =?) ORDER BY Serial.SerialNum"
    parameter=[ProdOrderx]
    ans=cursor.execute(query,parameter)
    try:
        if ans.rowcount!=0:     
            for row in ans:
                
                serialinfo.append(int(row.SerialNum))
                #print(int(row.SerialNum))
                
        else:   
            print("Fail i Serilano")
           
            #serialinfo['SensorElement_ID']=10000

    except TypeError or KeyError as e:
        dummy=0
        """ Registered_status='FALSE'
        Error_status='FALSE'
        serialinfo['SensorElement_ID']=10000

        print(f"Error: {e}") """

    #exit()
    
    cursor.close()
    cnxn.close()
    return serialinfo