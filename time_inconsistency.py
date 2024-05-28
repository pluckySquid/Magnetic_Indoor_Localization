import matplotlib.pyplot as plt
from constant_variable import AXIS_MAPPING

def time_inconsistency(delay):
    # plot time inconsistency
    fig = plt.figure()
    for i, axis in enumerate([0, 1, 2]):
        for j, frequency in enumerate([10, 100]):
            delay_time = [delay[axis][frequency][amplitude] for amplitude in [0.01, 0.03, 0.05, 0.07, 0.09]]
            if frequency == 10:
                plt.plot([10, 30, 50, 70, 90], delay_time, marker='o', label=f'Coil {AXIS_MAPPING[axis]}, Frequency {frequency}')
            else:
                plt.plot([10, 30, 50, 70, 90], delay_time, marker='o', linestyle='--', label=f'Coil {AXIS_MAPPING[axis]}, Frequency {frequency}')
        plt.xlabel('Amplitude (mA)')
        plt.ylabel('Time (microsecond)')
        plt.title(f'Time Inconsistency Analysis')
        plt.legend()
        plt.grid(True)

    plt.tight_layout()
    fig.savefig('image_results/delay.png')
    plt.close()

    # plot time inconsistency
    fig, axs = plt.subplots(5, 1, figsize=(10, 20))  # Create subplots for each amplitude
    amplitudes = [0.01, 0.03, 0.05, 0.07, 0.09]

    for i, amplitude in enumerate(amplitudes):
        for axis in [0, 1, 2]:
            frequencies = sorted(delay[axis].keys())  # Sort the frequencies
            delay_times = [delay[axis][frequency][amplitude] for frequency in frequencies]

            axs[i].plot(frequencies, delay_times, marker='o', label=f'Coil {AXIS_MAPPING[axis]}')
            axs[i].set_title(f'Amplitude {amplitude} mA')
            axs[i].set_xlabel('Frequency (Hz)')
            axs[i].set_ylabel('Time (microsecond)')
            axs[i].legend()
            axs[i].grid(True)

    plt.tight_layout()
    fig.savefig('image_results/delay_frequencies.png')
    plt.close()