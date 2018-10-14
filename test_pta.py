
def crop_PTA(filename_MOD_02, filename_MOD_03, filename_MOD_35, corrected_raw_data):
    '''
    INPUT:
           filename_MOD_02,
           filename_MOD_03,
           filename_MOD_35: - string - filepath to products (all same time/loc)
                                        aggregated to 1km
           corrected_raw_data: - 2D numpy array - contains processed data ready to be cropped
    RETURN:
           cropped corrected_raw_data
    '''

    fieldnames_MOD_02  = ['EV_500_Aggr1km_RefSB', 'EV_250_Aggr1km_RefSB']
    fieldnames_MOD_03  = ['SolarZenith', 'SensorZenith', 'SolarAzimuth',\
                          'SensorAzimuth', 'Latitude', 'Longitude']

    #choose grid spacing for subsetting datafield
    grid_space_250m = 0.25 #km
    grid_space_500m = 0.5
    grid_space_1km  = 1

    # #load file for geolocation data
    # choose_file(filename_MOD_03)

    #grab lat/lon
    lat = get_lat()
    lon = get_lon()

    #define limits of lat,lon, and bands for users
    max_lat = np.max(lat)
    max_lon = np.max(lon)

    min_lat = np.min(lat)
    min_lon = np.min(lon)

    #collect lat/lon and bands to display to user
    field_attributes_MOD_02 = data_field_MOD_02.attributes()
    bands_available         = field_attributes_MOD_02['band_names']

    lat_bounds = (min_lat, max_lat)
    lon_bounds = (min_lon, max_lon)

    #choose pixel and band
    print('Build lat/lon box for PTA')
    band       = int(input('enter desired band as index: ' + str(bands_available) + '\n\n'))
    lat_center = float(input('enter desired latitude range: ' + str(lat_bounds) + '\n\n'))
    lon_center = float(input('enter desired longitude range: ' + str(lon_bounds) + '\n\n'))

    #interpolate user input to available data
    radius_to_PTA = np.power((np.square(lat-lat_center) + np.square(lon-lon_center)), 0.5)
    min_radius    = np.min(radius_to_PTA)

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
