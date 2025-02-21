from datetime import datetime
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
    ans= cursornav.execute(query,parameter) 
    #print(ans)
    WOdetailNAV={}
    

    #rowlist=[]
    if ans.rowcount!=0:
        for row in ans:
            print(row)
            print (row.Description)
            print(row.ItemNumber)
            print(row.Quantity)
            print(row.No_)
            WOdetailNAV["No_"] = row.No_
            WOdetailNAV["Quantity"] = int(row.Quantity)
            WOdetailNAV["ItemNumber"] = row.ItemNumber
            WOdetailNAV["Description"] = row.Description

            """ #print(row.Prod_ Order No_)
            rowlist.append(row.No_)
            rowlist.append(int(row.Quantity))
            rowlist.append(row.ItemNumber)
            rowlist.append(row.Description) """


        cursornav.close()
        cnxnnav.close()
        return  WOdetailNAV
    else:
        print("Feil WO eller WO finner ikke NAV")
#Trust_connection=yes
""" WOdetailNAV=Read_WOdetail_NAVdb('WO224777')
#print(a)  
print(WOdetailNAV)
 """

def NavBOMniva5(Niva5_partno):
    cnxnnav, cursornav= Connect_NAVdb()
    query="SELECT TOP (200) [Scansense AS$Production BOM Header].No_, [Scansense AS$Production BOM Header].Description, [Scansense AS$Production BOM Header].[Search Name], [Scansense AS$Production BOM Line].[Production BOM No_], [Scansense AS$Production BOM Line].[Line No_], [Scansense AS$Production BOM Line].No_ AS EXPR1, [Scansense AS$Production BOM Line].Description AS EXPR2 FROM     [Scansense AS$Production BOM Header] INNER JOIN                   [Scansense AS$Production BOM Line] ON [Scansense AS$Production BOM Header].No_ = [Scansense AS$Production BOM Line].[Production BOM No_] WHERE  ([Scansense AS$Production BOM Header].No_ = ?)"
    parameter=Niva5_partno
    ans= cursornav.execute(query, parameter)
    #print(ans)
    NAVBOMNiv5detail={}
    rowlist=[]
    if ans.rowcount!=0:
        for row in ans:
            #print(row)
            NAVBOMNiv5detail["No_"] = row.No_
            #NAVBOMNiv5detail["Quantity"] = int(row.Quantity)
            #NAVBOMNiv5detail["ItemNumber"] = row.ItemNumber
            NAVBOMNiv5detail["Description"] = row.Description
            rowlist.append(row)
        cursornav.close()
        cnxnnav.close()
        return  NAVBOMNiv5detail,rowlist
    else:
        print("Feil Partno eller Partno finner ikke NAV")

b, c=NavBOMniva5('125860')
print(b) 


def getiteminfo(no):
    cnxnnav, cursornav= Connect_NAVdb()
    query="SELECT TOP (200) No_, [No_ 2], Description FROM     [Scansense AS$Item] WHERE  (No_ =?)"
    parameter=no
    ans= cursornav.execute(query,parameter)
    print(ans)
    iteminfo={}
    
    if ans.rowcount!=0:
        for row in ans:
            """ print(row)
            print (row.Description)
                    
            print(row.No_) """
            #print(row.Prod_ Order No_)
            
            iteminfo["No_"] = row.No_
            iteminfo["Description"] = row.Description

        cursornav.close()
        cnxnnav.close()
        return iteminfo
    else:
        print("Feil Partno eller Partno finner ikke NAV")
c=getiteminfo('124179')
print(c)




""" df_NAVWO=Read_WOdetail_NAVdb('WO'+str(224882))
print(df_NAVWO) 
#exit()
if (len(df_NAVWO)==0):
    print("finner ikke WO i NAV")
    exit()
else:
    Niva3ProductNo=df_NAVWO['ItemNumber']
    descrip=df_NAVWO['Description']
    index = descrip.find('Single')
    if index == -1:
        DUAL='TRUE'
    else:
        DUAL='FALSE'
    print (DUAL)
print(Niva3ProductNo)
#exit()
#print(type(Niva3ProductNo))
#exit()
Partno_Niva3=Niva3ProductNo[0:6]
df_NAVbom3=NavBOMniva5(Partno_Niva3)
print(df_NAVbom3)
exit()
niva3listpartno=df_NAVbom3['ItemNumber'].tolist()
print("nivå3",niva3listpartno)
niva3listdes=df_NAVbom3['Description'].tolist()
print("nivå3",niva3listdes)
"""