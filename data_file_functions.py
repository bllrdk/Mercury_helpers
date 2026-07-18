# Imports
import numpy as np
import datetime as dt
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LogNorm
from matplotlib.ticker import AutoMinorLocator, LogLocator
from matplotlib.transforms import offset_copy

import constants as c
import pickle
import read_data as rd

# finds the start and stop indices to center a plot around the magnetopause crossing location
def calculate_plot_range(time_data, b_time, x_idx, time_range):
    file_start = time_data[0]
    file_end = time_data[-1]
    file_len = len(time_data)

    delta = rd.calculate_delta(time_data)

    time_sum = 0
    for i in range(x_idx, 0, -1):
        time_sum += delta[i].total_seconds()
        if time_sum <= time_range/2 : shift_back = i
    time_sum = 0
    for i in range(x_idx, len(time_data)-1):
        time_sum += delta[i].total_seconds()
        if time_sum <= time_range/2: shift_forward = i

    new_start = time_data[shift_back]
    new_end = time_data[shift_forward]

    adj_x_idx = x_idx - shift_back

    b_start = np.where(b_time >= new_start)[0][0]
    b_end = np.where(b_time >= new_end)[0][0]

    return new_start, new_end, shift_back, shift_forward, b_start, b_end, adj_x_idx

## pickles the data
def pickle_data(data, filename):
    with open(filename, 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
    print(f'{filename} data has been pickled')
    return

# reads in pickled data
def read_pickle_data(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data


