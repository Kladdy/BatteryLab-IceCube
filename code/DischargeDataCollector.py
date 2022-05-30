# DischargeDataCollector.py
# AUTHOR: Sigfrid Stjärnholm
# DATE: 2/5 2022

import serial
import time
import numpy as np
from matplotlib import pyplot as plt
from wakepy import keepawake # For keeping the computer turned awake when running

# NOTE: This assumes that the electronic load is connected to COM4. This can be changed in the code below.

# Time units
sec = 1
min = 60 * sec
hour = 60 * min
day = 24 * hour

# Parameters
RUN_ID = "7"
COM_PORT = "COM4"
CW_POWER = 24 # CW power in W
MEASURING_TIME = 3 * day # Measuring time in s
MEASURING_INTERVAL = 2 * min # Measuring interval in s
NUMBER_OF_TIMES_TO_PLOT = 40 # Amount of times to do plotting during the measure interval

# NOTE: Not sure if CC_MAX_CURRENT works, as we are doing CW. 
CC_MAX_CURRENT = 10 # The maximum current to ouput (to prevent current spike in the end)

def byte_to_float(b):
    return float(b.decode())

def byte_to_bool(b):
    return bool(int(b.decode()))

def byte_to_string(b):
    return b.decode()

def encode(s):
    return (s + "\n").encode()

# # Get the set current and convert into a float representation
# def getSetCurrent(ser):
#     ser.write(encode("ISET01?"))
#     return byte_to_float(ser.readline())

# # Get the set voltage and convert into a float representation
# def getSetVoltage(ser):
#     ser.write(encode("VSET01?"))
#     return byte_to_float(ser.readline())

# # Get the set current and convert into a float representation
# def setSetCurrent(ser, current):
#     ser.write(encode("ISET01:" + str(current)))
#     return 

# # Get the set voltage and convert into a float representation
# def setSetVoltage(ser, voltage):
#     ser.write(encode("VSET01:" + str(voltage)))
#     return 

# # Get the output current and convert into a float representation
# def getOutputCurrent(ser):
#     ser.write(encode("IOUT01?"))
#     return byte_to_float(ser.readline())

# # Get the output voltage and convert into a float representation
# def getOutputVoltage(ser):
#     ser.write(encode("VOUT01?"))
#     return byte_to_float(ser.readline())

# Get the on state
def getOnState(ser):
    ser.write(encode(":INPut?"))
    res = byte_to_string(ser.readline()).strip()
    if res == "OFF":
        return False
    else:
        return True

# Set the on state
def setOnState(ser, state):
    if state:
        ser.write(b":INPut ON\n")
    else:
        ser.write(b":INPut OFF\n")

def getCWPower(ser):
    ser.write(encode(f":POW?"))
    return float(byte_to_string(ser.readline()).strip()[:-1]) # strip to remove newline, [:-1] to remove unit

def setCWPower(ser, power):
    ser.write(encode(f":POW {power}W"))
    return ser.readline()

def setCCCurrent(ser, current):
    ser.write(encode(f":CURR {current}W"))
    return ser.readline()

def getMeasureCurrent(ser):
    ser.write(encode(f":MEASure:CURRent?"))
    return float(byte_to_string(ser.readline()).strip()[:-1]) # strip to remove newline, [:-1] to remove unit

def getMeasureVoltage(ser):
    ser.write(encode(f":MEASure:VOLTage?"))
    return float(byte_to_string(ser.readline()).strip()[:-1]) # strip to remove newline, [:-1] to remove unit

def getMeasurePower(ser):
    ser.write(encode(f":MEASure:POWer?"))
    return float(byte_to_string(ser.readline()).strip()[:-1]) # strip to remove newline, [:-1] to remove unit

def setMode(ser, mode):
    raise Exception("setMode NOT WORKING!...")
    ser.write(encode(f":FUNC {mode}"))
    return ser.readline()

def getMode(ser):
    ser.write(encode(f":FUNC?"))
    return byte_to_string(ser.readline()).strip() # .strip() to remove newline (\n)

def test(ser):
    ser.write(encode("*IDN?"))
    return byte_to_string(ser.readline())

def main():
    # Connect to power supply
    ser = serial.Serial(COM_PORT, baudrate=115200, timeout=1)  # open serial port
    print("Connected to electronic load:", test(ser))

    # Check that the mode is CW
    mode = getMode(ser)
    if (mode != "CW"):
        raise Exception(f"The mode is not CW. Set the mode to CW and try again. Mode was '{mode}'")

    # Print details
    print(f"Port: {ser.port}, On: {getOnState(ser)}, Mode: {getMode(ser)}")
    print(f"\t Set CW Power: {getCWPower(ser)} W")
    print(f"\t Out current: {getMeasureCurrent(ser)} A")
    print(f"\t Out voltage: {getMeasureVoltage(ser)} V")
    print(f"\t Out power: {getMeasurePower(ser)} W")

    # Initilize
    print("\nInitializing measurement...")
    setOnState(ser, False)
    setCWPower(ser, CW_POWER)
    setCCCurrent(ser, CC_MAX_CURRENT)
    print("Measurement started!")
    
    try:
        # Use keepawake context to prevent computer from going asleep when we are running
        with keepawake(keep_screen_awake=False):
            pass
            # Turn on and start measuring
            setOnState(ser, True)
            time.sleep(1) # Sleep for 1 second before measurements start
            t_array = np.array([])
            I_array = np.array([])
            U_array = np.array([])
            P_array = np.array([])
            start = time.time()
            has_plotted_amount_of_times = 0
            while time.time() - start < MEASURING_TIME:
                t = time.time() - start
                i = getMeasureCurrent(ser)
                u = getMeasureVoltage(ser)
                p = getMeasurePower(ser)
                t_array = np.append(t_array, t)
                I_array = np.append(I_array, i)
                U_array = np.append(U_array, u)
                P_array = np.append(P_array, p)
                # print(f"Data: u = {u}, i = {i}")

                # Save data
                with open(f'data/discharging/DischargeData_RUN_ID-{RUN_ID}_POWER-{CW_POWER}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.npy', 'wb') as f:
                    np.save(f, t_array)
                    np.save(f, I_array)
                    np.save(f, U_array)
                    np.save(f, P_array)
                
                # Plot data occationally
                try:
                    if t / MEASURING_TIME * NUMBER_OF_TIMES_TO_PLOT > has_plotted_amount_of_times:
                        has_plotted_amount_of_times += 1
                        print(f"Plotting... ({has_plotted_amount_of_times}/{NUMBER_OF_TIMES_TO_PLOT}). Measurement time: {t:.0f}/{MEASURING_TIME} s ({(t/MEASURING_TIME*100):.0f} %)")

                        plt.plot(t_array, I_array)
                        plt.xlabel('Time (s)')
                        plt.ylabel('Current (A)')
                        plt.savefig(f"data/discharging/plots/CURRENT_DischargeData_RUN_ID-{RUN_ID}_POWER-{CW_POWER}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.png")
                        plt.close()

                        plt.plot(t_array, U_array)
                        plt.xlabel('Time (s)')
                        plt.ylabel('Voltage (V)')
                        plt.savefig(f"data/discharging/plots/VOLTAGE_DischargeData_RUN_ID-{RUN_ID}_POWER-{CW_POWER}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.png")
                        plt.close()

                        plt.plot(t_array, P_array)
                        plt.xlabel('Time (s)')
                        plt.ylabel('Power (W)')
                        plt.savefig(f"data/discharging/plots/POWER_DischargeData_RUN_ID-{RUN_ID}_POWER-{CW_POWER}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.png")
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
            plt.savefig(f"data/discharging/plots/CURRENT_DischargeData_RUN_ID-{RUN_ID}_POWER-{CW_POWER}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.png")
            plt.close()

            plt.plot(t_array, U_array)
            plt.xlabel('Time (s)')
            plt.ylabel('Voltage (V)')
            plt.savefig(f"data/discharging/plots/VOLTAGE_DischargeData_RUN_ID-{RUN_ID}_POWER-{CW_POWER}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.png")
            plt.close()

            plt.plot(t_array, P_array)
            plt.xlabel('Time (s)')
            plt.ylabel('Power (W)')
            plt.savefig(f"data/discharging/plots/POWER_DischargeData_RUN_ID-{RUN_ID}_POWER-{CW_POWER}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.png")
            plt.close()

            print("Measurement done!\n")
            
    finally:
        pass
        print("***********************************************************")
        print("Program exiting...")
        if ser.is_open:
            print("Port was open. Turnining off electronic load and closing.")
            setOnState(ser, False)
            time.sleep(1)
            if getOnState(ser):
                raise Exception("THE ELECTRONIC LOAD IS NOT OFF. PROCEED WITH CAUTION!")
            ser.close()             # close port
        else:
            print("Port was not open. Opening port, turnining off electronic load and closing.")
            ser = serial.Serial(COM_PORT, baudrate=115200, timeout=1)  # open serial port
            setOnState(ser, False)
            time.sleep(1)
            if getOnState(ser):
                raise Exception("THE ELECTRONIC LOAD IS NOT OFF. PROCEED WITH CAUTION!")
            ser.close()             # close port
        print("Port has been closed, and electronic load is off. Exiting...")
        print("***********************************************************\n")

if __name__ == "__main__":
    main()