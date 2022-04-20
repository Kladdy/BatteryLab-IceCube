import serial
import time
import numpy as np
from matplotlib import pyplot as plt

# NOTE: This assumes that the power supply is connected to COM3. This can be changed in the code below.
# NOTE: This assumes that the power supply has RS485 ID 01. This is set by holding down the "VSET" button.

# Parameters:
CC_CURRENT = 1 # CC current in A
CC_VOLTAGE = 20 # CC max voltage in V
MEASURING_TIME = 10 # Measuring time in s
MEASURING_INTERVAL = 0.1 # Measuring interval in s

def byte_to_float(b):
    return float(b.decode())

def byte_to_bool(b):
    return bool(int(b.decode()))

def encode(s):
    return (s + "\n").encode()

# Get the set current and convert into a float representation
def getSetCurrent(ser):
    ser.write(encode("ISET01?"))
    return byte_to_float(ser.readline())

# Get the set voltage and convert into a float representation
def getSetVoltage(ser):
    ser.write(encode("VSET01?"))
    return byte_to_float(ser.readline())

# Get the set current and convert into a float representation
def setSetCurrent(ser, current):
    ser.write(encode("ISET01:" + str(current)))
    return 

# Get the set voltage and convert into a float representation
def setSetVoltage(ser, voltage):
    ser.write(encode("VSET01:" + str(voltage)))
    return 

# Get the output current and convert into a float representation
def getOutputCurrent(ser):
    ser.write(encode("IOUT01?"))
    return byte_to_float(ser.readline())

# Get the output voltage and convert into a float representation
def getOutputVoltage(ser):
    ser.write(encode("VOUT01?"))
    return byte_to_float(ser.readline())

# Get the on state
def getOnState(ser):
    ser.write(encode("OUT01?"))
    return byte_to_bool(ser.readline())

# Set the on state
def setOnState(ser, state):
    if state:
        ser.write(b"OUT01:1\n")
    else:
        ser.write(b"OUT01:0\n")

def main():
    # Connect to power supply
    ser = serial.Serial('COM3', baudrate=115200, timeout=1)  # open serial port

    # Print details
    print(f"Port: {ser.port}, Onstate: {getOnState(ser)}")
    print(f"\t Set: Current: {getSetCurrent(ser)} A, Voltage: {getSetVoltage(ser)}")
    print(f"\t Out: Current: {getOutputCurrent(ser)} A, Voltage: {getOutputVoltage(ser)}")

    # Initilize
    setOnState(ser, False)
    setSetCurrent(ser, CC_CURRENT)
    setSetVoltage(ser, CC_VOLTAGE)
    
    # Turn on and start measuring
    setOnState(ser, True)
    t_array = np.array([])
    I_array = np.array([])
    U_array = np.array([])
    start = time.time()
    while time.time() - start < MEASURING_TIME:
        t = time.time() - start
        i = getOutputCurrent(ser)
        u = getOutputVoltage(ser)
        t_array = np.append(t_array, t)
        I_array = np.append(I_array, i)
        U_array = np.append(U_array, u)
        # print(f"Data: u = {u}, i = {i}")
        time.sleep(MEASURING_INTERVAL)

    setOnState(ser, False)
    ser.close()             # close port

    # Save data
    with open(f'data/PowerSupplyData_CURRENT-{CC_CURRENT}_VOLTAGE-{CC_VOLTAGE}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.npy', 'wb') as f:
        np.save(f, t_array)
        np.save(f, I_array)
        np.save(f, U_array)

    # Plot data
    plt.plot(t_array, I_array)
    plt.xlabel('Time (s)')
    plt.ylabel('Current (A)')
    plt.savefig(f"data/plots/CURRENT_PowerSupplyData_CURRENT-{CC_CURRENT}_VOLTAGE-{CC_VOLTAGE}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.png")
    plt.close()

    plt.plot(t_array, U_array)
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (V)')
    plt.savefig(f"data/plots/VOLTAGE_PowerSupplyData_CURRENT-{CC_CURRENT}_VOLTAGE-{CC_VOLTAGE}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.png")

    



if __name__ == "__main__":
    main()