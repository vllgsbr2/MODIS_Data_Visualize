'''
AUTHOR: Javier Villegas Bravo
DATE  : Fall 2018

FUNCTION:
find the timestamp of MISR granules that pass over our PTA
Then use this timestamp to grab the corresponding MODIS granules
(MODIS and MISR are on same satellite pointing in same direction)

PURPOSE:
Use the generated list to subselect MODIS granules from nearline storage
to feed into PTA_Subset.py to ultimately build the validation/training set
'''
