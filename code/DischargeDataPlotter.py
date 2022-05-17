# DischargeDataPlotter.py
# AUTHOR: Sigfrid Stjärnholm
# DATE: 2/5 2022

import numpy as np
from matplotlib import pyplot as plt
import os

# Plot params
plt.rc('figure', figsize=(4, 3))

# Time units
sec = 1
min = 60 * sec
hour = 60 * min
day = 24 * hour

# Parameters
RUN_ID = "4"
CW_POWER = 24 # CW power in W
MEASURING_TIME = 5 * day # Measuring time in s
MEASURING_INTERVAL = 2 * min # Measuring interval in s
plot_x_in_hours = True # Flag to choose if we are plotting x axis in hours instead of seconds

path = f'data/discharging/plots/final/RUN_ID-{RUN_ID}'

if plot_x_in_hours:
    x_label = "Time (h)"
    time_factor = 3600
else:
    x_label = "Time (s)"
    time_factor = 1

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
        plt.plot(t_array / time_factor, I_array)
        plt.xlabel(x_label)
        plt.ylabel('Current (A)')
        plt.yscale(yscale)
        plt.grid(True, "both")
        if yscale != "log": plt.gca().get_yaxis().get_major_formatter().set_useOffset(False) # Prevent y-axis from having an offset in tickers
        plt.tight_layout()
        plt.savefig(f"{path}/CURRENT_{yscale}_DischargeData_RUN_ID-{RUN_ID}_POWER-{CW_POWER}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.png", dpi=300)
        plt.close()

        plt.plot(t_array / time_factor, U_array)
        plt.xlabel(x_label)
        plt.ylabel('Voltage (V)')
        plt.yscale(yscale)
        plt.grid(True, "both")
        if yscale != "log": plt.gca().get_yaxis().get_major_formatter().set_useOffset(False) # Prevent y-axis from having an offset in tickers
        plt.tight_layout()
        plt.savefig(f"{path}/VOLTAGE_{yscale}_DischargeData_RUN_ID-{RUN_ID}_POWER-{CW_POWER}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.png", dpi=300)
        plt.close()

        plt.plot(t_array / time_factor, P_array)
        plt.xlabel(x_label)
        plt.ylabel('Power (W)')
        plt.yscale(yscale)
        plt.grid(True, "both")
        if yscale != "log": plt.gca().get_yaxis().get_major_formatter().set_useOffset(False) # Prevent y-axis from having an offset in tickers
        plt.tight_layout()
        plt.savefig(f"{path}/POWER_{yscale}_DischargeData_RUN_ID-{RUN_ID}_POWER-{CW_POWER}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.png", dpi=300)
        plt.close()

if __name__ == "__main__":
    main()