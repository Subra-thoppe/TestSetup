
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
    for row in ans:
        #print (row.OperNum)
        oprinfo["OperNum"]=row.OperNum
       
    cursor.close()
    cnxn.close()
    return  oprinfo
""" rowl=operatornumber_Operdb()
print(rowl) """


def serialdetail_thru_serialno_SERIALdb(SerialNumber):
    cnxn, cursor=Connect_SQLdb()
    query="SELECT TOP (1) SensorElement_ID, SerialNum FROM  ProdDB.dbo.Serial WHERE  (SerialNum = ?) order by datetime desc"
    parameter=str(SerialNumber)
    
    ans=cursor.execute(query,parameter)
    rowlist=[]
    for row in ans:
        print (row.SensorElement_ID)
        rowlist.append(row.SensorElement_ID)
    
    if len( rowlist)==0:
       

        Registered_status='FALSE'
        Error_status='FALSE'
    else:
      
        Registered_status='TRUE'
        Error_status='FALSE'
    cursor.close()
    cnxn.close()
    return rowlist,Registered_status,Error_status

seriallist,Registered_status,Error_status=serialdetail_thru_serialno_SERIALdb(27471)
print(seriallist,Registered_status,Error_status)


def FATcalver_WriteResulttoSQLdb_ProcessData(Prosess_ID,pressureset,Tempset,skaptemp, trykksigpr, readma, expectedma,FSerror, result):
    #Writes process esults
    cnxn,cursor=Connect_SQLdb()
   
    ResultType='mA'
    Max=0
    Min=0
    
    Unit='mA'
    Timenow = datetime.now().replace(microsecond=0)
    DateTime=Timenow
    cursor.execute("INSERT INTO ProdDB.dbo.ProsessData(Prosess_ID,SetL,SetT,RefT, RefL, ReadmA, ExpectedmA, FullScaleError, Result,Unit,DateTime) values (?,?,?,?,?,?,?,?,?,?,?)",int(Prosess_ID),pressureset,Tempset,skaptemp, trykksigpr, readma, expectedma,FSerror, result ,Unit,DateTime )
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
    rowlist=[]
    for row in ans:
        print (row.Prosess_ID)
        rowlist.append(row.Prosess_ID)
   
    FAT_calver_Prosess_ID=rowlist[0]
    print(FAT_calver_Prosess_ID)
    if FAT_calver_Prosess_ID == "" or np.isnan(rowlist[0]) == 'True':
        print("Processid error")
        exit()
    cursor.close()
    cnxn.close()
    return FAT_calver_Prosess_ID

