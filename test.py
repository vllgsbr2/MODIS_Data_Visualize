import h5py
import numpy as np


data = np.array(h5py.File('test.hf', 'r').get('2018233.1545/band_1'))
print(data)
