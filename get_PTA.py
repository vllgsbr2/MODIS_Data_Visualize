'''
Download MODIS 02,03,35 products from LAADS DAAC csv file
'''
import pandas as pd
import urllib.request
import sys
#sys.argv[0] is always the script filepath

filepath          = sys.argv[1]
filenames_archive = pd.read_csv(filepath, header=0)
url_base          = 'https://ladsweb.modaps.eosdis.nasa.gov'
save_path         = '/Users/vllgsbr2/Desktop/MODIS_Training/Data/test_getPTA_download/'

filenames_archive = filenames_archive['fileUrls for custom selected']

for url in filenames_archive:
    #check product to put into corresponding directory
    if url[23:25]=='03':
        n = 34
        directory = 'MOD_03'
    elif url[23:25]=='02':
        n = 38
        directory = 'MOD_02'
    else:
        n = 38
        directory = 'MOD_35'

    #give file its full name without url path
    filename = '{}'.format(url[n:])

    #arg1: Download the file and  arg2: save it locally
    urllib.request.urlretrieve(url_base+url, save_path + directory + filename)
