# PowerSupplyDataPlotter.py
# AUTHOR: Sigfrid Stjärnholm
# DATE: 2/5 2022

import numpy as np
from matplotlib import pyplot as plt

# Time units
sec = 1
min = 60 * sec
hour = 60 * min
day = 24 * hour

# Parameters
RUN_ID = "1"
CC_CURRENT = 2 # CC current in A
CC_VOLTAGE = 9*1.50 # CC max voltage in V
MEASURING_TIME = 20 * hour # Measuring time in s
MEASURING_INTERVAL = 2 * min # Measuring interval in s
NUMBER_OF_TIMES_TO_PLOT = 10 # Amount of times to do plotting during the measure interval

def main():
    # Load data
    with open(f'data/charging/PowerSupplyData_RUN_ID-{RUN_ID}_CURRENT-{CC_CURRENT}_VOLTAGE-{CC_VOLTAGE}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.npy', 'rb') as f:
        t_array = np.load(f)
        I_array = np.load(f)
        U_array = np.load(f)
        

    # Plot data in linear and log scale
    for yscale in ["linear", "log"]:
        plt.plot(t_array, I_array)
        plt.xlabel('Time (s)')
        plt.ylabel('Current (A)')
        plt.yscale(yscale)
        plt.grid(True, "both")
        plt.tight_layout()
        plt.savefig(f"data/charging/plots/final/CURRENT_{yscale}_PowerSupplyData_RUN_ID-{RUN_ID}_CURRENT-{CC_CURRENT}_VOLTAGE-{CC_VOLTAGE}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.png")
        plt.close()

        plt.plot(t_array, U_array)
        plt.xlabel('Time (s)')
        plt.ylabel('Voltage (V)')
        plt.yscale(yscale)
        plt.grid(True, "both")
        plt.tight_layout()
        plt.savefig(f"data/charging/plots/final/VOLTAGE_{yscale}_PowerSupplyData_RUN_ID-{RUN_ID}_CURRENT-{CC_CURRENT}_VOLTAGE-{CC_VOLTAGE}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.png")
        plt.close()

if __name__ == "__main__":
    main()