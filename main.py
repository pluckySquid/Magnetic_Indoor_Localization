import h5py
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr
from scipy.stats import linregress
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
import math
from tqdm import tqdm
import sys

from data_analysis import sine_wave, fit_sine_wave, question1_correlation, question1_proportion
from constant_variable import CURRENT_TO_MAG
from pre_processing import adjust_data
from rotation import rotation
from time_inconsistency import time_inconsistency
from visualization import visualization

import random
random.seed(42)

def str_to_bool(s):
    """Convert a string to a boolean value."""
    return s.lower() not in ['false', '0', 'n', 'no']

def main(param):
    groups = []
    image_saver = param

    # Create an empty dictionary to store the data
    data = {}
    delay = {}
    proportion = {}
    time_inconsistency_f100 = []
    time_inconsistency_f10 = []
    adjusted_proportion = {}

    with h5py.File('alg_challenge_dataset.hdf5', 'r') as hdf_file:
        
        # Assuming hdf_file is a dictionary-like object containing groups
        total_groups = len(hdf_file)  # Get total number of groups for progress bar
        for group_name in tqdm(hdf_file, total=total_groups):
            #group_name = 'Coil_X_Freq10_Amp90' 
            group = hdf_file[group_name]

            # if "Coil_Z" not in group_name:
            #     continue
            
            # Extract attributes
            amplitude = group.attrs['amplitude']
            frequency = group.attrs['frequency']
            axis = group.attrs['axis']
            sensor_orientation = group.attrs['sensor_orientation']
            timestamp_counts_per_s = group.attrs['timestamp_counts_per_s']
            adc_timestamp_offsets = group.attrs['adc_timestamp_offsets']
            current_mA_per_lsb = group.attrs['current_mA_per_lsb']
            mag_uT_per_lsb = group.attrs['mag_uT_per_lsb']

            # Extract datasets
            current_data = group['Current'][:]
            current_timestamps = group['Current_Timestamp'][:]
            mag_data = group['Mag'][:]
            mag_timestamps = group['Mag_Timestamp'][:]
            trigger_timestamps = group['Trigger_Timestamp'][:]/timestamp_counts_per_s

            # adjust the data
            actual_current_timestamps = current_timestamps/timestamp_counts_per_s + adc_timestamp_offsets[0][axis]/timestamp_counts_per_s
            actual_mag_timestamps = mag_timestamps/timestamp_counts_per_s + adc_timestamp_offsets[0][axis]/timestamp_counts_per_s

            actual_current_timestamps_adjust, actual_mag_timestamps_adjust, current_data, mag_data = adjust_data(actual_current_timestamps, actual_mag_timestamps, current_data, mag_data)

            actual_mag_data = mag_data[0,:,CURRENT_TO_MAG[axis]]*mag_uT_per_lsb[CURRENT_TO_MAG[axis]]
            actual_current_data = current_data[0,:,axis]*current_mA_per_lsb[axis]

            fit_params_mag, _ = curve_fit(sine_wave, actual_mag_timestamps_adjust, actual_mag_data, p0=[(max(actual_mag_data) - min(actual_mag_data))/2, 2 * math.pi * frequency, 0, (max(actual_mag_data) + min(actual_mag_data))/2], maxfev=5000)
            amplitude_mag, frequency_mag, phase_mag, offset_mag = fit_params_mag
                       
            fit_params_current, _ = curve_fit(sine_wave, actual_current_timestamps_adjust, actual_current_data, p0=[(max(actual_current_data) - min(actual_current_data))/2, 2 * math.pi * frequency, 0, (max(actual_current_data) + min(actual_current_data))/2], maxfev=5000)
            amplitude_current, frequency_current, phase_current, offset_current = fit_params_current
            #print(f"current function  y = {amplitude_current:.4f} * sin({frequency_current:.4f} * x + {phase_current:.4f}) + {offset_current:.4f}")

            # remove time variance
            delay_time= phase_mag - phase_current
            if delay_time > 2.5:
                delay_time -= math.pi
            elif delay_time < -2.5:
                delay_time = delay_time + math.pi
            delay_in_real_time = delay_time / frequency_mag   
                
            if frequency == 100:
                time_inconsistency_f100.append(delay_in_real_time)
            if frequency == 10:
                time_inconsistency_f10.append(delay_in_real_time)

            # ----------- turn on if need visualization
            if image_saver:
                visualization(actual_mag_timestamps_adjust, mag_data, mag_uT_per_lsb, actual_current_timestamps_adjust, current_data, current_mA_per_lsb, trigger_timestamps, axis, group_name)

            total_mag = np.sqrt((mag_data[0,:, 0]*mag_uT_per_lsb[0])**2+(mag_data[0,:, 1]*mag_uT_per_lsb[1])**2+(mag_data[0,:, 2]*mag_uT_per_lsb[2])**2)
            input_current = current_data[0,:,axis]*current_mA_per_lsb[axis]
            
            # Ensure that both arrays have the same length
            min_length = min(len(total_mag), len(input_current))
            total_mag = total_mag[:min_length]
            input_current = input_current[:min_length]

            correlation_coefficient0, _ = pearsonr(mag_data[0,:min_length, 2]*mag_uT_per_lsb[2], current_data[0,:min_length,0]*current_mA_per_lsb[0])
            correlation_coefficient1, _ = pearsonr(mag_data[0,:min_length, 0]*mag_uT_per_lsb[0], current_data[0,:min_length,1]*current_mA_per_lsb[1])
            correlation_coefficient2, _ = pearsonr(mag_data[0,:min_length, 1]*mag_uT_per_lsb[1], current_data[0,:min_length,2]*current_mA_per_lsb[2])
            correlation_coefficient=[correlation_coefficient0, correlation_coefficient1, correlation_coefficient2]

            # align time inconsistency and remove environment magnetic
            actual_mag_timestamps_algined = actual_mag_timestamps_adjust + delay_in_real_time
            actual_mag_data_algined  = actual_mag_data - offset_mag
            fit_params_mag_aligned, _ = curve_fit(sine_wave, actual_mag_timestamps_algined, actual_mag_data_algined, p0=[(max(actual_mag_data) - min(actual_mag_data))/2, 2 * math.pi * frequency, 0, (max(actual_mag_data_algined) + min(actual_mag_data_algined))/2], maxfev=5000)
            amplitude_mag_aligned, frequency_mag_aligned, phase_mag_aligned, offset_mag_aligned = fit_params_mag_aligned
            #print(f"aligned mag function  y = {amplitude_mag_aligned:.4f} * sin({frequency_mag_aligned:.4f} * x + {phase_mag_aligned:.4f}) + {offset_mag_aligned:.4f}")
            if image_saver:
                fit_sine_wave(actual_mag_timestamps_algined, actual_mag_data_algined, fit_params_mag_aligned, actual_current_timestamps_adjust, actual_current_data, fit_params_current, group_name)

            # update mag data with the aligned mag data
            mag_data[0,:,CURRENT_TO_MAG[axis]] = actual_mag_data_algined/mag_uT_per_lsb[CURRENT_TO_MAG[axis]]

            # skewness correction
            rotated_mag_data = rotation(actual_mag_timestamps_adjust, mag_data, mag_uT_per_lsb, axis, frequency, amplitude_mag, group_name, image_saver)
            if image_saver:
                visualization(actual_mag_timestamps_adjust, rotated_mag_data, mag_uT_per_lsb, actual_current_timestamps_adjust, current_data, current_mA_per_lsb, trigger_timestamps, axis, "rotated_" + group_name)
            actual_mag_data = rotated_mag_data[0,:,CURRENT_TO_MAG[axis]]*mag_uT_per_lsb[CURRENT_TO_MAG[axis]]

            fit_params_mag_rotated, _ = curve_fit(sine_wave, actual_mag_timestamps_adjust, actual_mag_data, p0=[(max(actual_mag_data) - min(actual_mag_data))/2, 2 * math.pi * frequency, 0, (max(actual_mag_data) + min(actual_mag_data))/2], maxfev=5000)
            amplitude_mag_rotated, frequency_mag_rotated, phase_mag_mag_rotated, offset_mag_mag_rotated = fit_params_mag_rotated

            if axis not in data:
                data[axis] = {}
                delay[axis] = {}
                proportion[axis] = {}
                adjusted_proportion[axis] = {}
            if frequency not in data[axis]:
                data[axis][frequency] = {}
                delay[axis][frequency] = {}
                proportion[axis][frequency] = {} 
                adjusted_proportion[axis][frequency] = {} 
            data[axis][frequency][amplitude] = correlation_coefficient
            delay[axis][frequency][amplitude] = delay_in_real_time* 1000000
            proportion[axis][frequency][amplitude] = abs(amplitude_mag/amplitude_current)
            adjusted_proportion[axis][frequency][amplitude] = abs(amplitude_mag_rotated/amplitude_current)

    question1_correlation(data)
    question1_proportion(proportion)
    question1_proportion(adjusted_proportion, "adjusted_proportion")
    time_inconsistency(delay)


if __name__ == "__main__":
    # Check if any argument is provided
    if len(sys.argv) > 1:
        # Convert the second command-line argument to boolean
        bool_arg = str_to_bool(sys.argv[1])
        print("image saver is ", bool_arg)
        main(bool_arg)
    else:
        main(True)