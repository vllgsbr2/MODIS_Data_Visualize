import numpy as np
import matplotlib.pyplot as plt
from pyhdf.SD import SD
from plt_MODIS_02 import get_data
import pprint

#.datasets for sd()
#.attributes fro sd().fieldnames

#grab data
filename = '/Users/vllgsbr2/Desktop/MODIS_Training/Data/toronto_09_05_18/MOD35_L2.A2018248.1630.061.2018249014414.hdf'
SD_field_rawData = 2 #0,1,2
fieldname = 'Cloud_Mask'#'Snow_IceSurfaceProcessedPct'
data_SD = get_data(filename, fieldname, SD_field_rawData)
#pprint.pprint(data_SD.datasets())
# pprint.pprint(data_SD.attributes())
print(np.shape(data_SD))

# x=7
# y=10
#
# print('x: ',x, '  y: ',y)
# bit_and = x & y
# bit_or  = x | y
# print('x & y: ',bit_and,' x | y: ',bit_or)
