# write data from verifisering file to database
#jeya V1_14.1124

def Writetosqldb(file, total_channels, total_steps,ProdOrderx,ProdNox,Station,sw,Batch,Operator_ID,Recipe_ID):
    import sys,numpy as np
    #sys.path.append("C:/Scansense/jeya/AM5000/python-libTestsetup/")
    sys.path.append("C:/Scansense/jeya/AM5000/AM5000_SUBVIS/python-lib")
    import modules.Database.proddbread_AM5000cal as db
    import pandas as pd
    import warnings
    warnings.filterwarnings('ignore')
    filename=file
    df = pd.read_excel(filename)
    #df = pd.read_csv(filename, delimiter=';')
    df.sort_values('Channel')
    print(df)
    #exit()
        #print(df['Serialnumber'])
    sllist=df['Serialnumber'].tolist()
    print(sllist)
    #exit()

    # total no of channels in verification 

    trimslist=sllist[0:total_channels]  # create processid for only the total channels
    print(trimslist)

    SCSCalibrationproceseeidlist=[]
    FATCALVERproceseeidlist=[]
    #exit()
    for k in range (len(trimslist)):
        print("k",k)
        SerialNumber=int(trimslist[k])
        print(SerialNumber)
        if (SerialNumber % 2 != 0):
            dfelement,Registered_status,Error_status=db.serialdetail_thru_serialno_SERIALdb(SerialNumber)
            elementid=dfelement['SensorElement_ID'].iloc[0]
            print(elementid)
        else:
            print("even channel")

        #elementid=97388
        if (SerialNumber % 2 != 0):
                channel=int(0)
        else:
                channel=int(1)
                SerialNumber=int(trimslist[k-1])
        
       
        #1.Generate PrcessId for SCS ,Calibration  - needed for Hyperbarisk
        Prosess='Calibration'
        #Prosess='_dummy'
        ProsessType='SCS'
        Kommentar='null'
        SCS_calibration_Prosess_ID=db.FAT_calver_Process(int(elementid),channel,Prosess,ProdOrderx,ProdNox,Station,ProsessType,sw,Batch,int(Operator_ID),Recipe_ID,Kommentar)
        print(SCS_calibration_Prosess_ID)
        SCSCalibrationproceseeidlist.append(SCS_calibration_Prosess_ID) 
       
        #2. Generate PrcessId for FAT ,CalibrationVerification
        #Prosess='_dummy'
        Prosess='CalibrationVerification'
        ProsessType='FAT'
        Kommentar='Finaldata'

        FAT_calver_Prosess_ID=db.FAT_calver_Process(int(elementid),channel,Prosess,ProdOrderx,ProdNox,Station,ProsessType,sw,Batch,int(Operator_ID),Recipe_ID,Kommentar)
        print(FAT_calver_Prosess_ID)
        FATCALVERproceseeidlist.append(FAT_calver_Prosess_ID)
    #print(SCSCalibrationproceseeidlist)
    print(FATCALVERproceseeidlist)

    final_FATCALVERproceseeidlist=[]
  
    # assigning processid s to correct sensor serial nos 
    for i in range(0,int(total_steps)):
        
        final_FATCALVERproceseeidlist.extend(FATCALVERproceseeidlist)
    #print("finalidlist",final_FATCALVERproceseeidlist)
    #exit()

    # use processid from final_FATCALVERproceseeidlist to write data to correct serial no
    for s in range (len(sllist)):
   
        print("s",s)
            
        proid=final_FATCALVERproceseeidlist[s]
        Prosess_ID=int(proid)
        print("processid",Prosess_ID)
        skaptemp=df['ThermalChamber'].iloc[s]
        #print(skaptemp)
        #exit()
        trykksigpr=float(df['PressureReference'].iloc[s])             
        #ReadmA= float(df['ReadmA'].iloc[s])
        ReadmA= float(df['MaxmA'].iloc[s])
        
        ExpectedmA=float(df['ExpectedmA'].iloc[s])
        #FSerror=float(df['FSError'].iloc[s])
        FSerror=float(df['MaxFSmA'].iloc[s])
        
        #Result=str(df['Pass_Fail'].iloc[s])

        Result=str(df['StatusmA'].iloc[s])
        #StatusmA
        pressureset=float(df['Pressure_set'].iloc[s])
        Tempset=float(df['Temp_set'].iloc[s])
        #print("oneprcessdata")
        #print(Prosess_ID, pressureset,Tempset,skaptemp, trykksigpr, ReadmA, ExpectedmA,FSerror, Result )
        db.FATcalver_WriteResulttoSQLdb_ProcessData(int(Prosess_ID), pressureset,Tempset,skaptemp, trykksigpr, ReadmA, ExpectedmA,FSerror, Result )
        #exit()


""" filename_Verificationtest=r'C:\Scansense\jeya\AM5000\AM5000_SUBVIS\python-lib_dbcheck\programs\log\WO224796_224801\Verification_2024-11-27.csv'
total_channels=120
total_steps=15
ProdOrderx=224796
ProdNox=124171
Station='K2'
sw='v1'
Batch='dummy'
Operator_ID=314
Recipe_ID=1
#file, total_channels, total_steps,ProdOrderx,ProdNox,Station,sw,Batch,Operator_ID,recipe_ID
Writetosqldb(filename_Verificationtest,total_channels,total_steps,ProdOrderx,ProdNox,Station,sw,Batch,int(Operator_ID),int(Recipe_ID))

 """