import numpy as np
import matplotlib.pyplot as plt
import h5py

band_1_coef = {\
           'b1ndvi0' : [32.00000000,   0.00000000,  0.00000000,  0.00000000,\
                        42.00000000,   0.00000000,  0.00000000,  0.00000000,\
                        52.00000000,   0.00000000,  0.00000000,  0.00000000],\
           'b1ndvi1' : [24.00000000,   0.00000000,  0.00000000,  0.00000000,\
                        28.00000000,   0.00000000,  0.00000000,  0.00000000,\
                        32.00000000,   0.00000000,  0.00000000,  0.00000000 ],\
           'b1ndvi2' : [99.13076923,  -2.00907925,  0.01492075, -0.00003531,\
                        122.19090909, -2.32652292,  0.01659848, -0.00003681,\
                        142.66293706, -2.57860528,  0.01773252, -0.00003685],\
           'b1ndvi3' : [85.07902098,  -1.59413364,  0.01123310, -0.00002556,\
                        144.56573427, -2.81054779,  0.01967366, -0.00004324,\
                        204.35454545, -4.03411810,  0.02816667, -0.00006103 ],\
           'b1ndvi4' : [85.03846154,  -1.50831391,  0.01006760, -0.00002199,\
                        165.15314685, -3.24716783,  0.02255594, -0.00004965,\
                        242.06363636, -4.90912587,  0.03445455, -0.00007587],\
           'b1ndvi5' : [81.00979021,  -1.37731935,  0.00881294, -0.00001859,\
                        220.36783217, -4.44111888,  0.03087762, -0.00006888,\
                        359.72587413, -7.50491841,  0.05294231, -0.00011917],\
           'b1ndvi6' : [76.94055944,  -1.35441725,  0.00896096, -0.00001952,\
                        172.36783217, -3.33144911,  0.02242308, -0.00004810,\
                        267.90909091, -5.31620047,  0.03597727, -0.00007698],\
           'b1ndvi7' : [85.83006993,  -1.55480575,  0.01025932, -0.00002216,\
                        160.73706294, -3.07291375,  0.02041900, -0.00004330,\
                        237.37622378, -4.63444833,  0.03091317, -0.00006525],\
           'b1ndvi8' : [105.02447552, -1.98017094,  0.01319522, -0.00002877,\
                        135.50699301, -2.59097902,  0.01749301, -0.00003811,\
                        165.33006993, -3.18872183,  0.02171387, -0.00004734],\
           'b1ndvi9' : [105.02447552, -1.98017094,  0.01319522, -0.00002877,\
                        135.50699301, -2.59097902,  0.01749301, -0.00003811,\
                        165.33006993, -3.18872183,  0.02171387, -0.00004734]\
               }

band_8_coef = {\

           'b8ndvi0' : [282.74916084, -5.42869658,  0.03660781, -0.00008092,\
                        344.87048951, -6.80660839,  0.04770163, -0.00010991,\
                        407.83734266, -8.20392385,  0.05894114, -0.00013926],\
           'b8ndvi1' : [229.50727273, -4.31606061,  0.02868182, -0.00006212,\
                        316.38517483, -6.41910256,  0.04603089, -0.00010787,\
                        403.78188811, -8.52743395,  0.06335781, -0.00015340],\
           'b8ndvi2' : [239.32391608, -4.49928127,  0.02977214, -0.00006436,\
                        270.31741259, -5.33625680,  0.03757168, -0.00008609,\
                        301.76013986, -6.18557498,  0.04546562, -0.00010806]\
               }


#4 coefficients (abcd) for 3 thresholds (confident clear & cloudy, midpoint)
#for 10 ndvi 0.1 intervals from 0 to 1
#T_NDVI_X = a*s**3 + b*s**2 + c*s + d
def get_threshold(granule_time_stamp, PTA_database_path):
    '''
    INPUT:
          granule_time_stamp: - str - YYYYDDD.HHMM
          PTA_database_path : - str - <filepath>.hf
    RETURN:
          numpy float array of thresholds (2030,1354)
    '''

    'solarAzimuth':solarAzimuth,\
                        'sensorAzimuth':sensorAzimuth,\
                        'solarZenith':solarZenith,\
                        'sensorZenith'
    #get granule from PTA file
    granule = h5py.File(PTA_database_path, 'r')
    #extract sunview geometery to calc scattering angle
    sza = np.array(granule.get(granule_time_stamp + \
                   '/sunView_geometry/solarZenith'))
    vza = np.array(granule.get(granule_time_stamp + \
                   '/sunView_geometry/sensorZenith'))
    raa = np.array(granule.get(granule_time_stamp + \
                   '/sunView_geometry/sensorAzimuth')) - \
          np.array(granule.get(granule_time_stamp + \
                   '/sunView_geometry/solarAzimuth'))

    #calc scattering angle
    scatter_angle = (180/np.pi) * np.arccos(−np.cos(sza) * np.cos(vza) \
                                - np.sin(sza) * np.sin(vza) * np.cos(raa))
    #extract bands b1 and b2
    b1 = np.array(granule.get(granule_time_stamp + \
                   '/reflectance/band_1'))
    b2 = np.array(granule.get(granule_time_stamp + \
                   '/reflectance/band_2'))
    #calc NDVI (b2-b1)/(b2+b1)
    NDVI   = (b2-b1)/(b2+b1)
    #find indicies where of 10 NDVI intervals from 0 to 1
    NDVI_0_idx = np.where(NDVI<=0.1)
    NDVI_1_idx = np.where(NDVI<=0.2 & NDVI>0.1)
    NDVI_2_idx = np.where(NDVI<=0.3 & NDVI>0.2)
    NDVI_3_idx = np.where(NDVI<=0.4 & NDVI>0.3)
    NDVI_4_idx = np.where(NDVI<=0.5 & NDVI>0.4)
    NDVI_5_idx = np.where(NDVI<=0.6 & NDVI>0.5)
    NDVI_6_idx = np.where(NDVI<=0.7 & NDVI>0.6)
    NDVI_7_idx = np.where(NDVI<=0.8 & NDVI>0.7)
    NDVI_8_idx = np.where(NDVI<=0.9 & NDVI>0.8)
    NDVI_9_idx = np.where(NDVI<=1.0 & NDVI>0.9)


    #make an array to put thresholds into
    thresholds = np.empty((2030,1354, 3))
    thresholds[NDVI_0_idx, :] = scatter_angle[NDVI_0_idx] * band_1_coef['b1ndvi0']\
