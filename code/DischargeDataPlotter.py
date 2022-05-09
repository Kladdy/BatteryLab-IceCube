# DischargeDataPlotter.py
# AUTHOR: Sigfrid Stjärnholm
# DATE: 2/5 2022

import numpy as np
from matplotlib import pyplot as plt
import os

# Time units
sec = 1
min = 60 * sec
hour = 60 * min
day = 24 * hour

# Parameters
RUN_ID = "2-merged"
CW_POWER = 6 # CW power in W
MEASURING_TIME = 3 * day # Measuring time in s
MEASURING_INTERVAL = 2 * min # Measuring interval in s

path = f'data/discharging/plots/final/RUN_ID-{RUN_ID}'

# Check whether the specified path exists or not
isExist = os.path.exists(path)

if not isExist:
  # Create a new directory because it does not exist 
  os.makedirs(path)
  print(f"The new directory is created! ({path})")

def main():
    # Load data
    with open(f'data/discharging/DischargeData_RUN_ID-{RUN_ID}_POWER-{CW_POWER}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.npy', 'rb') as f:
        t_array = np.load(f)
        I_array = np.load(f)
        U_array = np.load(f)
        P_array = np.load(f)
        

    # Plot data in linear and log scale
    for yscale in ["linear", "log"]:
        plt.plot(t_array, I_array)
        plt.xlabel('Time (s)')
        plt.ylabel('Current (A)')
        plt.yscale(yscale)
        plt.grid(True, "both")
        plt.tight_layout()
        plt.savefig(f"{path}/CURRENT_{yscale}_DischargeData_RUN_ID-{RUN_ID}_POWER-{CW_POWER}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.png")
        plt.close()

        plt.plot(t_array, U_array)
        plt.xlabel('Time (s)')
        plt.ylabel('Voltage (V)')
        plt.yscale(yscale)
        plt.grid(True, "both")
        plt.tight_layout()
        plt.savefig(f"{path}/VOLTAGE_{yscale}_DischargeData_RUN_ID-{RUN_ID}_POWER-{CW_POWER}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.png")
        plt.close()

        plt.plot(t_array, P_array)
        plt.xlabel('Time (s)')
        plt.ylabel('Power (W)')
        plt.yscale(yscale)
        plt.grid(True, "both")
        plt.tight_layout()
        plt.savefig(f"{path}/POWER_{yscale}_DischargeData_RUN_ID-{RUN_ID}_POWER-{CW_POWER}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.png")
        plt.close()

if __name__ == "__main__":
    main()