'''
author: Javier Villegas

Function: crop area out of MODIS file from lat lon
Application: subset PTAs for training set
            (projected target areas from MODIS data)
'''

from plt_MODIS_03 import *

filename_MOD_02 = '/Users/vllgsbr2/Desktop/MODIS_Training/Data/03032015TWHS/MOD021KM.A2015062.1645.061.2017319035334.hdf'
filename_MOD_03 = '/Users/vllgsbr2/Desktop/MODIS_Training/Data/03032015TWHS/MOD03.A2015062.1645.061.2017319034323.hdf'

fieldnames_MOD_02  = ['EV_500_Aggr1km_RefSB', 'EV_250_Aggr1km_RefSB']
fieldnames_MOD_03  = ['SolarZenith', 'SensorZenith', 'SolarAzimuth',\
                      'SensorAzimuth', 'Latitude', 'Longitude']

#choose grid spacing for subsetting datafield
grid_space_250m = 250 #meters
grid_space_500m = 500
grid_space_1km  = 1000

#load file for geolocation data
choose_file(filename_MOD_03)

#grab lat/lon
lat = get_lat()
lon = get_lon()

#get corrected raw data
rad_or_ref         = True #True fo radiance, False for BRF
SD_field_rawData   = 2 #0,1,2->SD,field,rawData
data_raw           = get_data(filename_MOD_02, fieldnames_MOD_02[1], SD_field_rawData)

SD_field_rawData   = 1 #0,1,2->SD,field,rawData
data_field_MOD_02  = get_data(filename_MOD_02, fieldnames_MOD_02[1], SD_field_rawData)

corrected_raw_data = get_radiance_or_reflectance(data_raw, data_field_MOD_02, rad_or_ref)

#define limits of lat,lon, and bands for users
max_lat = np.max(lat)
max_lon = np.max(lon)

min_lat = np.min(lat)
min_lon = np.min(lon)

#collect lat/lon and bands to display to user
field_attributes_MOD_02 = data_field_MOD_02.attributes()
#field_attributes_MOD_03 = data_field_MOD_03.attributes()
print(field_attributes_MOD_02)
bands_available = field_attributes_MOD_02['band_names']

lat_bounds = (min_lat, max_lat)
lon_bounds = (min_lon, max_lon)

# #don't nned width anymore for updated algorithm
# lat_range  =  max_lat - min_lat
# lon_range  =  max_lon - min_lon

#choose pixel and band
print('Build lat/lon box for PTA')
band       = input('enter desired band: ' + str(bands_available) + '\n')
lat_center = float(input('enter desired latitude\n range: ' + str(lat_bounds) + '\n'))
lon_center = float(input('enter desired longitude\n range: ' + str(lon_bounds) + '\n'))


#interpolate user input to available data
radius_to_PTA = np.power((np.square(lat-lat_center) + np.square(lon-lon_center)), 0.5)
min_radius    = np.min(radius_to_PTA)

#index from granule the corresponds to user lat/lon PTA
PTA_ij_index  = np.where(radius_to_PTA==min_radius)
PTA_i = PTA_ij_index[0]
PTA_j = PTA_ij_index[1]

#cut box out of granule M km x N km or max box in that area









# #don't need this code. gonna do km instead of degrees
# #half distances to PTA in degrees
# height = lat_width/2
# length = lon_width/2
#
# #find index of limits of box on 4 sides
# top_of_box = np.where(lat==(lat[PTA_i,PTA_j] + height))
# bot_of_box = np.where(lat==(lat[PTA_i,PTA_j] - height))
# right_edge = np.where(lat==(lat[PTA_i,PTA_j] + length))
# left_edge  = np.where(lat==(lat[PTA_i,PTA_j] - length))


#subset the image from brf/radiance
