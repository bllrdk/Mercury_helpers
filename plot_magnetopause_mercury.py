# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 11:02:28 2024

@author: mthacket
Purpose: This Python function plots a projection of Mercury's magnetopause
    into the specified plane. All plotting is done in MSO coordinates 
    (Mercury-Solar-Orbital, with Mercury's geometric center as the origin).
    The planes used are XZ and XY. The magnetopause is modeled with the
    Winslow 2013 Mercury magnetopause model (ref. 1). For the average 
    bow shock placement, parameters from Winslow, 2013 for the average are 
    used.
                                     
Major edit history:
    -- 6/4/2024: File/code created, using code written for Quals.

References:
    -- 1: Winslow, R. M., B. J. Anderson, C. L. Johnson, J. A. Slavin, 
            H. Korth, M. E. Purucker, D. N. Baker, and S. C. Solomon (2013), 
            Mercury's magnetopause and bow shock from MESSENGER Magnetometer 
            observa􀆟ons, Journal of Geophysical Research (Space Physics), 
            118, 2213-2227, doi: htps://doi.org/10.1002/jgra.50237.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import mpl_toolkits.mplot3d.art3d as art3d
import plotly.graph_objects as go
import plotly.figure_factory as ff
from scipy.spatial import Delaunay

def plot_mp_model(view, ax, Rss=1.45, alpha=0.5, Zd=0.196, n=1000, mp_color="blue", mp_linestyle="--"):
    
    # "view" is the view that the user wants: "XZ" or "XY".
    # The magnetopause is modeled as a paraboloid conic section.
    # "Rss" is the subsolar magnetopause distance. Default is 1.45.
    # "alpha" 
    # "Zd" is Mercury's dipole offset w.r.t. its geometric center. Default (and only real) value is 0.196.
    # "n" is the number of points to use to plot the outline.
    
    # The equation is defined polar. Set those up:
    theta = np.linspace(0,170,n)*np.pi/180
    R = Rss*((2/(1+np.cos(theta)))**(alpha))
    # Find the x- and y-components from the polar curve:
    mp_x = R*np.cos(theta)
    
    mp_y_top = R*np.sin(theta)
    mp_y_bottom = -1*R*np.sin(theta)
    
    mp_z_top = R*np.sin(theta)+Zd
    mp_z_bottom = -1*R*np.sin(theta)+Zd
    # Plot the magnetopause model:
    # mp_color = "blue"
    # mp_linestyle = "--"    
    
    if (view == "XY"):
        ax.plot(mp_x, mp_y_top, color=mp_color, linestyle=mp_linestyle)
        ax.plot(mp_x, mp_y_bottom, color=mp_color, linestyle=mp_linestyle)
    if (view == "XZ"):
        ax.plot(mp_x, mp_z_top, color=mp_color, linestyle=mp_linestyle)
        ax.plot(mp_x, mp_z_bottom, color=mp_color, linestyle=mp_linestyle)
    if (view == "YZ"):
        C = Circle((0, Zd), Rss, facecolor='none', edgecolor=mp_color, linestyle=mp_linestyle)
        ax.add_patch(C)
    if (view == 'XYZ'):

        ax.plot(mp_x, mp_y_top, zs=0, zdir='z',  color=mp_color, linestyle=mp_linestyle)
        ax.plot(mp_x, mp_y_bottom,  zs=0, zdir='z',  color=mp_color, linestyle=mp_linestyle)
        ax.plot(mp_x, mp_z_top, zs=0, zdir='y',  color=mp_color, linestyle=mp_linestyle)
        ax.plot(mp_x, mp_z_bottom, zs=0, zdir='y', color=mp_color, linestyle=mp_linestyle)
        C = Circle((0, Zd), Rss, facecolor='none', edgecolor=mp_color, linestyle=mp_linestyle)
        ax.add_patch(C)
        art3d.pathpatch_2d_to_3d(C, z=0, zdir='x')



