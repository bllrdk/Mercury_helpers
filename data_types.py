# Imports
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import sys

# Other Files
import constants as c
import read_data as rd
import plotting_functions as pf
import data_file_functions as dff
import statistical_analysis_functions as saf


# a class of plotting attributes for different variables of data
class data_attributes:
    def __init__(self, name, ylim, tick_positions, tick_labels, yscale = 'log', color='k', marker=None):
        self.name = name
        self.color = color
        self.ylim = ylim
        self.yscale = yscale
        self.tick_positions = tick_positions
        self.tick_labels = tick_labels
        self.marker = marker

    # calculates tick positions for a data set
    def data_based_ticks(self, data):
        min_val = int(round(np.min(data), -2))
        max_val = int(round(np.max(data), -2))
        tick_positions = np.arange(min_val, max_val, 100)
        self.tick_positions = tick_positions
        self.tick_labels = self.tick_positions
        return

# intializes an array of the class for all plotting varriables
def plot_characteristics():
    eq_info = data_attributes('E/q (KeV/e)', (-2, 1), [0.1, 1, 10], [0.1, 1, 10])
    clock_ang_info = data_attributes('Angle (deg)', (0, 360), [90, 180, 270, 360],
                                     ['90', '180', '270', '360'], 'linear', 'darkviolet')
    r_ang_info = data_attributes('Angle (deg)', (0, 360),[90, 180, 270, 360],
                                 ['90', '180', '270', '360'], 'linear', 'gold',)
    #pitch_info = data_attributes()

    h_flux_info = data_attributes(r'H$^+$ Flux',[], [10**10, 10**11, 10**12],
                                  [r'10$^{10}$', r'10$^{11}$', r'10$^{12}$'], color='k')

    ## composition
    he2_info = data_attributes(r'He2$^+$', (0.9, 100), [1, 10, 100], [1, 10, 100], color='green', marker='.')
    he1_info = data_attributes(r'He$^+$', (0.9, 100), [1, 10, 100], [1, 10, 100], color='blue', marker='+')
    o_info = data_attributes(r'O$^+$ Grp', (0.9, 100), [1, 10, 100], [1, 10, 100], color='purple', marker='s')
    na_info = data_attributes(r'Na$^+$ Grp', (0.9, 100), [1, 10, 100], [1, 10, 100], color='orange', marker='D')


    ## mag field
    bx_info = data_attributes(r'B$_x$ [nT]', [-200, 100], [], [], 'linear', 'red' )
    bz_info = data_attributes(r'B$_z$ [nT]', [-300, 100], [], [], 'linear', 'blue')
    mag_info = data_attributes('|B| [nT]', [0, 400], [], [], 'linear', 'k' )

    dist_info = data_attributes('d [km]', [0, 1000], [0, 1000], [0, 1000], 'linear', 'brown' )

    return np.array([eq_info, clock_ang_info, r_ang_info, h_flux_info, he2_info, he1_info, o_info, na_info, bx_info, bz_info, mag_info, dist_info])
