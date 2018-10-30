from read_MODIS_35 import *
from PTA_Subset import crop_PTA
from plt_MODIS_02 import prepare_data
import time
from multiprocessing import Pool
import multiprocessing as mp

filename_MOD_35 = '/Users/vllgsbr2/Desktop/MODIS_Training/Data/toronto_09_05_18/MOD35_L2.A2018248.1630.061.2018249014414.hdf'#'/Users/vllgsbr2/Desktop/MODIS_Training/Data/venezuela_08_21_18/MOD35_L2.A2018233.1545.061.2018234021557.hdf'
filename_MOD_03 = '/Users/vllgsbr2/Desktop/MODIS_Training/Data/toronto_09_05_18/MOD03.A2018248.1630.061.2018248230625.hdf'#'/Users/vllgsbr2/Desktop/MODIS_Training/Data/venezuela_08_21_18/MOD03.A2018233.1545.061.2018233214936.hdf'
PTA_lat = 43.65
PTA_lon = -79.38
im_single = []

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
        im_single.append(crop_cm)

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
    return crop_cm

if __name__ == '__main__':

    ############################################################################
    #single core
    print('single core result')
    t0 = time.time()
    single_Core_test(filename_MOD_35, filename_MOD_03, PTA_lat, PTA_lon)
    print('---------------------- ',time.time()-t0, ' ----------------------')
    ############################################################################
    #multicore
    print('number of cores ', mp.cpu_count())
    print('multi core result')
    t0 = time.time()
    arr = [[filename_MOD_35, filename_MOD_03, PTA_lat, PTA_lon, 0],\
           [filename_MOD_35, filename_MOD_03, PTA_lat, PTA_lon, 1],\
           [filename_MOD_35, filename_MOD_03, PTA_lat, PTA_lon, 2],\
           [filename_MOD_35, filename_MOD_03, PTA_lat, PTA_lon, 3],\
           [filename_MOD_35, filename_MOD_03, PTA_lat, PTA_lon, 4],\
           [filename_MOD_35, filename_MOD_03, PTA_lat, PTA_lon, 5]]

    pool = Pool(6)

    im_multi = pool.map(multi_Core_test, arr)
    print('---------------------- ',time.time()-t0, ' ----------------------')
    ############################################################################
    #test result

    print(np.shape(im_single))
    print(np.shape(im_multi))

    print('Cloud_Mask_Flag              :', np.all(im_multi[0]==im_single[0]))
    print('Unobstructed_FOV_Quality_Flag:', np.all(im_multi[1]==im_single[1]))
    print('Day_Night_Flag               :', np.all(im_multi[2]==im_single[2]))
    print('Sun_glint_Flag               :', np.all(im_multi[3]==im_single[3]))
    print('Snow_Ice_Background_Flag     :', np.all(im_multi[4]==im_single[4]))
    print('Land_Water_Flag              :', np.all(im_multi[5]==im_single[5]))

    ###########################################################################
    #plot results
    import matplotlib.colors as matCol
    from matplotlib.colors import ListedColormap

    f, ax = plt.subplots(ncols=6, nrows=2)

    cmap=plt.cm.PiYG
    cmap = ListedColormap(['white', 'green', 'blue','black'])
    norm = matCol.BoundaryNorm(np.arange(0,5,1), cmap.N)

    ax[0,0].set_title('Cloud_Mask_Flag')
    ax[0,1].set_title('Unobstructed_FOV_Quality_Flag')
    ax[0,2].set_title('Day_Night_Flag')
    ax[0,3].set_title('Sun_glint_Flag')
    ax[0,4].set_title('Snow_Ice_Background_Flag')
    ax[0,5].set_title('Land_Water_Flag')

    im = ax[0,0].imshow(im_single[0], vmin=0, vmax=3, cmap=cmap, norm=norm)
    im = ax[0,1].imshow(im_single[1], vmin=0, vmax=3, cmap=cmap, norm=norm)
    im = ax[0,2].imshow(im_single[2], vmin=0, vmax=3, cmap=cmap, norm=norm)
    im = ax[0,3].imshow(im_single[3], vmin=0, vmax=3, cmap=cmap, norm=norm)
    im = ax[0,4].imshow(im_single[4], vmin=0, vmax=3, cmap=cmap, norm=norm)
    im = ax[0,5].imshow(im_single[5], vmin=0, vmax=3, cmap=cmap, norm=norm)

    im = ax[1,0].imshow(im_multi[0], vmin=0, vmax=3, cmap=cmap, norm=norm)
    im = ax[1,1].imshow(im_multi[1], vmin=0, vmax=3, cmap=cmap, norm=norm)
    im = ax[1,2].imshow(im_multi[2], vmin=0, vmax=3, cmap=cmap, norm=norm)
    im = ax[1,3].imshow(im_multi[3], vmin=0, vmax=3, cmap=cmap, norm=norm)
    im = ax[1,4].imshow(im_multi[4], vmin=0, vmax=3, cmap=cmap, norm=norm)
    im = ax[1,5].imshow(im_multi[5], vmin=0, vmax=3, cmap=cmap, norm=norm)

    cbar_ax = f.add_axes([0.93, 0.15, 0.015, 0.7])
    cbar = plt.colorbar(im, cax=cbar_ax)
    cbar.set_ticks([0.5,1.5,2.5,3.5])
    cbar.set_ticklabels(['cloudy\nwater', 'uncertain\nclear\n\ncoastal'\
                        ,'probably\nclear\n\ndesert', 'confident\nclear\n\nland'])

    plt.suptitle('MODIS Cloud Mask\nSingle Core\nMulti Core')
    ax[0,0].set_ylabel('Single Core')
    ax[1,0].set_ylabel('Multi Core')

    plt.show()
