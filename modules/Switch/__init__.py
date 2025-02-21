import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

from modules import util

class Switch:
    def __new__(cls):
        if "instruments" not in util.config:
            raise Exception(util.Red("No 'instruments' is defined in config", ret=True))
        if "sw" not in util.config["instruments"]:
            raise Exception(util.Red("No switch 'sw' is defined in config", ret=True))
        if "module" not in util.config["instruments"]["sw"]:
            raise Exception(util.Red("The switch is missing 'module' in config", ret=True))
        if "port" not in util.config["instruments"]["sw"]:
            raise Exception(util.Red("The switch is missing 'port' in config", ret=True))

        sw = util.config["instruments"]["sw"]["module"]
        port = util.config["instruments"]["sw"]["port"]
        
        """ if sw == "Agilent_34970A":
            from modules.Switch.Agilent_34970A import Agilent_34970A
            return Agilent_34970A(port) """
    
        if sw == "Keithley_2750":
            from modules.Switch.Keithley_2750 import Keithley_2750
            return Keithley_2750(port)
        
        else:
            raise Exception(util.Red("The switch 'module' does not exist", ret=True))