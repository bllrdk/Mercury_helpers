#!/usr/bin/env python3

"""
@author: sarfeldm

This code is adapted from the IDL version 'find_msgr_orbit_dir.pro' originally created by Jim Raines. 

It finds the MESSENGER oribit direction from a .csv file containing the data for a given orbit number. 

Return values:
 1: MESSENGER ascends through the dayside and descends through the nightside
 2: MESSENGER ascends through the nightside and descends through the dayside
-1: Orbit direction cannot be determined 

"""

#### will include once created 

def find_msgr_orbit_dir(x, z, mag_lat):
    
    #need to isolate one hemisphere to determine latitude change 
    #first trying dayside (ds) then nightside (ns)
    filter = (x >= 0) & (z>=0)
    hemi = 'ds'
    if len(filter) <2: 
        filter = (x <= 0) & (z>=0)
        hemi = 'ns'
    if len(filter) <2: 
        print('Cannot Determine: Need 2 points for change in latitude calc')
        return -1 

    #determining latitude change 
    #selecting 2 points 1/3 from end of array to eliminate edge effects 
    mag_lat_masked = mag_lat[filter]
    frac = int(len(mag_lat_masked)/3)
    #print(f'len of mag_lat_masked is {len(mag_lat_masked)}')
#the .iloc assumes we're using a Pandas dataframe, which does indexing weird
    delta_lat = mag_lat_masked.iloc[-frac] - mag_lat_masked.iloc[frac]
    if delta_lat == 0: 
        print('Cannot Determine: change in latitude is 0')
        return -1 
    
    #determine direction based on hemisphere
    if hemi == 'ds':
        if delta_lat>0: return 1    #lat is increasing so SC is ascending through ds
        elif delta_lat<0: return 2  #lat is decreasing so SC is descending through ds

    if hemi == 'ns': 
        if delta_lat>0: return 2    #lat is increasing so SC is ascending through ns
        elif delta_lat<0: return 1  #lat is increasing so SC is descending through ns

#generate some data to see if this works 

# ##should return 1 
# sample_x = np.arange(1,100,1) #ds 
# sample_z = np.arange(1,100,1) 
# mag_lats = np.linspace(0,180,99) 

# dir = find_msgr_orbit_dir(sample_x,sample_z, mag_lats)
# print(dir) #success 
        
# #should return 2 
# sample_x = np.arange(1,100,1) #ds 
# sample_z = np.arange(1,100,1) 
# mag_lats = np.linspace(180,0,99) 

# dir = find_msgr_orbit_dir(sample_x,sample_z, mag_lats)
# print(dir) #success 
