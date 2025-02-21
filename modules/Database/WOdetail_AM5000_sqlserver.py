# write data from verifisering file to database
#jeya V1_14.1124
def WOdetails():
    import sys,numpy as np
    
    sys.path.append("C:/Scansense/AM5000/python-lib/")
    from modules.GUI import gui_wo_opr_calibration as guiwo
    #from modules.GUI import gui_wo_opr_calibration as guiwo
    #C:\Scansense\jeya\AM5000\AM5000_SUBVIS\python-lib\modules\GUI\gui_wo_opr_calibration.py
    import modules.Database.NAV_READ_simple_sqlserver as NAVdb
    import modules.Database.proddbread_AM5000cal_sqlserver as proddb
    import warnings
    import modules.util as util
    import ctypes
    warnings.filterwarnings('ignore')

    #common parameters for database
    ProdOrderx=int(guiwo.WORKORDER)
    
    detail_NAVWO=NAVdb.Read_WOdetail_NAVdb('WO'+str(ProdOrderx))
    #print(df_NAVWO)

    Station='SCS-K-SKAP0'  # testPC name
    sw='v3'
    Batch='SCS-K-SKAP0_'+str(ProdOrderx)
    Recipe_ID=1
    oprname=guiwo.opr
    Operator_ID=proddb.operatornumber_Operdb(oprname)

    if (len(detail_NAVWO)==0):
            print("finner ikke WO i NAV")
           
    else:
           
            descrip=detail_NAVWO["Description"]
            index = descrip.find('Single')
            if index == -1:
                DUAL='TRUE'
            else:
                DUAL='FALSE'
            print (DUAL)


    #find Product no from WO - NAV
    ProdNox=int(detail_NAVWO["ItemNumber"])
    # total channels and Skap from GUI - user
    #total_sensors=int(guiwo.Antall)
    #total_channels=int(guiwo.Antall)*2

    """ 
    if DUAL=='TRUE':

        total_channels=int(guiwo.Antall)*2
    else:
        total_channels=int(guiwo.Antall) """
    skap=guiwo.skapno
    
    # find if nivå 5 WO 
    Niva5_find=detail_NAVWO["Description"]

    if Niva5_find.find(',')!=-1:
        s1= Niva5_find.split(',')
        print(s1)
    #exit()
        if (s1[1]==' Calibrated'):
            # find calirbation range from WO - NAV, check this with range in sensor EEPROM
            index_rangefind=detail_NAVWO["Description"]

            s1=index_rangefind.split(',')
            print(s1)
            s2=s1[0].split('bar')
            
            fullrangestr=(s2[0][-5:])
            
            fullrange=int(fullrangestr)
            print(fullrange)
            WO=str(ProdOrderx)
            randomno=str(int(np.random.rand()*100))
            # random nummer used to differentiate between data files when we run any test more than once.
            #import util 
            filename_serialno=f"programs/log/{WO}_{skap}_{fullrange}_readserialno_{randomno}_{util.date()}.csv"
            #filename_adctest=f"programs/log/{WO}_{skap}_{fullrange}_ADCTest_{randomno}_{util.date()}.csv"
            #filename_mAstabiltytest=f"programs/log/{WO}_{skap}_{fullrange}_mAstbilityTest_{randomno}_{util.date()}.csv"
            filename_TEmpCyclingtest=f"programs/log/{WO}_{skap}_{fullrange}_TEmpCyclingtest_{randomno}_{util.date()}.csv"
            filename_Burninntest=f"programs/log/{WO}_{skap}_{fullrange}_Burninn_{randomno}_{util.date()}.csv"
            filename_OverPressuretest=f"programs/log/{WO}_{skap}_{fullrange}_OverPressuretest_{randomno}_{util.date()}.csv"
            filename_SCSCalibrationcsv=f"programs/log/{WO}_{skap}_{fullrange}_Calibration_{randomno}_{util.date()}.csv"
            filename_SCSCalibrationjson=f"programs/log/{WO}_{skap}_{fullrange}_Calibration_{randomno}_{util.date()}.json"
            filename_ProofPressuretest=f"programs/log/{WO}_{skap}_{fullrange}_ProofPressuretest_{randomno}_{util.date()}.csv"
            filename_Verificationtest=f"programs/log/{WO}_{skap}_{fullrange}_Verification_{randomno}_{util.date()}.csv"

        else:
            ctypes.windll.user32.MessageBoxW(0, "ikke nivå 5 WO", "Error", 0)
    else:
        ctypes.windll.user32.MessageBoxW(0, "sjekk WO nummer", "Error", 0)
        
    return fullrange,WO,DUAL, filename_serialno,filename_TEmpCyclingtest,filename_Burninntest,filename_OverPressuretest, filename_SCSCalibrationcsv,filename_SCSCalibrationjson,filename_ProofPressuretest,filename_Verificationtest,ProdOrderx,ProdNox,Station,sw,Batch,Operator_ID,Recipe_ID

fullrange,WO,DUAL, filename_serialno,filename_TEmpCyclingtest,filename_Burninntest,filename_OverPressuretest, filename_SCSCalibrationcsv,filename_SCSCalibrationjson,filename_ProofPressuretest,filename_Verificationtest,ProdOrderx,ProdNox,Station,sw,Batch,Operator_ID,Recipe_ID=WOdetails()
print(fullrange,WO,DUAL, filename_serialno,filename_TEmpCyclingtest,filename_Burninntest,filename_OverPressuretest, filename_SCSCalibrationcsv,filename_SCSCalibrationjson,filename_ProofPressuretest,filename_Verificationtest,ProdOrderx,ProdNox,Station,sw,Batch,Operator_ID,Recipe_ID)
