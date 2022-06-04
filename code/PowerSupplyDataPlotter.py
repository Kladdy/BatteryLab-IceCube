# PowerSupplyDataPlotter.py
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
RUN_ID = "8"
CC_CURRENT = 2 # CC current in A
CC_VOLTAGE = 9*1.5 # CC max voltage in V
MEASURING_TIME = 3 * day # Measuring time in s
MEASURING_INTERVAL = 2 * min # Measuring interval in s
plot_x_in_hours = True # Flag to choose if we are plotting x axis in hours instead of seconds
do_calculate_capacity = True # Flag to choose if we are calculating the capacity

path = f'data/charging/plots/final/RUN_ID-{RUN_ID}'

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
    with open(f'data/charging/PowerSupplyData_RUN_ID-{RUN_ID}_CURRENT-{CC_CURRENT}_VOLTAGE-{CC_VOLTAGE}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.npy', 'rb') as f:
        t_array = np.load(f)
        I_array = np.load(f)
        U_array = np.load(f)
        
    capacity_string_I = ""
    capacity_string_U = ""

    if do_calculate_capacity:
        # Find for which time the current drops below a certain threshold
        # NOTE: The units below assume that plot_x_in_hours = True. Otherwise, change h -> s, Ah -> As in the text (calculations are correct, however)
        current_threshold = 0.5
        current_drop_time = np.where(I_array < current_threshold)[0][0]
        time_at_which_current_dropped = t_array[current_drop_time]

        capacity_string_I = f"Charging - current vs time\nTime until charged: {(time_at_which_current_dropped / time_factor):.1f} h\nCapacity: {(time_at_which_current_dropped * np.average(I_array[0:current_drop_time]) / time_factor):.1f} Ah"
        capacity_string_U = f"Charging - voltage vs time\nTime until charged: {(time_at_which_current_dropped / time_factor):.1f} h"




    # Plot data in linear and log scale
    for yscale in ["linear", "log"]:
        plt.plot(t_array / time_factor, I_array)
        plt.xlabel(x_label)
        plt.ylabel('Current (A)')
        plt.yscale(yscale)
        plt.grid(True, "both")
        plt.title(capacity_string_I)
        plt.tight_layout()
        plt.savefig(f"{path}/CURRENT_{yscale}_PowerSupplyData_RUN_ID-{RUN_ID}_CURRENT-{CC_CURRENT}_VOLTAGE-{CC_VOLTAGE}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.png", dpi=300)
        plt.close()

        plt.plot(t_array / time_factor, U_array)
        plt.xlabel(x_label)
        plt.ylabel('Voltage (V)')
        plt.yscale(yscale)
        plt.grid(True, "both")
        plt.title(capacity_string_U)
        plt.tight_layout()
        plt.savefig(f"{path}/VOLTAGE_{yscale}_PowerSupplyData_RUN_ID-{RUN_ID}_CURRENT-{CC_CURRENT}_VOLTAGE-{CC_VOLTAGE}_TIME-{MEASURING_TIME}_INTERVAL-{MEASURING_INTERVAL}.png", dpi=300)
        plt.close()

if __name__ == "__main__":
    main()