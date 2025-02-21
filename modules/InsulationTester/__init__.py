import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

from modules import util

class InsulationTester:
    def __new__(cls):      
        if "instruments" not in util.config:
            raise Exception(util.Red("No 'instruments' is defined in config", ret=True))
        if "it" not in util.config["instruments"]:
            raise Exception(util.Red("No insulation tester 'it' is defined in config", ret=True))
        if "module" not in util.config["instruments"]["it"]:
            raise Exception(util.Red("The insulation tester is missing 'module' in config", ret=True))
        if "port" not in util.config["instruments"]["it"]:
            raise Exception(util.Red("The insulation tester is missing 'port' in config", ret=True))

        it = util.config["instruments"]["it"]["module"]
        port = util.config["instruments"]["it"]["port"]
        
        if it == "Kikusui_TOS7200":
            from modules.InsulationTester.Kikusui_TOS7200 import Kikusui_TOS7200
            return Kikusui_TOS7200(port)
        
        else:
            raise Exception(util.Red("The insulation tester 'module' does not exist", ret=True))