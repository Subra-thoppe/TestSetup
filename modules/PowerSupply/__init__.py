import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

from modules import util

class PowerSupply:
    def __new__(cls):
        if "instruments" not in util.config:
            raise Exception(util.Red("No 'instruments' is defined in config", ret=True))
        if "ps" not in util.config["instruments"]:
            raise Exception(util.Red("No power supply 'ps' is defined in config", ret=True))
        if "module" not in util.config["instruments"]["ps"]:
            raise Exception(util.Red("The power supply is missing 'module' in config", ret=True))
        if "port" not in util.config["instruments"]["ps"]:
            raise Exception(util.Red("The power supply is missing 'port' in config", ret=True))

        ps = util.config["instruments"]["ps"]["module"]
        port = util.config["instruments"]["ps"]["port"]
        
        if ps == "Agilent_E3632A":
            from modules.PowerSupply.Agilent_E3632A import Agilent_E3632A
            return Agilent_E3632A(port)
        
        elif ps == "GW_4323":
            from modules.PowerSupply.GW_4323 import GW_4323
            return GW_4323(port)
        
        elif ps == "HP_E3631A":
            from modules.PowerSupply.HP_E3631A import HP_E3631A
            return HP_E3631A(port)
        
        elif ps == "TTi_EX355P":
            from modules.PowerSupply.TTi_EX355P import TTi_EX355P
            return TTi_EX355P(port)
        
        elif ps == "TTi_QL355TP":
            from modules.PowerSupply.TTi_QL355TP import TTi_QL355TP
            return TTi_QL355TP(port)
        
        else:
            raise Exception(util.Red("The power supply 'module' does not exist", ret=True))