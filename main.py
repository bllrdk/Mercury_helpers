# Imports
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import sys
import os

# Other Files
import constants as c
import read_data as rd
import plotting_functions as pf
import data_file_functions as dff
import statistical_analysis_functions as saf
import epoch_analysis as ea
import mercurydata as md
import data_types as d

'''                   
▄▄▄▄   ▄▄▄ ▄▄▄▄▄▄ ▄▄▄  
██▀██ ██▀██  ██  ██▀██ 
████▀ ██▀██  ██  ██▀██ 
'''

## reads in pickled data
if c.PKL:
    print('Pickled data is being used')
    data = dff.read_pickle_data('data/pkl/data.pkl')
    dawndusk_data = dff.read_pickle_data('data/pkl/dawnduskdata.pkl')
    day_data = dff.read_pickle_data('data/pkl/day_data.pkl')

## creating a new pickled data set
else:
    ## different ways to read in files (time string, orbit number, loop through files)
    if c.BY_TIME:
        ## replace this with reading in an outside list of event time strings
        event_starts = ['2011-04-07T024645', '2011-06-08T11645']
        ## fix above
        list_loop = rd.string_list_to_time_list(event_starts, '%Y-%m-%dT%H%M%S')

    if c.BY_ORBIT:
        list_loop = [c.ORBIT]

    if c.BY_FILE:
        list_loop = np.arange(0, c.NUM_FILES, 1)


    '''                                                     
    ▄▄     ▄▄▄   ▄▄▄  ▄▄▄▄     ▄▄▄▄ ▄▄▄▄▄▄ ▄▄▄  ▄▄▄▄  ▄▄▄▄▄▄ 
    ██    ██▀██ ██▀██ ██▄█▀   ███▄▄   ██  ██▀██ ██▄█▄   ██   
    ██▄▄▄ ▀███▀ ▀███▀ ██      ▄▄██▀   ██  ██▀██ ██ ██   ██   
                                                             
    '''

    orbit_list = []
    dawndusk_data = []
    day_data = []

    ## loops through each separate orbit file
    for event in list_loop:

        file_data = rd.read_data(event)

        ## stops the code if the data file orbit doesn't match the desired orbit
        if c.BY_ORBIT and file_data.orbit() != c.ORBIT:
            print('Orbit is not available, or does not line up with the correct file')
            sys.exit()

        ## interpolate the data by time -- allows for all data sets to be uniform for epoch analysis
        if c.INTERPOLATE_TIME:
            delta = file_data.time[1] - file_data.time[0]
            b_delta = file_data.b_time[1] - file_data.b_time[0]
            file_data.interpolate_data_time(delta, b_delta)
            file_data.interp_type = 'time'

        ## interpolates the data by distance -- allows for all data sets to be uniform for epoch analysis
        if c.INTERPOLATE_DIST:
            delta = abs(file_data.distance[1] - file_data.distance[0])
            file_data.interpolate_data_dist(delta)
            file_data.calculate_crossing_direction()
            file_data.interp_type = 'distance'

        ## finds the clusters in each file based on parameters set in the functions
        file_data.count_based_flag()
        file_data.find_clusters(1)
        file_data.purge_clusters(3)

        ## plots the orbital paths for each file
        file_data.plot_orbital_direction()
        ## plots the time series plots for each file (centered on the magnetopause crossing)
        if c.PLOT:
            file_data.plot_file_timeseries(c.HALF_LENGTH_TIME * 2, c.PLOT_INFO)


        # saving data from each file into a list
        orbit_list.append(file_data)
        if file_data.cluster_flag == 1 or file_data.cluster_flag == 3:
            dawndusk_data.append(file_data)
        if file_data.cluster_flag == 2 or file_data.cluster_flag == 3:
            day_data.append(file_data)


    '''
    ▄▄     ▄▄▄   ▄▄▄  ▄▄▄▄    ▄▄▄▄▄ ▄▄  ▄▄ ▄▄▄▄
    ██    ██▀██ ██▀██ ██▄█▀   ██▄▄  ███▄██ ██▀██
    ██▄▄▄ ▀███▀ ▀███▀ ██      ██▄▄▄ ██ ▀██ ████▀
    '''

    ## saves file data into arrays of the information across files
    data = md.Mercury_Data(orbit_list, 'All Data')
    dawndusk_data = md.Mercury_Data(dawndusk_data, 'Dawn and Dusk')
    day_data = md.Mercury_Data(day_data, 'Dayside')



## saves pickle files for newly generated data
if c.SAVE_PKL:
    dff.pickle_data(data, 'data/pkl/data.pkl')
    dff.pickle_data(dawndusk_data, 'data/pkl/dawnduskdata.pkl')
    dff.pickle_data(day_data, 'data/pkl/day_data.pkl')


'''
▄▄▄▄  ▄▄     ▄▄▄ ▄▄▄▄▄▄ ▄▄▄▄▄▄ ▄▄ ▄▄  ▄▄  ▄▄▄▄ 
██▄█▀ ██    ██▀██  ██     ██   ██ ███▄██ ██ ▄▄ 
██    ██▄▄▄ ▀███▀  ██     ██   ██ ██ ▀██ ▀███▀ 
'''
## saves info for the magnetic field plot info
c.PLOT_INFO[8].data_based_ticks(data.bx[0])
c.PLOT_INFO[8].data_based_ticks(data.bz[0])
c.PLOT_INFO[8].data_based_ticks(data.bmag[0])

## plots scatter plots of some cluster variables
#data.plot_scatter()
## plots the orbital information for the identified clusters
data.plot_orbital_direction_stacked()
#data.plot_orbital_direction_3d()
## plots histogrammed information for the identified clusters
#data.plot_cluster_histogram()
data.plot_cluster_overlap(0)
data.plot_cluster_overlap(1)
data.plot_cluster_overlap(2)