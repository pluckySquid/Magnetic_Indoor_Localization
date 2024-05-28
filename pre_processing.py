def adjust_data(actual_current_timestamps, actual_mag_timestamps, current_data, mag_data):
    min_actual_start_time = max(actual_current_timestamps[0], actual_mag_timestamps[0])
    min_actual_end_time = min(actual_current_timestamps[len(actual_current_timestamps)-1], actual_mag_timestamps[len(actual_mag_timestamps) - 1])
    min_current_start_index = 0
    min_mag_start_index = 0
    min_current_end_index = 100000000
    min_mag_end_index = 100000000
    for i in range(0, len(actual_current_timestamps)):
        if actual_current_timestamps[i] >= min_actual_start_time:
            min_current_start_index = i
            break
    for i in range(0, len(actual_mag_timestamps)):
        if actual_mag_timestamps[i] >= min_actual_start_time:
            min_mag_start_index = i   
            break 
    for i in range(len(actual_current_timestamps)-1, 0, -1):
        if actual_current_timestamps[i] <= min_actual_end_time:
            min_current_end_index = i
            break
    for i in range(len(actual_mag_timestamps)-1, 0, -1):
        if actual_mag_timestamps[i] <= min_actual_end_time:
            min_mag_end_index = i
            break    

    actual_current_timestamps = actual_current_timestamps[min_current_start_index: min_current_end_index + 1]
    actual_mag_timestamps = actual_mag_timestamps[min_mag_start_index: min_mag_end_index + 1]


    current_data = current_data[:,min_current_start_index: min_current_end_index + 1,:]
    mag_data = mag_data[:,min_mag_start_index: min_mag_end_index + 1,:]

    return actual_current_timestamps, actual_mag_timestamps, current_data, mag_data