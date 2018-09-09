'''
MOD03: geolocation data
- produce latitude/longitude data set
- Show color bar for all graphs
- Sun field geometry (imshow the values over an area)
    - Viewing zenith angle
    - Relative azimuthal
    - Solar zenith angle
- Function to crop area out of modis file from lat lon
'''

from plt_MODIS_02 import * #includes matplotlib and numpy


filename   = ''
fieldnames_list  = ['', '']
rad_or_ref = True #True for radiance, False for reflectance
get_data(filename, fieldnames_list[0], SD_field_rawData)
