'''
Download MODIS 02,03,35 products from LAADS DAAC csv file
and check the integrity of the file
'''
import pandas as pd
import urllib.request
import h5py
import os
import sys
from plt_MODIS_02 import get_data
#sys.argv[0] is always the script filepath

def check_file_integrity(url, filename, fieldnames, save_path, directory):
    #check that file downloaded and has some size and datafields are not corrupt
    statinfo   = os.stat(save_path + directory + filename)
    file_size  = statinfo.st_size
    filename   = save_path + directory + filename

    if url[23:25]=='02':
        if file_size > 0 :
            try:
                get_data(filename, fieldnames[2], 2)
                get_data(filename, fieldnames[3], 2)
                get_data(filename, fieldnames[4], 2)
            except:
                print(save_path + directory + filename, ' is corrupt')

        else:
            print(save_path + directory + filename, 'failed to download properly')

    elif url[23:25]=='03':
        if file_size > 0:
            try:
                get_data(filename, fieldnames[5], 2)
                get_data(filename, fieldnames[6], 2)
                get_data(filename, fieldnames[7], 2)
                get_data(filename, fieldnames[8], 2)
                get_data(filename, fieldnames[9], 2)
                get_data(filename, fieldnames[10], 2)
            except:
                print(save_path + directory + filename, ' is corrupt')

        else:
            print(save_path + directory + filename, ' failed to download properly')

    else:
        if file_size > 0:
            try:
                get_data(filename, fieldnames[0], 2)
                get_data(filename, fieldnames[1], 2)
            except:
                print(save_path + directory + filename, ' is corrupt')
        else:
            print(save_path + directory + filename, 'failed to download properly')

def download_granule(url, url_base, save_path, download_check):
    #check product to put into corresponding directory
    if url[23:25]=='03':
        n = 35
        directory = 'MOD_03/'
    elif url[23:25]=='02':
        n = 38
        directory = 'MOD_02/'
    else:
        n = 38
        directory = 'MOD_35/'

    #give file its full name without url path
    filename = '{}'.format(url[n:])

    #arg1: Download the file and  arg2: save it locally
    if download_check:
        urllib.request.urlretrieve(url_base+url, save_path + directory + filename)
        print('file--- {} ---  {} ---downloaded\n '.format(filenum+1, filename))

    return filename, directory







filepath          = sys.argv[1]
filenames_archive = pd.read_csv(filepath, header=0)
url_base          = 'https://ladsweb.modaps.eosdis.nasa.gov'
save_path         = '/data/keeling/a/vllgsbr2/b/modis_data/toronto_PTA/'

filenames_archive = filenames_archive['fileUrls from query MOD021KM--61 MOD03--61 MOD35_L2--61 2017-01-01..2017-12-31 x-79.9y43.9 x-79.1y43.5[5]']

fieldnames = ['Cloud_Mask', 'Quality_Assurance',\
              'EV_1KM_RefSB', 'EV_250_Aggr1km_RefSB', 'EV_500_Aggr1km_RefSB',\
              'SolarZenith', 'SensorZenith', 'SolarAzimuth','SensorAzimuth', \
              'Latitude', 'Longitude']
# #use this loop to simultaniously check file after download
# for url in filenames_archive:
#     filename, directory  = download_granule(url, url_base, save_path)
#     check_file_integrity(url, filename, fieldnames, save_path, directory)

#use this loop to just check pre downloaded files
for url in filenames_archive:
    filename, directory  = download_granule(url, url_base, save_path, False)
    check_file_integrity(url, filename, fieldnames, save_path, directory)
