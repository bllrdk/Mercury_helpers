# Imports
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import sys
from matplotlib.patches import Wedge
from mpl_toolkits.mplot3d import Axes3D
from itertools import product, combinations
from scipy import cluster

# Other Files
import constants as c
import read_data as rd
import plotting_functions as pf
import data_file_functions as dff
import statistical_analysis_functions as saf
import Cluster as cl

## a class to store all of the data for one orbit
class Orbit_Data:
    def __init__(self, orbit, time, b_time, h_jdist, h_intflux, h_fdist, z_fips_clock_angle, z_fips_r_angle, counts_data,
                 composition_data, na_jdist, bx, bz, bmag, mlat, alt, lt, boundaries_data, met, b_met, x, y, z):
        self.interp_type = 'none'
        self.orbit = orbit

        ## time arrays
        self.time = time
        self.dt_time = saf.time_to_dt(time)
        self.b_time = b_time
        self.dtb_time = saf.time_to_dt(b_time)
        self.delta = 0
        self.b_delta = 0
        self.x = x
        self.y = y
        self.z = z
        self.distance = []


        ## attributes
        self.h_jdist = h_jdist.astype(float)
        self.h_intflux = h_intflux.astype(float)
        self.h_fdist = h_fdist.astype(float)

        self.z_fips_clock_angle = z_fips_clock_angle.astype(float)
        self.z_fips_r_angle = z_fips_r_angle.astype(float)

        ## compostions
        self.counts_he2 = counts_data[0, :].astype(float)
        self.counts_he1 = counts_data[1, :].astype(float)
        self.counts_o = counts_data[2, :].astype(float)
        self.counts_na = counts_data[3, :].astype(float)

        self.comp_he2 = composition_data[0, :].astype(float)
        self.comp_he1 = composition_data[1, :].astype(float)
        self.comp_o = composition_data[2, :].astype(float)
        self.comp_na = composition_data[3, :].astype(float)

        self.na_jdist = na_jdist.astype(float)

        ## magnetic
        self.bx = bx
        self.bz = bz
        self.bmag = bmag

        # positioning
        self.mlat = mlat.astype(float)
        self.alt = alt.astype(float)
        self.lt = lt.astype(float)

        # boundaries
        self.boundaries_data = list(boundaries_data)

    ## identifies the boundary index and direction within a start and stop time
    def redefine_boundaries(self, i, dual):
        file_start = self.time[0]
        file_end = self.time[-1]

        # identifies the direction of the magnetopause crossing
        direction = 'none'
        if dual:
            crossing_idx = 0
            for b in [i, i + 1]:
                if self.boundaries_data[b] >= file_start and self.boundaries_data[b] <= file_end:
                    crossing_idx = np.where(self.time >= self.boundaries_data[b])[0][0]
                    if b == 0: direction = 0  # in
                    if b == 1: direction = 1  # out
        else:
            crossing_idx = []
            for j in range(0, len(self.boundaries_data[i])):
                if self.boundaries_data[i][j] >= file_start and self.boundaries_data[i][j] <= file_end:
                    crossing_idx.append(np.where(self.time >= self.boundaries_data[i][j])[0][0])
        return crossing_idx, direction

    ## calculates the boundary locations and directions of crossing for each boundary
    def calculate_crossing_direction(self):
        self.x_idx, self.direction = self.redefine_boundaries(0, True)
        self.b_idx, self.b_direction = self.redefine_boundaries(2, True)
        self.m_idx, x = self.redefine_boundaries(4, False)
        self.idxs = [self.x_idx, self.b_idx, self.m_idx]

    ## calculates the distances from the magnetopause crossing
    def calc_distance_from_mp_crossing(self):
        x1 = self.x[self.x_idx]
        y1 = self.y[self.x_idx]
        z1 = self.z[self.x_idx]

        # loops through all data and calculates the distance from the orbital location to the crossing point
        i = 0
        for x2, y2, z2 in zip(self.x, self.y, self.z):
            if self.direction == 0:
                ## outside magnetopause
                if i < self.x_idx:
                    self.distance.append(-1 * np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2))
                ## inside magnetopause
                else:
                    self.distance.append(np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2))

            if self.direction == 1:
                # inside magnetopause
                if i < self.x_idx:
                    self.distance.append(np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2))
                # outside magnetopause
                else:
                    self.distance.append(-1 * np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2))
            i = i + 1

    ## plot the orbital pathing for the file
    def plot_orbital_direction(self):
        # calculates the direction of the orbit
        x0 = int(len(self.x)/4)
        i = x0

        x = self.x/c.RADIUS
        y = self.y/c.RADIUS
        z = self.z/c.RADIUS

        self.dx = x[x0 + 1] - x[x0]
        self.dy = y[x0 + 1] - y[x0]
        self.dz = z[x0 + 1] - z[x0]

        '''
        self.dx = x[-1] - x[0]
        self.dy = y[-1] - y[0]
        self.dz = z[-1] - z[0]
        '''
        self.o_direction = [self.dx, self.dy, self.dz]

        ## plots the orbits for each file
        if c.PLOT_ORBITS:
            fig = plt.figure(figsize=(5, 10))
            fig.set_dpi(100)
            ax_y, ax_z = fig.subplots(2, 1)

            for ax in [ax_y, ax_z]:
                w1 = Wedge((0, 0), 1, 270, 90, fc='lightgray')
                w2 = Wedge((0, 0), 1, 90, 270, fc='gray')
                for w in [w1, w2]:
                    ax.add_patch(w)
                    ax.set_aspect('equal')
                    ax.set_xlabel('X [R_m]')
                    ax.set_xlim(2, -2)



            ax_y.plot(x, y, color='k')
            arrow_y = x[x0 + 1], y[x0 + 1], x[x0 + 1] - x[x0], y[x0 + 1] - y[x0]
            ax_y.arrow(*arrow_y, color='k', length_includes_head=True,
                       head_width=0.2, head_length=0.2, shape='full')
            ax_y.set_ylabel('Y [R_m]')
            ax_y.set_ylim(2, -2)


            ax_z.plot(x, z, color = 'k' )
            arrow_z = x[x0 + 1], z[x0 + 1], x[x0 + 1] - x[x0], z[x0 + 1] - z[x0]
            ax_z.arrow(*arrow_z, color='k', length_includes_head=True,
                       head_width=0.2, head_length=0.2)
            ax_z.set_ylabel('Z [R_m]')
            ax_z.set_ylim(-2, 2)

            fig.suptitle('Messenger Orbit: ' + str(self.orbit) + ' ' + str(self.o_direction))
            plt.show()

    # flags which side of the magnetopause clusters are on
    ## (should be retired)
    def count_based_flag(self):
        left = 0
        right = 0
        i = 0
        while i < len(self.time) - 1:
            if self.counts_na[i] >= c.FLAG_COUNTS:
                if self.time[i] <= self.time[self.x_idx]:
                    left = 1
                    i = self.x_idx
                if self.time[i] > self.time[self.x_idx]:
                    right = 1
                    i = len(self.time)
            i += 1

        if left and right:
            self.cluster_loc = 'both'
        elif left and not right:
            self.cluster_loc = 'left'
        elif right and not left:
            self.cluster_loc = 'right'
        else:
            self.cluster_loc = 'none'

    # identifies the locations of clusters of sodium ions
    def find_clusters(self, x):
        max_x = 2
        more_clusters = True
        num_clusters = 0
        flag_val = 0
        cluster_list = []
        mask = np.ones_like(self.counts_na).astype(int)
        ## loops as long as not all of the data points have been gone through
        while more_clusters:
            # removes the previously identified clusters from the data being looked at
            if num_clusters > 0:
                si = cluster_list[num_clusters-1].start
                ei = cluster_list[num_clusters-1].end

                y = si - 0
                if y > 4: y = 4
                z = len(self.counts_na) - ei
                if z > 4: z = 4
                for i in range(si - y, ei + z):
                    mask[i] = 0

            # finds the maximum counts within the rest of the data
            max_val = np.max(self.counts_na * mask)
            mask = mask.astype(int)
            # stops looking for clusters if the maximum counts no longer meets a threshold
            if max_val < max_x:
                more_clusters = False
            # finds the new cluster based on the new maximum location
            else:
                max_idx = np.where(self.counts_na * mask == max_val)[0][0]
                cluster_list.append(self.cluster_attributes(max_idx, max_val, x))

                # flags the types of clusters in the orbit at the orbit level
                # 1 - dawn and dusk, 2 - day, 3 - both
                if flag_val == 0:
                    if cluster_list[num_clusters].flag == 1:
                        flag_val = 1
                    else:
                        flag_val = 2
                if flag_val == 1 and cluster_list[num_clusters].flag == 2:
                        flag_val = 3
                if flag_val == 2 and cluster_list[num_clusters].flag == 1:
                        flag_val = 3

                num_clusters += 1

        self.clusters = cluster_list
        self.cluster_flag = flag_val

    ## sets up the attributes for an identified cluster
    def cluster_attributes(self, max_idx, max_val, x):
        counts_sum = 0
        i = max_idx

        ## loops through the left side of the data
        start_i = i
        while i > 4:
            na0 = self.counts_na[i]
            na1 = self.counts_na[i - 1]
            na2 = self.counts_na[i - 2]
            na3 = self.counts_na[i - 3]
            na4 = self.counts_na[i - 4]
            ## confirms that the counts are not below the threshold for at least 3 consecutive points
            if na0 < x and na1 < x and na2 < x and na3 < x:
                ## if they are, adds this last point and stops the while loop
                counts_sum += na0
                start_i = i
                i = 0
            else:
                # otherwise adds this point and continues looping back towards the start of the data set
                counts_sum += na0
                start_i = i
                i = i - 1

        # loops through the right side of the data
        i = max_idx
        end_i = i
        while i < len(self.time) - 4:
            na0 = self.counts_na[i]
            na1 = self.counts_na[i + 1]
            na2 = self.counts_na[i + 2]
            na3 = self.counts_na[i + 3]
            na4 = self.counts_na[i + 4]
            ## confirms that the counts are not below the threshold for at least 3 consecutive points
            if na0 < x and na1 < x and na2 < x and na3 < x:
                ## if they are, adds this last point and stops the while loop
                counts_sum += na0
                end_i = i
                i = len(self.time)
            else:
                # otherwise adds this point and continues looping towards the end of the data set
                counts_sum += na0
                end_i = i
                i = i + 1

        # defines the cluster and calculates the attributes for the points within it
        cluster = cl.Cluster(start_i, end_i, counts_sum, max_idx, max_val)
        cluster.mid_calculations(self.distance, self.lt, self.alt, self.mlat)
        return cluster

    ## removes clusters that do not meet defined thresholds from the list
    def purge_clusters(self, cut_off):
        '''
        cluster_list = []
        for cl in self.clusters:
            if abs(cl.mid_mlat) <= 45:
                if abs(cl.mid_dist) <= 1000:
                    cluster_list.append(cl)
        '''
        cluster_list = []
        for cl in self.clusters:
            if abs(cl.mid_mlat) <= 45:
                if cl.start_dist / cl.end_dist < 0 :
                    cluster_list.append(cl)
        self.clusters = cluster_list

    # calculates the magnetopause standoff distance
    ## (Not implemented)
    def calculate_mp_standoff(self):
        pressure = 1/2 * self.h_n * self.h_v ** 2
        num = 2 * c.B_MERCURY ** 2
        den = c.Mu0 * pressure
        self.stand_off = (num / den) ** (1/6)

    ## unpacks data from the class so it can be stored in a multi-file array
    def unpack_data(self):
        return (self.orbit, self.time, self.b_time, self.h_jdist, self.h_intflux, self.z_fips_clock_angle,
                self.z_fips_r_angle, self.counts_he2, self.counts_he1, self.counts_o, self.counts_na, self.comp_he2,
                self.comp_he1, self.comp_o, self.comp_na, self.na_jdist, self.bx, self.bz, self.bmag, self.mlat, self.alt, self.x_idx,
                self.direction, self.x, self.y, self.z, self.distance, self.clusters, self.o_direction, self.h_fdist, self.cluster_flag)

    ## interpolates data over time
    def interpolate_data_time(self, delta, b_delta):
        file_start = self.time[0]
        file_end = self.time[-1]
        b_start = self.b_time[0]
        b_end = self.b_time[-1]

        ## calculate the new time array
        i_time = np.arange(file_start, file_end, delta).astype(dt.datetime)
        b_time = np.arange(b_start, b_end, b_delta).astype(dt.datetime)

        ## convert the new time array into datetime objects
        dti_time = saf.time_to_dt(i_time)
        dtb_time = saf.time_to_dt(b_time)

        ## attributes
        #self.distance = saf.interpolate_data(dti_time, self.dt_time, self.distance)
        self.x = saf.interpolate_data(dti_time, self.dt_time, self.x)
        self.y = saf.interpolate_data(dti_time, self.dt_time, self.y)
        self.z = saf.interpolate_data(dti_time, self.dt_time, self.z)

        self.h_jdist = saf.interpolate_data(dti_time, self.dt_time, self.h_jdist)
        self.h_intflux = saf.interpolate_data(dti_time, self.dt_time, self.h_intflux)

        self.z_fips_clock_angle = saf.interpolate_data(dti_time, self.dt_time, self.z_fips_clock_angle)
        self.z_fips_r_angle = saf.interpolate_data(dti_time, self.dt_time, self.z_fips_r_angle)

        ## compostions
        self.counts_he2 = saf.interpolate_data(dti_time, self.dt_time, self.counts_he2)
        self.counts_he1 = saf.interpolate_data(dti_time, self.dt_time, self.counts_he1)
        self.counts_o = saf.interpolate_data(dti_time, self.dt_time, self.counts_o)
        self.counts_na = saf.interpolate_data(dti_time, self.dt_time, self.counts_na)

        self.comp_he2 = saf.interpolate_data(dti_time, self.dt_time, self.comp_he2)
        self.comp_he1 = saf.interpolate_data(dti_time, self.dt_time, self.comp_he1)
        self.comp_o = saf.interpolate_data(dti_time, self.dt_time, self.comp_o)
        self.comp_na = saf.interpolate_data(dti_time, self.dt_time, self.comp_na)

        self.na_jdist = saf.interpolate_data(dti_time, self.dt_time, self.na_jdist)

        ## magnetic
        self.bx = saf.interpolate_data(dtb_time, self.dtb_time, self.bx)
        self.bz = saf.interpolate_data(dtb_time, self.dtb_time, self.bz)
        self.bmag = saf.interpolate_data(dtb_time, self.dtb_time, self.bmag)

        # positioning
        self.mlat = saf.interpolate_data(dti_time, self.dt_time, self.mlat)
        self.alt = saf.interpolate_data(dti_time, self.dt_time, self.alt)
        self.lt = saf.interpolate_data(dti_time, self.dt_time, self.lt)

        ## time
        self.time = i_time
        self.b_time = b_time
        self.dt_time = dti_time
        self.dtb_time = dtb_time
        self.delta = delta
        self.b_delta = b_delta

        self.calculate_crossing_direction()
        self.calc_distance_from_mp_crossing()

    ## interpolates the data by distance
    def interpolate_data_dist(self, delta):
        file_start = self.distance[0]
        file_end = self.distance[-1]

        # sets up the list of distances with a consistent delta
        dti_dist = np.arange(file_start, file_end, delta).astype(float)

        ## interpoles for all the
        ## time
        self.time = saf.interpolate_data(dti_dist, self.distance, self.time)
        self.b_time = saf.interpolate_data(dti_dist, self.distance, self.b_time)
        self.dt_time = saf.interpolate_data(dti_dist, self.distance, self.dt_time)
        self.dtb_time = saf.interpolate_data(dti_dist, self.distance, self.dtb_time)
        self.delta = delta
        self.b_delta = delta

        ## attributes
        self.h_jdist = saf.interpolate_data(dti_dist, self.distance, self.h_jdist)
        self.h_intflux = saf.interpolate_data(dti_dist, self.distance, self.h_intflux)

        self.z_fips_clock_angle = saf.interpolate_data(dti_dist, self.distance, self.z_fips_clock_angle)
        self.z_fips_r_angle = saf.interpolate_data(dti_dist, self.distance, self.z_fips_r_angle)

        ## compostions
        self.counts_he2 = saf.interpolate_data(dti_dist, self.distance, self.counts_he2)
        self.counts_he1 = saf.interpolate_data(dti_dist, self.distance, self.counts_he1)
        self.counts_o = saf.interpolate_data(dti_dist, self.distance, self.counts_o)
        self.counts_na = saf.interpolate_data(dti_dist, self.distance, self.counts_na)

        self.comp_he2 = saf.interpolate_data(dti_dist, self.distance, self.comp_he2)
        self.comp_he1 = saf.interpolate_data(dti_dist, self.distance, self.comp_he1)
        self.comp_o = saf.interpolate_data(dti_dist, self.distance, self.comp_o)
        self.comp_na = saf.interpolate_data(dti_dist, self.distance, self.comp_na)

        self.na_jdist =  saf.interpolate_data(dti_dist, self.distance, self.na_jdist)

        ## magnetic
        self.bx = saf.interpolate_data(dti_dist, self.distance, self.bx)
        self.bz = saf.interpolate_data(dti_dist, self.distance, self.bz)
        self.bmag = saf.interpolate_data(dti_dist, self.distance, self.bmag)

        # positioning
        self.mlat = saf.interpolate_data(dti_dist, self.distance, self.mlat)
        self.alt = saf.interpolate_data(dti_dist, self.distance, self.alt)
        self.lt = saf.interpolate_data(dti_dist, self.distance, self.lt)

        self.distance = dti_dist

    ## plots the time series data for each file
    def plot_file_timeseries(self, time_range, plot_info): ## time range in seconds
        ## function that calculates the start and end times of the plot based on magnetopause crossing time
        START_TIME, END_TIME, si, ei, sb, eb, adj_x_idx = dff.calculate_plot_range(self.time, self.b_time, self.x_idx, time_range)

        # Variables
        subplot = 0

        fig = plt.figure(figsize=(9, 8))
        fig.set_dpi(100)

        # SUBPLOTS
        ax_list, gs, x = pf.set_subplots(c.NUM_SUBPLOTS, fig)
        fig.suptitle('Orbit: ' + str(self.orbit) + '                              Range: ' + str(START_TIME) + ' - ' + str(END_TIME),
            fontsize=12, y=.9, x=0.125, horizontalalignment='left')


        # set up variables based on plot start and stop times
        time = self.time[si:ei]
        b_time = self.b_time[sb:eb]
        z_clock = self.z_fips_clock_angle[si:ei]
        z_r = self.z_fips_r_angle[si:ei]
        h_intflux = self.h_intflux[si:ei]
        counts_data = np.array([self.counts_he2[si:ei], self.counts_he1[si:ei], self.counts_o[si:ei], self.counts_na[si:ei]])
        comp_data = np.array([self.comp_he2[si:ei], self.comp_he1[si:ei], self.comp_o[si:ei], self.comp_na[si:ei]])

        cluster_info = []
        for cl in self.clusters:
            cluster_info.append(cl.adjusted_cluster(si, ei))

        ## plot attributes based on constants.py

        if c.EQ:
            clim = [10e5, 10e9]
            clabel = 'H+ Flux'
            ax_cm = fig.add_subplot(gs[x[subplot]:x[subplot + 1], 20:21])
            pf.eq_plotter(time, self.h_jdist[:, si:ei], ax_list[subplot], ax_cm, clim, clabel, plot_info[0])
            pf.plot_boundary_lines(ax_list[subplot], self.idxs, subplot, si, ei, self.time, self.direction)
            ax_list[subplot].margins(x=0)
            subplot += 1


        ##### ANGLE PLOTS

        if c.ANGLE:
            box_label = (1, .5)
            pf.angle_plotter(time, z_clock, z_r, ax_list[subplot], box_label, plot_info[1])
            pf.plot_boundary_lines(ax_list[subplot], self.idxs, subplot, si, ei, self.time, self.direction)
            ax_list[subplot].margins(x=0)
            subplot += 1

        if c.PITCH_ANGLE:
            pf.pa_plotter(time, z_clock, z_r, ax_list[subplot], plot_info[2])
            pf.plot_boundary_lines(ax_list[subplot], self.idxs, subplot, si, ei, self.time, self.direction)
            ax_list[subplot].margins(x=0)
            subplot += 1

        if c.H_FLUX:
            pf.h_flux_plotter(time, h_intflux, ax_list[subplot], plot_info[3])
            pf.plot_boundary_lines(ax_list[subplot], self.idxs, subplot, si, ei, self.time, self.direction)
            ax_list[subplot].margins(x=0)
            subplot += 1

        ## heavy ion related plots

        if c.COUNTS:
            box_label = (1, .5)
            pf.counts_plotter(time, counts_data, ax_list[subplot], box_label, plot_info[4:7], cluster_info)
            pf.plot_boundary_lines(ax_list[subplot], self.idxs, subplot, si, ei, self.time, self.direction)
            ax_list[subplot].margins(x=0)
            subplot += 1

        if c.NUMBER_DENSITY:
            box_label = (1, .5)
            pf.n_density_plotter(time, comp_data, ax_list[subplot], box_label, plot_info[4:7])
            pf.plot_boundary_lines(ax_list[subplot], self.idxs, subplot, si, ei, self.time, self.direction)
            ax_list[subplot].margins(x=0)
            subplot += 1

        if c.Na_EQ:
            clim = [10e7, 10e11]
            clabel = f'Na PSD \n $(s^3/km^6)$'
            ax_cm = fig.add_subplot(gs[x[subplot]:x[subplot + 1], 20:21])
            pf.eq_plotter(time, self.na_jdist[:, si:ei], ax_list[subplot], ax_cm, clim, clabel, plot_info[0])
            pf.plot_boundary_lines(ax_list[subplot], self.idxs, subplot, si, ei, self.time, self.direction)
            ax_list[subplot].margins(x=0)
            subplot += 1

        ##### MAGNETIC FIELD PLOTS
        if c.ENERGY_SPECTROGRAM:
            pf.e_spectrogram_plotter(time, self.bx[si:ei], ax_list[subplot], plot_info[8])
            pf.plot_boundary_lines(ax_list[subplot], self.idxs, subplot, si, ei, self.time, self.direction)
            ax_list[subplot].margins(x=0)
            subplot += 1

        if c.BX:
            pf.mag_field_plotter(b_time, self.bx[sb:eb], 'red', r'B$_x$ [nT]', ax_list[subplot], plot_info[8])
            pf.plot_boundary_lines(ax_list[subplot], self.idxs, subplot, si, ei, self.time, self.direction)
            ax_list[subplot].margins(x=0)
            subplot += 1

        if c.BZ:
            pf.mag_field_plotter(b_time, self.bz[sb:eb], 'blue', r'B$_z$ [nT]', ax_list[subplot], plot_info[9])
            pf.plot_boundary_lines(ax_list[subplot], self.idxs, subplot, si, ei, self.time, self.direction)
            ax_list[subplot].margins(x=0)
            subplot += 1

        if c.MAG_FIELD:
            pf.mag_field_plotter(b_time, self.bmag[sb:eb], 'k', '|B| [nT]', ax_list[subplot], plot_info[10])
            pf.plot_boundary_lines(ax_list[subplot], self.idxs, subplot, si, ei, self.time, self.direction)
            ax_list[subplot].margins(x=0)
            subplot += 1

        if c.DISTANCE:
            pf.distance_plotter(time, self.distance[si:ei], ax_list[subplot])
            pf.plot_boundary_lines(ax_list[subplot], self.idxs, subplot, si, ei, self.time, self.direction)
            ax_list[subplot].margins(x=0)
            subplot += 1

        ##### X-AXIS FORMATTING
        pf.format_x_labels(time, self.mlat, self.lt, self.alt, ax_list[-1], fig)

        if c.SAVE:
            plt.savefig(c.SAVE_FOLDER + 'O' + str(self.orbit))
        if c.SHOW:
            plt.show()