import serial

ser = serial.Serial('COM3', baudrate=115200, timeout=1)  # open serial port
# ser.rs485_mode = serial.rs485.RS485Settings()
print(ser.name)         # check which port was really used
# ser.write(b'\r\n' + b'ISET01?' + b'\r\n')     # write a string
ser.write(b"ISET01?\n")
# ser.flush()
print(ser.read(100))
ser.close()             # close port