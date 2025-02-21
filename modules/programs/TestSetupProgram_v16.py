# Test and setup on AM 5000
#Version=1.0
#date=23.mai.24
#jeya
#version 2
#date:07.08.24 jeya
#VERSION 3
#DATE 20.09.24
#rEMOVEIN GCONFIG UPLOAD FOR ELKTRONIKK THAT ARE ALREADY TESTED IN NORDBIT
#ELECTRONIC BATCHNO READING FROM EEPROM AND LINKING TO MATSERT
#ADDING  MATSERT LINKING FOR HOUSING IN TEST&SETUP

#version 4
#DAC tuning 
#inthe  PGA program seconf order and third order muted .- this was rolled back by waqas after trying on one sensor
#version 5
#14.oct.24
#offset limit test with innr limit test 
#VERSION 6
#17,10,24
#READING NORBIT SERAIL NO AND WRITING TO ELECTRONIC TABLE IN DATABASE
#BATCH NO WAS ALREADY READ FROM ELECTRONIC AND LINKED WIHT COMPTRAC 
#17,10,24
#version 9 
#28,10,24
# IR test last 2 result values are read and written to ProcsessRes Kommentar colon , Kommentar colon laget av LArs agge på28,oct.24
# IR test write result oppdated
#now all common paramters for a prcessid are at only one place.
#version no. 7,8 not used 
#21.11.14 - REading full full EEPROm after tuning and writein gto databse EEProm table
#VERSION 11,12, NOT USED
#VERSION 13 - JEYA - 05.01,25
# PGA , MULTIMER MODULE FROM CALIBRATION PROGRAM (GIT) USED. EEPROM READ AND WRITTEN TO DATABSE BEFORE AND AFTER TEST AND SETUP
#SL.NO IS WRITTEN ONLY ONCE IN EEPROM NOW. CH B IS ONLY ACCESSED IF SENSOR  IS DUAL 
#OFFSET INNER LIMTI CHANGED TO 500 FROM 20000 ADC SINCE SIDEMANKONTROLL IS DONE IN WIREBONDING . NO NEED TO CATCH <20000ADC ERROR
#version 14, jeya 12,01,25
# combined Test and setup result added , version 13 implemented in shaker2023 PC .
# seperate folder for limits added 
# VERSION 15 . JEY A15,01,25 - COMMON FOLDER FROM T FOLDER SO THTA UPDATES CAN BE MADE AT A SINGLE FOLDER 
# 20,01,25 waqas checked Test og setup program on both testpcs -HPSHAKER 01, SHAKER2023 and confirmed both work fine
#24,01,25 -jeya -Norbit - Batch and elctronic serail no registers are wrong ( Not got update/ info from waqas . checked self and reading correct registers now)
import pyvisa
import time
import ctypes 
from datetime import datetime

#sys.path.append("C:/Scansense/jeya/AM5000/python-libTestsetup/")
#sys.path.append("C:/AM5000/python-libTestsetup/")
import sys, os
sys.path.append("T:\ProdSW_AM5000\CommonTestSetupProgram_AM5000\python-libTestsetup-nysw")

#T:\ProdSW_AM5000\CommonTestSetupProgram_AM5000\python-libTestsetup-nysw\modules\GUI\gui_TS.py
""" sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))
print((os.path.abspath("."))) """
#exit()
#from main import *
# GUI


#import modules.GUI.GUI_OVERSTYR
import modules.GUI.gui_wo_opr as guiwo
import modules.GUI.gui_serial_mem_toplid_hus_electronikk as guisr
import modules.GUI.GUI_table as table
import modules.GUI.GUI_OVERSTYR as oversty
#instruments

import modules.Switch.agilent35970A as RelayMUx

#dastabase
import modules.Database.NAV_READ_simple1 as NAVdb
import modules.Database.proddbread as db
import modules.Database.limits_ResultsCheck as Limit_Result

#import PGA305 as PGA305   #mute050125

import modules.Insulation_Resistance.IR_TEst_agilent34970A_ver2_1 as IR6

from modules.Multimeter import *
from modules.PGA305 import *
from modules.PowerSupply import *

import modules.util as util
import time


Startime=datetime.now().replace(microsecond=0)
mm = Multimeter()
util.Purple(mm)

pga = PGA305()
util.Purple(pga)

Total_sensors=1
seriallist=[]
testlist=[]
resultlist=[]
resultdblist=[]
for t in range(Total_sensors):
    print("sensor",t)

    WO=guiwo.WORKORDER
    
    oprname=guiwo.title
    #print(oprname)
    df, Operator_ID=db.operatornumber_Operdb(oprname)

    guisr.create_window()
    SerialNumber=guisr.serialno
    Membraneno=guisr.MembraneNo
    toplid=guisr.ToplidNo
    Hus=guisr.Husno

    #db.Membranedetail_thru_Membranenodb(Membraneno)
    # if everythong is fine link Membrane and SErial no

    elementid, df, Registered_status,Error_status=db.Membranedetail_thru_Membranenodb(Membraneno)
    
    #db.Sensor_SerialNo_MembraneNo_Linkeddb(SerialNumber, Membraneno)

    

    # read nicå 3 WO detail fra NAV
    df_NAVWO=NAVdb.Read_WOdetail_NAVdb('WO'+str(WO))
    #print(df_NAVWO)
    #exit()
    if (len(df_NAVWO.index)==0):
        print("finner ikke WO i NAV")
        exit()
    else:
        Niva3ProductNo=df_NAVWO['ItemNumber'].iloc[0]
        descrip=df_NAVWO['Description'].iloc[0]
        index = descrip.find('Single')
        if index == -1:
            DUAL='TRUE'
        else:
            DUAL='FALSE'
        print (DUAL)
    print(Niva3ProductNo)
    print(type(Niva3ProductNo))
    #exit()
    Partno_Niva3=Niva3ProductNo[0:6]
    df_NAVbom3=NAVdb.NavBOMniva5(Partno_Niva3)
    print(df_NAVbom3)
    niva3listpartno=df_NAVbom3['EXPR1'].tolist()
    print("nivå3",niva3listpartno)
    niva3listdes=df_NAVbom3['EXPR2'].tolist()
    print("nivå3",niva3listdes)


    for m in niva3listdes:
        indexofniva1=m.find('+')
        if indexofniva1 !=-1:
            niva1des=m
    print(niva1des)


    y=df_NAVbom3.loc[df_NAVbom3['EXPR2']==niva1des].index[0]
    print(y)

    Partno_Niva1=niva3listpartno[y]

    print(Partno_Niva1)
    df_NAVbom3=NAVdb.NavBOMniva5(Partno_Niva3)
    print(df_NAVbom3)
    df_NAVbom3.to_csv('navbom3.txt', index=False,  sep="\t")

    niva3list=df_NAVbom3['EXPR1'].tolist()
    print(niva3list)
    niva3descriptionlist=df_NAVbom3['EXPR2'].tolist()
    print(niva3descriptionlist)

    for i in range (len(niva3descriptionlist)):
        #print (niva3descriptionlist[i].find("Housing"))

        if ("Housing" in niva3descriptionlist[i]):
            print("housing")
            print(df_NAVbom3['EXPR1'][i])
            prodno=df_NAVbom3['EXPR1'][i]
            print("prodno housing",prodno)
            prodnohus=prodno

        elif(("Toplid" in niva3descriptionlist[i] ) or ("GTMS" in niva3descriptionlist[i])):
            print("toplid")
            print(df_NAVbom3['EXPR1'][i])
            prodno=df_NAVbom3['EXPR1'][i]
            print("prodno toplid",prodno)
            prodnotoplid=prodno
        elif("Electronics" in niva3descriptionlist[i]):
            print("elektronics")
            prodno=df_NAVbom3['EXPR1'][i]
            print(df_NAVbom3['EXPR1'][i])
            print((df_NAVbom3['EXPR1'][i]))
            df_NAVbom1_1=NAVdb.NavBOMniva5(prodno)
            print(df_NAVbom1_1)
            niva1_1list=df_NAVbom1_1['EXPR1'].tolist()
            print(niva1_1list)
            time.sleep(2)
            prodno=niva1_1list[1]
            #prodno=df_NAVbom1_1['EXPR1'][i]
            print("prodno-elek",prodno)
            prodnoelek=prodno
    
    
    ProdOrderx=int(WO)
    #ProdNox=124196
    ProdNox=str(Niva3ProductNo)
    Station='HPSHAKER01'
    sw='v16'
    Batch=Station+'_'+str(WO)
    Recipe_ID=1
    ProsessType='Test&Setup'
    #1.1 wirebond
    #working

    dfw,error=db.wirebondid_Wirebonddb(WO)
    #print(dfw)
    if len(dfw)!=0:
        wirebondid=dfw['WireBonding_ID'].iloc[0]
        dfc=db.findcompsertid_from_compsert(wirebondid)
        if len(dfc)!=0:
            print("OK")
        else:
            ctypes.windll.user32.MessageBoxW(0, " Finner ikke BondeOppsett for denne WO ", "Error", 0)
            exit()
            #print(" Finner ikke BondeOppsett for denne WO ")
    else:
            #print(" wirebond detailjer finner ikke")
            ctypes.windll.user32.MessageBoxW(0, " wirebond detailjer finner ikke ", "Error", 0)
            exit()

    #exit()  
    # step 4.start testing 
    #RelayMUx.openallchannels()
    time.sleep(0.2)
    
    #exit()
    #4.1 
    if DUAL=='TRUE':
        ch=2
    else:
        ch=1
    for i in range(ch):
        print("Tester kanal",i+1)
        if i==0:
            #step 2. list sensor pec ,check article ,  get compp sert and write to comptrac
            # working

            #dfsp=db.ListSensorSpec_niva3_SensorSpecdb(Niva3ProductNo)
            #print(dfsp)
            #exit()
            #if len(dfsp.index!=0) :
                #for i in range (len(dfsp)-1): # ONLT WRITING COMPSERT ONCE
                    SerialNumber=guisr.serialno
                    Membraneno=guisr.MembraneNo
                    compsert_TOPLID=guisr.ToplidNo
                    compsert_hus=guisr.Husno
                    SerialNumber=int(SerialNumber)

                    print("ser.no",SerialNumber)
                    if (SerialNumber % 2 == 0):
                        ctypes.windll.user32.MessageBoxW(0, " Serial nummer skal være oddetall", "Error", 0)
                        print("Serial nummer skal være oddetall")
                        exit()
                    else:
                        ###check this 
                        db.Sensor_SerialNo_MembraneNo_Linkeddb(SerialNumber, Membraneno)

                    #dfa=db.Read_Articlebd(dfsp['Type'].iloc[i])
                    #if len(dfa)!=0 and dfsp['Type'].iloc[0]=='110921' :
                        #print("enter compsert")
                        #How to get user input?
                        #comsert=input(f"Enter Compsert to {dfa} ")
                        #compsert=str(comsert)
                        #compsert='c21211'

                        #WRITNG TOLID DETIAL 
                    
                        #prodno_TOPLID=dfsp['ProdNo'].iloc[0]

                        dfcmp_TOPLID=db.copmsert_compsertdb(compsert_TOPLID)
                        compsertid_TOPLID=dfcmp_TOPLID['CompSert_ID'].iloc[0]
                        #prodno='112109'
                        if len(dfcmp_TOPLID.index) ==0:
                            ctypes.windll.user32.MessageBoxW(0, " materail sertificate finner ikke PÅ toplid", "Error", 0)
                            exit()
                            #print(" materail sertificate finner ikke")
                        else:
                            #print(dfcmp)
                            db.Writecomptrac_elementid_Comptracdb(compsertid_TOPLID,elementid,WO,prodnotoplid)

                        #WRITING HUS DETAIL
                        #prodno_HUS='123778'
                        dfcmp_HUS=db.copmsert_compsertdb(compsert_hus)
                        compsertid_HUS=dfcmp_HUS['CompSert_ID'].iloc[0]
                        #prodno='112109'
                        if len(dfcmp_HUS.index) ==0:
                            ctypes.windll.user32.MessageBoxW(0, " materail sertificate finner ikke til HUS", "Error", 0)
                            exit()
                            #print(" materail sertificate finner ikke")
                        else:
                            #print(dfcmp)
                            db.Writecomptrac_elementid_Comptracdb(compsertid_HUS,elementid,WO,prodnohus)

                    # TEMPERARORY CODE TO AVOID EEPROM OR MA FAIL 

                    #1.clsoe Relays to communicate with ch A and measure current ch A
                    RelayMUx.CommunicateChA()
                    time.sleep(0.5)

                    #OWI  connect and activatepip 
                    pga.Activate()
                    #read eeprom 
                    location_list = [(j, i) for j in range(16) for i in range(8)]
                    #print(tuple_list)
                    #e=pga.ReadEEPROM(location_list,type_="hex",print="Reading EEPROM: ")
                    e=pga.ReadEEPROM(location_list,type_="hex")
                    #print(e)
                    
                    #5. create processid 
                    Prosess='EEPROM-BEFORE TEST-SETUP'
                    EEPType='AM5000'
                    EEPdata= ','.join(e)
                    #EEPdata=e
                    EEPROM_Prosess_ID=Limit_Result.offsetSQLdb_Process(int(elementid),i,Prosess,ProdOrderx, ProdNox, Station,ProsessType,sw,Batch,int(Operator_ID),Recipe_ID)
                    
                    Limit_Result.eepromWritetoSQLdb(int(EEPROM_Prosess_ID),EEPType,EEPdata)

                    #weite serial no to PGA 305 
                    #ElekSlnoch1= prevSerial = int("".join("".join(pga.ReadEEPROM([(12, 4), (12, 5), (12, 6), (12, 7)]))), 16)
                                                         
                    ElekSlnoch1= pga.ReadScanSenseSerial_prev()
                    if int(ElekSlnoch1) <10000 or int(ElekSlnoch1) >1000000:
                        ElekSlnoch1= pga.ReadScanSenseSerial()
                    print(ElekSlnoch1)
                    print("NORBIT SERIAL NO",ElekSlnoch1)


                    #compsert_Elektronikk=batchno= int("".join("".join(pga.ReadEEPROM([(13, 2), (13, 3), (13, 4)]))), 16)
                    compsert_Elektronikk= pga.ReadSupplierBatch_prev()
                    if int(compsert_Elektronikk) <10000 or int(compsert_Elektronikk) >1000000:
                        compsert_Elektronikk= pga.ReadSupplierBatch()
                    print("NORBIT BATCH NO",compsert_Elektronikk)
                    #exit()
                 

                    #WRITING electronikk DETAIL
                    prodno_electronikk=prodnoelek
                    
                    Kommenter=' '
                    Comments=' '
                    DateTime=datetime.now().replace(microsecond=0)
                    Bootloader=1
                    application=1

                    Limit_Result.ElectronicSQLdb_Process(int(elementid), ProdOrderx,ProdNox,SerialNumber,ElekSlnoch1,compsert_Elektronikk,int(Operator_ID),Comments,DateTime,0,Bootloader,application,Kommenter)
                
                    #exit()
                    print("writing serilano")
                    #pga.WriteScanSenseSerial(SerialNumber)
                    print("Write serial:\t\t",  pga.WriteScanSenseSerial(SerialNumber))
                    time.sleep(0.2)
                    print("reading serilano")
                    print("Read serial:\t\t", str(pga.ReadScanSenseSerial()))
                    #exit()

                    if (abs(compsert_Elektronikk) >=1000000):
                        compsert_Elektronikk=181024
                        ctypes.windll.user32.MessageBoxW(0, " materail sertificate finner ikke på Elektronikk, setter annen sertifikat", "Error", 0)
                        #print(dfcmp)
                        compsertid_electronikk=20081
                        db.Writecomptrac_elementid_Comptracdb(str(compsertid_electronikk),elementid,WO,prodnoelek)
                    else:
                        dfcmp_electronikk=db.copmsert_compsertdb(str(compsert_Elektronikk))
                        compsertid_electronikk=dfcmp_electronikk['CompSert_ID'].iloc[0]
                        print(compsertid_electronikk)
                        
                    #exit()
                    #prodno='112109'
                        if len(dfcmp_electronikk.index) ==0:
                            ctypes.windll.user32.MessageBoxW(0, " materail sertificate finner ikke på Elektronikk, setter annen sertifikat", "Error", 0)
                            #print(dfcmp)
                            compsertid_electronikk=20081
                            db.Writecomptrac_elementid_Comptracdb(str(compsertid_electronikk),elementid,WO,prodnoelek)
                        else:
                            db.Writecomptrac_elementid_Comptracdb(str(compsertid_electronikk),elementid,WO,prodnoelek)
                    


                    RelayMUx.openallchannels()
                    time.sleep(0.2)

                    ##### CH b 
                    #if Niva3ProductNo!='125859'# or Niva3ProductNo!='125510': #  checking single cahnnel T2 
                    #if Niva3ProductNo!='125510':# or Niva3ProductNo!='125510': #  checking single cahnnelg g6 
                    
                    #1.clsoe Relays to communicate with ch A and measure current ch A
                    RelayMUx.CommunicateChA()
                    time.sleep(0.5)

                    #OWI  connect and activate
                    pga.Activate()
                
                    #exit()
                    # read PADC , TADC
                    print("checking ADC")
                    Padc, Pavg, Pdiff = pga.ReadPadc(10)
                    Tadc, Tavg, Tdiff = pga.ReadTadc(10)
                    time.sleep(0.2)
                    print("PADC,TADC before tuning")
                    print(Pavg,Tavg)
                    
                    # DAC tunign so that 0 bar is 4 mA,CALC COEFF , UPLOAD COEFF , CALC CRC 
                    pga.UploadDummyData(4, mm, print=False)
                    #PGA305.PGA305_DacEnable(sn)
                    time.sleep(0.2)
                    #exit()
                    
                    # reset PGA 305 
                    RelayMUx.openallchannels()
                    time.sleep(0.2)
                    RelayMUx.CommunicateChA()
                    time.sleep(0.2)
                    # OWI
                    pga.Activate()
                
                    
                    # read PADC , TADC
                    Padc, Pavg, Pdiff = pga.ReadPadc(10)
                    Tadc, Tavg, Tdiff = pga.ReadTadc(10)
                    time.sleep(0.1)
                    print("PADC,TADC after tuning")
                    print(Pavg,Tavg)
                                        
                    #3.compare and giv result
                    #Overstyr=oversty.continuestatus
                    
                    Overstyr='FALSE' # get overstyr as user input

                    
                    #if offset is failed and all are o.k. , need to run with Oversytr as 'TRUE' again to get PASSED
                    ResultDisp, Resultdb,ChannelNo=Limit_Result.OffsetLimitAccep(i,Pavg,Overstyr)

                    #ctypes.windll.user32.MessageBoxW(0, ResultDisp, "PADC(offset)", 0)
                    if Resultdb =='PASSED':
                        print("tester inner limit")
                        ResultDisp, Resultdb,ChannelNo=Limit_Result.innerOffsetLimitAccep(i,Pavg,Overstyr)
                    #else:
                    
                        """ 
                        if oversty.continuestatus =='FALSE':
                    
                            Overstyr='FALSE'
                        elif oversty.continuestatus =='TRUE':
                            Overstyr='TRUE' """
                
                        
                        #ResultDisp, Resultdb,ChannelNo=Limit_Result.OffsetLimitAccep(i,Padc,Overstyr)
                    print(ResultDisp)

                    seriallist.append(ChannelNo+1)
                    testlist.append('PADC')
                    resultlist.append(ResultDisp)
                    resultdblist.append(Resultdb)
                    time.sleep(0.1)

                    #read eeprom 
                    location_list = [(j, i) for j in range(16) for i in range(8)]
                    #print(tuple_list)
                    e=pga.ReadEEPROM(location_list,type_="hex",print="Reading EEPROM: ")
                    print(e)
                    

                    #4.open all relays
                    RelayMUx.openallchannels()
                    time.sleep(0.2)

                    ProdOrderx=int(WO)
                    ProdNox=int(Niva3ProductNo)
                    #print("PRODNO",ProdNox)
                    #5. create processid 
                    Prosess='SADC'

                    offset_Prosess_ID=Limit_Result.offsetSQLdb_Process(int(elementid),i,Prosess,ProdOrderx, ProdNox, Station,ProsessType,sw,Batch,int(Operator_ID),Recipe_ID)
                    #exit()
                    time.sleep(0.2)
                    Limit_Result.OffsetWriteResulttoSQLdb_ProcessRes(int(offset_Prosess_ID),Resultdb,Pavg)
                    time.sleep(0.2)
                    #6. write current reuslt to database
                    #TADC - process
                    ResultDisp, Resultdb,ChannelNo=Limit_Result.TempLimitAccep(i,Tavg)
                    time.sleep(0.1)
                    seriallist.append(ChannelNo+1)
                    testlist.append('Tempchk')
                    resultlist.append(ResultDisp)
                    resultdblist.append(Resultdb)
                    #4.open all relays
                    RelayMUx.openallchannels()
                    time.sleep(0.2)

                    #5. create processid 9
                    Prosess='tempchk'
                    Temp_Prosess_ID=Limit_Result.TempSQLdb_Process(int(elementid),i,Prosess,ProdOrderx, ProdNox, Station,ProsessType,sw,Batch,int(Operator_ID),Recipe_ID)
                    time.sleep(0.2)
                    #6. write current reuslt to databas
                    Limit_Result.TempWriteResulttoSQLdb_ProcessRes(int(Temp_Prosess_ID),Resultdb,Tavg)


                    #5. create processid 
                    Prosess='EEPROM-AFTER TEST-SETUP'
                    EEPType='AM5000'
                    EEPdata= ','.join(e)
                    #EEPdata=e
                    EEPROM_Prosess_ID=Limit_Result.offsetSQLdb_Process(int(elementid),i,Prosess,ProdOrderx, ProdNox, Station,ProsessType,sw,Batch,int(Operator_ID),Recipe_ID)
                    
                    Limit_Result.eepromWritetoSQLdb(int(EEPROM_Prosess_ID),EEPType,EEPdata)
                    
                    #exit()
                    time.sleep(0.2)
                    #1
                    RelayMUx.mAtestChA()
                    time.sleep(0.2)
                    #2.measure current

                    #CurrentinmA_chA=Multimeter.measurecurrentDCmANew()
                    CurrentinmA_chA=mm.readCurrentDC() * 1000
                    print(CurrentinmA_chA)
                    #3.compare and giv result
                    ResultDisp, Resultdb,ChannelNo=Limit_Result.CurrentLimitAccep(i,CurrentinmA_chA)
                    print(ResultDisp, Resultdb,ChannelNo)
                    time.sleep(0.1)
                    seriallist.append(ChannelNo+1)
                    testlist.append('mAtest')
                    resultlist.append(ResultDisp)
                    resultdblist.append(Resultdb)

                    #4.open all relays
                    #RelayMUx.openallchannels()
                    time.sleep(0.2)
                    #5. create processid

                    Prosess='mAtest'
                
                    #Current_Prosess_ID=Limit_Result.CurrentSQLdb_Process(int(elementid),int(i),ProdOrderx, ProdNox, Station, sw,Batch,Operator_ID,Recipe_ID,Prosess,ProsessType)
                    Current_Prosess_ID=Limit_Result.CurrentSQLdb_Process(int(elementid),i,Prosess,ProdOrderx, ProdNox, Station,ProsessType,sw,Batch,int(Operator_ID),Recipe_ID)

                    time.sleep(0.2)
                        #6. write current reuslt to database
                    Limit_Result.CurrentWriteResulttoSQLdb_ProcessRes(int(Current_Prosess_ID),Resultdb,CurrentinmA_chA)
                    
                    #1.IR setup
                    
                    #1.close relays for IR test ChA
                    RelayMUx.IRtestChAandbody()
                    time.sleep(0.2)
                    #2.IR test -chA

                    #v6
                    ir=IR6.IRinitrun('A')
                    DSR1=[]
                    MeasValue=[]
                    timer=10
                    stop='FALSE'
                    DSR1,MeasValue,m, Result=IR6.IRdataread('A',ir,DSR1,MeasValue, timer,stop)
                    print("all result", DSR1,MeasValue,m)
                    print(MeasValue[-1])
                    sp=MeasValue[-1].split(",")
                    IRtid=timer- float(sp[2])
                    Res_TestTime= round(IRtid,4)
                    Res_IRvalue=sp[1]
                    Res_IRvalue=float(Res_IRvalue[0:4])
                    Res_TestVolt=sp[0]
                    print(type(Res_IRvalue))
                    allvauestillpass= ' ,'.join(MeasValue[-2:])
                    print("allvalues1",allvauestillpass)
                    allvaluestillpass=allvauestillpass[0:49] 
                    print("allvaluesfist 50",allvauestillpass)                    
                    ResultDisp, Resultdb, Testtime,ChannelNo=Limit_Result.IRLimitAccep(i,Res_IRvalue,Res_TestTime)
                    print(ResultDisp, Resultdb, Testtime,ChannelNo)
                    time.sleep(0.1) 



                    seriallist.append(ChannelNo+1)
                    testlist.append('IR-A')
                    resultlist.append(ResultDisp)
                    resultdblist.append(Resultdb)
                    #4.open all relays
                    #RelayMUx.openallchannels()
                    time.sleep(0.2)
                    Prosess='IrTest'
                    
                    #IR_Prosess_ID=Limit_Result.IRSQLdb_Process(int(elementid),int(i),ProdOrderx, ProdNox, Station, sw,Batch,Operator_ID,Recipe_ID,ProsessType,Prosess)
                    #IR_Prosess_ID=Limit_Result.IRSQLdb_Process(int(elementid),ProdOrderx, ProdNox, Station, Prosess,ProsessType,int(i),sw,Batch,Operator_ID,Recipe_ID)
                    IR_Prosess_ID=Limit_Result.IRSQLdb_Process(int(elementid),i,Prosess,ProdOrderx, ProdNox, Station,ProsessType,sw,Batch,int(Operator_ID),Recipe_ID)
                    #IR_Prosess_ID=IRSQLdb_Process(88542,0,'IR',224288,124189,'pc','Test&Setup','v1','jk22',324, 1)
                    time.sleep(0.2)
                    #5. write current reuslt to database
                    Limit_Result.IRWriteResult_v2toSQLdb_ProcessRes(int(IR_Prosess_ID),Resultdb, Res_IRvalue,Res_TestTime,allvaluestillpass)
                    ir.clear()
                    ir.close()
            
        elif(i==1):
                
                #ctypes.windll.user32.MessageBoxW(0, "SJEKKER KANAL B", "KANAL B", 0)
                SerialNumber=int(SerialNumber)+1
                #print(SerialNumber)
                #ctypes.windll.user32.MessageBoxW(0, str(SerialNumber), "KANAL B-serial no", 0)
                #db.Sensor_SerialNo_MembraneNo_Linkeddb(SerialNumber, Membraneno)
                RelayMUx.CommunicateChB()
                time.sleep(0.2)

                #OWI  connect and activate
                pga.Activate()
                location_list = [(j, i) for j in range(16) for i in range(8)]
                #print(tuple_list)
                e=pga.ReadEEPROM(location_list,type_="hex",print="Reading EEPROM: ")
                print(e)
                
                #5. create processid 
                Prosess='EEPROM-BEFORE TEST-SETUP'
                EEPType='AM5000'
                EEPdata= ','.join(e)
                #EEPdata=e
                EEPROM_Prosess_ID=Limit_Result.offsetSQLdb_Process(int(elementid),i,Prosess,ProdOrderx, ProdNox, Station,ProsessType,sw,Batch,int(Operator_ID),Recipe_ID)
                
                Limit_Result.eepromWritetoSQLdb(int(EEPROM_Prosess_ID),EEPType,EEPdata)

                #weite serial no to PGA 305 
                #print("Write serial:\t\t", PGA305.PGA305_WriteICSerial(sn, SerialNumber))
                ElekSlnoch2= pga.ReadScanSenseSerial_prev()
                if int(ElekSlnoch2) <10000 or int(ElekSlnoch2) >1000000:
                    ElekSlnoch2= pga.ReadScanSenseSerial()
                
                print("NORBIT SERIAL NO",ElekSlnoch1)


                #compsert_Elektronikk=batchno= int("".join("".join(pga.ReadEEPROM([(13, 2), (13, 3), (13, 4)]))), 16)
                compsert_Elektronikk2= pga.ReadSupplierBatch_prev()
                if int(compsert_Elektronikk2) <10000 or int(compsert_Elektronikk2) >1000000:
                    compsert_Elektronikk2= pga.ReadSupplierBatch()
                print("NORBIT BATCH NO",compsert_Elektronikk2)

                #WRITING electronikk DETAIL
                prodno_electronikk=prodnoelek
                
                Kommenter=' '
                Comments=' '
                DateTime=datetime.now().replace(microsecond=0)
                Bootloader=1
                application=1

                Limit_Result.ElectronicSQLdb_Process(int(elementid), ProdOrderx,ProdNox,SerialNumber,ElekSlnoch2,compsert_Elektronikk2,int(Operator_ID),Comments,DateTime,1,Bootloader,application,Kommenter)
            
                #exit()
            
                print("Write serial:\t\t", pga.WriteScanSenseSerial(SerialNumber))
                time.sleep(0.2)

                print("Read serial:\t\t", str(pga.ReadScanSenseSerial()))


                # read PADC , TADC

                Padc, Pavg, Pdiff = pga.ReadPadc(10)
                Tadc, Tavg, Tdiff = pga.ReadTadc(10)
                time.sleep(0.1)
                print("before tuning")
                print("PADC",Pavg,Tavg)
                
                # DAC tunign so that 0 bar is 4 mA
                
                time.sleep(0.1)
        
                pga.UploadDummyData(4, mm, print=False)
            


                # reset PGA 305 
                RelayMUx.openallchannels()
                time.sleep(0.2)
                RelayMUx.CommunicateChB()
                time.sleep(0.2)
                # OWI
            
                print("Activation:\t\t", pga.Activate())


                
                # read PADC , TADC
                Padc, Pavg, Pdiff = pga.ReadPadc(10)
                Tadc, Tavg, Tdiff = pga.ReadTadc(10)
                time.sleep(0.1)
                print("after tuning")
                print("PADC",Pavg,Tavg)
                #ctypes.windll.user32.MessageBoxW(0, str(Padc), "PADC", 0)
                
                
                #3.compare and giv result
                
                Overstyr='FALSE' # get overstyr as user input

                    
                #if offset is failed and all are o.k. , need to run with Oversytr as 'TRUE' again to get PASSED
                ResultDisp, Resultdb,ChannelNo=Limit_Result.OffsetLimitAccep(i,Pavg,Overstyr)

                #ctypes.windll.user32.MessageBoxW(0, ResultDisp, "PADC(offset)", 0)
                if Resultdb =='PASSED':
                    ResultDisp, Resultdb,ChannelNo=Limit_Result.innerOffsetLimitAccep(i,Pavg,Overstyr)
                #else:
                    
                    """ 
                    if oversty.continuestatus =='FALSE':
                
                        Overstyr='FALSE'
                    elif oversty.continuestatus =='TRUE':
                        Overstyr='TRUE' """
                
                    
                    #ResultDisp, Resultdb,ChannelNo=Limit_Result.OffsetLimitAccep(i,Padc,Overstyr)
                print(ResultDisp)

            
                """  Overstyr='TRUE'  # get overstyr as user input
                #if offset is failed and all are o.k. , need to run with Oversytr as 'TRUE' again to get PASSED
                ResultDisp, Resultdb,ChannelNo=Limit_Result.OffsetLimitAccep(i,Padc,Overstyr)
                #ctypes.windll.user32.MessageBoxW(0, ResultDisp, "offset", 0)
                time.sleep(0.1)
                if Resultdb !='PASSED':
                    
                    if oversty.continuestatus =='FALSE':
                    
                        Overstyr='FALSE'
                    elif oversty.continuestatus =='TRUE':
                        Overstyr='TRUE'
                ResultDisp, Resultdb,ChannelNo=Limit_Result.OffsetLimitAccep(i,Padc,Overstyr) """

                seriallist.append(ChannelNo+1)
                testlist.append('PADC')
                resultlist.append(ResultDisp)
                resultdblist.append(Resultdb)
                
                #read eeprom 
                #read eeprom 
                location_list = [(j, i) for j in range(16) for i in range(8)]
                #print(tuple_list)
                e=pga.ReadEEPROM(location_list,type_="hex",print="Reading EEPROM: ")
                print(e)


                #4.open all relays
                RelayMUx.openallchannels()
                time.sleep(0.2)
                #5. create processid

                Prosess='SADC'
                offset_Prosess_ID=Limit_Result.offsetSQLdb_Process(int(elementid),i,Prosess,ProdOrderx, ProdNox, Station,ProsessType,sw,Batch,int(Operator_ID),Recipe_ID)
        
                time.sleep(0.2)
                #6. write current reuslt to database
                Limit_Result.OffsetWriteResulttoSQLdb_ProcessRes(int(offset_Prosess_ID),Resultdb,Pavg)
                time.sleep(0.2)

                #TADC - process

                ResultDisp, Resultdb,ChannelNo=Limit_Result.TempLimitAccep(i,Tavg)
                time.sleep(0.1)
                seriallist.append(ChannelNo+1)
                testlist.append('Tmpchk')
                resultlist.append(ResultDisp)
                resultdblist.append(Resultdb)

                #4.open all relays
                RelayMUx.openallchannels()
                time.sleep(0.2)
                #5. create processid
                Prosess='tempchk'
                
                
                Temp_Prosess_ID=Limit_Result.TempSQLdb_Process(int(elementid),i,Prosess,ProdOrderx, ProdNox, Station,ProsessType,sw,Batch,int(Operator_ID),Recipe_ID)
            
                #6. write current reuslt to databas
                Limit_Result.TempWriteResulttoSQLdb_ProcessRes(int(Temp_Prosess_ID),Resultdb,Tavg)
            
                #5. create processid 
                Prosess='EEPROM-AFTER TEST-SETUP'
                EEPType='AM5000'
                EEPdata= ','.join(e)
                #EEPdata=e
                EEPROM_Prosess_ID=Limit_Result.offsetSQLdb_Process(int(elementid),i,Prosess,ProdOrderx, ProdNox, Station,ProsessType,sw,Batch,int(Operator_ID),Recipe_ID)
                
                Limit_Result.eepromWritetoSQLdb(int(EEPROM_Prosess_ID),EEPType,EEPdata)
                    

                #mA test ch B
                RelayMUx.mAtestChB()
                time.sleep(0.2)
                #2.measure current

                #CurrentinmA_chB=Multimeter.measurecurrentDCmANew()
                CurrentinmA_chB=mm.readCurrentDC() * 1000
                print(CurrentinmA_chB)
                #3.compare and giv result
                ResultDisp, Resultdb,ChannelNo=Limit_Result.CurrentLimitAccep(i,CurrentinmA_chB)
                print(ResultDisp, Resultdb,ChannelNo)
                time.sleep(0.1)
                seriallist.append(ChannelNo+1)
                testlist.append('mAtest')
                resultlist.append(ResultDisp)
                resultdblist.append(Resultdb)
                #4.open all relays
                RelayMUx.openallchannels()
                time.sleep(0.2)
                #5. create processid 
                Prosess='mAtest'
                
                Current_Prosess_ID=Limit_Result.CurrentSQLdb_Process(int(elementid),i,Prosess,ProdOrderx, ProdNox, Station,ProsessType,sw,Batch,int(Operator_ID),Recipe_ID)
                time.sleep(0.2)
                #6. write current reuslt to database
                Limit_Result.CurrentWriteResulttoSQLdb_ProcessRes(int(Current_Prosess_ID),Resultdb,CurrentinmA_chB)



                #1.IR setup
            
                #1.close relays for IR test ChB
                RelayMUx.IRtestChBandbody()
                time.sleep(0.2)

                #2.IR test -chB

                #v6
                ir2=IR6.IRinitrun('B')
                DSR2=[]
                MeasValue2=[]
                timer2=10
                stop2='FALSE'
                DSR2,MeasValue2,m2, Result2=IR6.IRdataread('B',ir2,DSR2,MeasValue2, timer2,stop2)
                print("all result", DSR2,MeasValue2,m2)
                print(MeasValue2[-1])
                sp=MeasValue[-1].split(",")
                
                IRtid2=timer2- float(sp[2])
                Res_TestTime2= round(IRtid2,4)
                Res_IRvalue2=sp[1]
                Res_IRvalue2=float(Res_IRvalue2[0:4])
                Res_TestVolt2=sp[0]
                
                allvauestillpass2= ' ,'.join(MeasValue2[-2:])
                print("allvaluesfist",allvauestillpass2)  
                allvaluestillpass2=allvauestillpass2[0:49] 
                print("allvaluesfist 50",allvauestillpass2)                      
                ResultDisp2, Resultdb2, Testtime2,ChannelNo2=Limit_Result.IRLimitAccep(i,Res_IRvalue2,Res_TestTime2)
                print(ResultDisp2, Resultdb2, Testtime2,ChannelNo2)
                time.sleep(0.1) 
                ir2.clear()
                ir2.close()
            


                seriallist.append(ChannelNo+1)
                testlist.append('IR-B')
                resultlist.append(ResultDisp2)
                resultdblist.append(Resultdb2)
                #4.open all relays
                RelayMUx.openallchannels()
                time.sleep(0.2)
                #4. create processid
                Prosess='IrTest'
                #Prosess='IrTest'  # got from calling funciton 
                
                IR_Prosess_ID=Limit_Result.IRSQLdb_Process(int(elementid),i,Prosess,ProdOrderx, ProdNox, Station,ProsessType,sw,Batch,int(Operator_ID),Recipe_ID)

                time.sleep(0.2)
                #5. write current reuslt to database
                Limit_Result.IRWriteResult_v2toSQLdb_ProcessRes(int(IR_Prosess_ID),Resultdb2, Res_IRvalue2,Res_TestTime2,allvaluestillpass2)

                #1.close relays for IR test bw Ch A and Ch B
                RelayMUx.IRtestChAandChB()
                time.sleep(0.2)

                

                #v6
                ir3=IR6.IRinitrun('AB')
                DSR3=[]
                MeasValue3=[]
                timer3=10
                stop3='FALSE'
                DSR3,MeasValue3,m3, Result3=IR6.IRdataread('AB',ir3,DSR3,MeasValue3, timer3,stop3)
                print("all result", DSR3,MeasValue3,m3)
                print(MeasValue3[-1])
                sp=MeasValue3[-1].split(",")
                
                IRtid=timer3- float(sp[2])
                Res_TestTime3= round(IRtid,4)
                Res_IRvalue3=sp[1]
                Res_IRvalue3=float(Res_IRvalue3[0:4])
                Res_TestVolt3=sp[0]
                
                allvauestillpass3= ' ,'.join(MeasValue3[-2:])
                print("allvaluesfist ",allvauestillpass3)  
                allvaluestillpass3=allvauestillpass3[0:49]
                print("allvaluesfist_50",allvauestillpass3)             
                ResultDisp3, Resultdb3, Testtime3,ChannelNo3=Limit_Result.IRLimitAccep(i,Res_IRvalue3,Res_TestTime3)
                print(ResultDisp3, Resultdb3, Testtime3,ChannelNo3)
                time.sleep(0.1) 


                seriallist.append(ChannelNo+1)
                testlist.append('IR-CH-AB')
                resultlist.append(ResultDisp3)
                resultdblist.append(Resultdb3)

                #4.open all relays
                RelayMUx.openallchannels()
                time.sleep(0.2)


                #4. create processid
                Prosess='IrTestAB'
                
                IR_Prosess_ID=Limit_Result.IRSQLdb_Process(int(elementid),i,Prosess,ProdOrderx, ProdNox, Station,ProsessType,sw,Batch,int(Operator_ID),Recipe_ID)
                time.sleep(0.1)
                #5. write current reuslt to database
                Limit_Result.IRWriteResult_v2toSQLdb_ProcessRes(int(IR_Prosess_ID),Resultdb3, Res_IRvalue3,Res_TestTime3,allvaluestillpass3)
                ir3.clear()
                ir3.close()
Stoptime=datetime.now().replace(microsecond=0)
timetaken=Stoptime-Startime
print("testingtime",timetaken)
print(resultdblist)
if all(element == 'PASSED' for element in resultdblist):
    Combinedbresult ='PASSED' 
else:
    Combinedbresult ='FAILED' 
print(Combinedbresult)
#4. create processid
Prosess='CombinedResult'

IR_Prosess_ID=Limit_Result.IRSQLdb_Process(int(elementid),0,Prosess,ProdOrderx, ProdNox, Station,ProsessType,sw,Batch,int(Operator_ID),Recipe_ID)
time.sleep(0.1)
#5. write current reuslt to database
Limit_Result.CombinedResult_v2toSQLdb_ProcessRes(int(IR_Prosess_ID),Combinedbresult)
table.displists(seriallist,testlist,resultlist)

    


        


        




