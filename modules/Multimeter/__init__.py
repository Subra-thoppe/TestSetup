import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

from modules import util

class Multimeter:
    def __new__(cls):
        if "instruments" not in util.config:
            raise Exception(util.Red("No 'instruments' is defined in config", ret=True))
        if "mm" not in util.config["instruments"]:
            raise Exception(util.Red("No multimeter 'mm' is defined in config", ret=True))
        if "module" not in util.config["instruments"]["mm"]:
            raise Exception(util.Red("The multimeter is missing 'module' in config", ret=True))
        if "port" not in util.config["instruments"]["mm"]:
            raise Exception(util.Red("The multimeter is missing 'port' in config", ret=True))

        mm = util.config["instruments"]["mm"]["module"]
        port = util.config["instruments"]["mm"]["port"]
        
        if mm == "Agilent_34410A":
            from modules.Multimeter.Agilent_34410A import Agilent_34410A
            return Agilent_34410A(port)
        
        elif mm == "Fluke_45":
            from modules.Multimeter.Fluke_45 import Fluke_45
            return Fluke_45(port)
        
        elif mm == "Fluke_8808A":
            from modules.Multimeter.Fluke_8808A import Fluke_8808A
            return Fluke_8808A(port)
        
        elif mm == "HP_34401A":
            from modules.Multimeter.HP_34401A import HP_34401A
            return HP_34401A(port)
        
        else:
            raise Exception(util.Red("The multimeter 'module' does not exist", ret=True))