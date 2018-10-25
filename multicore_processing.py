from read_MODIS_35 import *
from PTA_Subset import crop_PTA
from plt_MODIS_02 import prepare_data
import time
from multiprocessing import Pool
import multiprocessing as mp

filename_MOD_35 = '/Users/vllgsbr2/Desktop/MODIS_Training/Data/venezuela_08_21_18/MOD35_L2.A2018233.1545.061.2018234021557.hdf'
filename_MOD_03 = '/Users/vllgsbr2/Desktop/MODIS_Training/Data/venezuela_08_21_18/MOD03.A2018233.1545.061.2018233214936.hdf'
PTA_lat = 10
PTA_lon = -73

def single_Core_test(filename_MOD_35, filename_MOD_03, PTA_lat, PTA_lon):
    data_SD           = get_data(filename_MOD_35, 'Cloud_Mask', 2)
    data_SD_bit       = get_bits(data_SD, 0)
    # save_path         = './bits.hf'
    # save_mod35(data_SD_bit, save_path)
    # data_bits         = np.array(h5py.File(save_path, 'r').get('MOD_35_decoded'))
    data_decoded_bits = decode_byte_1(data_SD_bit)

    cloud_mask = {'Cloud_Mask_Flag':data_decoded_bits[0],\
                  'Unobstructed_FOV_Quality_Flag':data_decoded_bits[1],\
                  'Day_Night_Flag':data_decoded_bits[2],\
                  'Sun_glint_Flag':data_decoded_bits[3],\
                  'Snow_Ice_Background_Flag':data_decoded_bits[4],\
                  'Land_Water_Flag':data_decoded_bits[5]
                  }
    for cm_key, cm_val in cloud_mask.items():
        crop_cm = crop_PTA(filename_MOD_03, cm_val, PTA_lat, PTA_lon)

def multi_Core_test(arr):
    filename_MOD_35 = arr[0]
    filename_MOD_03 = arr[1]
    PTA_lat         = arr[2]
    PTA_lon         = arr[3]
    num             = arr[4]

    data_SD           = get_data(filename_MOD_35, 'Cloud_Mask', 2)
    data_SD_bit       = get_bits(data_SD, 0)
    save_path         = './bits.hf'
    # save_mod35(data_SD_bit, save_path)
    # data_bits         = np.array(h5py.File(save_path, 'r').get('MOD_35_decoded'))
    data_decoded_bits = decode_byte_1(data_SD_bit)

    crop_cm = crop_PTA(filename_MOD_03, data_decoded_bits[num], PTA_lat, PTA_lon)

if __name__ == '__main__':

    # print('single core result')
    # t0 = time.time()
    # single_Core_test(filename_MOD_35, filename_MOD_03, PTA_lat, PTA_lon)
    # print('---------------------- ',time.time()-t0, ' ----------------------')
    print(mp.cpu_count())
    print('multi core result')
    t0 = time.time()
    arr = [[filename_MOD_35, filename_MOD_03, PTA_lat, PTA_lon, 0],\
           [filename_MOD_35, filename_MOD_03, PTA_lat, PTA_lon, 1],\
           [filename_MOD_35, filename_MOD_03, PTA_lat, PTA_lon, 2],\
           [filename_MOD_35, filename_MOD_03, PTA_lat, PTA_lon, 3],\
           [filename_MOD_35, filename_MOD_03, PTA_lat, PTA_lon, 4],\
           [filename_MOD_35, filename_MOD_03, PTA_lat, PTA_lon, 5]]

    pool = Pool(6)

    pool.map(multi_Core_test, arr)
    print('---------------------- ',time.time()-t0, ' ----------------------')
