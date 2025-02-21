import pandas as pd
import time
from datetime import datetime
import numpy as np
import warnings,ctypes
warnings.filterwarnings('ignore')

#database connection
# working 
import pyodbc as odbc
def Connect_NAVdb():
    cnxnnav = odbc.connect('Driver={SQL Server};'
                            'Server=192.168.120.8;'
                            'Database=NAV_LIVE;'
                            'UID=SCSPythonRead;'
                            'PWD=jte35eFqKYJ^f;'
                            'Trusted_Connection=no;')

    #print(cnxnnav)
    cursornav=cnxnnav.cursor()
    #print(cursornav)
    return cnxnnav,cursornav

# TEst and setup to get Purchase order details from NAV for Nivå 3 based on WO 
def Read_WOdetail_NAVdb(WO):
    cnxnnav, cursornav= Connect_NAVdb()
    query= "SELECT Header.No_, Lines.Quantity,  (SELECT CASE Item.[No_ 2] WHEN '' THEN Item.[No_] ELSE Item.[No_ 2] END AS ItemNumber  FROM [Scansense AS$Item] AS Item WHERE   (No_ = Lines.[Item No_])) AS ItemNumber, Lines.Description FROM  [Scansense AS$Production Order] AS Header INNER JOIN  [Scansense AS$Prod_ Order Line] AS Lines ON Header.No_ = Lines.[Prod_ Order No_] WHERE  (Header.No_ =? )"
    parameter=WO
    df_NAVWO = pd.read_sql(query, cnxnnav, params=parameter) 
    if len(df_NAVWO)==0:
        ctypes.windll.user32.MessageBoxW(0,f" Hei, WO nummer finner ikke i NAV , sjekk med Produksjon leder(Peter) / Steiner ", "Error", 0)
        
        print("WO finner ikke i NAV")
        exit()
    else:
        print(df_NAVWO['No_'].iloc[0])
    cursornav.close()
    cnxnnav.close()
    return df_NAVWO

""" df_NAVWO=Read_WOdetail_NAVdb('WO224797')
print(df_NAVWO) """

def CheckWOniva(WO):
    #get WO detail fra NAV 
    cnxnnav, cursornav= Connect_NAVdb()
    query= "SELECT Header.No_, Lines.Quantity,  (SELECT CASE Item.[No_ 2] WHEN '' THEN Item.[No_] ELSE Item.[No_ 2] END AS ItemNumber  FROM [Scansense AS$Item] AS Item WHERE   (No_ = Lines.[Item No_])) AS ItemNumber, Lines.Description FROM  [Scansense AS$Production Order] AS Header INNER JOIN  [Scansense AS$Prod_ Order Line] AS Lines ON Header.No_ = Lines.[Prod_ Order No_] WHERE  (Header.No_ =? )"
    parameter=WO
    df_NAVWO = pd.read_sql(query, cnxnnav, params=parameter) 
    if len(df_NAVWO)==0:
        print("WO finner ikke i NAV")
        ctypes.windll.user32.MessageBoxW(0,f" Hei, WO nummer finner ikke i NAV , sjekk med Produksjon leder(Peter) / Steiner ", "Error", 0)
        exit()
    else:
        print(df_NAVWO['No_'].iloc[0])
    cursornav.close()
    cnxnnav.close()
    # check hvilken nivå er WO 
    wonivacheckcriteria=df_NAVWO.iloc[0]['Description']
    findstr_niva6_1='%'
    if ',' in wonivacheckcriteria:
        wonivacheckcriterailist=wonivacheckcriteria.split(',')
        rangeportion=wonivacheckcriterailist[0]
        nivaportion=wonivacheckcriterailist[1]
        print("renge,",rangeportion)
        print("nivå,", nivaportion)
        findstr_niva5_1='Calibrated'
        findstr_niva5_2='N5'
        findstr_niva3_1='Ready for cal'
        findstr_niva3_2='N3'
       
        if (findstr_niva5_1 in nivaportion) or (findstr_niva5_2 in nivaportion):
            WONiva='Niva_5'
            print("WO er nivå 5 WO")
        elif  (findstr_niva3_1 in nivaportion) or (findstr_niva3_2 in nivaportion):
            WONiva='Niva_3'
            print("WO er nivå 3 WO")
    elif  (findstr_niva6_1 in wonivacheckcriteria):
        WONiva='Niva_6'
        print("WO er nivå 6 WO")
    else:
        WONiva='Annet'
        ctypes.windll.user32.MessageBoxW(0,f" Hei, WO Nummer er ikke Nivå1 , ikke Nivå3, ikke nivå 5 , sjekk med Produksjon leder(Peter) / Steiner ", "Error", 0)
        print("WO Nummer er ikke Nivå1/ikke Nivå3/ikke nivå 5")
        exit()
    return WONiva
""" df_NAVWO=Read_WOdetail_NAVdb('WO224906')
print(df_NAVWO)
CheckWOniva('WO224906')  """

def NavBOMniva5(Niva5_partno):
    cnxnnav, cursornav= Connect_NAVdb()
    query="SELECT TOP (200) [Scansense AS$Production BOM Header].No_, [Scansense AS$Production BOM Header].Description, [Scansense AS$Production BOM Header].[Search Name], [Scansense AS$Production BOM Line].[Production BOM No_], [Scansense AS$Production BOM Line].[Line No_], [Scansense AS$Production BOM Line].No_ AS EXPR1, [Scansense AS$Production BOM Line].Description AS EXPR2 FROM     [Scansense AS$Production BOM Header] INNER JOIN                   [Scansense AS$Production BOM Line] ON [Scansense AS$Production BOM Header].No_ = [Scansense AS$Production BOM Line].[Production BOM No_] WHERE  ([Scansense AS$Production BOM Header].No_ = ?)"
    parameter=Niva5_partno
    df_NAVbom5 = pd.read_sql(query, cnxnnav, params=parameter)
    cursornav.close()
    cnxnnav.close()
    return df_NAVbom5

""" df_NAVbom5=NavBOMniva5('112330')
print(df_NAVbom5)
niva5list=df_NAVbom5['EXPR1'].tolist()
print(niva5list)
time.sleep(2)
df_NAVbom3=NavBOMniva5('112332')
print(df_NAVbom3)
niva3list=df_NAVbom3['EXPR1'].tolist()
print(niva3list)
time.sleep(2)
df_NAVbom1_1=NavBOMniva5('123205')
print(df_NAVbom1_1)
niva1_1list=df_NAVbom1_1['EXPR1'].tolist()
print(niva1_1list)
time.sleep(2)
df_NAVbom1_2=NavBOMniva5('111305')
print(df_NAVbom1_2)
niva1_2list=df_NAVbom1_2['EXPR1'].tolist()
print(niva1_2list)
SluttkontrollComptrackList=['110921','110938','124513','120144','112109']
 """

def getiteminfo(no):
    cnxnnav, cursornav= Connect_NAVdb()
    query="SELECT TOP (200) No_, [No_ 2], Description FROM     [Scansense AS$Item] WHERE  (No_ =?)"
    parameter=no
    df_item=pd.read_sql(query, cnxnnav, params=parameter)
    cursornav.close()
    cnxnnav.close()
    return df_item

""" df_item=getiteminfo('111305')
print(df_item)
df_item.to_csv('item.txt', index=False,  sep="\t") """
