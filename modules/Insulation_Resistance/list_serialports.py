
import serial
import serial.tools.list_ports as port_list
ports = list(port_list.comports())
for p in ports:
    print (p)


    

# Configure the serial port settings
ser = serial.Serial(
    #port='/dev/ttyUSB0',  # Adjust the port name as needed
    port ='COM7',
    baudrate=9600,
    timeout=1
)

# Send a command to the TOS7200
ser.write(b'*IDN?\n')  # Example: Query instrument identity
#ser.write(b'MON?\n')  # Example: Query instrument identity
#response = ser.readline().decode('utf-8', 'ignore').strip()
response = ser.readline().decode('ascii', 'ignore')
print(f"Response from TOS7200: {response}")

# Close the serial port
ser.close()



 