import pickle
import glob
import numpy as np
from scipy.io import readsav
import datetime as dt
import constants as c

import orbitdata as cdef

## converts a time string into the correct orbit number
def time_to_file(time):

    # orbit 38 2011 04 06 2:38:09 - 04:12:25
    # orbit 59 = 2011-04-16 16:09:15 - 17:44:47
    # orbit 58 = 2011-04-16 04:05:02 - 5:40:25
    orbit = time
    file_idx = orbit_to_file(orbit)
    return file_idx

## finds the correct file given an orbit number
def orbit_to_file(orbit):
    # f:20 - o:58
    file_idx = orbit - 38
    return file_idx

## functions Sarah wrote to process the timing of the data
# propagating UTC
def met_correct(met):
    ## This function takes an array of met values, in units of decimal second. Subtracts
    #  all values past index 0 by index 0

    #print(f'reset_i: {reset_i}')
    met_mod = np.zeros(len(met))

    #print('There was no reset')
    met_mod = met-met[0]
    return met_mod

# getting the appropriate magnetosphere boundary crossings
def boundaries(orbit, utc_start, met, mlat):
    '''
    This takes an orbit number, a utc start time, and an array of orbit MET times
    and returns the magnetopause and bow shock crossing times as datetime objects
    '''
    ##-----copied in from boundary_data.py-----#
    filename = c.CROSS_FILE

    #turning the IDL .sav into a dictionary adjacent struct recarray
    b_cross = readsav(filename, python_dict=True)

    #recarray only has one var, which is another array that contains the data
    b_cross_keys = list(b_cross.keys())
    b_cross = b_cross[b_cross_keys[0]]

    #print(b_cross.dtype.names)
    #('INDEX', 'BS_IN_MET', 'BS_OUT_MET', 'BS_ID', 'MP_IN_MET', 'MP_OUT_MET', 'MP_ID')

    #it looks like INDEX correspods to orbit #, and we want the magnetopause crossings

    cross_index = b_cross['INDEX']
    mp_in_met = b_cross['MP_IN_MET']
    mp_out_met = b_cross['MP_OUT_MET']
    bs_in_met =  b_cross['BS_IN_MET']
    bs_out_met =  b_cross['BS_OUT_MET']

    #only need from orbit 3758 onwards; paring down arrays

    filter = (cross_index == orbit)

    cross_index = cross_index[filter][0]
    mp_in_met = mp_in_met[filter][0]
    mp_out_met = mp_out_met[filter][0]
    bs_in_met = bs_in_met[filter][0]
    bs_out_met = bs_out_met[filter][0]

    start = dt.datetime.strptime(utc_start, '%Y-%m-%dT%H:%M:%S')

    #correcting the MEP of the mp and bs crossings
    mp_in_corr = mp_in_met-met[0]
    mp_out_corr = mp_out_met-met[0]
    bs_in_corr = bs_in_met-met[0]
    bs_out_corr = bs_out_met-met[0]

    #turning the magnetopause crossing MEP times into Datetime objects
    del_in_mp = dt.timedelta(seconds=mp_in_corr)
    mp_in_time = start + del_in_mp

    del_out_mp = dt.timedelta(seconds=mp_out_corr)
    mp_out_time = start + del_out_mp

    #turning the bow shock crossing MEP times into Datetime objects
    del_in_bs = dt.timedelta(seconds=bs_in_corr)
    bs_in_time = start + del_in_bs

    del_out_bs = dt.timedelta(seconds=bs_out_corr)
    bs_out_time = start + del_out_bs

    #turning the mlat times into Datetime objects
    signs = np.sign(mlat)
    mlat0_idx = []
    for i in range(1, len(mlat)-1):
        if signs[i] != signs[i - 1]:
            mlat0_idx.append(i)

    mlat0_time = []
    for i in mlat0_idx:
        mlat0_time.append(dt.timedelta(seconds=i) + start)

    return mp_in_time, mp_out_time, bs_in_time, bs_out_time, mlat0_time

# creating

#creating an array of Datetime objects to use as time
def create_time_array(start, met):
    time = []
    for i in range(len(met)):
        # Calculate total seconds
        if i == 0: time.append(start)
        else:
            #time_float = float(met[i])
            # Create timedelta and add to start date
            delta = dt.timedelta(seconds=met[i])
            date = start + delta
            time.append(date)
    return np.array(time)

# creates a list of the deltas between each time step
def calculate_delta(time):
    delta = []
    for i in range(0, len(time) -1):
        delta.append(time[i+1]-time[i])
    return np.array(delta)

# converts time strings into datetime objects
def string_list_to_time_list(string_list, format):
    new_list = []
    for s in string_list:
       new_list.append(dt.datetime.strptime(s, format))
    return new_list

# converts time strings to datetime objects
def glob_strings_to_times(glob_list):
    glob_times = [s[-39:] for s in glob_list]
    start_strs = [s[0:17] for s in glob_times]
    end_strs = [s[18:35] for s in glob_times]

    start_times = string_list_to_time_list(start_strs, '%Y-%m-%dT%H%M%S')
    end_times = string_list_to_time_list(end_strs, '%Y-%m-%dT%H%M%S')

    return np.array(start_times), np.array(end_times)


### Function that reads in and processes the data
def read_data(event):
    filename = c.DATA_FOLDER + '*.sav'
    glob_list = sorted(glob.glob(filename))

    if c.BY_ORBIT:
        file_idx = orbit_to_file(event)
        file_name = glob_list[file_idx]

    if c.BY_TIME:
        file_stimes, file_etimes = glob_strings_to_times(glob_list)
        file_idx = np.where(file_stimes >= event)[0][0]
        file_name = glob_list[file_idx]

    if c.BY_FILE:
        file_name = glob_list[event]

    sav_data = readsav(file_name, python_dict=True)

    ## Taken from Sarah's code to read in the files with the data alligned correctly

    # recarray only has one var, which is another array that contains the data
    sav_data_keys = list(sav_data.keys())
    sav_data = sav_data[sav_data_keys[0]]

    # define wanted variables out of dict keys
    h_jdist = np.transpose(sav_data['H_JDIST'][0])
    h_nobs = np.transpose(sav_data['H_NOBS'][0])
    h_v_rates = np.transpose(sav_data['H_V_RATES'][0])
    h_fdist = np.transpose(sav_data['H_FDIST'][0])
    z_fips_clock_angle = sav_data['Z_FIPS_CLOCK_ANGLE'][0]
    z_fips_r_angle = sav_data['Z_FIPS_R_ANGLE'][0]
    h_intflux = sav_data['H_INTFLUX'][0]

    bmag = sav_data['BMAG'][0]

    met = sav_data['MET'][0]
    mlat = sav_data['MLAT'][0]
    alt = sav_data['ALT'][0]
    ORBIT = sav_data['ORBIT'][0][0]
    UTC_START = sav_data['UTC_RANGE'][0][0]
    lt = sav_data['LOCT'][0]
    #pa_hist = sav_data['PA_HIST'][0]
    x = sav_data['X'][0]
    y = sav_data['Y'][0]
    z = sav_data['Z'][0]


    ## composition
    he2_data = sav_data['HE2_NOBS'][0]
    he1_data = sav_data['HE_NOBS'][0]
    oxy_data = sav_data['O_NOBS'][0]
    na_data = sav_data['NA_NOBS'][0]

    composition_data = np.array([he2_data, he1_data, oxy_data, na_data])

    ## counts
    he2_data = np.sum(sav_data['HE2_CDIST'][0], axis=1)
    he1_data = np.sum(sav_data['HE_CDIST'][0], axis=1)
    oxy_data = np.sum(sav_data['O_CDIST'][0], axis=1)
    na_data = np.sum(sav_data['NA_CDIST'][0], axis=1)

    counts_data = np.array([he2_data, he1_data, oxy_data, na_data])

    na_jdist = np.transpose(sav_data['NA_JDIST'][0])

    # getting the BX and BZ components is a little tricker
    b = sav_data['B'][0]
    # print(b)
    b_met = np.zeros(len(b))
    bx = np.zeros(len(b))
    bz = np.zeros(len(b))
    for i, tup in enumerate(b):
        b_met[i] = tup[0]
        bx[i] = tup[1]
        bz[i] = tup[3]

    # the UTC start time is a byte object, let's convert that to UTF-8 encoding
    UTC_START = UTC_START.decode('UTF-8')

    start = dt.datetime.strptime(UTC_START, '%Y-%m-%dT%H:%M:%S')

    boundaries_data = boundaries(ORBIT, UTC_START, met, mlat)

    # correcting the lt so the Datetime objects initiate properly
    met = met_correct(met)
    b_met = met_correct(b_met)

    ## creating time arrays for plotting
    time = create_time_array(start, met)
    b_time = create_time_array(start, b_met)

    # returns data into an orbit class data format
    return cdef.Orbit_Data(ORBIT, time, b_time, h_jdist, h_intflux, h_fdist, z_fips_clock_angle, z_fips_r_angle, counts_data, composition_data, na_jdist, bx, bz, bmag, mlat, alt, lt, boundaries_data, met, b_met, x, y, z)

