# write data from verifisering file to database
#jeya V1_14.11.24
#jeya v2_09.12.24

def Writetosqldb_verification(filename, total_channels, total_steps,ProdOrderx,ProdNox,Station,sw,Batch,Operator_ID,Recipe_ID):
    import sys
    sys.path.append("C:/Scansense/AM5000/python-lib/")
   
    #sys.path.append("C:/Scansense/AM5000/AM5000_SUBVIS/python-lib")
    #C:\Scansense\jeya\AM5000\AM5000_SUBVIS\python-lib\modules\Database\OnlyWritetodatabseas_AM5000_sqlserver.py
    import modules.Database.proddbread_AM5000cal_sqlserver as db
  
    import warnings
    import csv
    warnings.filterwarnings('ignore')
    sortdatalist=[]
    with open(filename, 'r') as x:
        csv_reader = csv.reader(x, delimiter=";")
        dictreader = csv.DictReader(x, delimiter=";")
        fieldnames1=dictreader.fieldnames
        #next(csv_reader)
        veridata= list(csv_reader)


    sorted_verdata = sorted(veridata, key=lambda x: x[fieldnames1.index("Serialnumber")])
    #print(sorted_verdata)
    """ with open('sortedveri.csv', 'w+',) as y:
        writer = csv.writer(y,delimiter=';')
        writer.writerows(sorted_verdata)  """
    #exit()
    serialno_list = [row[fieldnames1.index("Serialnumber")] for row in sorted_verdata ]
    uniqueserailnolist=list(dict.fromkeys(serialno_list))  # need to maintain ocurance order so dont use set
    print(uniqueserailnolist)
    
    #exit()
    SCSCalibrationproceseeidlist=[]
    FATCALVERproceseeidlist=[]
    #exit()
    serial_element_dict={}
    serial_FATCALverdict={}
    serial_scscaldict={}
    for k in range (len(uniqueserailnolist)):
        print("k",k)
        SerialNumber=int(uniqueserailnolist[k])
        print(SerialNumber)
        elementid1,Registered_status1,Error_status1=db.serialdetail_thru_serialno_SERIALdb(SerialNumber)
        print("1",elementid1,Registered_status1,Error_status1)
        if Registered_status1=='TRUE':
            if (SerialNumber % 2 != 0):
                elementid,Registered_status,Error_status=db.serialdetail_thru_serialno_SERIALdb(SerialNumber)
                print(elementid)

                serial_element_dict[SerialNumber]=elementid
                
            else:
                print("even channel")
        
            #elementid=97388
            if (SerialNumber % 2 != 0):
                    channel=int(0)
            else:
                    channel=int(1)
                    SerialNumber=int(uniqueserailnolist[k-1])
        
        
       
        #2. Generate PrcessId for FAT ,CalibrationVerification
        
        Prosess='CalibrationVerification'
        ProsessType='FAT'
        Kommentar='Finaldata'
         
        #Prosess='_dummy'
        #ProsessType='_dummy'
        #Kommentar='_dummy'
        
        #if Registered_status!='FALSE':
        FAT_calver_Prosess_ID=db.FAT_calver_Process(int(elementid),channel,Prosess,ProdOrderx,ProdNox,Station,ProsessType,sw,Batch,int(Operator_ID),Recipe_ID,Kommentar)
        print(FAT_calver_Prosess_ID)
        serial_FATCALverdict[SerialNumber]=FAT_calver_Prosess_ID
        FATCALVERproceseeidlist.append(FAT_calver_Prosess_ID)
        
    #print(SCSCalibrationproceseeidlist)
    #print(FATCALVERproceseeidlist)
    #print(serial_element_dict)
    print(serial_FATCALverdict)
    #exit()
    final_FATCALVERproceseeidlist=[]
    for i in range(0,int(total_steps)):
        
        final_FATCALVERproceseeidlist.extend(FATCALVERproceseeidlist)
    final_FATCALVERproceseeidlist=sorted(final_FATCALVERproceseeidlist)
    # use processid from final_FATCALVERproceseeidlist to write data to correct serial no
    try:
        for s in range (0,len(serialno_list)+1):
            Data3=0
            Data4=0
            #Prosess_ID=serial_FATCALverdict[int(sorted_verdata[s][fieldnames1.index("Serialnumber")])]
            Prosess_ID=final_FATCALVERproceseeidlist[s]
            skaptemp=float(sorted_verdata[s][fieldnames1.index("ThermalChamber")])
            trykksigpr=float(sorted_verdata[s][fieldnames1.index("PressureReference")])
            ReadmA=float(sorted_verdata[s][fieldnames1.index("MaxmA")])
            ExpectedmA=float(sorted_verdata[s][fieldnames1.index("ExpectedmA")])
            FSerror=float(sorted_verdata[s][fieldnames1.index("MaxFSmA")])
            Result=str(sorted_verdata[s][fieldnames1.index("StatusmA")])
            pressureset=float(sorted_verdata[s][fieldnames1.index("Pressure_set")])
            Tempset=float(sorted_verdata[s][fieldnames1.index("Temp_set")])
            datetime=str(sorted_verdata[s][fieldnames1.index("Dt1")])
            #print(Prosess_ID, pressureset,Tempset,skaptemp, trykksigpr, ReadmA, ExpectedmA,FSerror, Result )
            db.FATcalver_WriteResulttoSQLdb_ProcessData(int(Prosess_ID), pressureset,Tempset,datetime,skaptemp, trykksigpr, Data3,Data4, ReadmA, ExpectedmA,FSerror, Result )
            #exit()
    except IndexError as e:
        print(e)
    print("done")    

def Writetosqldb_Overpressure(filename, total_channels, total_steps,ProdOrderx,ProdNox,Station,sw,Batch,Operator_ID,Recipe_ID):
    import sys
    sys.path.append("C:/Scansense/AM5000/python-lib/")
    #sys.path.append("C:/Scansense/AM5000/AM5000_SUBVIS/python-lib")
    #C:\Scansense\jeya\AM5000\AM5000_SUBVIS\python-lib\modules\Database\OnlyWritetodatabseas_AM5000_sqlserver.py
    import modules.Database.proddbread_AM5000cal_sqlserver as db
  
    import warnings
    import csv
    warnings.filterwarnings('ignore')
    sortdatalist=[]
    with open(filename, 'r') as x:
        csv_reader = csv.reader(x, delimiter=";")
        dictreader = csv.DictReader(x, delimiter=";")
        fieldnames1=dictreader.fieldnames
        #next(csv_reader)
        veridata= list(csv_reader)


    sorted_verdata = sorted(veridata, key=lambda x: x[fieldnames1.index("Serialnumber")])
    #print(sorted_verdata)
    """ with open('sortedveri.csv', 'w+',) as y:
        writer = csv.writer(y,delimiter=';')
        writer.writerows(sorted_verdata)  """
    #exit()
    serialno_list = [row[fieldnames1.index("Serialnumber")] for row in sorted_verdata ]
    uniqueserailnolist=list(dict.fromkeys(serialno_list))  # need to maintain ocurance order so dont use set
    print(uniqueserailnolist)
    
    #exit()
    SCSCalibrationproceseeidlist=[]
    FATCALVERproceseeidlist=[]
    #exit()
    serial_element_dict={}
    serial_FATCALverdict={}
    serial_scscaldict={}
    for k in range (len(uniqueserailnolist)):
        print("k",k)
        SerialNumber=int(uniqueserailnolist[k])
        print(SerialNumber)
        elementid1,Registered_status1,Error_status1=db.serialdetail_thru_serialno_SERIALdb(SerialNumber)
        print("1",elementid1,Registered_status1,Error_status1)
        if Registered_status1=='TRUE':
            if (SerialNumber % 2 != 0):
                elementid,Registered_status,Error_status=db.serialdetail_thru_serialno_SERIALdb(SerialNumber)
                print(elementid)

                serial_element_dict[SerialNumber]=elementid
                
            else:
                print("even channel")
        
            #elementid=97388
            if (SerialNumber % 2 != 0):
                    channel=int(0)
            else:
                    channel=int(1)
                    SerialNumber=int(uniqueserailnolist[k-1])
        else:
            elementid=elementid1
            channel=int(1)
            SerialNumber=int(uniqueserailnolist[k])
       
        #2. Generate PrcessId for FAT ,CalibrationVerification
        
        Prosess='OverPressureTest'
        ProsessType='SCS'
        Kommentar='Finaldata'
         
        #Prosess='_dummy'
        #ProsessType='_dummy'
        #Kommentar='_dummy'
        
        #if Registered_status!='FALSE':
        FAT_calver_Prosess_ID=db.FAT_calver_Process(int(elementid),channel,Prosess,ProdOrderx,ProdNox,Station,ProsessType,sw,Batch,int(Operator_ID),Recipe_ID,Kommentar)
        print(FAT_calver_Prosess_ID)
        serial_FATCALverdict[SerialNumber]=FAT_calver_Prosess_ID
        FATCALVERproceseeidlist.append(FAT_calver_Prosess_ID)
        
    #print(SCSCalibrationproceseeidlist)
    #print(FATCALVERproceseeidlist)
    #print(serial_element_dict)
    print(serial_FATCALverdict)
    #exit()
    final_FATCALVERproceseeidlist=[]
    for i in range(0,int(total_steps)):
        
        final_FATCALVERproceseeidlist.extend(FATCALVERproceseeidlist)
    final_FATCALVERproceseeidlist=sorted(final_FATCALVERproceseeidlist)
    # use processid from final_FATCALVERproceseeidlist to write data to correct serial no
    try:
        for s in range (0,len(serialno_list)+1):
            Data3=0
            Data4=0
            ExpectedmA=0
            FSerror=0
            Result='null'
        
            #Prosess_ID=serial_FATCALverdict[int(sorted_verdata[s][fieldnames1.index("Serialnumber")])]
            Prosess_ID=final_FATCALVERproceseeidlist[s]
            skaptemp=float(sorted_verdata[s][fieldnames1.index("ThermalChamber")])
            trykksigpr=float(sorted_verdata[s][fieldnames1.index("PressureReference")])
            ReadmA=float(sorted_verdata[s][fieldnames1.index("ReadmA")])
            #ExpectedmA=float(sorted_verdata[s][fieldnames1.index("ExpectedmA")])
            #FSerror=float(sorted_verdata[s][fieldnames1.index("MaxFSmA")])
            #Result=str(sorted_verdata[s][fieldnames1.index("StatusmA")])
            pressureset=float(sorted_verdata[s][fieldnames1.index("Pressure_set")])
            Tempset=float(sorted_verdata[s][fieldnames1.index("Temp_set")])
            datetime=str(sorted_verdata[s][fieldnames1.index("Dt1")])
            #print(Prosess_ID, pressureset,Tempset,skaptemp, trykksigpr, ReadmA, ExpectedmA,FSerror, Result )
            db.FATcalver_WriteResulttoSQLdb_ProcessData(int(Prosess_ID), pressureset,Tempset,datetime,skaptemp, trykksigpr, Data3,Data4, ReadmA, ExpectedmA,FSerror, Result )
            #exit()
    except IndexError as e:
        print(e)
    print("done") 

def Writetosqldb_ProofPressure(filename, total_channels, total_steps,ProdOrderx,ProdNox,Station,sw,Batch,Operator_ID,Recipe_ID):
    import sys
    sys.path.append("C:/Scansense/AM5000/python-lib/")
    #sys.path.append("C:/Scansense/AM5000/AM5000_SUBVIS/python-lib")
    #C:\Scansense\jeya\AM5000\AM5000_SUBVIS\python-lib\modules\Database\OnlyWritetodatabseas_AM5000_sqlserver.py
    import modules.Database.proddbread_AM5000cal_sqlserver as db
  
    import warnings
    import csv
    warnings.filterwarnings('ignore')
    sortdatalist=[]
    with open(filename, 'r') as x:
        csv_reader = csv.reader(x, delimiter=";")
        dictreader = csv.DictReader(x, delimiter=";")
        fieldnames1=dictreader.fieldnames
        #next(csv_reader)
        veridata= list(csv_reader)


    sorted_verdata = sorted(veridata, key=lambda x: x[fieldnames1.index("Serialnumber")])
    #print(sorted_verdata)
    """ with open('sortedveri.csv', 'w+',) as y:
        writer = csv.writer(y,delimiter=';')
        writer.writerows(sorted_verdata)  """
    #exit()
    serialno_list = [row[fieldnames1.index("Serialnumber")] for row in sorted_verdata ]
    uniqueserailnolist=list(dict.fromkeys(serialno_list))  # need to maintain ocurance order so dont use set
    print(uniqueserailnolist)
    
    #exit()
    SCSCalibrationproceseeidlist=[]
    FATCALVERproceseeidlist=[]
    #exit()
    serial_element_dict={}
    serial_FATCALverdict={}
    serial_scscaldict={}
    for k in range (len(uniqueserailnolist)):
        print("k",k)
        SerialNumber=int(uniqueserailnolist[k])
        print(SerialNumber)
        elementid1,Registered_status1,Error_status1=db.serialdetail_thru_serialno_SERIALdb(SerialNumber)
        print("1",elementid1,Registered_status1,Error_status1)
        if Registered_status1=='TRUE':
            if (SerialNumber % 2 != 0):
                elementid,Registered_status,Error_status=db.serialdetail_thru_serialno_SERIALdb(SerialNumber)
                print(elementid)

                serial_element_dict[SerialNumber]=elementid
                
            else:
                print("even channel")
        
            #elementid=97388
            if (SerialNumber % 2 != 0):
                    channel=int(0)
            else:
                    channel=int(1)
                    SerialNumber=int(uniqueserailnolist[k-1])
        else:
            elementid=elementid1
            channel=int(1)
            SerialNumber=int(uniqueserailnolist[k])
       
        #2. Generate PrcessId for FAT ,CalibrationVerification
        
        Prosess='OverPressureTest'
        ProsessType='SCS'
        Kommentar='Finaldata'
         
        #Prosess='_dummy'
        #ProsessType='_dummy'
        #Kommentar='_dummy'
        
        #if Registered_status!='FALSE':
        FAT_calver_Prosess_ID=db.FAT_calver_Process(int(elementid),channel,Prosess,ProdOrderx,ProdNox,Station,ProsessType,sw,Batch,int(Operator_ID),Recipe_ID,Kommentar)
        print(FAT_calver_Prosess_ID)
        serial_FATCALverdict[SerialNumber]=FAT_calver_Prosess_ID
        FATCALVERproceseeidlist.append(FAT_calver_Prosess_ID)
        
    #print(SCSCalibrationproceseeidlist)
    #print(FATCALVERproceseeidlist)
    #print(serial_element_dict)
    print(serial_FATCALverdict)
    #exit()
    final_FATCALVERproceseeidlist=[]
    for i in range(0,int(total_steps)):
        
        final_FATCALVERproceseeidlist.extend(FATCALVERproceseeidlist)
    final_FATCALVERproceseeidlist=sorted(final_FATCALVERproceseeidlist)
    # use processid from final_FATCALVERproceseeidlist to write data to correct serial no
    try:
        for s in range (0,len(serialno_list)+1):
            Data3=0
            Data4=0
            ExpectedmA=0
            FSerror=0
            Result='null'
        
            #Prosess_ID=serial_FATCALverdict[int(sorted_verdata[s][fieldnames1.index("Serialnumber")])]
            Prosess_ID=final_FATCALVERproceseeidlist[s]
            skaptemp=float(sorted_verdata[s][fieldnames1.index("ThermalChamber")])
            trykksigpr=float(sorted_verdata[s][fieldnames1.index("PressureReference")])
            ReadmA=float(sorted_verdata[s][fieldnames1.index("ReadmA")])
            #ExpectedmA=float(sorted_verdata[s][fieldnames1.index("ExpectedmA")])
            #FSerror=float(sorted_verdata[s][fieldnames1.index("MaxFSmA")])
            #Result=str(sorted_verdata[s][fieldnames1.index("StatusmA")])
            pressureset=float(sorted_verdata[s][fieldnames1.index("Pressure_set")])
            Tempset=float(sorted_verdata[s][fieldnames1.index("Temp_set")])
            datetime=str(sorted_verdata[s][fieldnames1.index("Dt1")])
            #print(Prosess_ID, pressureset,Tempset,skaptemp, trykksigpr, ReadmA, ExpectedmA,FSerror, Result )
            db.FATcalver_WriteResulttoSQLdb_ProcessData(int(Prosess_ID), pressureset,Tempset,datetime,skaptemp, trykksigpr, Data3,Data4, ReadmA, ExpectedmA,FSerror, Result )
            #exit()
    except IndexError as e:
        print(e)
    print("done")    

def Writetosqldb_calibration(filename, total_channels, total_steps,ProdOrderx,ProdNox,Station,sw,Batch,Operator_ID,Recipe_ID):
    import sys
    sys.path.append("C:/Scansense/AM5000/python-lib/")
    #sys.path.append("C:/Scansense/AM5000/AM5000_SUBVIS/python-lib")
    #C:\Scansense\jeya\AM5000\AM5000_SUBVIS\python-lib\modules\Database\OnlyWritetodatabseas_AM5000_sqlserver.py
    import modules.Database.proddbread_AM5000cal_sqlserver as db
  
    import warnings
    import csv
    warnings.filterwarnings('ignore')
    sortdatalist=[]
    with open(filename, 'r') as x:
        csv_reader = csv.reader(x, delimiter=";")
        dictreader = csv.DictReader(x, delimiter=";")
        fieldnames1=dictreader.fieldnames
        #next(csv_reader)
        veridata= list(csv_reader)


    sorted_verdata = sorted(veridata, key=lambda x: x[fieldnames1.index("Serialnumber")])
    print(sorted_verdata)
    #exit()
    """ with open('sortedveri.csv', 'w+',) as y:
        writer = csv.writer(y,delimiter=';')
        writer.writerows(sorted_verdata)  """
    #exit()
    serialno_list = [row[fieldnames1.index("Serialnumber")] for row in sorted_verdata ]
    uniqueserailnolist=list(dict.fromkeys(serialno_list))  # need to maintain ocurance order so dont use set
    print(uniqueserailnolist)
    
    #exit()
    SCSCalibrationproceseeidlist=[]
    FATCALVERproceseeidlist=[]
    #exit()
    serial_element_dict={}
    serial_FATCALverdict={}
    serial_scscaldict={}
    for k in range (len(uniqueserailnolist)):
        print("k",k)
        SerialNumber=int(uniqueserailnolist[k])
        print(SerialNumber)
        elementid1,Registered_status1,Error_status1=db.serialdetail_thru_serialno_SERIALdb(SerialNumber)
        print("1",elementid1,Registered_status1,Error_status1)
        if Registered_status1=='TRUE':
            if (SerialNumber % 2 != 0):
                elementid,Registered_status,Error_status=db.serialdetail_thru_serialno_SERIALdb(SerialNumber)
                print(elementid)

                serial_element_dict[SerialNumber]=elementid
                
            else:
                print("even channel")
     
            #elementid=97388
            if (SerialNumber % 2 != 0):
                    channel=int(0)
            else:
                    channel=int(1)
                    SerialNumber=int(uniqueserailnolist[k-1])
      
        else:
            elementid=10000
            channel=int(1)
        print(SerialNumber,elementid,channel)
       
        #2. Generate PrcessId for FAT ,CalibrationVerification
        
        Prosess='Calibration'
        ProsessType='SCS'
        Kommentar='Finaldata'
        
        #Prosess='_dummy'
        #ProsessType='_dummy'
        #Kommentar='_dummy'
        
        #if Registered_status!='FALSE':
        FAT_calver_Prosess_ID=db.FAT_calver_Process(int(elementid),channel,Prosess,ProdOrderx,ProdNox,Station,ProsessType,sw,Batch,int(Operator_ID),Recipe_ID,Kommentar)
        print(FAT_calver_Prosess_ID)
        serial_FATCALverdict[SerialNumber]=FAT_calver_Prosess_ID
        FATCALVERproceseeidlist.append(FAT_calver_Prosess_ID)
        
    #print(SCSCalibrationproceseeidlist)
    #print(FATCALVERproceseeidlist)
    #print(serial_element_dict)
    print(serial_FATCALverdict)
    #exit()
    final_FATCALVERproceseeidlist=[]
    for i in range(0,int(total_steps)):
        
        final_FATCALVERproceseeidlist.extend(FATCALVERproceseeidlist)
    final_FATCALVERproceseeidlist=sorted(final_FATCALVERproceseeidlist)
    # use processid from final_FATCALVERproceseeidlist to write data to correct serial no
    #try:
    for s in range (0,len(serialno_list)+1):
            Data3=float(sorted_verdata[s][fieldnames1.index("Pmedian")])
            Data4=float(sorted_verdata[s][fieldnames1.index("Tmedian")])
            #Prosess_ID=serial_FATCALverdict[int(sorted_verdata[s][fieldnames1.index("Serialnumber")])]
            Prosess_ID=final_FATCALVERproceseeidlist[s]
            skaptemp=float(sorted_verdata[s][fieldnames1.index("ThermalChamber")])
            trykksigpr=float(sorted_verdata[s][fieldnames1.index("PressureReference")])
            ReadmA=float(sorted_verdata[s][fieldnames1.index("ReadmA")])
            ExpectedmA=float(sorted_verdata[s][fieldnames1.index("DacMeasured")])
            FSerror=0
            Result=0
            pressureset=float(sorted_verdata[s][fieldnames1.index("Pressure_set")])
            Tempset=float(sorted_verdata[s][fieldnames1.index("Temp_set")])
            datetime=str(sorted_verdata[s][fieldnames1.index("Dt1")])
            #print(Prosess_ID, pressureset,Tempset,skaptemp, trykksigpr, ReadmA, ExpectedmA,FSerror, Result )
            db.FATcalver_WriteResulttoSQLdb_ProcessData(int(Prosess_ID), pressureset,Tempset,datetime,skaptemp, trykksigpr, Data3,Data4, ReadmA, ExpectedmA,FSerror, Result )
            #exit()
    #except IndexError as e:
        #print(e)
    print("done")    

