# DischargeDataMerger.py
# AUTHOR: Sigfrid Stjärnholm
# DATE: 9/5 2022

# Imports
import numpy as np
import os

# Constants
ids_to_merge = ["2", "2.1"]
merge_to_id = "2-merged" # Dont use _ in name
directory = 'data/discharging'

filename_list = []
cw_power_list = []
measuring_time_list = []
measuring_interval_list = []

# Find the files corresponding to the ids_to_merge
for id in ids_to_merge:
    for file in os.listdir(directory):
        if "DischargeData" in file:
            if file.split("_")[2][3:] == id:
                filename_list.append(file)
                cw_power_list.append(file.split("_")[3][6:])
                measuring_time_list.append(int(file.split("_")[4][5:]))
                measuring_interval_list.append(int(file.split("_")[5].split('.')[0][9:]))

for cw in cw_power_list: # Make sure power is same for all runs
    assert(cw == cw_power_list[0])

measuring_time_total = sum(measuring_time_list)
measuring_interval = measuring_interval_list[0] # Take first measuring interval as the measuring interval

# Loop over all files
t_array = np.array([])
I_array = np.array([])
U_array = np.array([])
P_array = np.array([])

for file in filename_list:
    with open(f'{directory}/{file}', 'rb') as f:
        # If this is the first file, dont offset time. Else, offset by last datapoint for time
        if len(t_array) == 0: 
            t_array = np.append(t_array, np.load(f))
        else: 
            t_array = np.append(t_array, np.load(f) + t_array[-1])

        I_array = np.append(I_array, np.load(f))
        U_array = np.append(U_array, np.load(f))
        P_array = np.append(P_array, np.load(f))

# Save data
with open(f'{directory}/DischargeData_RUN_ID-{merge_to_id}_POWER-{cw_power_list[0]}_TIME-{measuring_time_total}_INTERVAL-{measuring_interval}.npy', 'wb') as f:
    np.save(f, t_array)
    np.save(f, I_array)
    np.save(f, U_array)
    np.save(f, P_array)

print("Done!")
