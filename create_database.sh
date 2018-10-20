#!bin/bash

#This script will call the appropiate python script to grab the PTA granule csv;
#call get_PTA.py to download the granules to MOD35, MOD02 & MOD03 directories;
#call PTA_Subset.py to crop one granule at a time and save it for all granule
#triplets;

f_name='/Users/vllgsbr2/Desktop/MODIS_Training/Data/mod_02_1km_2017_filenames.csv'

#download granules in f_name
python get_PTA.py f_name

#subset all files
./
