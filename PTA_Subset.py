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

lat_bounds = (max_lat, min_lat)
lon_bounds = (max_lon, min_lon)
lat_range  =  max_lat - min_lat
lon_range  =  max_lon - min_lon

#choose pixel and band
print('Build lat/lon box for PTA')
band       = input('enter desired band: ' + str(bands_available) + '\n')
lat_center = float(input('enter desired latitude\n range: ' + str(lat_bounds) + '\n'))
lon_center = float(input('enter desired longitude\n range: ' + str(lon_bounds) + '\n'))

#build lat/lon box around center lat/lon
lat_width = float(input('enter lat width ' + str(lat_range) + '[degrees]' + '\n'))
lon_width = float(input('enter lon width ' + str(lon_range) + '[degrees]' + '\n'))

#interpolate user input to available data
radius_to_PTA = np.power((np.square(lat-lat_center) + np.square(lon-lon_center)), 0.5)
min_radius    = np.min(radius_to_PTA)

#index from granule the corresponds to user lat/lon PTA
PTA_ij_index  = np.where(radius_to_PTA==min_radius)

#make box along lines of constant lat & lon or cut box out of granule?
#what if PTA is on the edge of the granule?
height = lat_width/2
length = lon_width/2



#subset the image from brf/radiance
