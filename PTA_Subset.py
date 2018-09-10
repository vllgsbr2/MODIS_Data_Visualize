'''
author: Javier Villegas

Function: to crop area out of modis file from lat lon
Application: subset PTA (projected target areas from MODIS data)
'''

from plt_MODIS_03 import *

#get corrected raw data and parse example
SD_field_rawData   = 2 #0,1,2->SD,field,rawData
data_raw           = get_data(filename, fieldnames_list[1], SD_field_rawData)
corrected_raw_data = get_radiance_or_reflectance(data_raw, data_field, rad_or_ref)

#choose pixel and band
band_index = 0
row_index  = 0
col_index  = 0
