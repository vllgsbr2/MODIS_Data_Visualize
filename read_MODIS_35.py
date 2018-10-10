import numpy as np
import matplotlib.pyplot as plt
from pyhdf.SD import SD
from plt_MODIS_02 import get_data
import h5py
import time


#.datasets for sd()
#.attributes for sd().fieldnames

#grab data
filename = '/Users/vllgsbr2/Desktop/MODIS_Training/Data/toronto_09_05_18/MOD35_L2.A2018248.1630.061.2018249014414.hdf'
SD_field_rawData = 2 #0,1,2
fieldname = 'Cloud_Mask'
data_SD = get_data(filename, fieldname, SD_field_rawData) #shape (byte, height, width) (6, 2030, 1354)
# print(data_SD.max())
# print(data_SD.min())

#dictionary to decode bitfield
#value is lists of lists
#[[bit combo, meaning], [bit combo, meaning], ...]
bitfield = { '0  Cloud Mask Flag'               : [['0' , 'not determined'], ['1', 'determined']],
             '12 Unobstructed FOV Quality Flag' : [['00', 'cloudy'],         ['01', 'uncertain clear'], ['10', 'probably clear'], ['11', 'confident clear']],
             '3  Day / Night Flag'              : [['0' , 'Night'],          ['1', 'Day']],
             '4  Sun glint Flag'                : [['0' , 'Yes'],            ['1', 'No']],
             '5  Snow / Ice Background Flag'    : [['0' , 'Yes'],            ['1', 'No']],
             '67 Land / Water Flag'             : [['00', 'Water'],          ['01', 'Coastal'], ['10', 'Desert'], ['11', 'Land']]
           }

def get_bit(data, N):
    '''
    INPUT:
        data - 3d numpy array - from cloud mask
        N    - into           - which byte block to use
    RETURN:
        numpy array - of shape (8, 2030, 1354) 8 bits to a byte
                      for every pixel in granule
    '''
    shape = np.shape(data)
    #Nth index for first dimension to work on 1st/6 bytes
    data_flat = np.reshape(data[N][:][:], (shape[1]*shape[2]))

    #save remiander and int division into lists
    #remainder is the bit, int division is for next step
    # shape = (2030*1354, 2)
    #divmod(x, y)	the pair (x // y, x % y)
    bit_index_0 = np.array([[int(i)%2, int(i)//2] for i in data_flat])
    bit_index_1 = np.array([[int(i)%2, int(i)//2] for i in bit_index_0[:, 1]])
    bit_index_2 = np.array([[int(i)%2, int(i)//2] for i in bit_index_1[:, 1]])
    bit_index_3 = np.array([[int(i)%2, int(i)//2] for i in bit_index_2[:, 1]])
    bit_index_4 = np.array([[int(i)%2, int(i)//2] for i in bit_index_3[:, 1]])
    bit_index_5 = np.array([[int(i)%2, int(i)//2] for i in bit_index_4[:, 1]])
    bit_index_6 = np.array([[int(i)%2, int(i)//2] for i in bit_index_5[:, 1]])
    bit_index_7 = np.array([ int(i)%2 for i in bit_index_6[:, 1]])
    # print(np.shape(bit_index_1))
    # print(np.shape(bit_index_1[:,0]))
    #dump the division row, we don't need it (note div not saved for last bit)
    bit_index_0 = np.reshape(bit_index_0, (shape[1], shape[2], 2))[:,:,0]
    bit_index_1 = np.reshape(bit_index_1, (shape[1], shape[2], 2))[:,:,0]
    bit_index_2 = np.reshape(bit_index_2, (shape[1], shape[2], 2))[:,:,0]
    bit_index_3 = np.reshape(bit_index_3, (shape[1], shape[2], 2))[:,:,0]
    bit_index_4 = np.reshape(bit_index_4, (shape[1], shape[2], 2))[:,:,0]
    bit_index_5 = np.reshape(bit_index_5, (shape[1], shape[2], 2))[:,:,0]
    bit_index_6 = np.reshape(bit_index_6, (shape[1], shape[2], 2))[:,:,0]
    bit_index_7 = np.reshape(bit_index_7, (shape[1], shape[2]))

    #return all bits
    return bit_index_0, bit_index_1, bit_index_2,\
           bit_index_3, bit_index_4, bit_index_5,\
           bit_index_6, bit_index_7
# bits = get_bits(data_SD, 0)

start_time = time.time()

def get_bits(data_SD, byte):
    '''
    cloud mask and byte stack to work on
    returns numpy.bytes array of byte stack of shape 2030x1354
    '''
    def int_2_bit(num):
        return np.string_('{0:08b}'.format(num)) #bin(num) is faster

    shape = np.shape(data_SD)
    data_SD = np.reshape(data_SD[byte,:,:], (shape[1]*shape[2]))
    data_SD_bit = [int_2_bit(num) for num in  data_SD]
    data_SD_bit = np.reshape(data_SD_bit, (shape[1], shape[2]))

    return data_SD_bit
data_SD_bit = get_bits(data_SD, 0)



def save_mod35(data, save_path):
    hf = h5py.File(save_path, 'w')
    hf.create_dataset('MOD_35_decoded', data=data)
    hf.close()

save_mod35(data_SD_bit, '/Users/vllgsbr2/Desktop/MODIS_Training/Data/mod_35/MOD_35.h5')


print("--- %s seconds ---" % (time.time() - start_time))


# 8   7  6  5  4 3 2 1
# 128 64 32 16 8 4 2 1

#possibilities
# -127 to 128
def decode_bits(decoded_mod35_hdf):
    data = decoded_mod35_hdf
    data_clear = [x[5:7]]




# #plot
data = np.array(h5py.File('/Users/vllgsbr2/Desktop/MODIS_Training/Data/mod_35/MOD_35.h5', 'r').get('MOD_35_decoded'))
print(type(data[0,0]))
print(np.shape(data))
print(data[0:10,0:10])
# plt.imshow(data)
# plt.show()


# #potential ideas
# x=7
# y=10
#
# print('x: ',x, '  y: ',y)
# bit_and = x & y
# bit_or  = x | y
# print('x & y: ',bit_and,' x | y: ',bit_or)
