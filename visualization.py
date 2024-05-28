import matplotlib.pyplot as plt
from constant_variable import AXIS_MAPPING
from data_analysis import ensure_directory_exists

# Plotting
def visualization(actual_mag_timestamps, mag_data, mag_uT_per_lsb, actual_current_timestamps, current_data, current_mA_per_lsb, trigger_timestamps, axis, group_name):
    fig, ax1 = plt.subplots()

    # Plot magnetic field measurements vs. time
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Magnetic Field (uT)', color='tab:blue')
    ax1.plot(actual_mag_timestamps[0:500], mag_data[0,0:500, 0]*mag_uT_per_lsb[0] , linestyle='--', color='tab:blue', label='Mag x')
    ax1.plot(actual_mag_timestamps[0:500], mag_data[0,0:500, 1]*mag_uT_per_lsb[1] , linestyle='--', color='tab:green', label='Mag y')
    ax1.plot(actual_mag_timestamps[0:500], mag_data[0,0:500, 2]*mag_uT_per_lsb[2] , linestyle='--', color='tab:red', label='Mag z')
    # ax1.plot(actual_mag_timestamps,np.sqrt((mag_data[0,:, 0]*mag_uT_per_lsb[0])**2+(mag_data[0,:, 1]*mag_uT_per_lsb[1])**2+(mag_data[0,:, 2]*mag_uT_per_lsb[2])**2) , color='tab:red', label='Combine')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.legend(loc='upper left')

    # Create a second y-axis for current measurements
    ax2 = ax1.twinx()
    ax2.set_ylabel('Current (mA)', color='tab:orange')
    ax2.plot(actual_current_timestamps[0:500], current_data[0,0:500,0]*current_mA_per_lsb[0], color='tab:orange', label='Current X')
    ax2.plot(actual_current_timestamps[0:500], current_data[0,0:500,1]*current_mA_per_lsb[1], color='tab:pink', label='Current Y')
    ax2.plot(actual_current_timestamps[0:500], current_data[0,0:500,2]*current_mA_per_lsb[2], color='tab:purple', label='Current Z')
    ax2.tick_params(axis='y', labelcolor='tab:orange')
    ax2.legend(loc='upper right')
    
    plt.title(f'Magnetic Field vs. Time and Current vs. Time (current on {AXIS_MAPPING[axis]})')
    plt.tight_layout()
    ensure_directory_exists("image_results/visualization")
    fig.savefig('image_results/visualization/' + group_name.split(".")[0] + ".png")
    plt.close()