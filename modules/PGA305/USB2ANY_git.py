import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

import ctypes, time
from modules import util

INT = ctypes.c_int
CHAR = ctypes.c_char_p

class USB2ANY():

    def __init__(self, Activate = None, Config = None):
        self.serialnumber = None

        self.LoadDll()
        self.IsUSB2ANYConnected()
        self.DisableFirmwareCheck()
        self.FindControllers()
        self.GetDeviceSerialNumbers()
        self.Activate_ = Activate
        self.Config_ = Config

    def LoadDll(self) -> int | Exception:
        """
        This function loads USB2ANY.dll file

        Returns 1 on success or error message
        """

        try:
            path = os.path.dirname(__file__)
            self.dll = ctypes.windll.LoadLibrary(f"{path}/USB2ANY.dll")
        except FileNotFoundError as e:
            return e

        return 1

    def IsUSB2ANYConnected(self) -> int | Exception:
        """
        This function reports whether the USB2ANY is connected.

        Returns 1 if a USB2ANY device is connected, otherwise negative error code.
        """
        self.dll.u2aIsUSB2ANYConnected.argtypes = []
        self.dll.u2aIsUSB2ANYConnected.restype = INT

        response = self.Retry(lambda: self.dll.u2aIsUSB2ANYConnected(), "dll.u2aIsUSB2ANYConnected()", "1", "Is USB2ANY connected and available?")
        return response

    def DisableFirmwareCheck(self) -> int | Exception:
        """
        This function disables firmware check on run

        Returns 0 on success. If an error occurs, a negative error code is returned.
        """

        response = self.Retry(lambda: self.dll.u2aSuppressFirmwareCheck(1), "dll.u2aSuppressFirmwareCheck()", "0,1", "Can not disable firmware check")
        return response

    def FindControllers(self) -> int | Exception:
        """
        This function scans the USB bus, enumerating USB2ANY devices and creating a list of the devices it finds. The list can be read using the u2aGetSerialNumber function.

        Returns the number of USB2ANY devices found or zero, if no devices were found.
        """

        self.dll.u2aFindControllers.argtypes = []
        self.dll.u2aFindControllers.restype = INT

        response = self.Retry(lambda: self.dll.u2aFindControllers(), "dll.u2aFindControllers()", "1", "Make sure only 1 USB2ANY is connected")
        return response

    def GetDeviceSerialNumbers(self) -> str | Exception:
        """
        This function returns the serial number of the USB2ANY devices found by a previous call to the u2aFindControllers function.

        Returns zero on success. If index is out of range, or there are no more devices to enumerate, ERR_PARAM_OUT_OF_RANGE is returned.
        """

        self.dll.u2aGetSerialNumber.argtypes = [INT, CHAR]
        self.dll.u2aGetSerialNumber.restype = INT

        serialnumber = ctypes.create_string_buffer(256)
        self.Retry(lambda: self.dll.u2aGetSerialNumber(0, serialnumber), "dll.u2aGetSerialNumber()", "0", "Can not get USB2ANY serialnumber")

        self.serialnumber = serialnumber.value.decode()
        return self.serialnumber

    def ErrorCodes(self, code: int) -> str:
        """
        This function converts error code to error message

        Returns string representation of a error code
        """

        if code == -1:
            return "-1 | ERR_COM_RX_OVERFLOW | Receiver overflowed"
        if code == -2:
            return "-2 | ERR_COM_RX_BUF_EMPTY | Receive buffer is empty"
        if code == -3:
            return "-3 | ERR_COM_TX_BUF_FULL | Transmit buffer is full"
        if code == -4:
            return "-4 | ERR_COM_TX_STALLED | Transmit is stalled "
        if code == -5:
            return "-5 | ERR_COM_TX_FAILED | Transmit failed"
        if code == -6:
            return "-6 | ERR_COM_OPEN_FAILED Failed to open communications port"
        if code == -7:
            return "-7 | ERR_COM_PORT_NOT_OPEN | Communications port is not open"
        if code == -8:
            return "-8 | ERR_COM_PORT_IS_OPEN | Communications port is open"
        if code == -9:
            return "-9 | ERR_COM_READ_TIMEOUT | Receive timeout "
        if code == -10:
            return "-10 | ERR_COM_READ_ERROR | Communications port read error"
        if code == -11:
            return "-11 | ERR_COM_WRITE_ERROR | Communications port write error"
        if code == -12:
            return "-12 | ERR_DEVICE_NOT_FOUND | Communications device not found "
        if code == -13:
            return "-13 | ERR_COM_CRC_FAILED | Communications CRC failed"
        if code == -14:
            return "-14 | ERR_DLL_NOT_FOUND | Can not load USB2ANY.dll file"

        if code == -20:
            return "-20 | ERR_INVALID_PORT | Invalid port"
        if code == -21:
            return "-21 | ERR_ADDRESS_OUT_OF_RANGE | Address is out of accepted range"
        if code == -22:
            return "-22 | ERR_INVALID_FUNCTION_CODE | Invalid function code"
        if code == -23:
            return "-23 | ERR_BAD_PACKET_SIZE | Invalid packet size"
        if code == -24:
            return "-24 | ERR_INVALID_HANDLE | Invalid handle"
        if code == -25:
            return "-25 | ERR_OPERATION_FAILED | Operation failed"
        if code == -26:
            return "-26 | ERR_PARAM_OUT_OF_RANGE | Parameter is out of range"
        if code == -27:
            return "-27 | ERR_PACKET_OUT_OF_SEQUENCE | Packet is out of sequence"
        if code == -28:
            return "-28 | ERR_INVALID_PACKET_HEADER | Invalid packet header"
        if code == -29:
            return "-29 | ERR_UNIMPLEMENTED_FUNCTION | Function not implemented"

        if code == -30:
            return "-30 | ERR_TOO_MUCH_DATA | Too much data"
        if code == -31:
            return "-31 | ERR_INVALID_DEVICE | Invalid device "
        if code == -32:
            return "-32 | ERR_UNSUPPORTED_FIRMWARE | Unsupported firmware version"
        if code == -33:
            return "-33 | ERR_BUFFER_TOO_SMALL | Buffer is too small"
        if code == -34:
            return "-34 | ERR_NO_DATA | No data available"
        if code == -35:
            return "-35 | ERR_RESOURCE_CONFLICT | Resource conflict"
        if code == -36:
            return "-36 | ERR_NO_EVM | EVM is required for external power"
        if code == -37:
            return "-37 | ERR_COMMAND_BUSY | Command is busy"
        if code == -38:
            return "-38 | ERR_ADJ_POWER_FAIL | Adjustable power supply failure"
        if code == -39:
            return "-39 | ERR_NOT_ENABLED | Interface or mode is not enabled"

        if code == -40:
            return "-40 | ERR_I2C_INIT_ERROR | I2C initialization failed"
        if code == -41:
            return "-41 | ERR_I2C_READ_ERROR | I2C read error"
        if code == -42:
            return "-42 | ERR_I2C_WRITE_ERROR | I2C write error"
        if code == -43:
            return "-43 | ERR_I2C_BUSY | I2C busy (transfer is pending)"
        if code == -44:
            return "-44 | ERR_I2C_ADDR_NAK | Address not acknowledged (NAK)"
        if code == -45:
            return "-45 | ERR_I2C_DATA_NAK | Data not acknowledged (NAK)"
        if code == -46:
            return "-46 | ERR_I2C_READ_TIMEOUT | Read timeout "
        if code == -47:
            return "-47 | ERR_I2C_READ_DATA_TIMEOUT | Read data timeout"
        if code == -48:
            return "-48 | ERR_I2C_READ_COMP_TIMEOUT | Timeout waiting for read complete"
        if code == -49:
            return "-49 | ERR_I2C_WRITE_TIMEOUT | Write timeout"

        if code == -50:
            return "-50 | ERR_I2C_WRITE_DATA_TIMEOUT | Write data timeout"
        if code == -51:
            return "-51 | ERR_I2C_WRITE_COMP_TIMEOUT | Timeout waiting for write complete"
        if code == -52:
            return "-52 | ERR_I2C_NOT_MASTER | I2C not in Master mode"
        if code == -53:
            return "-53 | ERR_I2C_ARBITRATION_LOST | I2C arbitration lost "
        if code == -54:
            return "-54 | ERR_I2C_NO_PULLUP_POWER | I2C pullups require the 3.3V EXT power to be on"

        if code == -60:
            return "-60 | ERR_SPI_INIT_ERROR | SPI initialization failed"
        if code == -61:
            return "-61 | ERR_SPI_WRITE_READ_ERROR | SPI write/read error"

        if code == -70:
            return "-70 | ERR_DATA_WRITE_ERROR | Data write error"
        if code == -71:
            return "-71 | ERR_DATA_READ_ERROR | Data read error"
        if code == -72:
            return "-72 | ERR_TIMEOUT | Operation timeout"
        if code == -73:
            return "-73 | ERR_DATA_CRC_FAILED | Data CRC failed"

        return code

    def Retry(self, func, func_name: str, expected: str, error: str):
        util.typeCheck("func_name", func_name, str)
        util.typeCheck("expected", expected, str)
        util.typeCheck("error", error, str)

        for i in range(1, 11):
            retryTime = time.time()
            response = func()

            if response == None:
                pass
            elif str(response) == expected:
                return response
            elif ">" in expected and response > int(expected.replace(">", "")):
                return response
            elif "<" in expected and response < int(expected.replace("<", "")):
                return response
            elif "!None" in expected and str(response) != expected.replace("!", ""):
                return response
            elif "!" in expected and response != int(expected.replace("!", "")):
                return response
            elif "$" in expected and response != str(expected.replace("$", "")):
                return response
            elif "," in expected and str(response) in expected.split(","):
                return response

            util.Red(f"Retrying {str(i).zfill(2)}/10: {func_name}, Result: {response}, Expected: {expected}, Error: {error}" , end="\r")

            if i >= 2 and func_name != "dll.u2aI2C_RegisterRead()" and func_name != "dll.u2aIsUSB2ANYConnected()":
                if hasattr(self, "Config_"):
                    self.Config_()
                if hasattr(self, "Activate_"):
                    self.Activate_()

            delta = 2 - (time.time() - retryTime)
            if delta > 0:
                time.sleep(delta)

        raise Exception(util.Red(
            f"\n\n" +
            f"Function: {func_name}\n" +
            f"Return: {response}\n" +
            f"Expected: {expected}\n"
            f"Error: {error}\n",
            ret=True
        ))

if __name__ == "__main__":
    util.setColor()

    dll = USB2ANY()
    util.Green(f"Connected to serialnumber: {dll.serialnumber}")