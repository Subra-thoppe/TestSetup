# write data from verifisering file to database
#jeya V1_14.1124
def WOdetails():
    import sys,numpy as np
    
    sys.path.append("C:/Scansense/AM5000/python-lib")
   
    from modules.GUI import gui_wo_opr_calibration as guiwo
    import modules.Database.NAV_READ_simple as NAVdb
    import modules.Database.proddbread_AM5000cal as proddb
    import pandas as pd
    import warnings
    import modules.util as util
    import ctypes
    warnings.filterwarnings('ignore')

    #common parameters for database
    ProdOrderx=int(guiwo.WORKORDER)
    
    df_NAVWO=NAVdb.Read_WOdetail_NAVdb('WO'+str(ProdOrderx))
    #print(df_NAVWO)

    Station='SCS-K-SKAP5'  # testPC name
    sw='v2'
    Batch='SCS-K-SKAP5_'+str(ProdOrderx)
    Recipe_ID=1
    oprname=guiwo.opr
    dfopr, Operator_ID=proddb.operatornumber_Operdb(oprname)

    if (len(df_NAVWO)==0):
            print("finner ikke WO i NAV")
           
    else:
            Niva3ProductNo=df_NAVWO['ItemNumber'].iloc[0]
            descrip=df_NAVWO['Description'].iloc[0]
            index = descrip.find('Single')
            if index == -1:
                DUAL='TRUE'
            else:
                DUAL='FALSE'
            print (DUAL)


    #find Product no from WO - NAV
    ProdNox=int(df_NAVWO['ItemNumber'].iloc[0])
    #get prodno fraom NAV

    #print(ProdNox,ProdOrderx)
    # total channels and Skap from GUI - user
    #total_sensors=int(guiwo.Antall)
    #total_channels=int(guiwo.Antall)*2

    """ 
    if DUAL=='TRUE':

        total_channels=int(guiwo.Antall)*2
    else:
        total_channels=int(guiwo.Antall) """
    skap=guiwo.skapno
    #station=int(skap.split('K')[1])

    # find if nivå 5 WO 
    Niva5_find=df_NAVWO['Description'].iloc[0]

    if Niva5_find.find(',')!=-1:
        s1= Niva5_find.split(',')
        print(s1)
    #exit()
        if (s1[1]==' Calibrated'):
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
            WO=str(ProdOrderx)
            randomno=str(int(np.random.rand()*100))
            # random nummer used to differentiate between data files when we run any test more than once.
            #import util 
            filename_serialno=f"programs/log/{WO}_{skap}_{fullrange}_readserialno_{randomno}_{util.date()}.csv"
            #filename_adctest=f"programs/log/{WO}_{skap}_{fullrange}_ADCTest_{randomno}_{util.date()}.csv"
            #filename_mAstabiltytest=f"programs/log/{WO}_{skap}_{fullrange}_mAstbilityTest_{randomno}_{util.date()}.csv"
            filename_ESSTEmpCyclingtest=f"programs/log/{WO}_{skap}_{fullrange}_ESSTEmpCyclingtest_{randomno}_{util.date()}.csv"
            filename_ESSBurninntest=f"programs/log/{WO}_{skap}_{fullrange}_ESSBurninn_{randomno}_{util.date()}.csv"
            filename_OverPressuretest=f"programs/log/{WO}_{skap}_{fullrange}_OverPressuretest_{randomno}_{util.date()}.csv"
            filename_SCSCalibrationcsv=f"programs/log/{WO}_{skap}_{fullrange}_Calibration_{randomno}_{util.date()}.csv"
            filename_SCSCalibrationjson=f"programs/log/{WO}_{skap}_{fullrange}_Calibration_{randomno}_{util.date()}.json"
            filename_ProofPressuretest=f"programs/log/{WO}_{skap}_{fullrange}_ProofPressuretest_{randomno}_{util.date()}.csv"
            filename_Verificationtest=f"programs/log/{WO}_{skap}_{fullrange}_Verification_{randomno}_{util.date()}.csv"

        else:
            ctypes.windll.user32.MessageBoxW(0, "ikke nivå 5 WO", "Error", 0)
    else:
        ctypes.windll.user32.MessageBoxW(0, "sjekk WO nummer", "Error", 0)
        
    return fullrange,WO,DUAL, filename_serialno,filename_OverPressuretest, filename_ESSTEmpCyclingtest,filename_ESSBurninntest, filename_SCSCalibrationcsv,filename_SCSCalibrationjson,filename_ProofPressuretest,filename_Verificationtest,ProdOrderx,ProdNox,Station,sw,Batch,Operator_ID,Recipe_ID

""" fullrange,WO,DUAL, filename_serialno,filename_OverPressuretest, filename_SCSCalibrationcsv,filename_SCSCalibrationjson,filename_ProofPressuretest,filename_Verificationtest,ProdOrderx,ProdNox,Station,sw,Batch,Operator_ID,Recipe_ID=WOdetails()
print(fullrange,WO,DUAL, filename_serialno,filename_OverPressuretest, filename_SCSCalibrationcsv,filename_SCSCalibrationjson,filename_ProofPressuretest,filename_Verificationtest,ProdOrderx,ProdNox,Station,sw,Batch,Operator_ID,Recipe_ID)
 """