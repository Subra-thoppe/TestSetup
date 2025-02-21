# write data from verifisering file to database
#jeya V1_14.1124

import sys,numpy as np
#sys.path.append("C:/Scansense/jeya/AM5000/python-libTestsetup/")
sys.path.append("C:/AM5000/python-libTestsetup/")
import GUI.gui_wo_opr_calibration as guiwo
import NAV_READ_simple_utenpandas as NAVdb
import proddbread_AM5000cal_sqlserver as proddb

import warnings
warnings.filterwarnings('ignore')

#common parameters for database
ProdOrderx=int(guiwo.WORKORDER)

detail_NAVWO=NAVdb.Read_WOdetail_NAVdb('WO'+str(ProdOrderx))
#print(df_NAVWO)

Station='SCS-K-SKAP0'  # testPC name
sw='v9'
Batch='SCS-K-SKAP0'+str(ProdOrderx)
Recipe_ID=1
oprname=guiwo.title
Operator_ID=proddb.operatornumber_Operdb(oprname)

if (len(detail_NAVWO)==0):
        print("finner ikke WO i NAV")
        #ctypes.windll.user32.MessageBoxW(0, " Finner ikke BondeOppsett for denne WO ", "Error", 0)
else:
        Niva3ProductNo=detail_NAVWO['ItemNumber']
        descrip=detail_NAVWO['Description']
        index = descrip.find('Single')
        if index == -1:
            DUAL='TRUE'
        else:
            DUAL='FALSE'
        print (DUAL)


#find Product no from WO - NAV
ProdNox=int(detail_NAVWO['ItemNumber'])
#get prodno fraom NAV

#print(ProdNox,ProdOrderx)
# total channels and Skap from GUI - user

total_channels=int(guiwo.Antall)*2

""" 
if DUAL=='TRUE':

    total_channels=int(guiwo.Antall)*2
else:
    total_channels=int(guiwo.Antall) """
skap=guiwo.skapno
station=int(skap.split('K')[1])

# find calirbation range from WO - NAV, check this with range in sensor EEPROM
index_rangefind=df_NAVWO['Description'].iloc[0]

s1=index_rangefind.split(',')
print(s1)
s2=s1[0].split('bar')
#print(s2)
fullrangestr=(s2[0][-5:])
#print(fullrange)
fullrange=int(fullrangestr)
print(fullrange)

#exit()
WO=str(ProdOrderx)
randomno=str(int(np.random.rand()*100))
# random nummer used to differentiate between data files when we run any test more than once.
#import util 
filename_seriano=f"programs/log/{WO}_{skap}_{fullrange}_readserialno_{randomno}_{util.date()}.csv"
filename_adctest=f"programs/log/{WO}_{skap}_{fullrange}_ADCTest_{randomno}_{util.date()}.csv"
filename_mAstabiltytest=f"programs/log/{WO}_{skap}_{fullrange}_mAstbilityTest_{randomno}_{util.date()}.csv"
filename_ESSTEmpCyclingtest=f"programs/log/{WO}_{skap}_{fullrange}_ESSTEmpCyclingtest_{randomno}_{util.date()}.csv"
filename_ESSBurninntest=f"programs/log/{WO}_{skap}_{fullrange}_ESSBurninn_{randomno}_{util.date()}.csv"
filename_SCSProofPressuretest=f"programs/log/{WO}_{skap}_{fullrange}_SCSProofPressuretest_{randomno}_{util.date()}.csv"
filename_SCSCalibrationcsv=f"programs/log/{WO}_{skap}_{fullrange}_SCSCalibration_{randomno}_{util.date()}.csv"
filename_SCSCalibrationjson=f"programs/log/{WO}_{skap}_{fullrange}_SCSCalibration_{randomno}_{util.date()}.json"
filename_ESSProofPressuretest=f"programs/log/{WO}_{skap}_{fullrange}_ESSProofPressuretest_{randomno}_{util.date()}.csv"
filename_ESSVerificationtest=f"programs/log/{WO}_{skap}_{fullrange}_ESSVerificationtest_{randomno}_{util.date()}.csv"




# weite calibration verification details to database , from verification file , Nomencalture form latest file WO224741


#filename=r'U:\KalibreringogFilerBackup\AM5000 log data\Batch10 kjeller WO224741_F9_690\Verification_2024-11-13_PMV_jeya.xlsx'

filename=r'U:\KalibreringogFilerBackup\AM5000 log data\Kalibrering data fra SKAP i KAlibreringrom\Batch9_WO224740_F9_690bar\224740_K2_690_SCSCalibration_71_2024-11-13.xlsx'
df = pd.read_excel(filename)
print(df)
#exit()

sllist=df['Serialnumber'].tolist()
print(sllist)
# total no of channels in verification 

trimslist=sllist[0:total_channels]
print(trimslist)
SCSCalibrationproceseeidlist=[]
FATCALVERproceseeidlist=[]
#exit()
for k in range (len(trimslist)):
    print("k",k)
    SerialNumber=int(trimslist[k])
    print(SerialNumber)
    if (SerialNumber % 2 != 0):
        dfelement,Registered_status,Error_status=proddb.serialdetail_thru_serialno_SERIALdb(SerialNumber)
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
    ProsessType='SCS'
    
    SCS_calibration_Prosess_ID=proddb.FAT_calver_Process(int(elementid),channel,Prosess,ProdOrderx,ProdNox,Station,ProsessType,sw,Batch,int(Operator_ID),Recipe_ID)
    print(SCS_calibration_Prosess_ID)
    SCSCalibrationproceseeidlist.append(SCS_calibration_Prosess_ID)

    #2. Generate PrcessId for FAT ,CalibrationVerification
    Prosess='CalibrationVerification'
    ProsessType='FAT'
    

    FAT_calver_Prosess_ID=proddb.FAT_calver_Process(int(elementid),channel,Prosess,ProdOrderx,ProdNox,Station,ProsessType,sw,Batch,int(Operator_ID),Recipe_ID)
    print(FAT_calver_Prosess_ID)
    FATCALVERproceseeidlist.append(FAT_calver_Prosess_ID)
print(SCSCalibrationproceseeidlist)
print(FATCALVERproceseeidlist)

final_FATCALVERproceseeidlist=[]
#exit()
# 15 is 
for i in range(0,18):
    
    final_FATCALVERproceseeidlist.extend(FATCALVERproceseeidlist)


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
    FSerror=float(df['FSError'].iloc[s])
    #FSerror=float(df['MaxFSmA'].iloc[s])
    
    Result=str(df['Pass_Fail'].iloc[s])
    #Result=str(df['StatusmA'].iloc[s])
    #StatusmA
    pressureset=str(df['Pressure_set'].iloc[s])
    Tempset=str(df['Temp_set'].iloc[s])
    
    proddb.FATcalver_WriteResulttoSQLdb_ProcessData(Prosess_ID, pressureset,Tempset,skaptemp, trykksigpr, ReadmA, ExpectedmA,FSerror, Result )




