import numpy as np
import matplotlib.pyplot as plt
from pyhdf.SD import SD
from plt_MODIS_02 import get_data
import h5py
import time


#.datasets for sd()
#.attributes for sd().fieldnames

# #grab data
# filename = '/Users/vllgsbr2/Desktop/MODIS_Training/Data/venezuela_08_21_18/MOD35_L2.A2018233.1545.061.2018234021557.hdf' #'/Users/vllgsbr2/Desktop/MODIS_Training/Data/toronto_09_05_18/MOD35_L2.A2018248.1630.061.2018249014414.hdf'
# SD_field_rawData = 2 #0,1,2
# fieldname = 'Cloud_Mask'
# data_SD = get_data(filename, fieldname, SD_field_rawData) #shape (byte, height, width) (6, 2030, 1354)

def get_bits_old(data, N):
    '''
    INPUT:
        data - 3d numpy array - from cloud mask
        N    - into           - which byte block to use
    RETURN:
        numpy array - of shape (6, 2030, 1354) 6 bytes
                      for every pixel in granule
    '''
    shape = np.shape(data)
    #Nth index for first dimension to work on 1st/6 bytes
    data_flat = np.reshape(data[N, :, :], (shape[1]*shape[2]))

    #save remiander and int division into lists
    #remainder is the bit, int division is for next step
    # shape = (2030*1354, 2)
    #divmod(x, y)	the pair (x // y, x % y)
    bit_index_0  = np.array([divmod(int(i), 2) for i in data_flat])
    bit_index_12 = np.array([divmod(int(i), 4) for i in bit_index_0[:, 0]])
    bit_index_3  = np.array([divmod(int(i), 2) for i in bit_index_12[:, 0]])
    bit_index_4  = np.array([divmod(int(i), 2) for i in bit_index_3[:, 0]])
    bit_index_5  = np.array([divmod(int(i), 2) for i in bit_index_4[:, 0]])
    bit_index_67 = np.array([[int(i)%4] for i in bit_index_5[:, 0]])

    # print(np.shape(bit_index_1))
    # print(np.shape(bit_index_1[:,0]))
    #dump the division row, we don't need it (note div not saved for last bit)
    bit_index_0  = np.reshape(bit_index_0,  (shape[1], shape[2], 2))[:,:,1]
    bit_index_12 = np.reshape(bit_index_12, (shape[1], shape[2], 2))[:,:,1]
    bit_index_3  = np.reshape(bit_index_3,  (shape[1], shape[2], 2))[:,:,1]
    bit_index_4  = np.reshape(bit_index_4,  (shape[1], shape[2], 2))[:,:,1]
    bit_index_5  = np.reshape(bit_index_5,  (shape[1], shape[2], 2))[:,:,1]
    bit_index_67 = np.reshape(bit_index_67, (shape[1], shape[2]))

    #return all bits
    return bit_index_0, bit_index_12,\
           bit_index_3, bit_index_4, bit_index_5,\
           bit_index_67
# start_time = time.time()
# data_SD_bit = get_bits_old(data_SD, 0)
# print("--- %s seconds ---" % (time.time() - start_time))


def get_bits(data_SD, N):
    '''
    cloud mask and byte stack to work on
    returns numpy.bytes array of byte stack of shape 2030x1354
    '''
    shape = np.shape(data_SD)
    #convert MODIS 35 signed ints to unsigned ints
    data_unsigned = np.bitwise_and(data_SD[N, :, :], 0xff)

    #type is int16, but unpackbits taks int8, so cast array
    data_unsigned = data_unsigned.astype(np.uint8)#data_unsigned.view('uint8')

    #return numpy array of length 8 lists for every element of data_SD
    data_bits = np.unpackbits(data_unsigned)
    data_bits = np.reshape(data_bits, (shape[1], shape[2], 8))

    return data_bits

#print('getting bits')
#start_time = time.time()
#data_SD_bit = get_bits(data_SD, 0)
#print("--- %s seconds ---" % (time.time() - start_time))


def save_mod35(data, save_path):
    hf = h5py.File(save_path, 'w')
    hf.create_dataset('MOD_35_decoded', data=data)
    hf.close()

save_mod35(data_SD_bit, '/Users/vllgsbr2/Desktop/MODIS_Training/Data/mod_35/MOD_35.h5')

#recover bit array
#shape = (2030, 1354, 8)
#data = np.array(h5py.File('/Users/vllgsbr2/Desktop/MODIS_Training/Data/mod_35/MOD_35.h5', 'r').get('MOD_35_decoded'))

def decode_bits(decoded_mod35_hdf):
    data = decoded_mod35_hdf
    shape = np.shape(data)

    #create empty arrays to fill later
    #binary 1 or 0 fill
    Cloud_Mask_Flag           = data[:,:, 7]
    Day_Night_Flag            = data[:,:, 4]
    Sun_glint_Flag            = data[:,:, 3]
    Snow_Ice_Background_Flag  = data[:,:, 2]

    #0,1,2,or 3 fill
    #cloudy, uncertain clear, probably clear, confident clear
    Unobstructed_FOV_Quality_Flag = data[:,:, 5:7]
    #find index of each cloud possibility
    #new list to stuff new laues into and still perform a good search
    new_Unobstructed_FOV_Quality_Flag = np.empty((shape[0], shape[1]))

    cloudy_index          = np.where((Unobstructed_FOV_Quality_Flag[:,:, 0]==0) & \
                                     (Unobstructed_FOV_Quality_Flag[:,:, 1]==0))
    uncertain_clear_index = np.where((Unobstructed_FOV_Quality_Flag[:,:, 0]==0) & \
                                     (Unobstructed_FOV_Quality_Flag[:,:, 1]==1))
    probably_clear_index  = np.where((Unobstructed_FOV_Quality_Flag[:,:, 0]==1) & \
                                     (Unobstructed_FOV_Quality_Flag[:,:, 1]==0))
    confident_clear_index = np.where((Unobstructed_FOV_Quality_Flag[:,:, 0]==1) & \
                                     (Unobstructed_FOV_Quality_Flag[:,:, 1]==1))

    new_Unobstructed_FOV_Quality_Flag[cloudy_index]          = 0
    new_Unobstructed_FOV_Quality_Flag[uncertain_clear_index] = 1
    new_Unobstructed_FOV_Quality_Flag[probably_clear_index]  = 2
    new_Unobstructed_FOV_Quality_Flag[confident_clear_index] = 3

    #water, coastal, desert, land
    Land_Water_Flag = data[:,:, 0:2]
    #find index of each land type possibility
    new_Land_Water_Flag = np.empty((shape[0], shape[1]))

    water_index   = np.where((Land_Water_Flag[:,:, 0]==0) & \
                             (Land_Water_Flag[:,:, 1]==0))
    coastal_index = np.where((Land_Water_Flag[:,:, 0]==0) & \
                             (Land_Water_Flag[:,:, 1]==1))
    desert_index  = np.where((Land_Water_Flag[:,:, 0]==1) & \
                             (Land_Water_Flag[:,:, 1]==0))
    land_index    = np.where((Land_Water_Flag[:,:, 0]==1) & \
                             (Land_Water_Flag[:,:, 1]==1))

    new_Land_Water_Flag[water_index]   = 0
    new_Land_Water_Flag[coastal_index] = 1
    new_Land_Water_Flag[desert_index]  = 2
    new_Land_Water_Flag[land_index]    = 3

    return Cloud_Mask_Flag, new_Unobstructed_FOV_Quality_Flag, Day_Night_Flag,\
            Sun_glint_Flag, Snow_Ice_Background_Flag,new_Land_Water_Flag
#print('decoding bits')
# start_time = time.time()
#bitsofthings = decode_bits(data)
# print("--- %s seconds ---" % (time.time() - start_time))


# #plot
# import matplotlib.colors as matCol
# from matplotlib.colors import ListedColormap
# cmap=plt.cm.PiYG
# cmap = ListedColormap(['white', 'green', 'blue','black'])
# norm = matCol.BoundaryNorm(np.arange(0,5,1), cmap.N)
# plt.imshow(bitsofthings[4], cmap=cmap, norm=norm)
# cbar = plt.colorbar()
# cbar.set_ticks([0.5,1.5,2.5,3.5])
# cbar.set_ticklabels
# (['cloudy', 'uncertain\nclear', 'probably\nclear', 'confident\nclear'])
# plt.title('MODIS Cloud Mask')
# plt.show()
