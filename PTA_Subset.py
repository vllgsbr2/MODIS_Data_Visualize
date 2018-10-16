'''
author: Javier Villegas

Function: crop area out of MODIS file from lat lon
Application: subset PTAs for training set
            (projected target areas from MODIS data)
'''
from plt_MODIS_03 import *

# rad_ref_files   = {'high_lat'  : '/Users/vllgsbr2/Desktop/MODIS_Training/Data/high_latitude/MOD021KM.A2018248.0450.061.2018248133406.hdf',\
#                    'toronto'   : '/Users/vllgsbr2/Desktop/MODIS_Training/Data/toronto_09_05_18/MOD021KM.A2018248.1630.061.2018249014250.hdf',\
#                    'maraciabo' : '/Users/vllgsbr2/Desktop/MODIS_Training/Data/venezuela_08_21_18/MOD021KM.A2018233.1545.061.2018234021223.hdf',\
#                    'twhs'      : '/Users/vllgsbr2/Desktop/MODIS_Training/Data/03032015TWHS/MOD021KM.A2015062.1645.061.2017319035334.hdf'}
# geo_files       = {'high_lat'  : '/Users/vllgsbr2/Desktop/MODIS_Training/Data/high_latitude/MOD03.A2018248.0450.061.2018248114733.hdf',
#                    'toronto'   : '/Users/vllgsbr2/Desktop/MODIS_Training/Data/toronto_09_05_18/MOD03.A2018248.1630.061.2018248230625.hdf',
#                    'maraciabo' : '/Users/vllgsbr2/Desktop/MODIS_Training/Data/venezuela_08_21_18/MOD03.A2018233.1545.061.2018233214936.hdf',
#                    'twhs'      : '/Users/vllgsbr2/Desktop/MODIS_Training/Data/03032015TWHS/MOD03.A2015062.1645.061.2017319034323.hdf'}
# PTA = 'high_lat'
# filename_MOD_02 = rad_ref_files[PTA]
# filename_MOD_03 = geo_files[PTA]


def crop_PTA(filename_MOD_03, corrected_raw_data):
    '''
    INPUT:
           filename_MOD_03: - string - filepath to product (all same time/loc)
                                        aggregated to 1km
           corrected_raw_data: - 2D numpy array - contains processed data ready to be cropped
    RETURN:
           cropped corrected_raw_data
    '''
    fieldnames_MOD_03  = ['SolarZenith', 'SensorZenith', 'SolarAzimuth',\
                          'SensorAzimuth', 'Latitude', 'Longitude']

    #choose grid spacing for subsetting datafield
    grid_space_250m = 0.25 #km
    grid_space_500m = 0.5
    grid_space_1km  = 1

    #grab lat/lon
    lat = get_lat(filename_MOD_03)
    lon = get_lon(filename_MOD_03)

    #define limits of lat,lon, and bands for users
    max_lat = np.max(lat)
    max_lon = np.max(lon)

    min_lat = np.min(lat)
    min_lon = np.min(lon)

    # #collect lat/lon and bands to display to user
    # field_attributes_MOD_02 = data_field_MOD_02.attributes()
    # bands_available         = field_attributes_MOD_02['band_names']

    lat_bounds = (min_lat, max_lat)
    lon_bounds = (min_lon, max_lon)

    #choose pixel and band
    print('Build lat/lon box for PTA')
    # band       = int(input('enter desired band as index: ' + str(bands_available) + '\n\n'))
    lat_center = float(input('enter desired latitude range: ' + str(lat_bounds) + '\n\n'))
    lon_center = float(input('enter desired longitude range: ' + str(lon_bounds) + '\n\n'))

    #interpolate user input to available data
    radius_to_PTA = np.power((np.square(lat-lat_center) + np.square(lon-lon_center)), 0.5)
    min_radius    = np.min(radius_to_PTA)

    ################################################################################
    # # calculate using haversine/great circle distance instead of Euclidian distance
    # #dont need constants R and 2  because we want min val, not absolute
    # #R            = 6378000
    # lat_r        = np.deg2rad(lat)
    # lon_r        = np.deg2rad(lon)
    # lat_center_r = np.deg2rad(lat_center)
    # lon_center_r = np.deg2rad(lon_center)
    #
    # alpha = (lat_r - lat_center_r)/2
    # beta  = (lon_r - lon_center_r)/2
    #
    # sigma = np.sin(alpha)**2 + np.cos(lat_center_r)*np.cos(lat_r)*(np.sin(beta)**2)
    #
    # radius_to_PTA = np.arcsin((sigma**0.5))  #2*R*
    # min_radius    = np.min(radius_to_PTA)
    ################################################################################


    #index from granule the corresponds to user lat/lon PTA
    PTA_ij_index  = np.where(radius_to_PTA==min_radius)
    PTA_i = int(PTA_ij_index[0])
    PTA_j = int(PTA_ij_index[1])

    #cut box out of granule M km x N km or max box in that area
    vertical   = 200 #km
    horizontal = 200 #km
    grid_space = grid_space_1km # _250m or _500m or _1km

    #width/height of desired box and granule
    box_height = int(grid_space * vertical)
    box_width  = int(grid_space * horizontal)
    granule_height = len(lat)
    granule_width  = len(lon[0])

    #LEFT ###########################################################################
    if PTA_j - int(box_width/2) >= 0:
        left_index   = PTA_j - int(box_width/2)
    else:
        left_index   = 0
    #RIGHT ##########################################################################
    if PTA_j + int(box_width/2) < granule_width:
        right_index  = PTA_j + int(box_width/2)
    else:
        right_index  = granule_width - 1
    #TOP ############################################################################
    if PTA_i - int(box_height/2) >= 0:
        top_index  = PTA_i - int(box_height/2)
    else:
        top_index  = 0
    #BOTTOM #########################################################################
    if PTA_j + int(box_height/2) < granule_height:
        bottom_index  = PTA_i + int(box_height/2)
    else:
        bottom_index  = granule_height - 1

    int(top_index)
    int(bottom_index)
    int(left_index)
    int(right_index)

    #fill new array with pre calculated dimensions with cropped data
    box_width  = int(right_index  - left_index) #by columns
    box_height = int(bottom_index - top_index )  #by rows

    #just slice array to crop
    cropped_corrected_data = corrected_raw_data[band, top_index : bottom_index, left_index : right_index]

    return cropped_corrected_data

################################################################################
# #plot
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
#
# fig, ax = plt.subplots(ncols=2)
# cmap = 'bone'
# vmin = 0
# vmax = 1
#
# #create circle on PTA center and rectangle over PTA
# circle = patches.Circle((PTA_j,PTA_i), radius=12, facecolor='r')
# circle_center_i = PTA_i - top_index
# circle_center_j = PTA_j - left_index
#
# circle_crop = patches.Circle((circle_center_j, circle_center_i), radius=4, facecolor='r')
# rect = patches.Rectangle((left_index,top_index), box_width, box_height ,linewidth=2,edgecolor='r',facecolor='none', fill=False)
#
# ax[0].imshow(corrected_raw_data[band,:,:], vmin=vmin, vmax=vmax, cmap=cmap)
# ax[0].set_title('full image')
# ax[0].add_patch(rect)
# ax[0].add_patch(circle)
#
# ax[1].add_patch(circle_crop)
# ax[1].imshow(cropped_corrected_data, vmin=vmin, vmax=vmax, cmap=cmap)
# ax[1].set_title('cropped image')
#
# list(bands_available)
# if band%2==1:
#     band = band + 1
# fig.suptitle('Band: '+str(bands_available[band]))
# print('PTA: ', PTA)
# print('i: ', PTA_i)
# print('j: ', PTA_j)
# print(np.shape(corrected_raw_data[0,:,:]))
# print('user lat: ', lat_center)
# print('calc lat: ', lat[PTA_i, PTA_j])
# print('user lon: ', lon_center)
# print('calc lon: ', lon[PTA_i, PTA_j])
#
# plt.show()

#subset the image from brf/radiance
