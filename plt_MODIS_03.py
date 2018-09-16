'''
MOD03: geolocation data
- Produce latitude/longitude data set ('Latitude', 'Longitude')
- Show color bar for all graphs
- Sun field geometry (imshow the values over an area)
    - Viewing zenith angle ('SensorZenith')
    - Relative azimuthal   ('SensorAzimuth'-'SolarAzimuth')
    - Solar zenith angle   ('SolarZenith')
- Function to crop area out of modis file from lat lon
'''

from plt_MODIS_02 import * #includes matplotlib and numpy

#used by get functions(filename can be modified by choose_file function)
filename   = '/Users/vllgsbr2/Desktop/MODIS_Training/Data/03032015TWHS/MOD03.A2015062.1645.061.2017319034323.hdf'
fieldnames_list  = ['SolarZenith', 'SensorZenith', 'SolarAzimuth','SensorAzimuth', 'Latitude', 'Longitude']

#create dictionaries for angles (used by get functions)
solar_zenith  = {}
sensor_zenith = {}
solar_azimuth = {}
sensor_azimuth = {}

def choose_file(file_name):
    '''
    INPUT
          file_name: string - path to file
    RETURN
          No return; effect is to change what filename points to outside of def
    '''
    filename = file_name

def get_solarZenith():
    #obtain field information to grab scales/offsets
    SD_field_rawData = 1 #0 SD, 1 field & 2 returns raw data
    solar_zenith['scale_factor']   = get_data(filename, fieldnames_list[0], SD_field_rawData).attributes()['scale_factor']

    #correct values by scales/offsets
    SD_field_rawData = 2 #0 SD, 1 field & 2 returns raw data
    solar_zenith['corrected_raw_data']   = get_data(filename, fieldnames_list[0], SD_field_rawData) * solar_zenith['scale_factor']

    return solar_zenith['corrected_raw_data']

def get_sensorZenith():
    #obtain field information to grab scales/offsets
    SD_field_rawData = 1 #0 SD, 1 field & 2 returns raw data
    sensor_zenith['scale_factor']  = get_data(filename, fieldnames_list[1], SD_field_rawData).attributes()['scale_factor']

    #correct values by scales/offsets
    SD_field_rawData = 2 #0 SD, 1 field & 2 returns raw data
    sensor_zenith['corrected_raw_data']  = get_data(filename, fieldnames_list[1], SD_field_rawData) * sensor_zenith['scale_factor']

    return sensor_zenith['corrected_raw_data']

def get_solarAzimuth():
    #obtain field information to grab scales/offsets
    SD_field_rawData = 1 #0 SD, 1 field & 2 returns raw data
    solar_azimuth['scale_factor']  = get_data(filename, fieldnames_list[2], SD_field_rawData).attributes()['scale_factor']

    #correct values by scales/offsets
    SD_field_rawData = 2 #0 SD, 1 field & 2 returns raw data
    solar_azimuth['corrected_raw_data']  = get_data(filename, fieldnames_list[2], SD_field_rawData) * solar_azimuth['scale_factor']

    return solar_azimuth['corrected_raw_data']

def get_sensorAzimuth():
    #obtain field information to grab scales/offsets
    SD_field_rawData = 1 #0 SD, 1 field & 2 returns raw data
    sensor_azimuth['scale_factor'] = get_data(filename, fieldnames_list[3], SD_field_rawData).attributes()['scale_factor']

    #correct values by scales/offsets
    SD_field_rawData = 2 #0 SD, 1 field & 2 returns raw data
    sensor_azimuth['corrected_raw_data'] = get_data(filename, fieldnames_list[3], SD_field_rawData) * sensor_azimuth['scale_factor']

    return sensor_azimuth['corrected_raw_data']

def get_relativeAzimuth():
    relative_azimuth = get_sensorAzimuth() - get_solarAzimuth()
    return relative_azimuth

def get_lat():
    SD_field_rawData = 2
    lat = get_data(filename, fieldnames_list[4], SD_field_rawData)

    return lat

def get_lon():
    SD_field_rawData = 2
    lon = get_data(filename, fieldnames_list[5], SD_field_rawData)

    return lon



# #plot
# fig, axes = plt.subplots(ncols=3)
# cmap = 'jet'
#
# plot_1 = axes[0].imshow(get_solarZenith(), cmap = cmap)
# axes[0].set_title('Solar Zenith Angle\n[degrees]')
#
# plot_2 = axes[1].imshow(get_sensorZenith(), cmap = cmap)
# axes[1].set_title('Sensor Zenith Angle\n[degrees]')
#
# plot_3 = axes[2].imshow(get_relativeAzimuth(), cmap = cmap, vmin=-260, vmax=-210)
# axes[2].set_title('Relative Azimuthal Angle\n[degrees]')
#
# fig.colorbar(plot_1, ax=axes[0])
# fig.colorbar(plot_2, ax=axes[1])
# fig.colorbar(plot_3, ax=axes[2])
#
# fig1, axes1 = plt.subplots(ncols=2)
#
# plot_11  = axes1[0].imshow(get_lon(), cmap = cmap)
# axes1[0].set_title('Longitude\n[degrees]')
# plot_22 = axes1[1].imshow(get_lat(), cmap = cmap)
# axes1[1].set_title('Latitude\n[degrees]')
#
# fig1.colorbar(plot_1, ax=axes1[0])
# fig1.colorbar(plot_2, ax=axes1[1])
#
# plt.show()

# #debugging tools
# file = SD('/Users/vllgsbr2/Desktop/MODIS_Training/Data/03032015TWHS/MOD03.A2015062.1645.061.2017319034323.hdf')
# data = file.select('EV_500_Aggr1km_RefSB')
# pprint.pprint(data.attributes()) #tells me scales, offsets and bands
# pprint.pprint(file.datasets()) # shows data fields in file from SD('filename')
