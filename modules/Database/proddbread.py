# read nivå 3 sensopr spec, ARticle
import ctypes
import pyodbc as odbc
import pandas as pd
import time
from datetime import datetime
import numpy as np
import warnings
warnings.filterwarnings('ignore')
# import NAV_READ_simple1 as navdb
# database connection
# working
# used


def Connect_SQLdb():
    # import pyodbc as odbc
    # import sqlite3
    DRIVER_NAME = 'SQL SERVER'
    SERVER_NAME = 'SQL04'
    DABASE_NAME = 'ProdDB'

    Connection_string = f""" 

    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABSE={DABASE_NAME};
    Trust_connection=yes
    uid='jetsub'
    pwd='Laget2501!'
    """
    cnxn = odbc.connect(Connection_string)
    cursor = cnxn.cursor()
    # print(cursor)
    return cnxn, cursor
# cnxn, cursor=Connect_SQLdb()
# when WO Value is entered check these
# read sensor spec table
# used


def ListSensorSpec_niva3_SensorSpecdb(niva3productnummer):
    cnxn, cursor = Connect_SQLdb()
    query = "SELECT TOP (20) SensorSpec_ID, Product, ProdNo, Rev, Spec, Type, Max, Min, Unit, DateTime FROM  ProdDB.dbo.SensorSpec WHERE  (ProdNo =? ) AND (Unit = N'Batch') AND (Spec = N'Test&Setup')"
    # parameter='102332S2'
    parameter = str(niva3productnummer)
    df = pd.read_sql(query, cnxn, params=parameter)
    # print(df)
    """ if df['Type'].iloc[0]=='112109':
        print(" compsert not needed") """
    cursor.close()
    cnxn.close()
    return df
# ListSensorSpec_niva3_SensorSpecdb('102332S2')

# read article table
# used


def Read_Articlebd(partno):
    cnxn, cursor = Connect_SQLdb()
    query = "SELECT TOP (5) Article_ID, PartNo, Descr, Comments, DateTime, IncomingInspection, ProcedurePath FROM ProdDB.dbo.Article WHERE  (PartNo = ?)"
    # parameter='3TK2000-S2'
    parameter = str(partno)
    df = pd.read_sql(query, cnxn, params=parameter)
    cursor.close()
    cnxn.close()
    return df


# read wirebond table
# used

def wirebondid_Wirebonddb(WO):
    cnxn, cursor = Connect_SQLdb()
    query = "SELECT TOP (1) WireBonding_ID FROM    ProdDB.dbo. WireBonding WHERE  (ProdOrder =? ) ORDER BY WireBonding_ID DESC"
    # parameter=223971
    parameter = int(WO)
    df = pd.read_sql(query, cnxn, params=parameter)
    if (len(df) == 0):
        Error = 'TRUE'
    else:
        Error = 'FALSE'
    cursor.close()
    cnxn.close()
    return df, Error


""" df=wirebondid_Wirebonddb(223971)
print(df) """

# read compsert table
# used


def findcompsertid_from_compsert(compsert):
    cnxn, cursor = Connect_SQLdb()
    query = "SELECT TOP (20) CompSert_ID FROM  ProdDB.dbo. CompSert WHERE  (CompSert =?) order by datetime desc "
    # parameter='432'
    parameter = str(compsert)
    df = pd.read_sql(query, cnxn, params=parameter)
    cursor.close()
    cnxn.close()
    return df
    """ if len(df)==0:
        print ("wirebond detailjer finner ikke") """


# read operator table
# used

def operatornumber_Operdb(name):
    cnxn, cursor = Connect_SQLdb()
    query = "SELECT TOP (1) OperNum FROM   ProdDB.dbo. Oper WHERE  (OperName = ?)"
    # parameter='Ann Kristin Johnsen'
    parameter = name
    df = pd.read_sql(query, cnxn, params=parameter)
    if len(df) == 0:
        ctypes.windll.user32.MessageBoxW(
            0, " operator finner ikke", "Error", 0)
        # print ("operator finner ikke")
    else:
        oprnum = df['OperNum'].iloc[0]
    cursor.close()
    cnxn.close()
    return df, oprnum


# when material sertificate is entered for toplid

# read compsert table
# check
def copmsert_compsertdb(compsert):
    # working
    cnxn, cursor = Connect_SQLdb()
    query = "SELECT TOP (20) CompSert_ID FROM  ProdDB.dbo. CompSert WHERE  (CompSert =?) order by datetime desc"
    # parameter='c21211'
    parameter = compsert
    df = pd.read_sql(query, cnxn, params=parameter)
    # print(df)

    if len(df) == 0:
        ctypes.windll.user32.MessageBoxW(
            0, " Material sertifikat detailjer finner ikke til Enten HUS/TOPLID/iNLET/ELEKTRONIKK- Kontakt STEINER", "Error", 0)
        # print ("Material sertifikat detailjer finner ikke")
    cursor.close()
    cnxn.close()
    return df


""" DF= copmsert_compsertdb('79833')
print(DF) """
""" 
pd.readsql standard format
query="SELECT TOP (20) CompSert_ID FROM  ProdDB.dbo. CompSert WHERE  (CompSert =?) order by datetime desc"
parameter='c21211'
df = pd.read_sql("SELECT TOP (200) CompSert_ID FROM  ProdDB.dbo. CompSert WHERE  (CompSert ='c21211') order by datetime desc",cnxn) 
if len(df)==0:
    print ("Material sertifikat detailjer finner ikke")
print(df) """

# link compsertid of part nummer to element id
# used


def Writecomptrac_elementid_Comptracdb(compsertid, elementid, WO, prodno):
    cnxn, cursor = Connect_SQLdb()
    Type = 0
    Operator_ID = 306
    Timenow = datetime.now().replace(microsecond=0)
    DateTime = Timenow
    cursor.execute("INSERT INTO ProdDB.dbo.CompTrac(SensorElement_ID, CompSert_ID, ProdOrder, Prodno, Operator_ID, DateTime ) values (?,?,?,?,?,?)", int(
        elementid), int(compsertid), WO, prodno, Operator_ID, DateTime)
    cnxn.commit()
    # print("one")
    cursor.close()
    cnxn.close()


def Writecomptrac_elementid_Comptracdb_pp0322(compsertid, elementid, WO, prodno, Kommentar):
    cnxn, cursor = Connect_SQLdb()
    Type = 0
    Operator_ID = 306
    Timenow = datetime.now().replace(microsecond=0)
    DateTime = Timenow
    cursor.execute("INSERT INTO ProdDB.dbo.CompTrac(SensorElement_ID, CompSert_ID, ProdOrder, Prodno, Operator_ID, DateTime,Kommentar ) values (?,?,?,?,?,?,?)", int(
        elementid), int(compsertid), WO, prodno, Operator_ID, DateTime, Kommentar)
    cnxn.commit()
    # print("one")
    cursor.close()
    cnxn.close()


""" compsertid=19887
elementid=97612
WO=224690
prodno=124170
Kommentar='2024/11'
 """
# Writecomptrac_elementid_Comptracdb(compsertid, elementid, WO,prodno)

# Writecomptrac_elementid_Comptracdb_pp0322(compsertid, elementid, WO,prodno,Kommentar)


def getallserialnofraWO(WO):
    cnxn, cursor = Connect_SQLdb()
    print(cnxn, cursor)
    parameter = WO
    query = " SELECT DISTINCT TOP (200) Prosess.SensorElement_ID, Prosess.ProdOrder, Prosess.ProdNo, Serial.SerialNum FROM     ProdDB.dbo.Prosess INNER JOIN  ProdDB.dbo.Serial ON Prosess.SensorElement_ID = Serial.SensorElement_ID WHERE  (Prosess.ProdOrder = ?)ORDER BY Serial.SerialNum "
    df = pd.read_sql(query, cnxn, params=parameter)
    # print(df)
    if len(df) == 0:
        print(" WO finnerikke")
    cursor.close()
    cnxn.close()
    return df


# df_serial=getallserialnofraWO(224058)
""" df_serial=getallserialnofraWO(int(224372))
print(df_serial) """

# precheck
# check sensor number
# used


def serialdetail_thru_serialno_SERIALdb(SerialNumber):
    cnxn, cursor = Connect_SQLdb()
    query = "SELECT TOP (1) SensorElement_ID, SerialNum FROM  ProdDB.dbo.Serial WHERE  (SerialNum = ?) order by datetime desc"
    parameter = str(SerialNumber)

    df = pd.read_sql(query, cnxn, params=parameter)
    # print(df)

    if len(df) == 0:
        # ctypes.windll.user32.MessageBoxW(0, "serial Number er nyt ", "o.k.", 0)
        # print ("serial Number er ikke regitsert ")

        Registered_status = 'FALSE'
        Error_status = 'FALSE'
    else:
        # ctypes.windll.user32.MessageBoxW(0, "serial nummer allerede registert", "Error", 0)
        # print("serial nummer allerede registert")
        Registered_status = 'TRUE'
        Error_status = 'FALSE'
    cursor.close()
    cnxn.close()
    return df, Registered_status, Error_status

# serialdetail_thru_serialno_SERIALdb(99999)


def serialdetail_thru_Elementid_SERIALdb(Elelementid):
    cnxn, cursor = Connect_SQLdb()
    query = "SELECT TOP (1) SensorElement_ID,SerialNum  FROM  ProdDB.dbo.Serial WHERE  (SensorElement_ID = ?) order by datetime desc"
    parameter = Elelementid
    df = pd.read_sql(query, cnxn, params=parameter)
    # print(df)
    if len(df) == 0:
        ctypes.windll.user32.MessageBoxW(
            0, " Den serial Number er ikke brukt /regitsert enna . Den nummer er klar til bruk", "Error", 0)
        # print ("serial Number er ikke regitsert ")
        Registered_status = 'FALSE'
        Error_status = 'TRUE'
    else:
        ctypes.windll.user32.MessageBoxW(
            0, "Serial nummer er allerede registert eller Test og SEtup er allerede gjort på den sensor -Sjekk hvis du har skrevet SErial no riktig . Kontakt Are", "Error", 0)
        # print("serial nummer allerede registert")
        Registered_status = 'TRUE'
        Error_status = 'FALSE'
    cursor.close()
    cnxn.close()
    return df, Registered_status, Error_status
# serialdetail_thru_Elementid_db(78897)


def ManufacDate_thru_Elementid(Elementid):
    cnxn, cursor = Connect_SQLdb()
    query = "SELECT  TOP (1) SensorElement_ID, Prodno, Kommentar FROM ProdDB.dbo.CompTrac WHERE  (SensorElement_ID = ?) AND (Prodno = N'PP-0322')"
    # parameter='c21211'
    parameter = int(Elementid)
    df = pd.read_sql(query, cnxn, params=parameter)
    # print(df)

    if len(df) == 0:
        ctypes.windll.user32.MessageBoxW(
            0, " ManufacureDate finner ikke", "Error", 0)
        # print ("Material sertifikat detailjer finner ikke")
    cursor.close()
    cnxn.close()
    return df


""" df=ManufacDate_thru_Elementid(97612)
print(df) """


""" df,Registered_status,Error_status=serialdetail_thru_Elementid_SERIALdb(92817)
print(df,Registered_status,Error_status) """

# check if STW Membrane id is in correct format
# used


def STWMembrane_Formatcheck(Membraneno):
    if len(Membraneno) != 10:
        ctypes.windll.user32.MessageBoxW(
            0, "Sjekk hvis MembraneNo. er skrevet riktig", "Error", 0)
        # print("Sjekk hvis MembraneNo. er skrevet riktig")
        Error_status = 'TRUE'
    else:
        Error_status = 'FALSE'
    return Error_status
    cursor.close()
    cnxn.close()

# STWMembrane_Formatcheck('STAA01-A01')


# check sensor element id
# used
def Membranedetail_thru_Membranenodb(Membraneno):
    cnxn, cursor = Connect_SQLdb()
    error_membraneformat = STWMembrane_Formatcheck(Membraneno)
    if (error_membraneformat == 'FALSE'):
        query = "SELECT TOP (1) SensorElement_ID, SensorNo, PartNo, Descr, Operator_ID, DateTime FROM     ProdDB.dbo.SensorElement WHERE  (SensorNo = ?) ORDER BY DateTime DESC"
        parameter = Membraneno
        df = pd.read_sql(query, cnxn, params=parameter)
        print(df)
        elementid = df['SensorElement_ID'].iloc[0]
        print(elementid)
        if len(df) == 0:
            ctypes.windll.user32.MessageBoxW(
                0, "Membrane no er ikke regitsert i PID /Element booking. sjekk med STEINER/SVEIS", "Error", 0)
            # print ("SEnsor Element er ikke regitsert. klar til bruk")
            Registered_status = 'FALSE'
            Error_status = 'FALSE'
            exit()
        else:
            # ctypes.windll.user32.MessageBoxW(0, "Finner Membraneno.", "o.k", 0)
            print("sensor Element nummer er ellerede registert,Finner Membraneno.")
            Registered_status = 'TRUE'
            Error_status = 'FALSE'
        # return df, Registered_status,Error_status
    else:
        ctypes.windll.user32.MessageBoxW(
            0, "sJeKk MEmbraneNummer format", "Error", 0)
        # print("check MEmbraneNummer format")
    cursor.close()
    cnxn.close()
    return elementid, df, Registered_status, Error_status


""" Membraneno='STAA99-A01'
elementid, df, Registered_status,Error_status=Membranedetail_thru_Membranenodb(Membraneno)
#print(elementid, df, Registered_status,Error_status)
print(elementid) """


def Membranedetail_thru_Elementiddb(Elementid):
    cnxn, cursor = Connect_SQLdb()
    query = "SELECT TOP (1) SensorElement_ID, SensorNo, PartNo, Descr, Operator_ID, DateTime FROM     ProdDB.dbo.SensorElement WHERE  (SensorElement_ID = ?) ORDER BY DateTime DESC"
    parameter = int(Elementid)
    df = pd.read_sql(query, cnxn, params=parameter)
    print(df)
    if len(df) == 0:
        ctypes.windll.user32.MessageBoxW(
            0, "Membrane No  er ikke regitsert .Kontakt steiner. ", "o.k", 0)
        # print ("SEnsor Element er ikke regitsert. klar til bruk")
        Registered_status = 'FALSE'
        Error_status = 'FALSE'
    else:
        # ctypes.windll.user32.MessageBoxW(0, "sensor Element nummer er ellerede registert", "o.k", 0)
        # print("SEnsor Element er allerede regitsert.")
        Registered_status = 'TRUE'
        Error_status = 'FALSE'
    cursor.close()
    cnxn.close()
    return df, Registered_status, Error_status

# Membranedetail_thru_Elementid(78897)
# used


def SerialNumberWrite_Serialdb(Elementid, serailno):
    cnxn, cursor = Connect_SQLdb()
    Type = 0
    Timenow = datetime.now().replace(microsecond=0)
    DateTime = Timenow
    cursor.execute("INSERT INTO ProdDB.dbo.Serial(SensorElement_ID, Type, SerialNum, DateTime ) values (?,?,?,?)", int(
        Elementid), Type, str(serailno), DateTime)
    cnxn.commit()
    cursor.close()
    cnxn.close()


# check if sensor serial no and membrane no are connected with other allerede in datrabase
# used
def Sensor_SerialNo_MembraneNo_Linkeddb(serailno, Membraneno):
    cnxn, cursor = Connect_SQLdb()
    error_membraneformat = STWMembrane_Formatcheck(Membraneno)
    if (error_membraneformat == 'FALSE'):
        df1, Registered_status1, Error_status1 = serialdetail_thru_serialno_SERIALdb(
            serailno)
        if Registered_status1 == 'TRUE':
            ctypes.windll.user32.MessageBoxW(
                0, "Serial nummer brukt allerede. Kansjke Test of SEtup er allerede gjort på den sensor.Sjekk serail no / Kontakt Are ", "error", 0)
            # print("SErial nummer allerede brukt")
            elelmentid1 = df1['SensorElement_ID'].iloc[0]
            elementid, df2, Registered_status2, Error_status2 = Membranedetail_thru_Membranenodb(
                Membraneno)
            if Registered_status2 == 'TRUE':
                elelmentid2 = df2['SensorElement_ID'].iloc[0]
                if (elelmentid1 == elelmentid2):
                    ctypes.windll.user32.MessageBoxW(
                        0, "serial Nummer og MembraneNo er allerede linket med hverandre- Test of SEtup er allerede gjort på den sensor", "error", 0)
                    # print(" serial Nummer og MembraneNo er allerede linket med hverandre")
            else:
                ctypes.windll.user32.MessageBoxW(
                    0, "membrane ikke registert", "error", 0)
                # print("membrane ikke registert")
        else:
            elementid, df2, Registered_status2, Error_status2 = Membranedetail_thru_Membranenodb(
                Membraneno)
            elelmentid2 = df2['SensorElement_ID'].iloc[0]
            SerialNumberWrite_Serialdb(elelmentid2, serailno)
    else:
        ctypes.windll.user32.MessageBoxW(
            0, "check MEmbrane numer format", "error", 0)
        # print("check MEmbrane numer format")
    cursor.close()
    cnxn.close()


def ListElementidfraNiva5WO_ProcessVibration(niva5WOno):
    cnxn, cursor = Connect_SQLdb()

    # elelment id fra Nivå 5 WO

    query = "SELECT DISTINCT TOP (2000) SensorElement_ID, ProdOrder, ProdNo, Station, Prosess, ProsessType, Batch   FROM     ProdDB.dbo.Prosess   WHERE  (ProdOrder =?) AND (ProsessType = N'FAT') AND (Prosess = N'Vibration')    ORDER BY SensorElement_ID"
    parameter = int(niva5WOno)
    df = pd.read_sql(query, cnxn, params=parameter)

    # print(df)
    if len(df) == 0:
        ctypes.windll.user32.MessageBoxW(
            0, "Sjekk WO no eller noe fail . kontakt Are", "error", 0)
        print(" Sjekk WO no/noe fail")
    cursor.close()
    cnxn.close()
    return df


""" df= ListElementidfraNiva5WO_ProcessVibration( 223116)
print(df) """
# ListSensorSpec_niva3_SensorSpecdb('102332S2')
# Sensor_SerialNo_MembraneNo_Linkeddb(99999, 'STAA99-A01')


def ListElementidfraNiva3WO_ProcessTestSetup(niva3WOno):
    cnxn, cursor = Connect_SQLdb()

    # elelment id fra Nivå 5 WO

    query = "SELECT DISTINCT TOP (2000) SensorElement_ID, ProdOrder, ProdNo, Station, Prosess, ProsessType, Batch   FROM     ProdDB.dbo.Prosess   WHERE  (ProdOrder =?) AND (ProsessType = N'Test&Setup') AND (Prosess = N'SADC')    ORDER BY SensorElement_ID"
    parameter = int(niva3WOno)
    df = pd.read_sql(query, cnxn, params=parameter)

    # print(df)
    if len(df) == 0:
        ctypes.windll.user32.MessageBoxW(
            0, "Sjekk WO no/noe fail. kontakt Are", "error", 0)
        print(" Sjekk WO no/noe fail")
    cursor.close()
    cnxn.close()
    return df


""" df= ListElementidfraNiva3WO_ProcessTestSetup(224592)
print(df)  """

"""
print(df['SensorElement_ID'])
elemenidlist=df['SensorElement_ID'].tolist()
lenelemenidlist=len(elemenidlist)

for id in elemenidlist:
    db.Writecomptrac_elementid_Comptracdb(compsertid_PIH,elementid,WO,prodno_PIH)
    db.Writecomptrac_elementid_Comptracdb(compsertid_PHT,elementid,WO,prodno_PHT)
    db.Writecomptrac_elementid_Comptracdb(compsertid_ECT,elementid,WO,prodno_ECT)
 """


def Processdatafraprocessid(processid):
    # processdata from process id

    cnxn, cursor = Connect_SQLdb()
    query = "SELECT TOP (200) ProsessData_ID, Prosess_ID, SigL, Unit, DateTime FROM     ProdDB.dbo.ProsessData WHERE  (Prosess_ID = ?)"
    parameter = int(processid)
    df = pd.read_sql(query, cnxn, params=parameter)

    # print(df)
    if len(df) == 0:
        ctypes.windll.user32.MessageBoxW(
            0, "Sjekk - Process iD finner ikke . Kontakt Are", "error", 0)
        print(" Sjekk ")
    cursor.close()
    cnxn.close()
    return df


def risting_27mai24():
    # risting data from a date to a date
    cnxn, cursor = Connect_SQLdb()

    # elelment id fra Nivå 5 WO
    query = "SELECT DISTINCT TOP (2000) Prosess.Prosess_ID, Prosess.SensorElement_ID, Prosess.ProdOrder, Prosess.ProdNo, Prosess.Station, Prosess.Prosess, Prosess.ProsessType, Prosess.Channel, Prosess.SW, Prosess.Batch, Prosess.Operator_ID, Prosess.DateTime, Prosess.Recipe_ID, ProsessRes.Result, ProsessRes.Max, ProsessRes.Min, ProsessRes.KeyValue FROM     ProdDB.dbo.Prosess INNER JOIN  ProdDB.dbo.ProsessRes ON Prosess.Prosess_ID = ProsessRes.Prosess_ID WHERE  (Prosess.ProsessType = N'FAT') AND (Prosess.Prosess = N'Vibration') AND (Prosess.DateTime >= '2024-05-23') ORDER BY Prosess.DateTime DESC, Prosess.Channel"

    # query="SELECT DISTINCT TOP (2000) SensorElement_ID, ProdOrder, ProdNo, Station, Prosess, ProsessType, Batch   FROM     ProdDB.dbo.Prosess   WHERE  (ProdOrder =?) AND (ProsessType = N'FAT') AND (Prosess = N'Vibration')    ORDER BY SensorElement_ID"
    # parameter=int(niva5WOno)
    df = pd.read_sql(query, cnxn)

    # print(df)
    if len(df) == 0:
        ctypes.windll.user32.MessageBoxW(0, "Sjekk WO no/noe fail", "error", 0)
        print(" Sjekk WO no/noe fail")
    cursor.close()
    cnxn.close()
    return df
# WO details


def getprocesidfromelementid(ProsessType, Process, elementid, ch):
    cnxn, cursor = Connect_SQLdb()

    # to get viantion detail detail based on element id, sorting with elelmtn id , date dscending, channel no
    query = "SELECT DISTINCT TOP (2) Prosess.Prosess_ID, Prosess.SensorElement_ID, Prosess.ProdOrder, Prosess.ProdNo, Prosess.Station, Prosess.Prosess, Prosess.ProsessType, Prosess.Channel, Prosess.SW, Prosess.Batch, Prosess.Operator_ID, Prosess.DateTime, Prosess.Recipe_ID, ProsessRes.Result, ProsessRes.Max, ProsessRes.Min, ProsessRes.KeyValue FROM     ProdDB.dbo.Prosess INNER JOIN   ProdDB.dbo.ProsessRes ON Prosess.Prosess_ID = ProsessRes.Prosess_ID WHERE  (Prosess.ProsessType =? ) AND (Prosess.Prosess = ?) AND (Prosess.SensorElement_ID = ?) AND (Prosess.Channel = ?) ORDER BY Prosess.SensorElement_ID, Prosess.DateTime DESC, Prosess.Channel"
    parameter1 = int(elementid)
    parameter2 = str(ProsessType)
    parameter3 = str(Process)
    parameter4 = int(ch)

    df = pd.read_sql(query, cnxn,  params=(
        parameter2, parameter3, parameter1, parameter4))
    # takes long time if more than one parameter is used , or due to 3 sorting?

    # takes long time with this also
    # cursor.execute ("SELECT DISTINCT TOP (2) Prosess.Prosess_ID, Prosess.SensorElement_ID, Prosess.ProdOrder, Prosess.ProdNo, Prosess.Station, Prosess.Prosess, Prosess.ProsessType, Prosess.Channel, Prosess.SW, Prosess.Batch, Prosess.Operator_ID, Prosess.DateTime, Prosess.Recipe_ID, ProsessRes.Result, ProsessRes.Max, ProsessRes.Min, ProsessRes.KeyValue FROM     ProdDB.dbo.Prosess INNER JOIN   ProdDB.dbo.ProsessRes ON Prosess.Prosess_ID = ProsessRes.Prosess_ID WHERE  (Prosess.ProsessType =? ) AND (Prosess.Prosess = ?) AND (Prosess.SensorElement_ID = ?) ORDER BY Prosess.SensorElement_ID, Prosess.DateTime DESC, Prosess.Channel",ProsessType, Process, int(elementid))

    # print(df)
    if len(df) == 0:
        ctypes.windll.user32.MessageBoxW(
            0, "Sjekk WO no /noe fail", "error", 0)
        print(" Sjekk WO no /noe fail")
    cursor.close()
    cnxn.close()
    return df


# elementid=87884
""" df =getprocesidfromelementid('FAT','Vibration', elementid, 0)

print(df) """

""" df =getvibrationprocessdatafromelementid('FAT','CalibrationVerification',elementid)

print(df) """

""" df =getvibrationprocessdatafromelementid('FAT','CalibrationVerification', elementid)

print(df) """

""" df =getvibrationprocessdatafromelementid('FAT','ESSBurnIn', elementid)

print(df) """
""" df =getvibrationprocessdatafromelementid('FAT','ESSTemperatureCycling', elementid)

print(df) """

""" df =getvibrationprocessdatafromelementid('FAT','ESSHydraulicCyclingTest', elementid)

print(df) """

""" df =getvibrationprocessdatafromelementid('Test&Setup','mATest', elementid)

print(df) """
# processidlist=df['Prosess_ID'].tolist()


""" def Hyperbarictest(WOno):
query="SELECT DISTINCT   TOP (1000) Prosess.Prosess_ID, Prosess.SensorElement_ID, Prosess.ProdOrder, Prosess.ProdNo, Prosess.Station, Prosess.Prosess, Prosess.ProsessType, Prosess.Channel, Prosess.SW, Prosess.Batch, Prosess.Operator_ID, 
                  Prosess.DateTime, Prosess.Recipe_ID, ProsessRes.Result, ProsessRes.Max, ProsessRes.Min, ProsessRes.KeyValue
FROM     ProdDB.dbo.Prosess INNER JOIN
                  ProdDB.dbo.ProsessRes ON Prosess.Prosess_ID = ProsessRes.Prosess_ID
WHERE  (Prosess.Prosess = N'HyperbaricPressureTest') AND (Prosess.ProdOrder = 223984) AND (Prosess.ProsessType = N'FAT')
ORDER BY Prosess.DateTime DESC
 """


# cehck result for both ch 0 , 1
def ProcessResultfromProcessid(Processid):
    cnxn, cursor = Connect_SQLdb()
    query = "SELECT TOP (200) ProsessRes_ID, Prosess_ID, ResultType, Result, Max, Min, KeyValue, Unit, DateTime     FROM     ProdDB.dbo.ProsessRes     WHERE  (Prosess_ID = ?)"
    # 2524405
    parameter = int(Processid)
    df = pd.read_sql(query, cnxn,  params=parameter)

    # print(df)
    if len(df) == 0:
        ctypes.windll.user32.MessageBoxW(
            0, "Sjekk WO no/noe fail med process id. kontakt Are", "error", 0)
        print(" Sjekk WO no/noe fail")
    cursor.close()
    cnxn.close()
    return df


""" df=ProcessResultfromProcessid(2524405)
print(df)
if df['Result'].iloc[0] =='PASSED':
    ResultStatus='PASS'
else:
    ResultStatus='FAIL'
print(ResultStatus) """
# SerialNumberWrite_SQLdb_Serial(95000,99999)

# Sensor_SerialNo_MembraneNo_Linkeddb(21211,'STAA26-C07')
# print(df)


def Hyperbaricprocessidfrombatchno(Batchno):
    cnxn, cursor = Connect_SQLdb()
    # query=" SELECT TOP (10) Prosess_ID, SensorElement_ID, ProdOrder, ProdNo, Station, Prosess, ProsessType, Channel, SW, Batch, Operator_ID, DateTime, Recipe_ID FROM    ProdDB.dbo.Prosess   WHERE  (Batch = ?) AND (Prosess =? ) "
    query = "SELECT TOP (20) Prosess_ID, SensorElement_ID, ProdOrder, ProdNo, Station, Prosess, ProsessType, Channel, SW, Batch, Operator_ID, DateTime, Recipe_ID FROM     ProdDB.dbo.Prosess    WHERE  (Batch =?) AND (Prosess = 'HyperbaricPressureTest')"
    parameter1 = Batchno
    # parameter2=str('HyperbaricPressureTest')
    # print(parameter1)
    # parameter2=ch
    df = pd.read_sql(query, cnxn,  params=parameter1)
    if len(df) == 0:
        ctypes.windll.user32.MessageBoxW(
            0, "Sjekk batchno/noe fail. kontakt Are", "error", 0)
        print(" Sjekk batchno/noe fail")
    cursor.close()
    cnxn.close()


""" df=Hyperbaricprocessidfrombatchno('K2-0364')
print(df) """


def batchnofromelementid(elementid):
    cnxn, cursor = Connect_SQLdb()
    query = "SELECT TOP (1) Prosess_ID, SensorElement_ID, ProdOrder, ProdNo, Station, Prosess, ProsessType, Channel, SW, Batch, Operator_ID, DateTime, Recipe_ID FROM    ProdDB.dbo.Prosess WHERE  (SensorElement_ID = ?) AND (Prosess = 'Calibration') ORDER BY DateTime DESC"
    parameter = int(elementid)
    df = pd.read_sql(query, cnxn,  params=parameter)
    if len(df) == 0:
        ctypes.windll.user32.MessageBoxW(
            0, "Sjekk batchno/noe fail. kontakt Are", "error", 0)
        print(" Sjekk batchno/noe fail")
    batchno = df['Batch'].iloc[0]
    cursor.close()
    cnxn.close()
    return batchno


""" print(batchnofromelementid(87884)) """


def elementidfinner(elementid):
    cnxn, cursor = Connect_SQLdb()
    query = "SELECT TOP (200) SensorElement_ID, SensorNo, PartNo, Descr, Operator_ID, DateTime    FROM    ProdDB.dbo.SensorElement     WHERE  (SensorElement_ID = ?)"
    parameter = int(elementid)
    # print(parameter)
    df = pd.read_sql(query, cnxn, params=parameter)
    if len(df) == 0:
        ctypes.windll.user32.MessageBoxW(
            0, "Membrane no finner ikke. Membrane er ikke registert i PID/ Element booking. Kontakt STEINER", "error", 0)
        print(" element no finner ikke")
        exit()
    cursor.close()
    cnxn.close()
    return df
# print(elementidfinner(87884))


def Elementid_fra_serialno(Serialno):
    cnxn, cursor = Connect_SQLdb()
    query = "SELECT TOP (1) Serial_ID, SensorElement_ID, Type, SerialNum, DateTime, MrbNr, SaleOrderNo FROM   ProdDB.dbo.Serial WHERE  (SerialNum = ?)"
    parameter = Serialno
    # print(parameter)
    df = pd.read_sql(query, cnxn, params=parameter)
    if len(df) == 0:
        ctypes.windll.user32.MessageBoxW(
            0, "Membrane no finner ikke. Membrane er ikke registert i PID/ Element booking. Kontakt STEINER", "error", 0)
        print(" element no finner ikke")
        exit()
    cursor.close()
    cnxn.close()
    return df


""" df=Elementid_fra_serialno('24157')
elementid=df['SensorElement_ID'][0]
print("elementid")
print(elementid) """


def Compsertchecksluttkontrol(elementid):
    cnxn, cursor = Connect_SQLdb()
    # print (cnxn,cursor)
    parameter = int(96152)
    query = "SELECT TOP (200) CompTrac_ID, SensorElement_ID, CompSert_ID, ProdOrder, Prodno, Operator_ID, DateTime FROM  ProdDB.dbo.CompTrac WHERE  (SensorElement_ID = ?)"
    df = pd.read_sql(query, cnxn, params=parameter)
    # print(df)
    if len(df) == 0:
        ctypes.windll.user32.MessageBoxW(
            0, "Membrane no finner ikke. Membrane er ikke registert i PID/ Element booking. Kontakt STEINER", "error", 0)
        print(" element no finnerikke")
        exit()
    cursor.close()
    cnxn.close()
    return df


""" 
SELECT TOP (200) CompTrac_ID, SensorElement_ID, CompSert_ID, ProdOrder, Prodno, Operator_ID, DateTime
FROM     CompTrac
WHERE  (SensorElement_ID = 96152) """


# df= Compsertchecksluttkontrol(elementid)
""" print("hi")
print(df)  """
""" cursor.close()
cnxn.close() """


def comptrac_compsert(elementid):
    cnxn, cursor = Connect_SQLdb()
    # print (cnxn,cursor)
    parameter = int(elementid)
    query = "SELECT TOP (10) CompTrac.CompTrac_ID, CompTrac.SensorElement_ID, CompTrac.CompSert_ID, CompTrac.ProdOrder, CompTrac.Prodno, CompTrac.Operator_ID, CompTrac.DateTime, CompSert.Articel, CompSert.CompSert FROM   ProdDB.dbo.CompTrac INNER JOIN   ProdDB.dbo.CompSert ON CompTrac.CompSert_ID = CompSert.CompSert_ID WHERE  (CompTrac.SensorElement_ID = ?)"
    df = pd.read_sql(query, cnxn, params=parameter)
    # print(df)
    if len(df) == 0:
        ctypes.windll.user32.MessageBoxW(
            0, "Membrane no finner ikke. Membrane er ikke registert i PID/ Element booking. Kontakt STEINER", "error", 0)
        print(" element no finnerikke")
        exit()
    cursor.close()
    cnxn.close()
    return df


""" df=comptrac_compsert(91940)
print(df) """


def comptrac(elementid, partno):
    cnxn, cursor = Connect_SQLdb()
    # print (cnxn,cursor)
    parameter1 = int(elementid)
    parameter2 = partno
    query = "SELECT TOP (200) CompTrac_ID, SensorElement_ID, CompSert_ID, ProdOrder, Prodno, Operator_ID, DateTime FROM    ProdDB.dbo.CompTrac WHERE  (SensorElement_ID = ?) AND (Prodno = ?)"

    df = pd.read_sql(query, cnxn, params=(parameter1, parameter2))
    # print(df)
    if len(df) == 0:
        ctypes.windll.user32.MessageBoxW(
            0, "Membrane no finner ikke. Membrane er ikke registert i PID/ Element booking. Kontakt STEINER", "error", 0)
        print(" element no finnerikke")
        exit()
    cursor.close()
    cnxn.close()
    return df


# partno=navdb.
""" f_comptrac=comptrac(91940,'110921')
print("with partno")
print(df_comptrac) """


def compsert(compsertid):
    cnxn, cursor = Connect_SQLdb()
    # print (cnxn,cursor)
    parameter = int(compsertid)
    query = "SELECT TOP (200) CompSert_ID, CompSert, Article_ID, Articel, SW, Operator_ID, DateTime FROM    ProdDB.dbo.CompSert WHERE  (CompSert_ID =?)"
    df = pd.read_sql(query, cnxn, params=parameter)
    # print(df)
    if len(df) == 0:
        ctypes.windll.user32.MessageBoxW(
            0, "compsert finnerikke til HUS/TOPLID/INLET/Elektronikk. kontakt Steiner", "error", 0)
        print(" compsert finnerikke")
    cursor.close()
    cnxn.close()
    return df


""" df_compsert=compsert(18232)
print(df_compsert)
print(df_compsert['CompSert'].iloc[0],df_compsert['Articel'].iloc[0] )
 """

"""
WHAT DOES THIS ???
count_rows = df.shape[0]
for i in range (count_rows):
    if(df['Articel'][i]=='SVEISEPROSEDYRE'):
        print("Sveisreport:")
        print (df['CompSert'][i])
    elif(df['Articel'][i]=='PP-0322'):
        print("Eddy current:")
        print (df['CompSert'][i])
    else:
        print((df['CompSert_ID'][i]))
    #print(df['Articel'][i])
"""


def sjekk_TS_teststatus(WO):
    cnxn, cursor = Connect_SQLdb()
    # print (cnxn,cursor)
    parameter = int(WO)
    query = '''
    SELECT        TOP (200) Prosess.ProdOrder, Prosess.ProdNo, Prosess.Station, Prosess.DateTime, Serial.SerialNum, ProsessRes.Result
    FROM             ProdDB.dbo.Prosess INNER JOIN
                            ProdDB.dbo.Serial ON Prosess.SensorElement_ID = Serial.SensorElement_ID INNER JOIN
                            ProdDB.dbo.ProsessRes ON Prosess.Prosess_ID = ProsessRes.Prosess_ID
    WHERE        (Prosess.ProsessType LIKE N'%Test%') AND (Prosess.Prosess = N'CombinedResult') AND (Prosess.ProdOrder = ?) AND (Prosess.Channel = 0)
    ORDER BY Serial.SerialNum

    '''
    df = pd.read_sql(query, cnxn, params=parameter)
    # print(df)
    if len(df) == 0:
        ctypes.windll.user32.MessageBoxW(
            0, "compsert finnerikke til HUS/TOPLID/INLET/Elektronikk. kontakt Steiner", "error", 0)
        print(" compsert finnerikke")
    cursor.close()
    cnxn.close()
    return df
