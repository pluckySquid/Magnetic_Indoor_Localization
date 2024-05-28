import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit
import numpy as np
from data_analysis import sine_wave

from constant_variable import AXIS_MAPPING, CURRENT_TO_MAG
from data_analysis import ensure_directory_exists

def create_rotation_matrices(roll, pitch, yaw):
    R_roll = np.array([[1, 0, 0],
                       [0, np.cos(roll), -np.sin(roll)],
                       [0, np.sin(roll), np.cos(roll)]])
    
    R_pitch = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                        [0, 1, 0],
                        [-np.sin(pitch), 0, np.cos(pitch)]])
    
    R_yaw = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                      [np.sin(yaw), np.cos(yaw), 0],
                      [0, 0, 1]])
    
    return np.dot(R_yaw, np.dot(R_pitch, R_roll))


def rotation(actual_mag_timestamps, mag_data, mag_uT_per_lsb, current_axis, frequency, amplitude_default, group_name, image_saver):
    fit_params_mag = []
    roll = np.radians(0)  # Convert degrees to radians
    pitch = np.radians(0)
    yaw = np.radians(0)   

    for axis in range(3):
        actual_mag_data = mag_data[0, :, axis] * mag_uT_per_lsb[axis]

        # Fit for mag_data
        params_mag, _ = curve_fit(sine_wave, actual_mag_timestamps, actual_mag_data, p0=[(max(actual_mag_data) - min(actual_mag_data))/2, 2 * math.pi * frequency, 0, (max(actual_mag_data) + min(actual_mag_data))/2], maxfev=5000)
        fit_params_mag.append(params_mag)

    amp_records = 0
    for axis in range(3):
        actual_mag_data = mag_data[0, :, axis] * mag_uT_per_lsb[axis]

        amplitude_mag, frequency_mag, phase_mag, offset_mag = fit_params_mag[axis]

        sine_wave_mag = sine_wave(actual_mag_timestamps, amplitude_mag, frequency_mag, phase_mag, offset_mag)

        rotation_amp = amplitude_mag / amplitude_default * 1
        amp_records = math.sqrt(amp_records*amp_records + rotation_amp*rotation_amp)
        tan = np.arctan(rotation_amp)
        degree = np.degrees(tan) 
        # print("amp_records: ", amp_records)
        # print("rotation_amp:", rotation_amp)
        # print("degree:", degree)

        if current_axis == 1: # mag on -X
            if axis == 0:
                continue
            elif axis == 1:
                yaw = np.radians(degree)
            elif axis == 2:
                pitch = np.radians(degree)
        if current_axis == 2: # mag on -Y
            if axis == 1:
                continue
            elif axis == 0:
                yaw = np.radians(degree)
            elif axis == 2:
                roll = np.radians(-degree)
        if current_axis == 0: # mag on Z
            if axis == 2:
                continue
            elif axis == 0:
                pitch = np.radians(-degree)
            elif axis == 1:
                roll = np.radians(degree)
    
    # Visualizing the fitted sine wave for each axis
    if image_saver: 
        print(image_saver)
        plt.figure(figsize=(15, 10))
        for axis in range(3):
            plt.subplot(3, 1, axis * 1 + 1)
            plt.scatter(actual_mag_timestamps, actual_mag_data, label="Original Mag Data (Axis {})".format(axis))
            plt.plot(actual_mag_timestamps, sine_wave_mag, color='red', label="Fitted Sine Wave (Mag, Axis {})".format(axis))
            plt.xlabel("Timestamps")
            plt.ylabel("Magnitude")
            plt.title("Magnetic Data and Fitted Sine Wave (Axis {})".format(axis))
            plt.legend()
        ensure_directory_exists("image_results/rotation")
        plt.savefig('image_results/rotation/' + group_name.split(".")[0] + ".png")
        plt.close()

    R = create_rotation_matrices(roll, pitch, yaw)
    rotated_mag_data = np.dot(mag_data, R.T)

    #also increase the length of the default mag
    rotated_mag_data[0,:,CURRENT_TO_MAG[current_axis]] *= amp_records

    if image_saver: 
        plt.figure(figsize=(15, 10))

        for axis in range(3):
            actual_mag_data = rotated_mag_data[0, :, axis] * mag_uT_per_lsb[axis]

            params_mag, _ = curve_fit(sine_wave, actual_mag_timestamps, actual_mag_data, p0=[(max(actual_mag_data) - min(actual_mag_data))/2, 2 * math.pi * frequency, 0, (max(actual_mag_data) + min(actual_mag_data))/2], maxfev=5000)
            amplitude_mag, frequency_mag, phase_mag, offset_mag = params_mag

            sine_wave_mag = sine_wave(actual_mag_timestamps, amplitude_mag, frequency_mag, phase_mag, offset_mag)

            plt.subplot(3, 1, axis * 1 + 1)
            plt.scatter(actual_mag_timestamps[0:500], actual_mag_data[0:500], label="Original Mag Data (Axis {})".format(axis))
            plt.plot(actual_mag_timestamps[0:500], sine_wave_mag[0:500], color='red', label="Fitted Sine Wave (Mag, Axis {})".format(axis))
            plt.xlabel("Timestamps")
            plt.ylabel("Magnitude")
            plt.title("Rotated Magnetic Data and Fitted Sine Wave (Axis {})".format(axis))
            plt.legend()
        
        ensure_directory_exists("image_results/rotation")
        plt.savefig('image_results/rotation/' + "rotated_" + group_name.split(".")[0] + ".png")
        plt.close()  
    return rotated_mag_data