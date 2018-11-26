'''
MODIS statistics.
Produce PDFs of cloud masking tests vs cloud mask output.
Therefore 4(cloudy confidence levels) for 5(cloud mask tests) = 4 PDFs
x axis is each test
y axis is frequency it returns yes
will allow to see what test is most dominate for each cloudy interval
'''

import numpy as np
import os
import h5py
import matplotlib.pyplot as plt
import time

# file_path  = 'sdjfhglsjfhg.h5'
# granule    = '2017233.1635'
# subgroup_1 = 'cloud_mask'
# subgroup_2 = 'Unobstructed_FOV_Quality_Flag'
# group_path = granule + subgroup_1 + subgroup_2
# cloud_mask = np.array(h5py.File(file, 'r').get(group_path))
# #make a list of all granules
# granules   = np.array(h5py.File(file, 'r').visit()
# #access a
# for i in range(len(granule)):
num_granules   = 20   #704
num_height     = 203 #2030
num_width      = 135 #1354
num_tests      = 5
num_cloudiness = 1
data = np.random.randint(low=0, high=4, size=(num_granules,   \
                                              num_height,     \
                                              num_width,      \
                                              num_tests + num_cloudiness))
# #cloudiness per pixel
# data[:,:,:,0]
# #all the tests per pixel
# data[:,:,:,1:]
# np.set_printoptions(threshold=np.nan)
# print(data[:,:,:,1:])

################################################################################
#calculate PDFs
#5 cm tests/pixel, 1cloudy confidence/pixel
#group pixel by cloudy/prob cloudy/prob clear/clear
#data shape -> (704, 4, 5, 2030, 1354) ->
#(granule, cloudiness, test, hieght,width)
#data_<cloudiness> shape -> (XXX_, 5, XXXX, XXXX) ->
#(granules, test, hieght, width)
# print(np.where(data[:,0,:,:,:]==0))
data_cloudy       = data[np.where(data[:,:,:,0]==0)]
data_prob_cloudy  = data[np.where(data[:,:,:,0]==1)]
data_prob_clear   = data[np.where(data[:,:,:,0]==2)]
data_clear        = data[np.where(data[:,:,:,0]==3)]

#cloudiness dimension will collapse. all other dims may change shape
#cloudy PDF
#now collapse (return) test dim, then flatten across granule, height & width
def get_tests(data):
    '''
    INPUT:
          data - numpy array shape (XXX, 5, XXXX, XXXX) - cloudiness array
    RETURN:
          5 numpy arrays flattened to dim0*dim2*dim3 of data
    '''
    test_1 = data[:,1].flatten()
    test_2 = data[:,2].flatten()
    test_3 = data[:,3].flatten()
    test_4 = data[:,4].flatten()
    test_5 = data[:,5].flatten()

    return test_1, test_2, test_3, test_4, test_5

cloudy_tests       = get_tests(data_cloudy)
prob_cloudy_tests  = get_tests(data_prob_cloudy)
prob_clear_tests   = get_tests(data_prob_clear)
cloudy_clear_tests = get_tests(data_clear)



#get length of each test
#this will be the height of each bar in histogram/PDF
#new shape will be (test1, test2, test3, test4)
#each test contains the num times returned yes to cloudy confidence of pixel

#FORGOT ONE STEP. TAKE YES ANSWERS FROM CLOUD MASK!!****************************
#cloudy_yes = np.where(cloudy_tests[0]==)
cloudy_hist      = [cloudy_tests[0].size, cloudy_tests[1].size,\
                    cloudy_tests[2].size, cloudy_tests[3].size,\
                    cloudy_tests[4].size]
prob_cloudy_hist = [prob_cloudy_tests[0].size, prob_cloudy_tests[1].size,\
                    prob_cloudy_tests[2].size, prob_cloudy_tests[3].size,\
                    prob_cloudy_tests[4].size]
prob_clear_hist  = [prob_clear_tests[0].size, prob_clear_tests[1].size,\
                    prob_clear_tests[2].size, prob_clear_tests[3].size,\
                    prob_clear_tests[4].size]
clear_hist       = [cloudy_tests[0].size, cloudy_tests[1].size,\
                    cloudy_tests[2].size, cloudy_tests[3].size,\
                    cloudy_tests[4].size]

#the prepared arrays above are now ready to be plotted
f, ax = plt.subplots(ncols=2, nrows=2)
position = np.arange(5)
#graph
ax[0,0].bar(position, cloudy_hist     )
ax[0,1].bar(position, prob_cloudy_hist)
ax[1,0].bar(position, prob_clear_hist )
ax[1,1].bar(position, clear_hist      )

#set title
ax[0,0].set_title('cloudy_hist')
ax[0,1].set_title('prob_cloudy_hist')
ax[1,0].set_title('prob_clear_hist')
ax[1,1].set_title('clear_hist')

#label axies
ax[0,0].set_xticks(position)
ax[0,1].set_xticks(position)
ax[1,0].set_xticks(position)
ax[1,1].set_xticks(position)

ax[0,0].set_xticklabels(['test 1', 'test 2', 'test 3','test 4', 'test 5'])
ax[0,1].set_xticklabels(['test 1', 'test 2', 'test 3','test 4', 'test 5'])
ax[1,0].set_xticklabels(['test 1', 'test 2', 'test 3','test 4', 'test 5'])
ax[1,1].set_xticklabels(['test 1', 'test 2', 'test 3','test 4', 'test 5'])

plt.show()
