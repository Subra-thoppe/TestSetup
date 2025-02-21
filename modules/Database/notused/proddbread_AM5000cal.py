import pandas as pd
from datetime import datetime
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import pyodbc as odbc

import ctypes
#database connection


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

#100
def operatornumber_Operdb(name):
    cnxn, cursor=Connect_SQLdb()
    query="SELECT TOP (1) OperNum FROM   ProdDB.dbo. Oper WHERE  (OperName = ?)"
    #parameter='Ann Kristin Johnsen'
    parameter=name
    df = pd.read_sql(query, cnxn, params=parameter) 
    if len(df)==0:
        ctypes.windll.user32.MessageBoxW(0, " operator finner ikke", "Error", 0)
        #print ("operator finner ikke")
    else:
        oprnum=df['OperNum'].iloc[0]
    cursor.close()
    cnxn.close()
    return df,oprnum



#100
def serialdetail_thru_serialno_SERIALdb(SerialNumber):
    cnxn, cursor=Connect_SQLdb()
    query="SELECT TOP (1) SensorElement_ID, SerialNum FROM  ProdDB.dbo.Serial WHERE  (SerialNum = ?) order by datetime desc"
    parameter=str(SerialNumber)
    
    df = pd.read_sql(query, cnxn, params=parameter) 
    #print(df)
    
    if len(df)==0:
        #ctypes.windll.user32.MessageBoxW(0, "serial Number er nyt ", "o.k.", 0)
        #print ("serial Number er ikke regitsert ")

        Registered_status='FALSE'
        Error_status='FALSE'
    else:
        #ctypes.windll.user32.MessageBoxW(0, "serial nummer allerede registert", "Error", 0)
        #print("serial nummer allerede registert")
        Registered_status='TRUE'
        Error_status='FALSE'
    cursor.close()
    cnxn.close()
    return df,Registered_status,Error_status



#100
def FATcalver_WriteResulttoSQLdb_ProcessData(Prosess_ID,pressureset,Tempset,skaptemp, trykksigpr, readma, expectedma,FSerror, result):
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
    cursor.execute("INSERT INTO ProdDB.dbo.ProsessData(Prosess_ID,SetL,SetT,RefT, RefL, ReadmA, ExpectedmA, FullScaleError, Result,Unit,DateTime) values (?,?,?,?,?,?,?,?,?,?,?)",int(Prosess_ID),pressureset,Tempset,skaptemp, trykksigpr, readma, expectedma,FSerror, result ,Unit,DateTime )
    cnxn.commit()
    cursor.close()
    cnxn.close()


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

#100
def FAT_calver_Process(SensorElement_ID, channel, Prosess,ProdOrderx,ProdNox,Station,ProsessType,sw,Batch, Operator_ID, Recipe_ID,Kommentar):
    # inserts new row in prosess table and gets the prosess ID
    cnxn,cursor=Connect_SQLdb()
    """ Prosess='SADC'
    ProsessType='Test&Setup' """
    Timenow = datetime.now().replace(microsecond=0)
    DateTime=Timenow
    print("all print",SensorElement_ID, channel, Prosess,ProdOrderx,ProdNox,Station,ProsessType,sw,Batch, Operator_ID, Recipe_ID, DateTime)
    cursor.execute("INSERT INTO ProdDB.dbo.Prosess( SensorElement_ID,ProdOrder,ProdNo, Station, Prosess,ProsessType, Channel, SW,Batch,Operator_ID,DateTime,Recipe_ID,Kommentar) values (?,?,?,?,?,?,?,?,?,?,?,?,?)", SensorElement_ID, ProdOrderx, ProdNox, Station, Prosess, ProsessType, channel,sw,Batch,Operator_ID,DateTime,Recipe_ID,Kommentar)
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



