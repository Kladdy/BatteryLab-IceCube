import serial
import time
import numpy as np
from matplotlib import pyplot as plt
from wakepy import keepawake # For keeping the computer turned awake when running

# NOTE: This assumes that the power supply is connected to COM3. This can be changed in the code below.
# NOTE: This assumes that the power supply has RS485 ID 01. This is set by holding down the "VSET" button.

# Time units
sec = 1
min = 60 * sec
h = 60 * min
d = 24 * h

# Parameters
RUN_ID = "1"
CC_CURRENT = 2 # CC current in A
CC_VOLTAGE = 20 # CC max voltage in V
MEASURING_TIME = 4 * h # Measuring time in s
MEASURING_INTERVAL = 10 * sec # Measuring interval in s

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
    
    # Use keepawake context to prevent computer from going asleep when we are running
    with keepawake(keep_screen_awake=False):
        # Turn on and start measuring
        setOnState(ser, True)
        time.sleep(1) # Sleep for 1 second before measurements start
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

            # Save data
            with open(f'data/PowerSupplyData_RUN_ID-{RUN_ID}_CURRENT-{CC_CURRENT}_VOLTAGE-{CC_VOLTAGE}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.npy', 'wb') as f:
                np.save(f, t_array)
                np.save(f, I_array)
                np.save(f, U_array)

            time.sleep(MEASURING_INTERVAL)

        # Plot data
        plt.plot(t_array, I_array)
        plt.xlabel('Time (s)')
        plt.ylabel('Current (A)')
        plt.savefig(f"data/plots/CURRENT_PowerSupplyData_RUN_ID-{RUN_ID}_CURRENT-{CC_CURRENT}_VOLTAGE-{CC_VOLTAGE}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.png")
        plt.close()

        plt.plot(t_array, U_array)
        plt.xlabel('Time (s)')
        plt.ylabel('Voltage (V)')
        plt.savefig(f"data/plots/VOLTAGE_PowerSupplyData_RUN_ID-{RUN_ID}_CURRENT-{CC_CURRENT}_VOLTAGE-{CC_VOLTAGE}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.png")
        plt.close()

        setOnState(ser, False)
        ser.close()             # close port


if __name__ == "__main__":
    main()