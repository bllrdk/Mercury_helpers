# imports
import data_types as d

from scipy.constants import mu_0

## Constants

RADIUS = 2439.7 #km
B_MERCURY = 300 # nT
Mu0 = mu_0


'''
▄▄▄▄   ▄▄▄ ▄▄▄▄▄▄ ▄▄▄
██▀██ ██▀██  ██  ██▀██
████▀ ██▀██  ██  ██▀██
'''

PKL = True
SAVE_PKL = False
INTERPOLATE_TIME = True
INTERPOLATE_DIST = False




'''                  
▄▄▄▄▄ ▄▄ ▄▄    ▄▄▄▄▄  ▄▄▄▄ 
██▄▄  ██ ██    ██▄▄  ███▄▄ 
██    ██ ██▄▄▄ ██▄▄▄ ▄▄██▀ 
'''
## Filenames
### 'pileup_data_files/'  'data/'
DATA_FOLDER = 'pileup_data_files/'
CROSS_FILE = 'FIPS_REGIONCROSS_20160115.sav'

## type of looping and constants needed for it
## looping through all the files in a folder of data
BY_FILE = True
NUM_FILES = 48 ## 48 for pileup_data

## looking at a specific orbit
BY_ORBIT = False
ORBIT = 38

## looping through a list of event times
BY_TIME = False
EVENT_LIST = 'file_name'


'''                                          
▄▄▄▄  ▄▄     ▄▄▄ ▄▄▄▄▄▄ ▄▄▄▄▄▄ ▄▄ ▄▄  ▄▄  ▄▄▄▄ 
██▄█▀ ██    ██▀██  ██     ██   ██ ███▄██ ██ ▄▄ 
██    ██▄▄▄ ▀███▀  ██     ██   ██ ██ ▀██ ▀███▀ 
                                               
'''

## plot general
PLOT = False
SHOW = True
SAVE = True
SAVE_FOLDER = 'pileup_data_plots/' # folder to save the plots into
SUBPLOT_WIDTH = 2
HALF_LENGTH_TIME = 600 # seconds (600 for 10 minutes)
HALF_LENGTH_DISTANCE = 2000 # km (approx 30 km for 10 seconds)
PLOT_INFO = d.plot_characteristics()
FLAG_COUNTS = 10

PLOT_ORBITS = False

'''                                                                                   
▄▄▄▄  ▄▄     ▄▄▄ ▄▄▄▄▄▄    ▄▄▄▄  ▄▄▄  ▄▄   ▄▄ ▄▄▄▄   ▄▄▄  ▄▄  ▄▄ ▄▄▄▄▄ ▄▄  ▄▄ ▄▄▄▄▄▄ ▄▄▄▄ 
██▄█▀ ██    ██▀██  ██     ██▀▀▀ ██▀██ ██▀▄▀██ ██▄█▀ ██▀██ ███▄██ ██▄▄  ███▄██   ██  ███▄▄ 
██    ██▄▄▄ ▀███▀  ██     ▀████ ▀███▀ ██   ██ ██    ▀███▀ ██ ▀██ ██▄▄▄ ██ ▀██   ██  ▄▄██▀ 
                                                                                                                                         
'''
EQ = True
ANGLE = False
PITCH_ANGLE = False

H_FLUX = False

## composition
COUNTS = True
NUMBER_DENSITY = False
Na_EQ = True

ENERGY_SPECTROGRAM = False

BX = True
BZ = True
MAG_FIELD = True

DISTANCE = True


NUM_SUBPLOTS = sum([EQ, ANGLE, PITCH_ANGLE, H_FLUX, COUNTS, NUMBER_DENSITY, Na_EQ, ENERGY_SPECTROGRAM, BX, BZ, MAG_FIELD, DISTANCE])

## plot specifics
# H FLUX

# PITCH ANGLE

# NUMBER DENSITY
He2 = True
He1 = True
O = True
Na = True

# ENERGY SPECTROGRAM

# MAG FIELD

######################### Superimposed Epoch #######################################################

## plot general
sea_PLOT = False
sea_SHOW = True
sea_SAVE = False


sea_EQ = False
sea_ANGLE = False
sea_PITCH_ANGLE = False

sea_H_FLUX = False

sea_ENERGY_SPECTROGRAM = False

sea_BX = False
sea_BZ = False
sea_MAG_FIELD = False

# NUMBER DENSITY
sea_He2 = False
sea_He1 = False
sea_O = False
sea_Na = True

sea_DISTANCE = True

sea_NUM_SUBPLOTS = sum([sea_EQ, sea_ANGLE, sea_PITCH_ANGLE, sea_H_FLUX, sea_ENERGY_SPECTROGRAM, sea_BX,
                        sea_BZ, sea_MAG_FIELD, sea_He2, sea_He1, sea_O, sea_Na, sea_DISTANCE])