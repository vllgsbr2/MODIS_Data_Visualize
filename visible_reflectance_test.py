'''
use thresholds from unpack_thresholds.py to bin radiances (or reflectances???)
into 4 confidence levels and into a binary (clear/cloudy) as well
'''
from unpack_thresholds import get_threshold
from plt_MODIS_02 import prepare_data
import matplotlib.pyplot as plt
import numpy as np
import h5py
#granule_time_stamp+'/cloud_mask_test/Cloud_Flag_Visible_Reflectance'
granule_time_stamp = '2017228.1545'
PTA_database_path = '/Users/vllgsbr2/Desktop/toronto_PTA_Subsets.HDF5'

thresholds = get_threshold(granule_time_stamp, PTA_database_path)

#crop radiances
granule = h5py.File(PTA_database_path, 'r')
#extract sunview geometery to calc scattering angle
radiances = np.array(granule.get(granule_time_stamp + \
                          '/radiance/band_1'))
vis_ref_test = np.array(granule.get(granule_time_stamp + \
                        '/cloud_mask_tests/Cloud_Flag_Visible_Reflectance'))
sfc_type = np.array(granule.get(granule_time_stamp + \
                        '/cloud_mask/Land_Water_Flag'))
granule.close()

#threshold has shape of (height, width, 3)
#height & width will depend on cropped size of image & 3 thresholds per pixel

#we need to check every pixel individualy with its 3 thresholds for cloud mask
#only mid point threshold for binary cloud mask

swath_shape = np.shape(radiances)
#place to store the reprduced cloud mask
cloud_mask  = np.zeros(swath_shape)

#find where the thresholds are passed and mark it with a boolean
cloudy      =  radiances >= thresholds[:,:,2]
prob_cloudy = (radiances <  thresholds[:,:,2]) & (radiances > thresholds[:,:,1])
prob_clear  = (radiances <= thresholds[:,:,1]) & (radiances > thresholds[:,:,0])
clear       =  radiances <= thresholds[:,:,0]

#save the indicies of where the conditions showed true
cloudy_idx      = np.where(cloudy==True)
prob_cloudy_idx = np.where(prob_cloudy==True)
prob_clear_idx  = np.where(prob_clear==True)
clear_idx       = np.where(clear==True)

cloud_mask[cloudy_idx]      = 3
cloud_mask[prob_cloudy_idx] = 2
cloud_mask[prob_clear_idx]  = 1
cloud_mask[clear_idx]       = 0

#plot
f, ax = plt.subplots(nrows=2, ncols=2)
cmap = 'PiYG'
cax_rad = ax[0,0].imshow(radiances, cmap=cmap)
ax[0,0].set_title('659nm Radiance Field')
ax[0,0].set_xticks([])
ax[0,0].set_yticks([])

#f.colorbar(cax_rad)


cax_cm = ax[0,1].imshow(cloud_mask, cmap = cmap)
ax[0,1].set_title('Reproduced MODIS Cloud Mask')
ax[0,1].set_xticks([])
ax[0,1].set_yticks([])
#f.colorbar(cax_cm)

cax_cm = ax[1,1].imshow(vis_ref_test, cmap = cmap)
ax[1,1].set_title('MODIS Cloud Mask')
ax[1,1].set_xticks([])
ax[1,1].set_yticks([])

cax_cm = ax[1,0].imshow(sfc_type)
ax[1,0].set_title('Surface Type')
ax[1,0].set_xticks([])
ax[1,0].set_yticks([])

plt.show()
















#
