# PowerSupplyDataCollector.py
# AUTHOR: Sigfrid Stjärnholm
# DATE: 2/5 2022

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
hour = 60 * min
day = 24 * hour

# Parameters
RUN_ID = "2"
COM_PORT = "COM3"
CC_CURRENT = 2 # CC current in A
CC_VOLTAGE = 9*1.50 # CC max voltage in V
MEASURING_TIME = 20 * hour # Measuring time in s
MEASURING_INTERVAL = 2 * min # Measuring interval in s
NUMBER_OF_TIMES_TO_PLOT = 10 # Amount of times to do plotting during the measure interval

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
    ser = serial.Serial(COM_PORT, baudrate=115200, timeout=1)  # open serial port

    # Print details
    print(f"Port: {ser.port}, Onstate: {getOnState(ser)}")
    print(f"\t Set: Current: {getSetCurrent(ser)} A, Voltage: {getSetVoltage(ser)}")
    print(f"\t Out: Current: {getOutputCurrent(ser)} A, Voltage: {getOutputVoltage(ser)}")

    # Initilize
    print("\nInitializing measurement...")
    setOnState(ser, False)
    setSetCurrent(ser, CC_CURRENT)
    setSetVoltage(ser, CC_VOLTAGE)
    print("Measurement started!")
    
    try:
        # Use keepawake context to prevent computer from going asleep when we are running
        with keepawake(keep_screen_awake=False):
            # Turn on and start measuring
            setOnState(ser, True)
            time.sleep(1) # Sleep for 1 second before measurements start
            t_array = np.array([])
            I_array = np.array([])
            U_array = np.array([])
            start = time.time()
            has_plotted_amount_of_times = 0
            while time.time() - start < MEASURING_TIME:
                t = time.time() - start
                i = getOutputCurrent(ser)
                u = getOutputVoltage(ser)
                t_array = np.append(t_array, t)
                I_array = np.append(I_array, i)
                U_array = np.append(U_array, u)
                # print(f"Data: u = {u}, i = {i}")

                # Save data
                with open(f'data/charging/PowerSupplyData_RUN_ID-{RUN_ID}_CURRENT-{CC_CURRENT}_VOLTAGE-{CC_VOLTAGE}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.npy', 'wb') as f:
                    np.save(f, t_array)
                    np.save(f, I_array)
                    np.save(f, U_array)
                
                # Plot data occationally
                try:
                    if t / MEASURING_TIME * NUMBER_OF_TIMES_TO_PLOT > has_plotted_amount_of_times:
                        has_plotted_amount_of_times += 1
                        print(f"Plotting... ({has_plotted_amount_of_times}/{NUMBER_OF_TIMES_TO_PLOT}). Measurement time: {t:.0f}/{MEASURING_TIME} s ({(t/MEASURING_TIME*100):.0f} %)")

                        plt.plot(t_array, I_array)
                        plt.xlabel('Time (s)')
                        plt.ylabel('Current (A)')
                        plt.savefig(f"data/charging/plots/CURRENT_PowerSupplyData_RUN_ID-{RUN_ID}_CURRENT-{CC_CURRENT}_VOLTAGE-{CC_VOLTAGE}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.png")
                        plt.close()

                        plt.plot(t_array, U_array)
                        plt.xlabel('Time (s)')
                        plt.ylabel('Voltage (V)')
                        plt.savefig(f"data/charging/plots/VOLTAGE_PowerSupplyData_RUN_ID-{RUN_ID}_CURRENT-{CC_CURRENT}_VOLTAGE-{CC_VOLTAGE}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.png")
                        plt.close()
                except: 
                    print("Error occureted when plotting. Continuing...")

                time.sleep(MEASURING_INTERVAL)

            # Turn off power supply
            setOnState(ser, False)

            # Plot one last time
            plt.plot(t_array, I_array)
            plt.xlabel('Time (s)')
            plt.ylabel('Current (A)')
            plt.savefig(f"data/charging/plots/CURRENT_PowerSupplyData_RUN_ID-{RUN_ID}_CURRENT-{CC_CURRENT}_VOLTAGE-{CC_VOLTAGE}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.png")
            plt.close()

            plt.plot(t_array, U_array)
            plt.xlabel('Time (s)')
            plt.ylabel('Voltage (V)')
            plt.savefig(f"data/charging/plots/VOLTAGE_PowerSupplyData_RUN_ID-{RUN_ID}_CURRENT-{CC_CURRENT}_VOLTAGE-{CC_VOLTAGE}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.png")
            plt.close()

            print("Measurement done!\n")
            
    finally:
        print("***********************************************************")
        print("Program exiting...")
        if ser.is_open:
            print("Port was open. Turnining off power supply and closing.")
            setOnState(ser, False)
            time.sleep(1)
            if getOnState(ser):
                raise Exception("THE POWER SUPPLY IS NOT OFF. PROCEED WITH CAUTION!")
            ser.close()             # close port
        else:
            print("Port was not open. Opening port, turnining off power supply and closing.")
            ser = serial.Serial(COM_PORT, baudrate=115200, timeout=1)  # open serial port
            setOnState(ser, False)
            time.sleep(1)
            if getOnState(ser):
                raise Exception("THE POWER SUPPLY IS NOT OFF. PROCEED WITH CAUTION!")
            ser.close()             # close port
        print("Port has been closed, and power supply is off. Exiting...")
        print("***********************************************************\n")

if __name__ == "__main__":
    main()