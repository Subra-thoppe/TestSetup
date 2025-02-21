import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

import json, winsound, datetime, re
import time as tm

Color = False
Log = False

def typeCheck(name: str, value: type, type_: type) -> None:
    if not isinstance(value, type_):
        raise TypeError(Red(f"'{name}' can only be a {type_} not {type(value)} = {value}", ret=True))

def errorCheck(type_: str, name: str = None, value: str | int = None) -> None:
    typeCheck("type", type_, str)
    typeCheck("name", name, str | None)
    typeCheck("value", value, str | int | None)

    if type_ == "VisaIOError":
        raise ConnectionRefusedError(Red(f"Could not open connection on {name}: {value}", ret=True))
    
    if type_ == "VisaReadError":
        raise ConnectionAbortedError(Red(f"Could not read from pyvisa on {name}: {value}", ret=True))
    
    if type_ == "ModuleNotFound":
        raise LookupError(Red(f"Could not find module for {name}: {value}", ret=True))
    
    if type_ == "IdnError":
        raise AttributeError(Red(f"Could not read IDN for {name}: {value}", ret=True))
    
    if type_ == "FileNotFound":
        raise FileNotFoundError(Red(f"Could not find file {name} in {value}", ret=True))
    
    if type_ == "OnlyOneController":
        raise ConnectionAbortedError(Red(f"Only one {name} is supported found: {value}", ret=True))
    
    if type_ == "CommandInvalid":
        raise ValueError(Red(f"The command is invalid: {value}", ret=True))
    
    if type_ == "ReadError":
        raise ConnectionError(Red(f"Can not read {name} from the sensor: {value}", ret=True))
    
    if type_ == "PortError":
        raise ConnectionError(Red(f"Please specify port for {name} as param or in config file", ret=True))
    
    if type_ == "PageLengthError":
        raise ValueError(Red(f"The list :{name} has to contain exactly 8 values | {name} = {value}", ret=True))
    
    if type_ == "ListLengthError":
        raise ValueError(Red(f"The lists: {name} has to contain the same number of values | {name} = {value}", ret=True))
    
    if type_ == "PinError":
        raise ValueError(Red(f"Only pin 2 and 6 can be used, not {name} = {value}", ret=True))

def minMaxCheck(name: str, value: int | float, minValue: int | float, maxValue: int | float) -> None:
    typeCheck("name", name, str)
    typeCheck("value", value, int | float)
    typeCheck("minValue", minValue, int | float)
    typeCheck("maxValue", maxValue, int | float)

    if not (value >= minValue and value <= maxValue):
        raise ValueError(Red(f"{name} has to be between {minValue} and {maxValue} = {value}", ret=True))

def writeCsv(path: str, data: list):
    typeCheck("path", path, str)
    typeCheck("data", data, list)

    try:
        with open(path, "a") as f:
            if len(data) > 0:
                s = re.sub(r";\s+", ";", White(data, ret=True, sep=";"))
                f.write((s[:-1] if s.endswith(";") else s) + "\n")
    except Exception as e:
        raise Exception(Red(f"Can not write csv file: '{path}', error: {e}"))

def writeJson(path: str, data: dict):
    typeCheck("path", path, str)
    typeCheck("data", data, dict)

    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        raise Exception(Red(f"Can not write Json file: '{path}', error: {e}"))
    
def writeLog(path: str, text: str):
    typeCheck("path", path, str)
    typeCheck("text", text, str)

    try:
        with open(path, "a") as f:
            f.write(f"{date()}\t{time()}\t{text}\n")
    except Exception as e:
        raise Exception(Red(f"Can not write log file: '{path}', error: {e}"))

def readCsv(path: str):
    typeCheck("path", path, str)

    data = []
    try:
        with open(path, 'r') as file:
            for line in file.readlines():
                rows =  list(map(lambda s: str(s).strip(), line.strip().split(';')))
                if rows:
                    data.append(rows)

        return data
    except Exception as e:
        raise Exception(Red(f"Can not read csv file '{path}', error: {e}"))

def readCsvAsJson(path: str):
    typeCheck("path", path, str)

    jData = []
    cData = readCsv(path)
    
    for row in cData[1:]:
        jData.append({cData[0][i]: row[i] for i in range(len(cData[0]))})
    
    return jData

def readJson(path: str):
    typeCheck("path", path, str)

    try:
        open(path, "a")
        with open(path, 'r') as file:
            data: dict = json.loads(file.read() or "{}")
            return data
        
    except json.decoder.JSONDecodeError as e:
        raise Exception(Red(f"There is a error in the json file: '{path}'", ret=True))
    except Exception as e:
        raise Exception(Red(f"Can not read Json file '{path}', error: {e}"))
    
def toJson(data: list | dict):
    typeCheck("data", data, list | dict)

    return json.dumps(data, indent=4)

def date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

def time():
    return datetime.datetime.now().strftime("%H:%M:%S")

def eta(seconds: int | float):
    typeCheck("seconds", seconds, int | float)

    return str(datetime.timedelta(seconds = int(seconds)))

def start():
    global startTime
    startTime = tm.time()
    Grey(f"Current timestamp: {startTime}")

def finish():
    Green("Done")
    Cyan(f"Time: {eta(tm.time() - startTime)}")
    Beep()

def checkConfig(config: dict, keys: list):
    typeCheck("config", config, dict)
    typeCheck("keys", keys, list)

    for key in keys:
        if key not in config:
            raise Exception(Red(f"'{key}' is not defined in config", ret=True))

def setColor() -> None:
    global Color
    Color = True

def unsetColor(msg: str) -> str:
    typeCheck("msg", msg, str)
    
    for color in ["\033[0m", "\033[90m", "\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m", "\033[96m", "\033[97m", "\033[98m", "\033[99m"]:
        msg = msg.replace(color, "")
    return msg

def setLog() -> None:
    global Log
    Log = True

def color(*args, sep):
    text = []
    for arg in args:
        if isinstance(arg, int):
            text.append(str(arg))
        elif isinstance(arg, float):
            text.append(f"{arg:.8f}".rstrip('0').rstrip('.'))
        elif isinstance(arg, list):
            text += map(lambda s: f"{s:.8f}".rstrip('0').rstrip('.') if isinstance(s, float) else str(s).strip(), arg)
        elif isinstance(arg, dict):
            text += [str(item).strip() for pair in arg.items() for item in pair]
        else:
            text.append(str(arg))

    while len(text) <= 5:
        text.append("")

    if sep == "\t":
        data = f"".join(map(lambda t: str(t).ljust(25), text))
        if Log: writeLog("log.log", data)
        return data
    elif sep == ";":
        data = f"".join(map(lambda t: f"{t}{sep}".ljust(25), text))
        if Log: writeLog("log.log", data)
        return data
    
    data = f"{sep}".join(text)
    if Log: writeLog("log.log", data)
    return data

def White(*data: int | float | str | list, sep = "\t", end = "\n", ret = False):
    text = "" + color(*data, sep=sep) + ""
    if not ret: print(text, end=end)
    return text

def Grey(*data: int | float | str | list, sep = "\t", end = "\n", ret = False):
    text = "\033[90m" + color(*data, sep=sep) + "\033[0m"
    if not ret: print(text, end=end)
    return text

def Purple(*data: int | float | str | list, sep = "\t", end = "\n", ret = False):
    text = "\033[95m" + color(*data, sep=sep) + "\033[0m"
    if not ret: print(text, end=end)
    return text

def Blue(*data: int | float | str | list, sep = "\t", end = "\n", ret = False):
    text = "\033[94m" + color(*data, sep=sep) + "\033[0m"
    if not ret: print(text, end=end)
    return text

def Cyan(*data: int | float | str | list, sep = "\t", end = "\n", ret = False):
    text = "\033[96m" + color(*data, sep=sep) + "\033[0m"
    if not ret: print(text, end=end)
    return text

def Green(*data: int | float | str | list, sep = "\t", end = "\n", ret = False):
    text = "\033[92m" + color(*data, sep=sep) + "\033[0m"
    if not ret: print(text, end=end)
    return text

def Yellow(*data: int | float | str | list, sep = "\t", end = "\n", ret = False):
    text = "\033[93m" + color(*data, sep=sep) + "\033[0m"
    if not ret: print(text, end=end)
    return text

def Red(*data: int | float | str | list, sep = "\t", end = "\n", ret = False):
    text = "\033[91m" + color(*data, sep=sep) + "\033[0m"
    if not ret: print(text, end=end)
    return text

def Beep(duration = 1500):
    winsound.Beep(1000, duration)

def HexToInt2s(hex: int | str, nbits = 24):
    typeCheck("hex", hex, int | str)

    if isinstance(hex, str):
        val = int(hex, 16)
    else:
        val = int(hex)

    if (val & (1 << (nbits - 1))) != 0:
        val = val - (1 << nbits)
    return val 

def Int2sToHex(value: int | float, nbits = 24):
    typeCheck("value", value, int | float)

    v = (int(value) + (1 << nbits)) % (1 << nbits)
    return hex(v).replace("0x", "").zfill(6).upper()

def MapRange(x: int | float, in_min = -0x800000, in_max = 0x7FFFFF, out_min = -2.5, out_max = 2.5):
    typeCheck("x", x, int | float)
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

configPath = "C:\AM5000\python-libTestsetup-nysw\config.json"
config = readJson(configPath)

if __name__ == "__main__":
    setColor()
    setLog()

    White(1/3)
    Grey(1/3, 456, sep=" ")
    Purple(1/3, 456, 789, sep=" - ")
    Blue("1/3")
    Cyan("1/3", "456", sep=" | ")
    Green("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "456", "789")
    Yellow(1/3.0)
    Red(1/3.0, 456.0)
    White(1/3.0, 456.0, 789.0)
    Grey([1/3])
    Purple([1/3, 456])
    Blue([1/3, 456, 789])
    Cyan(["1/3"])
    Green(["1/3", "456"])
    Yellow(["1/3", "456", "789"])
    print(Red([1/3], [456, 789], ret=False))
    White({"A": 1, "B": 2})

    Red(1, 2, 3, 4, 5, 6, 7, 8, end="\r")
    Yellow(1, 2, 3, 4, 5, 6, 7, end="\r")
    Green(1, 2, 3, 4, 5, 6, end="\r")
    Cyan(1, 2, 3, 4, 5, end="\r")
    Blue(1, 2, 3, 4, end="\r")
    Purple(1, 2, 3, end="\r")
    Grey(1, 2, end="\r")
    White(1)
    Red(1, "", "", "", "", "", "", 8, end="\r")
    White(1, "", 3)