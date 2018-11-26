'''
author: Javier Villegas

Format data base into hdf5 file containing every time stamp associated with a
granule, with associated dataset of radiance, reflectance, cloudmask, sun view
geometry, and geolocation.
'''
from read_MODIS_02 import prepare_data
from read_MODIS_03 import *
from read_MODIS_35 import *
from PTA_Subset import crop_PTA
#from multicore_processing import multi_core_crop
import h5py
import sys
import os
import time

# #Just gonna use with one PTA and one granule
# #next step is to develop a feeder system from keeling
# filename_MOD_02 = '/Users/vllgsbr2/Desktop/MODIS_Training/Data/venezuela_08_21_18/MOD021KM.A2018233.1545.061.2018234021223.hdf'
# filename_MOD_03 = '/Users/vllgsbr2/Desktop/MODIS_Training/Data/venezuela_08_21_18/MOD03.A2018233.1545.061.2018233214936.hdf'
# filename_MOD_35 = '/Users/vllgsbr2/Desktop/MODIS_Training/Data/venezuela_08_21_18/MOD35_L2.A2018233.1545.061.2018234021557.hdf'
#
#
# PTA_lat = 10
# PTA_lon = -73
#
# hf_path    = './test.hf'
# hf         = h5py.File(hf_path, 'w')
# group_name = '2018233.1545'

def build_data_base(filename_MOD_02, filename_MOD_03, filename_MOD_35, PTA_lat,\
                    PTA_lon, hf_path):
    '''
    INPUT:
        filename_MOD_02 - str   - filepath to MOD02
        filename_MOD_03 - str   - filepath to MOD03
        filename_MOD_35 - str   - filepath to MOD35
        PTA_lat         - float - lat of projected target area
        PTA_lon         - float - lon of projected target area
        hf_path         - str   - file path to previously created hdf5 file to
                                  store it in. (1 HDF5 file)/PTA
    RETURN:
        saves all calculated fields into hdf 5 file structure
    '''

    t0 = time.time()

    fieldname       = ['EV_250_RefSB', 'EV_250_Aggr1km_RefSB',\
                       'EV_500_RefSB', 'EV_500_Aggr1km_RefSB',\
                       'EV_1KM_RefSB']

    rad_or_ref              = True
    radiance_250_Aggr1km    = prepare_data(filename_MOD_02, fieldname[1], rad_or_ref)
    radiance_500_Aggr1km    = prepare_data(filename_MOD_02, fieldname[3], rad_or_ref)
    radiance_1KM            = prepare_data(filename_MOD_02, fieldname[4], rad_or_ref)

    rad_or_ref              = False
    reflectance_250_Aggr1km = prepare_data(filename_MOD_02, fieldname[1], rad_or_ref)
    reflectance_500_Aggr1km = prepare_data(filename_MOD_02, fieldname[3], rad_or_ref)
    reflectance_1KM         = prepare_data(filename_MOD_02, fieldname[4], rad_or_ref)

    #calculate geolocation

    lat = get_lat(filename_MOD_03)
    lon = get_lon(filename_MOD_03)

    #calculate geometry
    solarZenith   = get_solarZenith(filename_MOD_03)
    sensorZenith  = get_sensorZenith(filename_MOD_03)
    solarAzimuth  = get_solarAzimuth(filename_MOD_03)
    sensorAzimuth = get_sensorAzimuth(filename_MOD_03)


    #calculate cloudmask
    data_SD           = get_data(filename_MOD_35, 'Cloud_Mask', 2)
    data_SD_bit       = get_bits(data_SD, 0)
    save_path         = './bits.hf'
    save_mod35(data_SD_bit, save_path)
    data_bits         = np.array(h5py.File(save_path, 'r').get('MOD_35_decoded'))
    data_decoded_bits = decode_byte_1(data_bits)

    #calculate cloud mask tests
    data_SD_cloud_mask = data_SD
    decoded_cloud_mask_tests = decode_tests(data_SD_cloud_mask, filename_MOD_35)

    #subset granule


    #open hdf5 file to write to
    hf         = h5py.File(hf_path, 'r')
    group      = hf.create_group(group_name)
    subgroup_radiance           = group.create_group('radiance')
    subgroup_reflectance        = group.create_group('reflectance')
    subgroup_geolocation        = group.create_group('geolocation')
    subgroup_sunView_geometry   = group.create_group('sunView_geometry')
    subgroup_cloud_mask         = group.create_group('cloud_mask')
    subgroup_cloud_mask_test    = group.create_group('cloud_mask_tests')


    def save_crop(subgroup, dataset_name, cropped_data):
        '''
        INPUT:
              cropped data from PTA_Subset.crop_PTA()
              subgroup: - h5py group - belongs to subgroup of MODIS dataset i.e.
                                       radiance
              dataset_name: - str - name to save data to
        RETURN:
              save cropped data into hdf5 file without closing it. This is to add
              data into the hdf5 file and then freeing dereferenced pointers in
              order to have good memory management
        '''
        #add dataset to 'group'
        subgroup.create_dataset(dataset_name, data=cropped_data)

    #crop and save the datasets

    #reflectance and radiance
    band_index = {'1':0,
                  '2':1,
                  '3':0,
                  '4':1,
                  '6':3,
                  '12':4,
                  '26':12
                  }
    for band, index in band_index.items():
        if band=='1' or band=='2':
            crop_radiance = crop_PTA(filename_MOD_03, radiance_250_Aggr1km[index], PTA_lat, PTA_lon)
            crop_reflectance = crop_PTA(filename_MOD_03, reflectance_250_Aggr1km[index], PTA_lat, PTA_lon)

        elif band=='3' or band=='4' or band=='6':
            crop_radiance = crop_PTA(filename_MOD_03, radiance_500_Aggr1km[index], PTA_lat, PTA_lon)
            crop_reflectance = crop_PTA(filename_MOD_03, reflectance_500_Aggr1km[index], PTA_lat, PTA_lon)

        else:
            crop_radiance = crop_PTA(filename_MOD_03, radiance_1KM[index], PTA_lat, PTA_lon)
            crop_reflectance = crop_PTA(filename_MOD_03, reflectance_1KM[index], PTA_lat, PTA_lon)

        #group_name is granule, radiance is subgroup, band_1 is dataset, then the data
        save_crop(subgroup_radiance, 'band_{}'.format(band), crop_radiance)
        save_crop(subgroup_reflectance, 'band_{}'.format(band), crop_reflectance)

    #*******************************************************************************
    #Sun view geometry
    sunView_geometry = {'solarAzimuth':solarAzimuth,\
                        'sensorAzimuth':sensorAzimuth,\
                        'solarZenith':solarZenith,\
                        'sensorZenith':sensorZenith
                        }
    for sun_key, sun_val in sunView_geometry.items():
        crop_sun = crop_PTA(filename_MOD_03, sun_val, PTA_lat, PTA_lon)
        save_crop(subgroup_sunView_geometry, sun_key, crop_sun)

    crop_geo = crop_PTA(filename_MOD_03, lat, PTA_lat, PTA_lon)
    save_crop(subgroup_geolocation, 'lat', crop_geo)

    crop_geo = crop_PTA(filename_MOD_03, lon, PTA_lat, PTA_lon)
    save_crop(subgroup_geolocation, 'lon', crop_geo)

    #*******************************************************************************
    #cloud mask
    cloud_mask = {'Cloud_Mask_Flag':data_decoded_bits[0],\
                  'Unobstructed_FOV_Quality_Flag':data_decoded_bits[1],\
                  'Day_Night_Flag':data_decoded_bits[2],\
                  'Sun_glint_Flag':data_decoded_bits[3],\
                  'Snow_Ice_Background_Flag':data_decoded_bits[4],\
                  'Land_Water_Flag':data_decoded_bits[5]
                  }
    for cm_key, cm_val in cloud_mask.items():
        crop_cm = crop_PTA(filename_MOD_03, cm_val, PTA_lat, PTA_lon)
        save_crop(subgroup_cloud_mask, cm_key, crop_cm)

    #*******************************************************************************
    #cloud mask tests
    cloud_mask_tests = {'High_Cloud_Flag_1380nm':decoded_cloud_mask_tests[0],\
                        'Cloud_Flag_Visible_Reflectance':decoded_cloud_mask_tests[1],\
                        'Cloud_Flag_Visible_Ratio':decoded_cloud_mask_tests[2],\
                        'Near_IR_Reflectance':decoded_cloud_mask_tests[3],\
                        'Cloud_Flag_Spatial_Variability':decoded_cloud_mask_tests[4],\
                        }
    for cm_test_key, cm_test_val in cloud_mask_tests.items():
        crop_cm_test = crop_PTA(filename_MOD_03, cm_test_val, PTA_lat, PTA_lon)
        save_crop(subgroup_cloud_mask_test, cm_test_key, crop_cm_test)



    print('---------------------- ',time.time()-t0, ' ----------------------')

if __name__ == '__main__':

    import pandas as pd

    #choose PTA from keeling
    PTA_file_path   = '/data/keeling/a/vllgsbr2/b/modis_data/toronto_PTA'

    #choose PTA lat lon
    PTA_lat = 10
    PTA_lon = -73

    #grab files names for PTA
    filename_MOD_02 = np.array(os.listdir(PTA_file_path + '/MOD_02'))
    filename_MOD_03 = np.array(os.listdir(PTA_file_path + '/MOD_03'))
    filename_MOD_35 = np.array(os.listdir(PTA_file_path + '/MOD_35'))

    #sort files by time so we can access corresponding files without searching in for loop
    filename_MOD_02 = np.sort(filename_MOD_02)
    filename_MOD_03 = np.sort(filename_MOD_03)
    filename_MOD_35 = np.sort(filename_MOD_35)

    #grab time stamp (YYYYDDD.HHMM) to name each group after the granule it comes from
    #filename_MOD_02_timeStamp = [x[10:22] for x in filename_MOD_02]
    #filename_MOD_03_timeStamp = [x[7:19]  for x in filename_MOD_03]
    #filename_MOD_35_timeStamp = [x[10:22] for x in filename_MOD_35]


    print(directories)
    #print(directories['MOD_02_sorted'], directories['MOD_03_sorted'],\
    #      directories['MOD_35_sorted'])

    # #create/open file
    # hf_path = './test.hf'
    # hf      = h5py.File(hf_path, 'w')
    #
    # for MOD02, MOD03, MOD35 in zip():
    #     #filename_MOD_02, filename_MOD_03, filename_MOD_35, PTA_lat, PTA_lon, hf_path
    #     build_data_base(MOD02, MOD03, MOD35, PTA_lat, PTA_lon, hf_path)
    #
    # group_name = '2018233.1545'
    #
    # hf.close()
