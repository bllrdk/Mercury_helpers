# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 10:32:25 2024

@author: mthacket

Purpose: This Python function plots an outline of Mercury in terms of Rm (Mercury 
radius = 2440 km) in MSO coordinates (Mercury-Solar-Orbital, with Mercury's 
geometric center as the origin).
                                     
Major edit history:
    -- 6/4/2024: File/code created, using code written for Quals
"""

import numpy as np
import matplotlib.pyplot as plt

def plot_outline_mercury(ax, n=1000, ):
    # "ax" is the axes object used to make the plot. If the plot is made 
    #    with "fig, ax = ", then pass that ax in here. 
    # "n" is the number of points to plot the outline with. Default is 1000.
    
    merc_outline_x = np.linspace(-1,1,n)
    merc_outline_y_top = np.sqrt(1-merc_outline_x**2)
    merc_outline_y_bottom = -1*np.sqrt(1-merc_outline_x**2)
    ax.plot(merc_outline_x,merc_outline_y_top, color='black', label="Mercury")
    ax.plot(merc_outline_x,merc_outline_y_bottom, color='black')

