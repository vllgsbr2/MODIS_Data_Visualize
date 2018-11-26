'''
Here we create the relevant MODIS tests plus the additional MAIA tests to
reproduce MODIS cloud mask results. The reference data is the MODIS cloud mask
results of cloudiness and 5 comparable tests (comparable in wavelength). This
exercise is to form a base line for the MAIA cloud mask algorithm.
'''
import numpy as np
import h5py
import time
