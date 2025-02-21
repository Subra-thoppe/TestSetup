import sys, os
sys.path.append("T:\ProdSW_AM5000\CommonTestSetupProgram_AM5000\python-libTestsetup-nysw")

import modules.Database.proddbread as db
import modules.GUI.gui_wo_opr as gui
import modules.util as util
WO=int(gui.WORKORDER)
df=db.sjekk_TS_teststatus(WO)
print(df)
util.Green(f"Antall sensorer som er testet i Test og SEtup i WO  {WO} inntil nå er " , len(df) , " Passe på at noen sensorer kan være testet flere ganger")