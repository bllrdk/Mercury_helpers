# imports
import matplotlib.pyplot as plt
import numpy as np
import spacepy.seapy as se
import datetime as dt
import constants as c

import statistical_analysis_functions as saf
import plotting_functions as pf

# adds the values in two lists together [a, b] + [1, 2] = [a+1, b+2]
def add_same_position(list1, list2):
    length = len(list1)
    result = []
    for i, j in zip(list1, list2):
        result.append(i + j)
    return result

def epoch_plotter(time, mean, median, q1, q3, ax, plot_info):

    x_idx = len(time)/2

    ax.plot(time, mean, linewidth=2, color='k')
    ax.plot(time, median, linewidth=2, linestyle='--', color='magenta')
    color = plot_info.color
    if color == 'k': color = 'gray'
    ax.fill_between(time, q1, q3, color=color)

    ax.set_yscale(plot_info.yscale)
    ax.set_ylabel(plot_info.name, fontsize=10)
    ax.set_ylim(plot_info.ylim)
    ax.axvline(x_idx, color='k', linestyle='--')
    pf.format_axis(ax, plot_info.tick_positions, plot_info.tick_labels, False)
    return