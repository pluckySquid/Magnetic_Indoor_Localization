import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr
from scipy.stats import linregress
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
import os

from constant_variable import AXIS_MAPPING, CURRENT_TO_MAG

def ensure_directory_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Define a sine function
def sine_wave(x, amplitude, frequency, phase, offset):
    return amplitude * np.sin(frequency * x + phase) + offset

def fit_sine_wave(actual_mag_timestamps, actual_mag_data, fit_params_mag, actual_current_timestamps, actual_current_data, fit_params_current, group_name = "none"):
    fig, ax1 = plt.subplots()

    # Plot magnetic field measurements vs. time
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Magnetic Field (uT)', color='tab:red')
    ax1.scatter(actual_mag_timestamps[0:500], 
        actual_mag_data[0:500], 
        color="red", 
        label="Original mag Data",
        s=5)
    ax1.plot(actual_mag_timestamps[0:500], sine_wave(actual_mag_timestamps, *fit_params_mag)[0:500], color='red', linestyle='--', label="Fitted mag Wave")
    ax1.tick_params(axis='y', labelcolor='tab:red')
    ax1.legend(loc='upper left')

    # Create a second y-axis for current measurements
    ax2 = ax1.twinx()
    ax2.set_ylabel('Current (mA)', color='tab:blue')
    ax2.scatter(actual_current_timestamps[0:500],  
        actual_current_data[0:500], 
        color="b", 
        label="Original current Data",
        s=5)
    ax2.plot(actual_current_timestamps[0:500], sine_wave(actual_current_timestamps, *fit_params_current)[0:500], color='b', label="Fitted current Wave")
    ax2.tick_params(axis='y', labelcolor='tab:blue')
    ax2.legend(loc='upper right')
    
    
    plt.xlabel("Timestamps")
    plt.ylabel("Amplitude (mA)")
    plt.title("Fitting a Sine Waves to Data")
    plt.legend()
    ensure_directory_exists("image_results/fit_sine_waves")
    plt.savefig('image_results/fit_sine_waves/' + group_name.split(".")[0] + ".png")
    plt.close()  

def question1_correlation(data):
    fig = plt.figure()
    for i, axis in enumerate([0, 1, 2]):
        for j, frequency in enumerate([10, 100]):
            correlations = [data[axis][frequency][amplitude] for amplitude in [0.01, 0.03, 0.05, 0.07, 0.09]]
            if frequency == 10:
                plt.plot([10, 30, 50, 70, 90], [corr[axis] for corr in correlations], marker='o', label=f'Coil {AXIS_MAPPING[axis]}, Frequency {frequency}')
            else:
                plt.plot([10, 30, 50, 70, 90], [corr[axis] for corr in correlations], marker='o', linestyle='--', label=f'Coil {AXIS_MAPPING[axis]}, Frequency {frequency}')
        plt.xlabel('Amplitude (mA)')
        plt.ylabel('Correlation Coefficient')
        plt.title(f'Correlation Coefficients between current and magnetic ')
        plt.legend()
        plt.grid(True)

    plt.tight_layout()
    ensure_directory_exists("image_results")
    fig.savefig('image_results/correlation_plots.png')

def question1_proportion(proportion_data, figure_name="proportion"):
    figure_name = figure_name + ".png"
    fig = plt.figure()
    for i, axis in enumerate([0, 1, 2]):
        for j, frequency in enumerate([10, 100]):
            proportion = [proportion_data[axis][frequency][amplitude] for amplitude in [0.01, 0.03, 0.05, 0.07, 0.09]]
            if frequency == 10:
                plt.plot([10, 30, 50, 70, 90], proportion, marker='o', label=f'Coil {AXIS_MAPPING[axis]}, Frequency {frequency}')
            else:
                plt.plot([10, 30, 50, 70, 90], proportion, marker='o', linestyle='--', label=f'Coil {AXIS_MAPPING[axis]}, Frequency {frequency}')
        plt.xlabel('Amplitude (mA)')
        plt.ylabel('Proportion')
        plt.title(f'Proportion between magnetic field and current ')
        plt.legend()
        plt.grid(True)

    plt.tight_layout()
    ensure_directory_exists("image_results")
    fig.savefig("image_results/" + figure_name)


