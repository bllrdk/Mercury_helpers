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

## defines a class for cluster attributes
class Cluster:
     def __init__(self, start, end, counts, max_idx, max):
        self.start = start
        self.end = end

        self.mid = int((end - start) / 2 + start)

        self.counts = counts

        self.max_idx = max_idx
        self.max = max

     ## adjustments to cluster indexes for shifted time series plots
     def adjusted_cluster(self, start_idx, end_idx):
         start = self.start - start_idx
         end = self.end - start_idx
         max_idx = self.max_idx - start_idx

         return Cluster(start, end, self.counts, max_idx, self.max)

    # defines cluster attributes from initialized information and file data
     def mid_calculations(self, distance, local_time, alt, mlat):
        self.start_lt = local_time[self.start]
        self.end_lt = local_time[self.end]
        self.mid_lt = local_time[self.mid]

        self.start_alt = alt[self.start]
        self.mid_alt = alt[self.mid]
        self.end_alt = alt[self.end]

        self.start_mlat = mlat[self.start]
        self.mid_mlat = mlat[self.mid]
        self.end_mlat = mlat[self.end]

        self.mid_dist = distance[self.mid]
        self.start_dist = distance[self.start]
        self.end_dist = distance[self.end]

        ## defines the rough time of day the cluster occurs during
        if self.mid_lt <= 8:
            self.time = 'dawn'
            self.flag = 1
        elif self.mid_lt > 8 and self.mid_lt < 11:
            self.time = 'post dawn'
            self.flag = 2
        elif self.mid_lt >= 15:
            self.time = 'dusk'
            self.flag = 1
        elif self.mid_lt > 13 and self.mid_lt < 15:
            self.time = 'pre dusk'
            self.flag = 2
        else:
            self.time = 'day'
            self.flag = 2








