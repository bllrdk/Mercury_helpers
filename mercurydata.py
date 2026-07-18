# Imports
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import sys
from matplotlib.patches import Wedge
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
import plotly.graph_objects as go

# Other Files
import constants as c
import read_data as rd
import plotting_functions as pf
import data_file_functions as dff
import statistical_analysis_functions as saf
import epoch_analysis as ea
import plot_magnetopause_mercury as pmm
import plot_bow_shock_mercury as pbm

class Mercury_Data:
    def __init__(self, array, name):
        self.name = name
        self.interp_type = array[0].interp_type
        self.orbit = []

        ## time arrays
        self.time = []
        self.dt_time = []
        self.b_time = []
        self.dtb_time = []
        self.delta = array[0].delta
        self.b_delta = array[0].b_delta
        self.x = []
        self.y = []
        self.z = []
        self.distance= []

        ## attributes
        self.h_jdist = []
        self.h_intflux = []
        self.h_fdist = []

        self.z_fips_clock_angle = []
        self.z_fips_r_angle = []

        ## compostions
        self.counts_he2 = []
        self.counts_he1 = []
        self.counts_o = []
        self.counts_na = []
        self.cluster = []
        self.cluster_flag = []

        self.comp_he2 = []
        self.comp_he1 = []
        self.comp_o = []
        self.comp_na = []

        self.na_jdist = []

        ## magnetic
        self.bx = []
        self.bz = []
        self.bmag = []

        # positioning
        self.mlat = []
        self.alt = []
        self.lt = []

        # boundaries
        self.x_idx = []
        self.direction = []
        self.o_direction = []

        ## saves all file data into arrays for cross-orbit comparison
        for i in array:
            (orbit,time, b_time, h_jdist, h_intflux,z_fips_clock_angle,
             z_fips_r_angle, counts_he2, counts_he1, counts_o, counts_na, comp_he2,
            comp_he1, comp_o, comp_na, na_jdist, bx, bz, bmag, mlat, alt, x_idx,
            direction, x, y, z, distance, cluster_attributes, o_direction, h_fdist, cluster_flag) = i.unpack_data()
            self.orbit.append(orbit)
            self.time.append(time)
            self.b_time.append(b_time)
            self.x.append(x)
            self.y.append(y)
            self.z.append(z)
            self.h_jdist.append(h_jdist)
            self.h_intflux.append(h_intflux)
            self.z_fips_clock_angle.append(z_fips_clock_angle)
            self.z_fips_r_angle.append(z_fips_r_angle)
            self.counts_he2.append(counts_he2)
            self.counts_he1.append(counts_he1)
            self.counts_o.append(counts_o)
            self.counts_na.append(counts_na)
            self.comp_he2.append(comp_he2)
            self.comp_he1.append(comp_he1)
            self.comp_o.append(comp_o)
            self.comp_na.append(comp_na)
            self.bx.append(bx)
            self.bz.append(bz)
            self.bmag.append(bmag)
            self.mlat.append(mlat)
            self.alt.append(alt)
            self.x_idx.append(x_idx),
            self.direction.append(direction)
            self.distance.append(distance)
            self.cluster.append(cluster_attributes)
            self.o_direction.append(o_direction)
            self.h_fdist.append(h_fdist)
            self.na_jdist.append(na_jdist)
            self.cluster_flag.append(cluster_flag)

    # superimposed epoch analysis by file
    def superimposed_epoch_analysis(self, data, half_window):

        if self.interp_type == 'time':
            ## set up epoch time array
            delta = self.delta.total_seconds()

        if self.interp_type == 'distance':
            ## set up epoch distance array
            delta = self.delta

        half_idxs = half_window / delta
        time_indices = np.arange(0, int(2 * half_idxs)-1, 1)


        ## adjust other arrays based on epoch array
        si = []
        ei = []
        for i in range(0, len(data)):
            si.append(int(self.x_idx[i] - half_idxs))
            ei.append(int(self.x_idx[i] + half_idxs))

        indexed_data = []
        for j in range(0, len(data)):
            s = si[j]
            e = ei[j]
            current_data = data[j]
            adjusted_data = []
            for x in range(s, e):
                if x < 0: adjusted_data.append(np.nan)
                elif x >= len(current_data): adjusted_data.append(np.nan)
                else: adjusted_data.append(current_data[x])
            indexed_data.append(adjusted_data)



        mean_array = []
        q1_array = []
        q3_array = []
        median_array = []
        ## calculate statistics for each time point
        for t in time_indices:
            t_data = []
            for i in range(0, len(indexed_data)-1):
                t_data.append(indexed_data[i][t])
            mean_array.append(np.nanmean(t_data))
            q1_array.append(np.nanpercentile(t_data, 25))
            q3_array.append(np.nanpercentile(t_data, 75))
            median_array.append(np.nanmedian(t_data))

        ## return calculated statistical arrays

        return mean_array, median_array, q1_array, q3_array, time_indices

    # plot the superimposed epoch results
    def plot_epoch(self, half_window):

        fig = plt.figure(figsize=(9, 8))
        fig.set_dpi(100)

        # SUBPLOTS
        ax_list, gs, x = pf.set_subplots(c.sea_NUM_SUBPLOTS, fig)
        fig.suptitle( 'Superimposed Epoch Analysis for ' + self.name , fontsize=20)

        subplot = 0
        ## for attributes turned on in constants.py

        if c.sea_He2:
            data = self.counts_he2
            plot_info = c.PLOT_INFO[4]
            mean, median, q1, q3, e_time = self.superimposed_epoch_analysis(data, half_window)
            ea.epoch_plotter(e_time, mean, median, q1, q3, ax_list[subplot], plot_info)
            subplot += 1

        if c.sea_He1:
            data = self.counts_he1
            plot_info = c.PLOT_INFO[5]
            mean, median, q1, q3, e_time = self.superimposed_epoch_analysis(data, half_window)
            ea.epoch_plotter(e_time, mean, median, q1, q3, ax_list[subplot], plot_info)
            subplot += 1

        if c.sea_O:
            data = self.counts_o
            plot_info = c.PLOT_INFO[6]
            mean, median, q1, q3, e_time = self.superimposed_epoch_analysis(data, half_window)
            ea.epoch_plotter(e_time, mean, median, q1, q3, ax_list[subplot], plot_info)
            subplot += 1

        if c.sea_Na:
            data = self.counts_na
            plot_info = c.PLOT_INFO[7]
            mean, median, q1, q3, e_time = self.superimposed_epoch_analysis(data, half_window)
            ea.epoch_plotter(e_time, mean, median, q1, q3, ax_list[subplot], plot_info)
            subplot += 1

        if c.sea_BX:
            data = self.bx
            plot_info = c.PLOT_INFO[8]
            mean, median, q1, q3, e_time = self.superimposed_epoch_analysis(data, half_window)
            ea.epoch_plotter(e_time, mean, median, q1, q3, ax_list[subplot], plot_info)
            subplot += 1

        if c.sea_BZ:
            data = self.bz
            plot_info = c.PLOT_INFO[9]
            mean, median, q1, q3, e_time = self.superimposed_epoch_analysis(data, half_window)
            ea.epoch_plotter(e_time, mean, median, q1, q3, ax_list[subplot], plot_info)
            subplot += 1

        if c.sea_MAG_FIELD:
            data = self.bmag
            plot_info = c.PLOT_INFO[10]
            mean, median, q1, q3, e_time = self.superimposed_epoch_analysis(data, half_window)
            ea.epoch_plotter(e_time, mean, median, q1, q3, ax_list[subplot], plot_info)
            subplot += 1

        if c.sea_DISTANCE:
            data = self.distance
            plot_info = c.PLOT_INFO[11]
            mean, median, q1, q3, e_time = self.superimposed_epoch_analysis(data, half_window)
            ea.epoch_plotter(e_time, mean, median, q1, q3, ax_list[subplot], plot_info)
            subplot += 1


        start = e_time[0]
        end = e_time[-1]

        ## calculates axis information for the epoch plots
        tick_positions = np.linspace(start, end, 5)
        if self.interp_type == 'time':
            tick_labels = [-half_window/60, -half_window/120, 0, half_window/120, half_window/60]
            ax_list[-1].set_xlabel('Time From Magnetopause Crossing (min)', fontsize=12)
        if self.interp_type == 'distance':
            tick_labels = [-half_window, -half_window/2, 0, half_window/2, half_window]
            ax_list[-1].set_xlabel('Distance From Magnetopause Crossing (km)', fontsize=12)
        ax_list[-1].set_xticks(tick_positions, labels=tick_labels)

        plt.figtext(0.7, 0.89, f'Number of Events: {len(self.orbit)}')

        if c.sea_SAVE:
            plt.savefig(c.SAVE_FOLDER + 'O' + str(self.orbit))
        if c.sea_SHOW:
            plt.show()

    # plots 2d plots for various cluster attributes
    def plot_scatter(self):

        ## loops through various combinations of attributes
        for y in range(0, 6):
            fig = plt.figure(figsize=(9, 8))
            fig.set_dpi(100)
            handles = []

            # loops through orbits
            for j in range(0, len(self.cluster)):
                cl = self.cluster[j]
                o_direction = self.o_direction[j][2]
                h_flux = self.h_intflux[j]
                bmag = self.bmag[j]
                # loops through clusters within the orbit
                for i in range(0, len(cl)):
                    color = 'k'

                    ## define all the attributes
                    if bmag[cl[i].mid] > 200: color = 'red'
                    if bmag[cl[i].mid] < 200: color = 'blue'


    
                    start = cl[i].start
                    end = cl[i].end
                    mid = cl[i].mid
                    counts = cl[i].counts

                    start_dist = cl[i].start_dist
                    end_dist = cl[i].end_dist
                    mid_dist = cl[i].mid_dist
                    s_err = abs(mid_dist - start_dist)
                    e_err = abs(end_dist - mid_dist)
                    dist_err = [[s_err], [e_err]]
    
                    start_lt = cl[i].start_lt
                    end_lt = cl[i].end_lt
                    mid_lt = cl[i].mid_lt
                    s_err = mid_lt - start_lt
                    e_err = end_lt - mid_lt
                    lt_err = [[s_err], [e_err]]
    
                    start_alt = cl[i].start_alt
                    end_alt = cl[i].end_alt
                    mid_alt = cl[i].mid_alt
                    s_err = abs(mid_alt - start_alt)
                    e_err = abs(end_alt - mid_alt)
                    alt_err = [[s_err], [e_err]]
    
                    start_mlat = cl[i].start_mlat
                    end_mlat = cl[i].end_mlat
                    mid_mlat = cl[i].mid_mlat
                    s_err = abs(mid_mlat - start_mlat)
                    e_err = abs(end_mlat - mid_mlat)
                    mlat_err = [[s_err], [e_err]]
    
                    h_mid = h_flux[mid]

                    '''
                    if cl[i].time == 'dawn': color = 'red'
                    if cl[i].time == 'post dawn': color = 'orange'
                    if cl[i].time == 'pre dusk': color = 'purple'
                    if cl[i].time == 'dusk': color = 'blue'
                    if cl[i].time == 'day': color = 'goldenrod'
                    '''
                    
                    xlabel = 'Local Time'
                    start_x = start_lt
                    width_x = end_lt - start_lt
                    x_data = mid_lt
                    x_err = lt_err

                    ## defines the plot info for the loop
                    if y == 0:
                        ylabel = 'Distance from the Magnetopause [km]'
                        start_y = start_dist
                        width_y = end_dist - start_dist
                        y_data = mid_dist
                        y_err = dist_err
                    if y == 1:
                        ylabel = 'MLAT'
                        start_y = start_mlat
                        width_y = end_mlat - start_mlat
                        y_data = mid_mlat
                        y_err = mlat_err
                    if y == 2: 
                        ylabel = 'Altitude [km]'
                        start_y = start_alt
                        width_y = end_alt - start_alt
                        y_data = mid_alt
                        y_err = alt_err
                    if y == 3: 
                        ylabel = 'Counts'
                        start_y = counts
                        width_y = .5
                        y_data = counts
                        y_err = [[0], [0]]
                    if y == 4: 
                        ylabel = 'Maximum'
                        start_y = cl[i].max
                        width_y = .5
                        y_data = cl[i].max
                        y_error = [[0], [0]]
                    if y == 5: 
                        xlabel = 'Distance from the Magnetopause'
                        start_x = start_dist
                        width_x = end_dist - start_dist
                        x_data = mid_dist
                        x_err = dist_err
                        ylabel = 'MLAT'
                        start_y = start_mlat
                        width_y = end_mlat - start_mlat
                        y_data = mid_mlat 
                        y_err = mlat_err

                    #x = start_x
                    #y = start_y
                    #xw = width_x
                    #yw = width_y

                    # plots the cluster information
                    plt.errorbar(x_data, y_data, xerr=x_err, yerr=y_err, color=color, capsize=5, marker='o', label=cl[i].time)
                    #plt.gca().add_patch(Rectangle((x,y), xw, yw, facecolor=color))

            custom_dots = [Line2D([0], [0], marker='o', color='red',),
                            Line2D([0], [0], marker='o', color='orange',),
                            Line2D([0], [0], marker='o', color='goldenrod'),
                           Line2D([0], [0], marker='o', color='purple'),
                           Line2D([0], [0], marker='o', color='blue'),]
            plt.legend(custom_dots, ['Dawn', 'Post Dawn', 'Day', 'Pre Dusk', 'Dusk'])

            plt.title(xlabel + ' vs ' + ylabel + ' for Identified Clusters', fontsize=15)
            plt.xlabel(xlabel + ' [km]', fontsize = 12)
            plt.ylabel(ylabel + ' [degrees]', fontsize = 12)
            plt.show()

    ## plots the orbital paths for the identified clusters
    def plot_orbital_direction_stacked(self):
        fig = plt.figure(figsize=(5, 10))
        fig.set_dpi(100)
        ax_y, ax_z, ax_yz = fig.subplots(3, 1)

        i = 0
        for ax in [ax_y, ax_z, ax_yz]:
            w1 = Wedge((0, 0), 1, 270, 90, fc='lightgray')
            if i != 2:
                w2 = Wedge((0, 0), 1, 90, 270, fc='gray')
            else:
                w2 = Wedge((0, 0), 1, 90, 270, fc='lightgray')
            for w in [w1, w2]:
                ax.add_patch(w)
                ax.set_aspect('equal')
                if i != 2:
                    ax.set_xlabel(r'X $[R_m]$', fontsize=12)
                else:
                    ax.set_xlabel(r'Y $[R_m]$', fontsize=12)
                ax.set_xlim(3, -3)
            i += 1

        ## loop through each orbit
        for i_orbit in range(0, len(self.orbit)):
            xo = self.x[i_orbit] / c.RADIUS
            yo = self.y[i_orbit] / c.RADIUS
            zo = self.z[i_orbit] / c.RADIUS

            mp_idx = self.x_idx[i_orbit]

            #ax_y.scatter(xo[mp_idx], yo[mp_idx], color='magenta', alpha=1 )
            #ax_z.scatter(xo[mp_idx], zo[mp_idx], color='magenta', alpha=1)

            for cl in self.cluster[i_orbit]:
                start = cl.start
                end = cl.end
                x0 = cl.mid - cl.start

                x = self.x[i_orbit][start:end] / c.RADIUS
                y = self.y[i_orbit][start:end] / c.RADIUS
                z = self.z[i_orbit][start:end] / c.RADIUS

                #if self.o_direction[i_orbit][0] > 0:
                    #color = 'red'
                #else: color =  'blue'

                if cl.time == 'dawn': color = 'red'
                if cl.time == 'post dawn': color = 'orange'
                if cl.time == 'pre dusk': color = 'purple'
                if cl.time == 'dusk': color = 'blue'
                if cl.time == 'day': color = 'goldenrod'


                # plots the orbit lines
                ax_y.plot(xo, yo, color='k', alpha=0.1)
                ax_z.plot(xo, zo, color='k', alpha=0.1)
                ax_yz.plot(yo, zo, color='k', alpha=0.1)

                # plot the magnetopause lines
                pmm.plot_mp_model('XY', ax_y)
                pmm.plot_mp_model('XZ', ax_z)
                pmm.plot_mp_model('YZ', ax_yz)

                # plots the arrows and duration of each cluster
                plot =  ax_y.plot(x, y, color=color, alpha=1, label=cl.time)
                arrow_y = x[x0 + 1], y[x0 + 1], x[x0 + 1] - x[x0], y[x0 + 1] - y[x0]
                ax_y.arrow(*arrow_y, color=color, length_includes_head=True,
                           head_width=0.07, head_length=0.07, shape='full')


                ax_z.plot(x, z, color=color, alpha=1, label=cl.time)
                arrow_z = x[x0 + 1], z[x0 + 1], x[x0 + 1] - x[x0], z[x0 + 1] - z[x0]
                ax_z.arrow(*arrow_z, color=color, length_includes_head=True,
                           head_width=0.07, head_length=0.07)

                ax_yz.plot(y, z, color=color, alpha=1, label=cl.time)
                arrow_yz = y[x0 + 1], z[x0 + 1], y[x0 + 1] - y[x0], z[x0 + 1] - z[x0]
                ax_yz.arrow(*arrow_yz, color=color, length_includes_head=True,
                           head_width=0.07, head_length=0.07)

        custom_dots = [Line2D([0], [0], marker='o', color='red', ),
                       Line2D([0], [0], marker='o', color='orange', ),
                       Line2D([0], [0], marker='o', color='goldenrod'),
                       Line2D([0], [0], marker='o', color='purple'),
                       Line2D([0], [0], marker='o', color='blue'), ]
        #ax_y.legend(custom_dots, ['Dawn', 'Post Dawn', 'Day', 'Pre Dusk', 'Dusk'], loc='center right')

        # labels the plots
        ax_y.set_ylabel(r'Y $[R_m]$', fontsize = 12)
        ax_y.set_ylim(3, -3)

        ax_z.set_ylabel(r'Z $[R_m]$', fontsize = 12)
        ax_z.set_ylim(-3, 3)

        ax_yz.set_ylabel(r'Z $[R_m]$', fontsize = 12)
        ax_yz.set_ylim(-3, 3)

        fig.suptitle('Messenger Orbits for Clusters', fontsize=15)
        plt.show()

    # plots histograms of cluster attributes
    def plot_cluster_histogram(self):
        fig = plt.figure(figsize=(9, 8))
        fig.set_dpi(100)

        hist_data = []
        for j in range(0, len(self.orbit)):
            for cl in self.cluster[j]:
                hist_data.append(cl.mid_dist)

        #plt.hist(hist_data, bins=11, range=(6, 17))
        plt.hist(hist_data, bins=11)
        plt.show()

    # plot overlapping plot for clusters
    def plot_cluster_overlap(self, flag):
        fig = plt.figure(figsize=(5, 10))
        fig.set_dpi(100)

        ax1, ax2 = fig.subplots(2, 1)

        for j in range(0, len(self.orbit)):
            for cl in self.cluster[j]:
                if cl.flag == 1: color = 'blue'
                if cl.flag == 2: color = 'goldenrod'
                if cl.flag == flag or flag == 0:
                    x_data = np.arange(0, cl.end - cl.start, 1)
                    ax1.plot(x_data, self.distance[j][cl.start:cl.end], color=color)

                    x_data_shift = np.arange(cl.start - cl.max_idx, cl.end - cl.max_idx, 1)
                    ax2.plot(x_data_shift, self.distance[j][cl.start:cl.end], color=color)
        plt.show()


    def plot_orbital_direction_3d(self):
        fig = plt.figure(figsize=(5, 10))
        fig.set_dpi(100)
        ax = plt.figure().add_subplot(projection='3d')

        i = 0

        ## loop through each orbit
        for i_orbit in range(0, len(self.orbit)):
            xo = self.x[i_orbit] / c.RADIUS
            yo = self.y[i_orbit] / c.RADIUS
            zo = self.z[i_orbit] / c.RADIUS

            for cl in self.cluster[i_orbit]:
                start = cl.start
                end = cl.end
                x0 = cl.mid - cl.start

                x = self.x[i_orbit][start:end] / c.RADIUS
                y = self.y[i_orbit][start:end] / c.RADIUS
                z = self.z[i_orbit][start:end] / c.RADIUS

                # if self.o_direction[i_orbit][0] > 0:
                # color = 'red'
                # else: color =  'blue'

                if cl.time == 'dawn': color = 'red'
                if cl.time == 'post dawn': color = 'orange'
                if cl.time == 'pre dusk': color = 'purple'
                if cl.time == 'dusk': color = 'blue'
                if cl.time == 'day': color = 'goldenrod'

                # plots the orbit lines
                ax.plot(xo, yo, zo,  color='k', alpha=0.1)

                # plots the arrows and duration of each cluster
                ax.plot(x, y, z, color=color, alpha=1, label=cl.time)
                #arrow_y = x[x0 + 1], y[x0 + 1], x[x0 + 1] - x[x0], y[x0 + 1] - y[x0]
                #ax.arrow(*arrow_y, color=color, length_includes_head=True,
                           #head_width=0.07, head_length=0.07, shape='full')

        # draw sphere
        u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
        x = np.cos(u) * np.sin(v)
        y = np.sin(u) * np.sin(v)
        z = np.cos(v)
        ax.plot_surface(x, y, z, color="gray", alpha=0.5)

        pmm.plot_mp_model('XYZ', ax)

        # 6. Customize labels and display
        ax.view_init(elev=0, azim=0)
        ax.set_title('3D orbit')
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')
        ax.set_zlabel('Z Axis')
        ax.set_xlim((-3, 3))
        ax.set_ylim((-3, 3))
        ax.set_zlim((-3, 3))
        plt.show()