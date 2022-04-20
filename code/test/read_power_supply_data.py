from asyncore import loop
import serial
import serial.rs485
import time

COM_PORT = 3

ser = serial.rs485.RS485(port=f'COM{COM_PORT}',
                baudrate = 9600,
                bytesize=8,
                timeout=3,
                stopbits = serial.STOPBITS_ONE,
                parity = serial.PARITY_NONE)

ser.rs485_mode = serial.rs485.RS485Settings()

if (ser.isOpen() == True):
  ser.close()
ser.open()
ser.reset_input_buffer()

# ser = serial.Serial(f'COM{COM_PORT}')
print("rs485_mode: ", ser.rs485_mode)
print(ser)

# data = bytearray(b'\xfa\x02\x02\x2a\xfe\x0c')
# data = bytearray(b'VSET01?')
# data = "VSETO3?"
ser.write(b'ISET01?')

# while True:
#     mHex = ser.read()
#     if len(mHex)!= 0:
#         print("get",binascii.hexlify(bytearray(mHex)))
#     time.sleep(0.1)

dataIn = ser.readlines()
print([line.decode('utf-8') for line in dataIn])

ser.close()

