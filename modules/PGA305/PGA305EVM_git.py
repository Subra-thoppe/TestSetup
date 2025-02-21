import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

import time, ctypes
from modules.PGA305.USB2ANY import USB2ANY
from modules import util

INT = ctypes.c_int
CHAR = ctypes.c_char_p
BYTE = ctypes.c_uint8
BYTEX = ctypes.POINTER(BYTE)
INT16 = ctypes.c_int16
UINT16 = ctypes.c_uint16
HANDLE = UINT16

class PGA305EVM(USB2ANY):

    def __init__(self) -> None:
        self.pulseDelay = float(util.config["pulseDelay"]) if "pulseDelay" in util.config else 0.07

        super().__init__(self.Activate, self.Configure)
        self.handle = self.Open()
        self.Configure()

    def Open(self) -> int | Exception:
        """
        This function opens communication with the USB2ANY controller.

        Returns a handle, which must be used for subsequent calls to API functions. The handle is always a positive number (never zero). If an error occurs, a negative error code is returned.
        """

        self.dll.u2aOpen.argtypes = [CHAR]
        self.dll.u2aOpen.restype = INT

        response = self.Retry(lambda: self.dll.u2aOpen(self.serialnumber.encode()), "dll.u2aOpen()", ">0", "Can not open connection to USB2ANY")
        return response

    def Close(self) -> int | Exception:
        """
        This function closes communication with the USB2ANY controller associated with the specified handle.

        Returns zero on success. If an error occurs, a negative error code is returned.
        """

        self.serialnumber = None

        self.dll.u2aOpen.argtypes = [HANDLE]
        self.dll.u2aOpen.restype = INT

        response = self.Retry(lambda: self.dll.u2aClose(self.handle), "dll.u2aClose()", "0", "Can not close connection to USB2ANY")
        return response

    def GetDeviceFirmwareVersions(self) -> int | Exception:
        """
        This function reads the firmware version number of the USB2ANY controller associated with the specified handle.

        Returns version number as a string
        """

        self.dll.u2aFirmwareVersion_Read.argtypes = [HANDLE, BYTEX, INT]
        self.dll.u2aFirmwareVersion_Read.restype = INT

        pBuffer = (BYTE * 4)()
        self.Retry(lambda: self.dll.u2aFirmwareVersion_Read(self.handle, pBuffer, 4), "dll.u2aFirmwareVersion_Read()", "4", "Can not read device firmware version on USB2ANY")
        return str(pBuffer[0]) + "." + str(pBuffer[1]) + "." + str(pBuffer[2]) + "." + str(pBuffer[3])

    def Power_Enable(self, _3V: int, _5V: int) -> int | Exception:
        """
        This function enables/disables the 3.3V, 5.0V, and Adjustable power outputs.

        :_3V = Sets the state of the +3.3V_EXT power output pin. Valid values are:

        | _3V | Enum              |
        | :-  | :-                |
        | 0   | Power_3V3_Disable |
        | 1   | Power_3V3_Enable  |
        | 2   | Power_3V3_Ignore  |

        :_5V = Sets the state of the +5.0V_EXT power output pin. Valid values are:

        | _5V | Enum              |
        | :-  | :-                |
        | 0   | Power_5V0_Disable |
        | 1   | Power_5V0_Enable  |
        | 2   | Power_5V0_Ignore  |

        Returns zero on success. If an error occurs, a negative error code is returned.
        """

        self.dll.u2aPower_Enable.argtypes = [HANDLE, INT, INT, INT]
        self.dll.u2aPower_Enable.restype = INT

        response = self.Retry(lambda: self.dll.u2aPower_Enable(self.handle, _3V, _5V, 2), "dll.u2aPower_Enable()", "0", "Can not enable power on USB2ANY")
        return response

    def Power_Read(self) -> int | Exception:
        """
        This function reads the status of the 3.3V and 5.0V power outputs.

        On success, returns one of the values from the table below. If an error occurs, a negative error code is returned.

        | Return Value | 3.3V Power | 5.0V Power |
        | ------------ | ---------- | ---------- |
        | 0            | OK         | OK         |
        | 1            | FAULT      | OK         |
        | 2            | OK         | FAULT      |
        | 3            | FAULT      | FAULT      |

        Returns zero on success. If an error occurs, a negative error code is returned.
        """

        self.dll.u2aPower_ReadStatus.argtypes = [HANDLE]
        self.dll.u2aPower_ReadStatus.restype = INT

        response = self.Retry(lambda: self.dll.u2aPower_ReadStatus(self.handle), "dll.u2aPower_ReadStatus()", "0", "Can not read power on USB2ANY")
        return response

    def SetReceiveTimeout(self) -> int | Exception:
        """
        This function sets the timeout value, in milliseconds, used during USB receive operations.

        Returns the previous timeout value on success. If an error occurs, the timeout value is not
        changed and one of the following error codes is returned:
        - ERR_PARAM_OUT_OF_RANGE
        - ERR_COM_PORT_NOT_OPEN
        - ERR_OPERATION_FAILED

        Returns zero on success. If an error occurs, a negative error code is returned.
        """

        self.dll.u2aSetReceiveTimeout.argtypes = [INT16]
        self.dll.u2aSetReceiveTimeout.restype = INT

        response = self.Retry(lambda: self.dll.u2aSetReceiveTimeout(500), "dll.u2aSetReceiveTimeout()", "20,500", "Can not set timeout on USB2ANY")
        return response

    def I2C_Control(self, Speed: int, AddressLength: int, PullUps: int) -> int | Exception:
        """
        This function sets the communications parameters (speed, address length, and pullup state) for the I2C interface.

        :Speed: The bitrate for I2C communications. Valid values are:

        | State | Enum       |
        | :-    | :-         |
        | 0     | I2C_100kHz |
        | 1     | I2C_400kHz |
        | 2     | I2C_10kHz  |

        :AddressLength: Size of the I2C slave device address. May be 7 or 10 bits. Valid values are:

        | State | Enum       |
        | :-    | :-         |
        | 0     | I2C_7Bits  |
        | 1     | I2C_10Bits |

        :PullUps: Sets the state of the I2C pullups. May be 0 (off) or 1 (on). Valid values are:

        | State | Enum            |
        | :-    | :-              |
        | 0     | I2C_PullUps_OFF |
        | 1     | I2C_PullUps_ON  |

        Returns zero on success. If an error occurs, a negative error code is returned.
        """

        self.dll.u2aI2C_Control.argtypes = [HANDLE, BYTE, BYTE, BYTE]
        self.dll.u2aI2C_Control.restype = INT

        response = self.Retry(lambda: self.dll.u2aI2C_Control(self.handle, Speed, AddressLength, PullUps), "dll.u2aI2C_Control()", "0", "Can not set I2C control on USB2ANY")
        return response

    def I2C_RegisterRead(self, I2C_Address: int, RegisterAddress: int) -> int | Exception:
        """
        This function reads a single byte from a register of a device on the I2C bus.

        :I2C_Address: The address of the I2C device. May be 7 or 10 bits. See u2aI2C_Control.
        :RegisterAddress: Address of the register in the I2C slave device. Must be a single byte value.

        Returns the value of the byte read on success. If an error occurs, a negative error code is returned.
        """

        self.dll.u2aI2C_RegisterRead.argtypes = [HANDLE, UINT16, BYTE]
        self.dll.u2aI2C_RegisterRead.restype = INT

        if I2C_Address == 64:
            response = self.Retry(lambda: self.dll.u2aI2C_RegisterRead(self.handle, I2C_Address, RegisterAddress), "dll.u2aI2C_RegisterRead()", "-44", "Can not read I2C data")
            return response

        response = self.Retry(lambda: self.dll.u2aI2C_RegisterRead(self.handle, I2C_Address, RegisterAddress), "dll.u2aI2C_RegisterRead()", ">0", "Is PGA305 EVM connected and powered?")
        return response

    def I2C_RegisterWrite(self, I2C_Address: int, RegisterAddress: int, Value: int) -> int | Exception:
        """
        This function writes a single byte to a register of a device on the I2C bus.

        :I2C_Address: The address of the I2C device. May be 7 or 10 bits. See u2aI2C_Control.
        :RegisterAddress: Address of the register in the I2C slave device. Must be a single byte value.
        :Value: The single-byte value to be written to the specified register.

        Returns zero on success. If an error occurs, a negative error code is returned.
        """

        self.dll.u2aI2C_RegisterWrite.argtypes = [HANDLE, UINT16, BYTE, BYTE]
        self.dll.u2aI2C_RegisterWrite.restype = INT

        response = self.Retry(lambda: self.dll.u2aI2C_RegisterWrite(self.handle, I2C_Address, RegisterAddress, Value), "dll.u2aI2C_RegisterWrite()", "0", "Can not write I2C data")
        return response

    def UART_Control(self, BaudRate: int, Parity: int, BitDirection: int, CharacterLength: int, StopBits: int) -> int | Exception:
        """
        This function sets the USART parameters for serial communication.

        :BaudRate: Sets the baud rate for the USART transmitter and receiver:

        | State  | Enum             |
        | :-     | :-               |
        | 0      | UART_9600_bps    |
        | 1      | UART_19200_bps   |
        | 2      | UART_38400_bps   |
        | 3      | UART_57600_bps   |
        | 4      | UART_115200_bps  |
        | 5      | UART_230400_bps  |
        | 6      | UART_300_bps     |
        | 7      | UART_320_bps     |
        | 8      | UART_600_bps     |
        | 9      | UART_1200_bps    |
        | 10     | UART_2400_bps    |
        | 11     | UART_4800_bps    |

        :Parity: Sets the parity encoding/decoding

        | State | Enum       |
        | :-    | :-         |
        | 0     | UART_None  |
        | 1     | UART_Even  |
        | 2     | UART_Odd   |

        :BitDirection: Defines which bit of each byte is sent first:

        | State | Enum           |
        | :-    | :-             |
        | 0     | UART_LSB_First |
        | 1     | UART_MSB_First |

        :CharacterLength: Sets the number of data bits in each character:

        | State | Enum       |
        | :-    | :-         |
        | 0     | UART_8_Bit |
        | 1     | UART_7_Bit |

        :StopBits: Sets the number of stop bits:

        | State | Enum          |
        | :-    | :-            |
        | 0     | UART_One_Stop |
        | 1     | UART_Two_Stop |

        Returns zero on success. If an error occurs, a negative error code is returned.
        """

        self.dll.u2aUART_Control.argtypes = [HANDLE, UINT16, UINT16, UINT16, UINT16, UINT16]
        self.dll.u2aUART_Control.restype = INT

        response = self.Retry(lambda: self.dll.u2aUART_Control(self.handle, BaudRate, Parity, BitDirection, CharacterLength, StopBits), "dll.u2aUART_Control()", "0", "Can not set UART control on USB2ANY")
        return response

    def UART_SetMode(self) -> int | Exception:
        """
        This is used to allow the UART functions to operate in special modes.

        Returns zero on success. If an error occurs, a negative error code is returned.
        """

        self.dll.u2aUART_SetMode.argtypes = [HANDLE, UINT16]
        self.dll.u2aUART_SetMode.restype = INT

        response = self.Retry(lambda: self.dll.u2aUART_SetMode(self.handle, 2), "dll.u2aUART_SetMode()", "0", "Can not set UART mode on USB2ANY")
        return response

    def UART_Write(self, Data: list) -> int | Exception:
        """
        This function writes serial data via the USART.

        :Data: Data to be written

        Returns zero on success. If an error occurs, a negative error code is returned.
        """

        self.dll.u2aUART_Write.argtypes = [HANDLE, BYTE, BYTEX]
        self.dll.u2aUART_Write.restype = INT

        Data_array = (BYTE * len(Data))(*Data)

        response = self.Retry(lambda: self.dll.u2aUART_Write(self.handle, len(Data), Data_array), "dll.u2aUART_Write()", "0", "Can not write UART data to USB2ANY")
        return response

    def UART_Read(self, count: int) -> str | int | Exception:
        """
        This function reads serial data via the USART.

        :count = Number of bytes to read

        On success, returns the number of bytes read. If an error occurs, a negative error code is returned.
        """

        self.dll.u2aUART_Read.argtypes = [HANDLE, BYTE, BYTEX]
        self.dll.u2aUART_Read.restype = INT

        if count != 0:
            data_array = (BYTE * count)()
            self.Retry(lambda: self.dll.u2aUART_Read(self.handle, count, data_array), "dll.u2aUART_Read()", ">-1", "Can not read UART data from USB2ANY")
            return data_array[0]
        else:
            return None

    def UART_GetRxCount(self) -> int | Exception:
        """
        This function checks the receive queue for data received by the UART and returns the number of data bytes that are currently available to be read.

        On success, returns the number of bytes available to be read (possibly zero). If an error occurs, a negative error code is returned.
        """

        self.dll.u2aUART_GetRxCount.argtypes = [HANDLE]
        self.dll.u2aUART_GetRxCount.restype = INT

        response = self.Retry(lambda: self.dll.u2aUART_GetRxCount(self.handle), "dll.u2aUART_GetRxCount()", ">-1", "Can not read UART count on USB2ANY")
        return response

    def GPIO_WriteControl(self, GPIO0 = 0, GPIO1 = 0, GPIO2 = 0, GPIO3 = 0, GPIO4 = 0, GPIO5 = 0, GPIO6 = 0, GPIO7 = 0, GPIO8 = 0, GPIO9 = 0, GPIO10 = 0, GPIO11 = 0, GPIO12 = 0) -> int | Exception:
        """
        This function writes control data to all of the GPIO pins, simultaneously.

        :GPIO0 - GPIO12: Set the function of the GPIO pin from the table below

        | State | Enum                   | Description                                     |
        | :-    | :-                     | :-                                              |
        | 0     | GPIO_No_Change         | The pin's function is not changed.              |
        | 1     | GPIO_Output            | Sets pin as an output.                          |
        | 2     | GPIO_Input_No_Resistor | Sets pin as a floating input with no resistor.  |
        | 3     | GPIO_Input_Pull_Up     | Sets pin as an input with a pull-up resistor.   |
        | 4     | GPIO_Input_Pull_Down   | Sets pin as an input with a pull-down resistor. |

        Returns zero on success. If an error occurs, a negative error code is returned.
        """

        self.dll.u2aGPIO_WriteControl.argtypes = [HANDLE, BYTE, BYTE, BYTE, BYTE, BYTE, BYTE, BYTE, BYTE, BYTE, BYTE, BYTE, BYTE, BYTE, BYTE, BYTE, BYTE]
        self.dll.u2aGPIO_WriteControl.restype = INT

        GPIO_functions = [GPIO0, GPIO1, GPIO2, GPIO3, GPIO4, GPIO5, GPIO6, GPIO7, GPIO8, GPIO9, GPIO10, GPIO11, GPIO12, 0, 0, 0]
        GPIO_functions_array = (BYTE * len(GPIO_functions))(*GPIO_functions)

        response = self.Retry(lambda: self.dll.u2aGPIO_WriteControl(self.handle, *GPIO_functions_array), "dll.u2aGPIO_WriteControl()", "0", "Can not set GPIO control on USB2ANY")
        return response

    def GPIO_WriteState(self, GPIO0 = 0, GPIO1 = 0, GPIO2 = 0, GPIO3 = 0, GPIO4 = 0, GPIO5 = 0, GPIO6 = 0, GPIO7 = 0, GPIO8 = 0, GPIO9 = 0, GPIO10 = 0, GPIO11 = 0, GPIO12 = 0) -> int | Exception:
        """
        This function sets the output state of all GPIO pins, simultaneously.

        :GPIO0 - GPIO12: Set the output state of the GPIO pin from table below

        | State | Enum               | Description                        |
        | :-    | :-                 | :-                                 |
        | 0     | GPIO_Out_No_Change | The pin's output is not changed.   |
        | 1     | GPIO_Out_Low       | Sets pin's output to a low state.  |
        | 2     | GPIO_Out_High      | Sets pin's output to a high state. |

        Returns zero on success. If an error occurs, a negative error code is returned.
        """

        self.dll.u2aGPIO_WriteState.argtypes = [HANDLE, BYTE, BYTE, BYTE, BYTE, BYTE, BYTE, BYTE, BYTE, BYTE, BYTE, BYTE, BYTE, BYTE, BYTE, BYTE, BYTE]
        self.dll.u2aGPIO_WriteState.restype = INT

        GPIO_states  = [GPIO0, GPIO1, GPIO2, GPIO3, GPIO4, GPIO5, GPIO6, GPIO7, GPIO8, GPIO9, GPIO10, GPIO11, GPIO12, 0, 0, 0]
        GPIO_states_array = (BYTE * len(GPIO_states))(*GPIO_states)

        response = self.Retry(lambda: self.dll.u2aGPIO_WriteState(self.handle, *GPIO_states_array), "dll.u2aGPIO_WriteState()", "0", "Can not write GPIO state on USB2ANY")
        return response

    def GPIO_WritePulse(self, GPIO_Port: int, polarity: int, duration: int) -> int | Exception:
        """
        This function outputs a single pulse on a specified GPIO output pin. The pulse can be either “high” or “low” with a width of 5 to 65535 microseconds

        :GPIO_Port: The GPIO port to be used for output. Must be in the range 0 - 12
        :polarity: The polarity of the pulse: 0 = low pulse, 1 = high pulse.
        :duration: The desired pulse width, in microseconds. Must be at least 5 microseconds. May be set to zero to initialize the output state, without producing a pulse.

        Returns zero on success, or a negative error code on failure. Returns the error code ERR_INVALID_CONFIGURATION if the specified pin is not valid, or the specified pulse width is less than 5 microseconds.
        """

        self.dll.u2aGPIO_WritePulse.argtypes = [HANDLE, BYTE, BYTE, UINT16]
        self.dll.u2aGPIO_WritePulse.restype = INT

        response = self.Retry(lambda: self.dll.u2aGPIO_WritePulse(self.handle, GPIO_Port, polarity, duration), "dll.u2aGPIO_WritePulse()", "0", "Can not write GPIO pulse on USB2ANY")
        return response

    def GPIO_WritePort(self, GPIO_Port: int, state: int) -> int | Exception:
        """
        This function sets the state of a single GPIO output pin.

        :GPIO_Port: The GPIO port to be configured. Must be in the range 0 - 12.
        :state: A state constant from the table below.

        | State | Enum      | Description                        |
        | :-    | :-        | :-                                 |
        | 0     | No_Change | The pin's output is not changed.   |
        | 1     | Low       | Sets pin's output to a low state.  |
        | 2     | High      | Sets pin's output to a high state. |

        Returns zero on success, or a negative error code on failure. Returns ERR_INVALID_CONFIGURATION if the specified pin is not configured as an output.
        """

        self.dll.u2aGPIO_WritePort.argtypes = [HANDLE, BYTE, BYTE]
        self.dll.u2aGPIO_WritePort.restype = INT

        response = self.Retry(lambda: self.dll.u2aGPIO_WritePort(self.handle, GPIO_Port, state), "dll.u2aGPIO_WritePort()", "0", "Can not write GPIO port on USB2ANY")
        return response

    def GPIO_SetPort(self, GPIO_Port: int, function_code: int) -> int | Exception:
        """
        This function configures a single GPIO pin as an output or input (with resistor options).

        :GPIO_Port: The GPIO port to be configured. Must be in the range 0 - 12.
        :function_code: A function code from the table below.

        | State | Enum                   | Description                                     |
        | :-    | :-                     | :-                                              |
        | 0     | GPIO_No_Change         | The pin's function is not changed.              |
        | 1     | GPIO_Output            | Sets pin as an output.                          |
        | 2     | GPIO_Input_No_Resistor | Sets pin as a floating input with no resistor.  |
        | 3     | GPIO_Input_Pull_Up     | Sets pin as an input with a pull-up resistor.   |
        | 4     | GPIO_Input_Pull_Down   | Sets pin as an input with a pull-down resistor. |

        Returns zero on success. If an error occurs, a negative error code is returned.
        """

        self.dll.u2aGPIO_SetPort.argtypes = [HANDLE, BYTE, BYTE]
        self.dll.u2aGPIO_SetPort.restype = INT

        response = self.Retry(lambda: self.dll.u2aGPIO_SetPort(self.handle, GPIO_Port, function_code), "dll.u2aGPIO_SetPort()", "0", "Can not set GPIO port on USB2ANY")
        return response

    def Configure(self) -> None:
        """
        This function will configure USB2ANY and PGA305 EVM card to allow communication with PGA305 IC.
        """

        self.GetDeviceFirmwareVersions()
        self.Power_Enable(1, 1)
        self.Power_Read()
        self.I2C_Control(0, 0, 1)

        self.GPIO_WriteControl(0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0)
        self.GPIO_WriteState(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        self.I2C_RegisterRead(0x2D, 0x00)
        self.I2C_RegisterRead(0x40, 0x0C)

        self.I2C_RegisterWrite(0x2D, 0x00, 0x19)
        self.I2C_RegisterWrite(0x57, 0x00, 0x00)
        self.I2C_RegisterRead(0x57, 0x10)
        self.I2C_RegisterRead(0x57, 0x10)
        self.I2C_RegisterRead(0x57, 0x10)
        self.I2C_RegisterRead(0x57, 0x10)
        self.I2C_RegisterRead(0x57, 0x10)
        self.I2C_RegisterWrite(0x57, 0x01, 0x00)

        self.SetAdditionalVoltage(0)
        self.SetRloop(10)

        self.UART_Control(11, 0, 0, 0, 1)
        self.UART_SetMode()
        self.SetReceiveTimeout()

        self.GPIO_WriteControl(0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0)
        self.GPIO_WriteState(0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0)

    def SetAdditionalVoltage(self, volt: float | int) -> int:
        """
        This function can be used to set additional voltage

        :serial_number = Specify the serial number of the USB2ANY device you want to set the additional voltage on
        :volt = voltage values between 0v and 2.618v

        Returns voltage value or raises exception
        """

        x = volt + 5.13
        y = 4.43795418879017000000E+00*x**6 - 1.65885529511077000000E+02*x**5 + 2.58174908147055000000E+03*x**4 - 2.14058283528947000000E+04*x**3 + 9.96962072909720000000E+04*x**2 - 2.47248981250184000000E+05*x + 2.55025843590454000000E+05
        data = int(y)

        self.I2C_Control(0, 0, 1)
        self.Power_Enable(1, 1)
        self.Power_Read()
        self.I2C_RegisterWrite(0x57, 0x00, data)
        self.I2C_RegisterRead(0x57, 0x10)
        self.I2C_RegisterRead(0x57, 0x10)
        self.I2C_RegisterRead(0x57, 0x10)
        self.I2C_RegisterWrite(0x57, 0x01, data)
        return volt

    def SetRloop(self, ohm: int) -> int:
        """
        This function will set Rloop value on the EVM board.

        :serial_number = Specify the serial number of the USB2ANY device you want to set the Rloop on
        :ohm = ohm values between 0Ω and 210Ω

        Returns a status message or list of status messages
        """

        x = ohm
        if x == 0:
            y = 19
        else:
            y = 0.00000000000118820306*x**6 - 0.00000000033785361986*x**5 - 0.00000003359927530644*x**4 + 0.0000195302737111547*x**3 - 0.00212384864744308*x**2 + 0.689563723710307*x + 23.4479077063734

        data = round(y)

        self.I2C_Control(0, 0, 1)
        self.Power_Enable(1, 1)
        self.Power_Read()
        self.I2C_RegisterWrite(0x2D, 0x00, data)
        return ohm

    def Pulse(self) -> list:
        """
        This function will create the pulse necessary to activate OWI mode on PGA305

        Returns the response code
        """

        for i in range(10):
            self.GPIO_WriteState(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0)

            pulseTime = time.time()
            self.GPIO_WritePulse(7, 1, 10000)
            self.GPIO_WritePulse(7, 1, 10000)
            self.GPIO_WritePulse(7, 1, 10000)
            time.sleep(self.pulseDelay)
            self.GPIO_WritePulse(7, 1, 10000)
            self.GPIO_WritePulse(7, 1, 10000)
            self.GPIO_WritePulse(7, 1, 10000)
            pulse = int((time.time() - pulseTime) * 1000)

            self.GPIO_WriteState(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0)

            if pulse > 160 and pulse < 270:
                break

            util.Red(f"Retrying {i+1}/10:", f"pulse: {pulse} | 160 < pulse < 270")
            time.sleep(1)

        return 3

    def Activate(self) -> list:
        """
        This function will activate OWI mode on PGA305 by sending activating pulse

        Returns the response code
        """

        self.Configure()
        response = self.Retry(lambda: self.Pulse(), "Pulse()", ">2", "Can not activate OWI on PGA305, is it connected and powered?")
        return response

    def _ReadPadc(self):
        for _ in range(100):
            self.UART_Read(self.UART_GetRxCount())
            self.UART_Write([0x55, 0x22, 0x22, 0x55, 0x73])
            B1 = self.UART_Read(1)
            self.UART_Read(self.UART_GetRxCount())
            if B1 == None: continue

            self.UART_Read(self.UART_GetRxCount())
            self.UART_Write([0x55, 0x22, 0x21, 0x55, 0x73])
            B2 = self.UART_Read(1)
            self.UART_Read(self.UART_GetRxCount())
            if B2 == None: continue

            self.UART_Read(self.UART_GetRxCount())
            self.UART_Write([0x55, 0x22, 0x20, 0x55, 0x73])
            B3 = self.UART_Read(1)
            self.UART_Read(self.UART_GetRxCount())
            if B3 == None: continue

            return "".join(map(lambda b: hex(b).replace("0x", "").upper().zfill(2), [B1, B2, B3]))
        return None

    def _ReadTadc(self):
        for _ in range(100):
            self.UART_Read(self.UART_GetRxCount())
            self.UART_Write([0x55, 0x22, 0x26, 0x55, 0x73])
            B1 = self.UART_Read(1)
            self.UART_Read(self.UART_GetRxCount())
            if B1 == None: continue

            self.UART_Read(self.UART_GetRxCount())
            self.UART_Write([0x55, 0x22, 0x25, 0x55, 0x73])
            B2 = self.UART_Read(1)
            self.UART_Read(self.UART_GetRxCount())
            if B2 == None: continue

            self.UART_Read(self.UART_GetRxCount())
            self.UART_Write([0x55, 0x22, 0x24, 0x55, 0x73])
            B3 = self.UART_Read(1)
            self.UART_Read(self.UART_GetRxCount())
            if B3 == None: continue

            return "".join(map(lambda b: hex(b).replace("0x", "").upper().zfill(2), [B1, B2, B3]))
        return None

    def _ReadEEPROM(self, index: int):
        for _ in range(100):
            self.UART_Read(self.UART_GetRxCount())
            self.UART_Write([0x55, 0x52, index, 0x55, 0x73])
            Read1 = self.UART_Read(1)
            self.UART_Read(self.UART_GetRxCount())
            if Read1 == None: continue

            self.UART_Read(self.UART_GetRxCount())
            self.UART_Write([0x55, 0x52, index, 0x55, 0x73])
            Read2 = self.UART_Read(1)
            self.UART_Read(self.UART_GetRxCount())
            if Read2 == None: continue

            if Read1 == Read2:
                return Read2

        return None

    def ReadEEPROM(self, location: tuple | list, type_ = "hex", print = None):
        if not isinstance(location, list):
            location = [location]

        response = []
        for i, d in enumerate(location):
            if print:
                util.White(print, f"{i+1}/{len(location)}", end="\r")

            index = d[0] * 8 + d[1]
            Read = self.Retry(lambda: self._ReadEEPROM(index), "_ReadEEPROM()", "!None", "Can not read data, is PGA305 connected and powered?")

            if type_ == "int":
                response.append(Read)
            elif type_ == "hex":
                response.append(hex(Read).replace("0x", "").zfill(2).upper())

        return response

    def WriteEEPROM(self, page: int, data: list, verify=True):
        """
        This function will write data to PGA305 EEPROM
        """

        if len(data) != 8:
            util.errorCheck("PageLengthError", "data", str(data))

        locations = [(page, i) for i in range(8)]

        for ii in range(10):
            prevData = self.ReadEEPROM(locations, type_="int")

            for i in range(len(data)):
                if data[i] == None:
                    data[i] = prevData[i]

            self.UART_Write([0x55, 0x51, 0x88, page])
            self.UART_Write([0x55, 0xD0, *data])
            self.UART_Write([0x55, 0x51, 0x89, 0x04])

            readData = self.ReadEEPROM(locations, type_="int")

            if not verify:
                return readData

            if data == readData:
                return readData

            util.Red(f"Writing data on page {page}, attempt: {ii+1}/10")
            time.sleep(1)
            self.Activate()

        raise ConnectionError(util.Red(f"Writing data to EEPROM failed", ret=True))

    def WriteControl(self, location: int | list, data: int | list):
        if not isinstance(location, list):
            location = [location]

        if not isinstance(data, list):
            data = [data]

        for l, d in zip(location, data):
            self.UART_Write([0x55, 0x21, l, d])

        return "OK"

    def __repr__(self) -> str:
        return f"Connected to USB2ANY: {self.serialnumber}"

if __name__ == "__main__":
    util.setColor()

    pga = PGA305EVM()
    pga.Activate()
    util.Green(pga)
    util.Cyan(f"Device firmware version: {pga.GetDeviceFirmwareVersions()}")
    while True:
        util.Cyan(f"Serialnumber: {''.join(pga.ReadEEPROM([(12, 7), (12, 6), (12, 5), (12, 4)]))}")