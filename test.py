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
          numpy float array of thresholds (2030,1354,3)
    '''

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

    #convert to radians
    sza = sza * np.pi/180
    vza = vza * np.pi/180
    raa = raa * np.pi/180
    #calc scattering angle (radians or degrees?)
    scatter_angle = (180/np.pi) * np.arccos(-np.cos(sza) * np.cos(vza) \
                                - np.sin(sza) * np.sin(vza) * np.cos(raa))
    #extract bands b1 and b2
    b1 = np.array(granule.get(granule_time_stamp + \
                   '/reflectance/band_1'))
    b2 = np.array(granule.get(granule_time_stamp + \
                   '/reflectance/band_2'))
    #calc NDVI (b2-b1)/(b2+b1)
    NDVI = (b2-b1)/(b2+b1)

    #find indicies for 10 NDVI intervals from [0,1)
    NDVI_0_idx = np.where(NDVI<0.1)
    NDVI_1_idx = np.where(np.any(NDVI>=0.1) and np.any(NDVI<0.2))
    NDVI_2_idx = np.where(np.any(NDVI>=0.2) and np.any(NDVI<0.3))
    NDVI_3_idx = np.where(np.any(NDVI>=0.3) and np.any(NDVI<0.4))
    NDVI_4_idx = np.where(np.any(NDVI>=0.4) and np.any(NDVI<0.5))
    NDVI_5_idx = np.where(np.any(NDVI>=0.5) and np.any(NDVI<0.6))
    NDVI_6_idx = np.where(np.any(NDVI>=0.6) and np.any(NDVI<0.7))
    NDVI_7_idx = np.where(np.any(NDVI>=0.7) and np.any(NDVI<0.8))
    NDVI_8_idx = np.where(np.any(NDVI>=0.8) and np.any(NDVI<0.9))
    NDVI_9_idx = np.where(np.any(NDVI>=0.9) and np.any(NDVI<1))

    #find where NDVI <0.25 to alert function to switch to band 8 coefficients
    NDVI_sub25_idx = np.where(NDVI<0.25)

    def thresholds_helper_func(ndvi_bin_base, NDVI_X_idx, scatter_angle, thresholds,\
                               thresh_num):
        '''
        INPUT:
              ndvi_bin     : - int - 0-9 which interval of ndvi every 0.1 steps
              NDVI_X_idx   : - 2D numpy array - indicies of NDVI interval
              scatter_angle: - 2D numpy array - scattering angle for every pixel
                                                (2030,1354)
              thresholds   : - 2D numpy array - array to fill with thresholds
                                                (2030,1354,3)
              thresh_num   : - int - which threshold are you calculating?
                                     0,1,2 -> clear,midpoint,cloudy
        RETURN:
              thresholds : - numpy array (2030,1354, 3) - with 3 thresholds for
                                                          every pixel; confident
                                                          cloudy, confident
                                                          clear, and a midpoint
        '''

        ndvi_bin = 'b{0}ndvi{1}'.format('1', ndvi_bin_base)

        #collect band 1 coefficients for 1 of 3 threshold types
        if thresh_num == 0:
            a,b,c,d = band_1_coef[ndvi_bin][3],  band_1_coef[ndvi_bin][2],\
                      band_1_coef[ndvi_bin][1],  band_1_coef[ndvi_bin][0]
        elif thresh_num == 1:
            a,b,c,d = band_1_coef[ndvi_bin][7],  band_1_coef[ndvi_bin][6],\
                      band_1_coef[ndvi_bin][5],  band_1_coef[ndvi_bin][4]
        else:
            a,b,c,d = band_1_coef[ndvi_bin][11], band_1_coef[ndvi_bin][10],\
                      band_1_coef[ndvi_bin][9] , band_1_coef[ndvi_bin][8]
        print('scatter_angle shape: ', np.shape(scatter_angle))
        print('hi')
        #T_NDVI_X = a*S^3 + b*S^2 + c*S + d
        #where S is scattering angle & a,b,c,d are the coefficients
        (thresholds[:,:,thresh_num])[NDVI_X_idx] =          \
           np.power(scatter_angle[NDVI_X_idx], 3) * a \
         + np.power(scatter_angle[NDVI_X_idx], 2) * b \
         + scatter_angle[NDVI_X_idx] * c              \
         + d * np.ones(np.shape(scatter_angle[NDVI_X_idx]))

        #recalc thresholds w/band 8 coefficients for incidies in NDVI_sub25_idx
        ndvi_bin = 'b{0}ndvi{1}'.format('8', ndvi_bin_base)
        #collect band 8 coefficients for 1 of 3 threshold types
        if thresh_num == 0:
            a,b,c,d = band_8_coef[ndvi_bin][3],  band_8_coef[ndvi_bin][2],\
                      band_8_coef[ndvi_bin][1],  band_8_coef[ndvi_bin][0]
        elif thresh_num == 1:
            a,b,c,d = band_8_coef[ndvi_bin][7],  band_8_coef[ndvi_bin][6],\
                      band_8_coef[ndvi_bin][5],  band_8_coef[ndvi_bin][4]
        else:
            a,b,c,d = band_8_coef[ndvi_bin][11], band_8_coef[ndvi_bin][10],\
                      band_8_coef[ndvi_bin][9],  band_8_coef[ndvi_bin][8]


        (thresholds[:,:,thresh_num])[NDVI_sub25_idx] = \
           np.power(scatter_angle[NDVI_sub25_idx], 3) * a \
         + np.power(scatter_angle[NDVI_sub25_idx], 2) * b \
         + scatter_angle[NDVI_sub25_idx] * c              \
         + d * np.ones((np.shape(scatter_angle[NDVI_sub25_idx])))

        return thresholds

    #create empty thresholds array to fill with thresholds_helper_func()
    thresholds  = np.empty((2030,1354, 3))

    thresholds = thresholds_helper_func(0, NDVI_0_idx, scatter_angle, thresholds, 0)
    thresholds = thresholds_helper_func(1, NDVI_1_idx, scatter_angle, thresholds, 0)
    thresholds = thresholds_helper_func(2, NDVI_2_idx, scatter_angle, thresholds, 0)
    thresholds = thresholds_helper_func(3, NDVI_3_idx, scatter_angle, thresholds, 0)
    thresholds = thresholds_helper_func(4, NDVI_4_idx, scatter_angle, thresholds, 0)
    thresholds = thresholds_helper_func(5, NDVI_5_idx, scatter_angle, thresholds, 0)
    thresholds = thresholds_helper_func(6, NDVI_6_idx, scatter_angle, thresholds, 0)
    thresholds = thresholds_helper_func(7, NDVI_7_idx, scatter_angle, thresholds, 0)
    thresholds = thresholds_helper_func(8, NDVI_8_idx, scatter_angle, thresholds, 0)
    thresholds = thresholds_helper_func(9, NDVI_9_idx, scatter_angle, thresholds, 0)

    thresholds = thresholds_helper_func(0, NDVI_0_idx, scatter_angle, thresholds, 1)
    thresholds = thresholds_helper_func(1, NDVI_1_idx, scatter_angle, thresholds, 1)
    thresholds = thresholds_helper_func(2, NDVI_2_idx, scatter_angle, thresholds, 1)
    thresholds = thresholds_helper_func(3, NDVI_3_idx, scatter_angle, thresholds, 1)
    thresholds = thresholds_helper_func(4, NDVI_4_idx, scatter_angle, thresholds, 1)
    thresholds = thresholds_helper_func(5, NDVI_5_idx, scatter_angle, thresholds, 1)
    thresholds = thresholds_helper_func(6, NDVI_6_idx, scatter_angle, thresholds, 1)
    thresholds = thresholds_helper_func(7, NDVI_7_idx, scatter_angle, thresholds, 1)
    thresholds = thresholds_helper_func(8, NDVI_8_idx, scatter_angle, thresholds, 1)
    thresholds = thresholds_helper_func(9, NDVI_9_idx, scatter_angle, thresholds, 1)

    thresholds = thresholds_helper_func(0, NDVI_0_idx, scatter_angle, thresholds, 2)
    thresholds = thresholds_helper_func(1, NDVI_1_idx, scatter_angle, thresholds, 2)
    thresholds = thresholds_helper_func(2, NDVI_2_idx, scatter_angle, thresholds, 2)
    thresholds = thresholds_helper_func(3, NDVI_3_idx, scatter_angle, thresholds, 2)
    thresholds = thresholds_helper_func(4, NDVI_4_idx, scatter_angle, thresholds, 2)
    thresholds = thresholds_helper_func(5, NDVI_5_idx, scatter_angle, thresholds, 2)
    thresholds = thresholds_helper_func(6, NDVI_6_idx, scatter_angle, thresholds, 2)
    thresholds = thresholds_helper_func(7, NDVI_7_idx, scatter_angle, thresholds, 2)
    thresholds = thresholds_helper_func(8, NDVI_8_idx, scatter_angle, thresholds, 2)
    thresholds = thresholds_helper_func(9, NDVI_9_idx, scatter_angle, thresholds, 2)
    print(thresholds[:2, :2, 0:])

    #at this time thresholds should be a completely full array of (2030,1354,3)
    return thresholds




if __name__ == '__main__':

    granule_time_stamp = '2017228.1545'
    PTA_database_path  = '/data/keeling/a/vllgsbr2/b/modis_data/toronto_PTA/'\
                         'database/toronto_PTA_Subsets.hf'
    get_threshold(granule_time_stamp, PTA_database_path)
