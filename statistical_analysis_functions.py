# Imports
import numpy as np
import datetime as dt
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import LogNorm
from matplotlib.ticker import AutoMinorLocator, LogLocator
from matplotlib.transforms import offset_copy
from scipy.interpolate import make_interp_spline

import constants as c
import read_data as rd

# converts time information into datetimes
def time_to_dt(times):
    dt_times = []
    for t in times:
        d = t.timestamp()
        dt_times.append(d)
    return np.array(dt_times)

# interpolates data of any shape array along only one axis
def interpolate_data(new_time, time, data):
    if data.ndim > 1:
        new_data = np.zeros((data.shape[0], len(new_time)))
        for i in range(data.shape[0]):
            new_data[i, :] = np.interp(new_time, time, data[i, :])
        return new_data

    else:
        new_data = np.interp(new_time, time, data)
        return new_data

# adds up the values of data between two equal total times on either side of the crossing point
def counts_data(time_data, counts_data, x_idx, count_time):
    delta = rd.calculate_delta(time_data)
    counts_left = []
    time_sum = 0
    for i in range(x_idx, 0, -1):
        time_sum += delta[i].total_seconds()
        if time_sum <= count_time : counts_left.append(counts_data[3, i])

    counts_right = []
    time_sum = 0
    for i in range(x_idx, len(time_data) - 1):
        time_sum += delta[i].total_seconds()
        if time_sum <= count_time: counts_right.append(counts_data[3, i])

    return sum(counts_left), sum(counts_right)

# plots a histogram of counts on either side of the magnetopause
def plot_counts_data(counts_data):
    left_data = counts_data[0, :]
    right_data = counts_data[1, :]

    bins = 50
    plt.title('Histogram of Counts For Left of MP', fontsize=18)
    plt.hist(left_data, bins=bins, log=False, color='gray')
    plt.xlabel('Sum of Counts', fontsize=12)
    plt.ylabel('Number', fontsize=12)
    plt.show()

    plt.title('Histogram of Counts For Right of MP', fontsize=18)
    plt.hist(right_data, bins=bins, log=False, color='gray')
    plt.xlabel('Sum of Counts', fontsize=12)
    plt.ylabel('Number', fontsize=12)
    plt.show()

