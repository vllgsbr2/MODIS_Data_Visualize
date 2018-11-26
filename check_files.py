import pandas as pd
import numpy as np
import sys
import os

filepath          = sys.argv[1]
filenames_archive = pd.read_csv(filepath, header=0)
url_base          = 'https://ladsweb.modaps.eosdis.nasa.gov'
save_path         = '/data/keeling/a/vllgsbr2/b/modis_data/toronto_PTA/'

filenames_archive = filenames_archive['fileUrls from query MOD021KM--61 MOD0'\
                                      '3--61 MOD35_L2--61 2017-01-01..2017-1'\
                                      '2-31 x-79.9y43.9 x-79.1y43.5[5]']

#everything
filenames_archive_mod35_L0 = filenames_archive.sort_values()[:21]
filenames_archive_mod02    = filenames_archive.sort_values()[21:704+21]
filenames_archive_mod03    = filenames_archive.sort_values()[704+21:1408+21]
filenames_archive_mod35    = filenames_archive.sort_values()[1408+21:]

#what did not download
filenames_archive_mod02    = filenames_archive_mod02[-19:]
filenames_archive_mod03    = filenames_archive_mod03[-19:]
filenames_archive_mod35_L0 = filenames_archive_mod35_L0

PTA_file_path   = '/data/keeling/a/vllgsbr2/b/modis_data/toronto_PTA'

filename_MOD_02 = np.array(os.listdir(PTA_file_path + '/MOD_02'))
filename_MOD_03 = np.array(os.listdir(PTA_file_path + '/MOD_03'))
filename_MOD_35 = np.array(os.listdir(PTA_file_path + '/MOD_35'))

# print(filenames_archive_mod02)
# print(filenames_archive_mod03)
# print(filenames_archive_mod35_L0)

for i in filenames_archive_mod02:
    print(i,end=',')
for i in filenames_archive_mod03:
    print(i,end=',')
for i in filenames_archive_mod35_L0:
    print(i,end=',')
