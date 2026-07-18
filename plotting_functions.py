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
import data_types as d

## formats the x-axis labels for timeseries plots
def format_x_labels(time, mlat, lt, alt, ax, fig):
    start = time[0]
    end = time[-1]

    UTC = []
    MLAT = []
    LT = []
    ALT = []
    positions = []

    tick_seperation = (end - start)/5
    i = 0
    # finds the value of each variable at each tick index
    while i < 6:
        idx = np.where(time >= start + tick_seperation * i)[0][0]
        positions.append(time[idx])
        UTC.append(str(time[idx].time()))
        MLAT.append(str(round(mlat[idx], 2)))
        LT.append(str(round(lt[idx], 2)))
        ALT.append(str(round(alt[idx], 1)))
        i += 1

    # combines the labels into one attribute
    nl = '\n'
    combined_labels = [f"{u}{nl}{m}{nl}{l}{nl}{a}" for u, m, l, a in zip(UTC, MLAT, LT, ALT)]
    positions.insert(0, start)
    combined_labels.insert(0, f"UTC{nl}MLAT{nl}LT{nl}ALT{nl}")

    ax.set_xticks(positions, labels=combined_labels)
    ax.tick_params(pad=9)

    t = offset_copy(ax.transAxes, y=-(ax.xaxis.get_tick_padding() + ax.xaxis.majorTicks[0].get_pad()), fig=fig,
                    units='dots')

    # plots the ticklabels at the given points
    ax.xaxis.set_label_coords(0, -.05, transform=t)
    ax.set_xlabel(f'UTC{nl}MLAT{nl}LT{nl}ALT', va='top', ha='left', x=-.1)

    return

# formats the x and y axes for time series plots
def format_axis(ax, tick_positions, tick_labels, mag):
    ax.set_xticklabels([])
    ax.tick_params(axis='y', which='minor', direction='in', length=3)
    ax.tick_params(axis='x', which='major', direction='in')
    ax.tick_params(axis='x', which='minor', direction='in')

    if mag:
        ax.set_yticks(tick_positions)
    else:
        ax.set_yticks(tick_positions, labels=tick_labels)
        ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs=np.arange(2, 10) * 0.1, numticks=10))

    minor_x = AutoMinorLocator(10)  # 5 minor ticks between each major tick
    ax.xaxis.set_minor_locator(minor_x)
    return

## adds in the vertical lines for various boundaries within the plotted time range
def plot_boundary_lines(ax, idxs, subplot, start, end, time, direction):
    ## location where labels should be places (changes based on data set)
    y = 0
    # identifies found direction of the magnetopause crossing
    if direction == 0: d_str = 'in'
    if direction == 1: d_str = 'out'

    # mp_crossing
    if idxs[0] >= start and idxs[0] <= end:
        ax.axvline(time[idxs[0]], color='magenta', linestyle='--')
        if subplot == 2 or c.NUM_SUBPLOTS < 2:
            ax.annotate('MP ' + d_str, xy=(time[idxs[0]] + dt.timedelta(minutes=.5), y), xycoords='data', color='magenta')

    # bow shock crossing
    if idxs[1] >= start and idxs[1] <= end:
        ax.axvline(time[idxs[2]], color='red', linestyle=(0, (1, 7)))
        if subplot == 2 or c.NUM_SUBPLOTS < 2:
            ax.annotate('BS', xy=(time[idxs[1]] + dt.timedelta(minutes=1), y), xycoords='data', color='red')

    # Points where the MLAT is 0
    for i in idxs[2]:
        if i >= start and i <= end:
            ax.axvline(time[i], color='orange', linestyle=(0, (1, 5)))
            if subplot == 2 or c.NUM_SUBPLOTS < 2:
                ax.annotate('MLAT0', xy=(time[i] + dt.timedelta(minutes=1), y), xycoords='data', color='orange')

    return

## plots the e/q data (color density map)
def eq_plotter(time, data, ax, ax_cm, clim, clabel, plot_info):
    # sets up color map
    cmap = mpl.colormaps['rainbow']
    #cmap.set_under(color='white')

    # adjusts the bin locations for the time data
    time_centers = time[:-1] + np.diff(time) / 2
    energy = np.logspace(-2, 1, 64)
    # creates a grid of bin centers and energy bins to plot the data in
    X, Y = np.meshgrid(time_centers, energy)
    # plots the data within the grid
    pcm = ax.pcolormesh(X, Y, data[:, 1:], shading='nearest', cmap=cmap, norm=LogNorm(clim[0], clim[1]))

    # plots the colorbar on the side of the plot
    cbar = plt.colorbar(pcm, cax=ax_cm, orientation='vertical', aspect=50)
    cbar.set_label(clabel, fontsize=9)
    cbar.ax.tick_params(labelsize=8, labelbottom=True, labeltop=True)

    # sets the axes, scale, and tick labels
    ax.set_yscale('log')
    ax.set_ylabel('E/q (KeV/e)', fontsize=10)

    tick_positions = [0.1, 1, 10]
    tick_labels = [0.1, 1, 10]
    format_axis(ax, tick_positions, tick_labels, False)

    return

## plots the h flux over time
def h_flux_plotter(time, data, ax, plot_info):
    ax.plot(time, data, linewidth=0.5, color='k')
    ax.set_ylabel(r'H$^+$ Flux', fontsize=10)

    ax.set_yscale('log')
    tick_positions = [10**10, 10**11, 10**12]
    tick_labels = [r'10$^{10}$', r'10$^{11}$', r'10$^{12}$']
    format_axis(ax, tick_positions, tick_labels, False)

    return

# plot the clock angle data over time
def angle_plotter(time, clock_angle, r_angle, ax, label_box, plot_info):
    ax.plot(time, clock_angle, c='darkviolet', label='Clock (YZ)', lw=1)
    ax.plot(time, r_angle, c='gold', label='nadir', lw=1)

    ax.legend(loc='center left', bbox_to_anchor=label_box, edgecolor='k')
    ax.set_ylim(0, 360)
    ax.set_ylabel('Angle (deg)', fontsize=10)

    tick_positions = [90, 180, 270, 360]
    tick_labels = ['90', '180', '270', '360']
    format_axis(ax, tick_positions, tick_labels, False)

    return

# plot a 2d histogram of binned data
## not set up
def pa_plotter(time, clock_angle, r_angle, ax, plot_info):
    # data normalized by max flux
    # data outside fips fov is white

    # counts, x_edges, y_edges, image = ax.hist2d(time, data, bins=100, cmap=cmap, range=[[0.1, 10]], alpha=1, vmin=1e6, vmax=1e10)

    ax.set_ylabel('PA (deg)', fontsize=10)
    ax.set_ylim([0, 180])

    tick_positions = [0.1, 1, 10]
    tick_labels = [0.1, 1, 10]
    format_axis(ax, tick_positions, tick_labels, False)
    return

# plots the composition counts for compositions turned on in constants.py
def counts_plotter(time, data, ax, label_box, plot_info, cluster_info):

    ## sodium
    if c.Na:
        ax.scatter(time, data[3], marker='D', facecolors='none', color='orange', label=r'Na$^+$ Grp', s=10)

    ## highlights identified cluster range within the plot
        start = 0
        end = len(time) - 1
        for cl in cluster_info:
            s = cl.start
            e = cl.end
            m  = cl.mid
            plot_cluster = False
            if s >= start and s <= end and e >= start and e <= end:
                plot_cluster = True
            elif s < start and e >= start and e <= end:
                s = 0
                if m < start: m = 0
                plot_cluster = True
            elif s >= start and s <= end and e > end:
                e = end
                if m > end: m = end
                plot_cluster = True

            if plot_cluster:
                ax.axvspan(time[s], time[e], color='orange', alpha=0.3)
                ax.axvline(time[m], color = 'red', linestyle='-', alpha=0.3)

    # Oxygen
    if c.O:
        ax.scatter(time, data[2], marker='s', facecolors='none', edgecolors='purple', label=r'O$^+$ Grp', s=10)
    # Helium 1
    if c.He1:
        ax.scatter(time, data[1], marker='+', facecolors='blue', label=r'He$^+$', s=30)
    # Helium 2
    if c.He2:
        ax.scatter(time, data[0], marker='.', facecolors='green', edgecolors='none', label=r'He2$^+$', s=20)

    # defines the axies and tick labels
    ax.set_ylabel(r'counts', fontsize=10)
    ax.set_yscale('log')
    ax.set_ylim([0.9, 100])
    ax.legend(loc='center left', bbox_to_anchor=label_box, edgecolor='k', fontsize=7)

    tick_positions = [1, 10, 100]
    tick_labels = [1, 10, 100]
    format_axis(ax, tick_positions, tick_labels, False)

    return

# plots the normalized number density for each ion as specified in constants.py
def n_density_plotter(time, data, ax, label_box, plot_info):

    if c.Na:
        ax.scatter(time, data[3], marker='D', facecolors='none', color='orange', label=r'Na$^+$ Grp')
    if c.O:
        ax.scatter(time, data[2], marker='s', facecolors='none', edgecolors='purple', label=r'O$^+$ Grp')
    if c.He1:
        ax.scatter(time, data[1], marker='+', facecolors='blue', edgecolors='blue', label=r'He$^+$')
    if c.He2:
        ax.scatter(time, data[0], marker='.', facecolors='green', edgecolors='none', label=r'He2$^+$')


    ax.set_ylabel(r'n$_{obs}$ ($cm^{-3}$)', fontsize=10)
    ax.set_yscale('log')
    ax.set_ylim([0, 1.2])
    ax.legend(loc='center left', bbox_to_anchor=label_box, edgecolor='k')

    tick_positions = [0.01, 0.10, 1]
    tick_labels = [0.01, 0.10, 1.00]

    format_axis(ax, tick_positions, tick_labels, False)

    return

# plots an energy spectogram histogram
def e_spectrogram_plotter(time, data, ax, plot_info):
    cmap = mpl.colormaps['gist_rainbow']
    cmap.set_under(color='white')

    counts, x_edges, y_edges, image = ax.hist2d(time, data, bins=100, cmap=cmap, range=[[0.1, 10]], alpha=1, vmin=1e8, vmax=1e12)

    ax.set_ylabel('E/q (KeVee)', fontsize=10)
    ax.set_ylim([0, 2])

    tick_positions = [0.1, 1, 10]
    tick_labels = [0.1, 1, 10]
    format_axis(ax, tick_positions, tick_labels, False)

    return

# plots the magnetic field data (plots a line vs time)
def mag_field_plotter(time, data, color, label, ax, plot_info):
    ax.axhline(0, color='k', linestyle='dotted', alpha=0.9, linewidth=0.5)
    ax.plot(time, data, linewidth=0.5, color=color)
    ax.set_ylabel(label, fontsize=10)

    # calculates the min and max values for the magnetic field data being shown
    min_val = int(round(np.min(data), -2))
    max_val = int(round(np.max(data), -2))
    tick_positions = np.arange(min_val, max_val, 100)
    format_axis(ax, tick_positions, 0, True)
    return

# plots the distance from the magnetopause crossing
def distance_plotter(time, data, ax):
    ax.axhline(1000, color='k', linestyle='dotted', alpha=1, linewidth=1)
    ax.axhline(-1000, color='k', linestyle='dotted', alpha=1, linewidth=1)
    ax.plot(time, data, linewidth=1.2, color='brown')
    ax.set_ylabel('d MP [Km]', fontsize=10)

    min_val = int(round(np.min(data), -2))
    max_val = int(round(np.max(data), -2))
    tick_positions = np.arange(min_val, max_val, 1000)
    format_axis(ax, tick_positions, 0, True)


# sets the axes for the subplots based ont he figure size and number of desired subplots
def set_subplots(NUM_SUBPLOTS, fig):
    x = []
    y = []
    ax_list = []
    rows = int((NUM_SUBPLOTS) * c.SUBPLOT_WIDTH)

    gs = gridspec.GridSpec(rows, 21, hspace=0.25)

    for i in range(0, NUM_SUBPLOTS +1):
        x.append(int(c.SUBPLOT_WIDTH * i ))

    # creates a list of axes to assign each subplot to
    i = 0
    while i < NUM_SUBPLOTS:
        axi = fig.add_subplot(gs[x[i]:x[i + 1], 0:20])
        ax_list.append(axi)
        i += 1

    return ax_list, gs, x

