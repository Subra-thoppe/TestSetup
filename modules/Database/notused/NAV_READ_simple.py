import pandas as pd
import time
from datetime import datetime
import numpy as np
import warnings
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
        print("WO finner ikke i NAV")
    else:
        print(df_NAVWO['No_'].iloc[0])
    cursornav.close()
    cnxnnav.close()
    return df_NAVWO
#Trust_connection=yes
""" 
df_NAVWO=Read_WOdetail_NAVdb('WO224777')
print(df_NAVWO) """

def NavBOMniva5(Niva5_partno):
    cnxnnav, cursornav= Connect_NAVdb()
    query="SELECT TOP (200) [Scansense AS$Production BOM Header].No_, [Scansense AS$Production BOM Header].Description, [Scansense AS$Production BOM Header].[Search Name], [Scansense AS$Production BOM Line].[Production BOM No_], [Scansense AS$Production BOM Line].[Line No_], [Scansense AS$Production BOM Line].No_ AS EXPR1, [Scansense AS$Production BOM Line].Description AS EXPR2 FROM     [Scansense AS$Production BOM Header] INNER JOIN                   [Scansense AS$Production BOM Line] ON [Scansense AS$Production BOM Header].No_ = [Scansense AS$Production BOM Line].[Production BOM No_] WHERE  ([Scansense AS$Production BOM Header].No_ = ?)"
    parameter=Niva5_partno
    df_NAVbom5 = pd.read_sql(query, cnxnnav, params=parameter)
    cursornav.close()
    cnxnnav.close()
    return df_NAVbom5




def getiteminfo(no):
    cnxnnav, cursornav= Connect_NAVdb()
    query="SELECT TOP (200) No_, [No_ 2], Description FROM     [Scansense AS$Item] WHERE  (No_ =?)"
    parameter=no
    df_item=pd.read_sql(query, cnxnnav, params=parameter)
    cursornav.close()
    cnxnnav.close()
    return df_item

