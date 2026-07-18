# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 10:41:16 2024

@author: mthacket
Purpose: This Python function plots a projection of Mercury's bow shock
    into the specified plane. All plotting is done in MSO coordinates 
    (Mercury-Solar-Orbital, with Mercury's geometric center as the origin).
    The planes used are XZ and XY. The bow shock is modeled with the
    Slavin 2009 Mercury bow shock model (ref. 1). For the average 
    bow shock placement, parameters from Slavin 2010 (ref. 2) are used.
                                     
Major edit history:
    -- 6/4/2024: File/code created, using code written for Quals.

References:
    -- 1: Slavin, J. A., B. J. Anderson, T. H. Zurbuchen, D. N. Baker, 
            S. M. Krimigis, M. H. Acuña, M. Benna, S. A., Boardsen, 
            G. Gloeckler, R. E. Gold, G. C. Ho, H. Korth, R. L. McNut, 
            J. M. Raines, M. Sarantos, D.Schriver, S. C. Solomon, and 
            P. Trávníček (2009), MESSENGER observa􀆟ons of Mercury's 
            magnetosphere during northward IMF, Geophysical Research Leters,
            36, L02101, doi:htps://doi.org/10.1029/2008GL036158.
    
    -- 2: Slavin (2010) , J. A., B. J. Anderson, D. N. Baker, M. Benna, 
            S. A. Boardsen, G. Gloeckler, R. E. Gold, G. C. Ho, H. Korth, 
            S. M. Krimigis, R. L. McNut, L. R. Nitler, J. M. Raines, 
            M. Sarantos, D. Schriver, S. C. Solomon, R. D. Starr, 
            P. M. Trávníček, and T. H. Zurbuchen (2010), MESSENGER 
            Observations of Extreme Loading and Unloading of Mercury’s 
            Magnetic Tail, Science, 329, 665, 
            doi: htps://doi.org/10.1126/science.1188067.
"""

import numpy as np
import matplotlib.pyplot as plt

def plot_bs_model(view, 
                  X0=0.475, eps=1.04, L=2.59, Zd=0.196,
                  n=1000,
                  bs_color="blue", bs_linestyle="-."):
    
    # "view" is the view that the user wants: "XZ" or "XY".
    # The bow shock is modeled as a conic section.
    # "X0" is the focus of the conic section, along the X-MSO axis. Default is 0.475
    # "eps" is the eccentricity of the conic section. Default is 1.04.
    # "L" is the semi-latus rectum of the conic section. Default is 2.59.
    # "Zd" is Mercury's dipole offset w.r.t. its geometric center. Default (and only real) value is 0.196.
    
    # The equation is defined polar. Set those up:
    theta = np.linspace(0,170,n)*np.pi/180
    R = L/(1 + eps*np.cos(theta))
    # Find the x- and y-components from the polar curve:
    bs_x = R*np.cos(theta) + X0

    bs_y_top = R*np.sin(theta)
    bs_y_bottom = -1*R*np.sin(theta)

    bs_z_top = R*np.sin(theta)+Zd
    bs_z_bottom = -1*R*np.sin(theta)+Zd
    
    # Do the plotting:
    bs_color = bs_color
    bs_linestyle = bs_linestyle
    
    if (view == "XY"):
        plt.plot(bs_x, bs_y_top, color=bs_color, linestyle=bs_linestyle)
        plt.plot(bs_x, bs_y_bottom, color=bs_color, linestyle=bs_linestyle)
    if (view == "XZ"):
        plt.plot(bs_x, bs_z_top, color=bs_color, linestyle=bs_linestyle)
        plt.plot(bs_x, bs_z_bottom, color=bs_color, linestyle=bs_linestyle)

