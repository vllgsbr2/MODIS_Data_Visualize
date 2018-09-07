import numpy as np
from pyhdf.SD import SD
import pprint
import matplotlib.pyplot as plt

def get_data(filename, fieldname, SD_field_rawData):
    '''
    INPUT
          filename:      string  - hdf file filepath
          fieldname:     string  - name of desired dataset
          SD_or_rawData: boolean - 0 returns SD, 1 returns field, 2 returns rawData
    RETURN SD/ raw dataset
    '''
    if SD_field_rawData==0:
        return SD(filename) #science data set
    elif SD_field_rawData==1:
        return SD(filename).select(fieldname) #field
    else:
        return SD(filename).select(fieldname).get() #raw data

def get_scale_and_offset(data_field, num_bands, rad_or_ref):
    '''
    INPUT
          data:       numpy float array - get_data(filename,fieldname,SD_or_rawData=1)
          rad_or_ref: boolean           - True if radaince or False if reflectance offsets/scale desired
    RETURN
          2 numpy float arrays, scale factor & offset of size=number of bands
          for the chosen field
    '''

    if rad_or_ref:
        offset_name = 'radiance_offsets'
        scale_name  = 'radiance_scales'
    else:
        offset_name = 'reflectance_offsets'
        scale_name  = 'reflectance_scales'

    offset = np.empty((num_bands))
    scale_factor = np.empty((num_bands))

    for key, value in data_field.attributes().items():
        #print(key, value)
        if key == offset_name:
            offset = value
        if key == scale_name:
            scale_factor = value

    return scale_factor, offset

def get_radiance_or_reflectance(data_raw, data_field, rad_or_ref):
    '''
    INPUT
          data_raw:   get_data(filename, fieldname, SD_field_rawData=2)
          data_field: get_data(filename, fieldname, SD_field_rawData=1)
          rad_or_ref: boolean - True if radiance, False if reflectance
    RETURN
          radiance: numpy float array - shape=(number of bands, horizontal, vertical)
    '''
    #get dimensions of raw data
    num_bands = np.ma.size(data_raw, axis=0)
    num_horizontal = np.ma.size(data_raw, axis=1)
    num_vertical = np.ma.size(data_raw, axis=2)

    #reshape raw data to perform scale and offset correction
    data_raw_temp = np.reshape(data_raw,(num_bands, num_horizontal * num_vertical))
    scale_factor, offset = get_scale_and_offset(data_field, num_bands, rad_or_ref)

    #correct raw data to get radiance values
    #correct first band manually
    data_corrected_total = (data_raw_temp[0,:] - offset[0]) * scale_factor[0]
    #for loop to put all the bands together
    for i in range(1,num_bands):
        #corrected band
        data_corrected = (data_raw_temp[i,:] - offset[i]) * scale_factor[i]
        #aggregate bands
        data_corrected_total = np.concatenate((data_corrected_total, data_corrected), axis=0)

    #get original shape and return radiance/reflectance
    return data_corrected_total.reshape((num_bands, num_horizontal, num_vertical))


filename   = '/Users/vllgsbr2/Desktop/MODIS_Training/Data/MOD02HKM.A2018210.1530.061.2018211014142.hdf'
fieldname  = 'EV_250_Aggr1km_RefSB'
data_raw   = get_data(filename, fieldname, 2)
data_field = get_data(filename, fieldname, 1)
data_SD    = get_data(filename, fieldname, 0)
rad_or_ref = False #True for radiance, False for reflectance
radiance_EV_250_Aggr1km_RefSB = get_radiance_or_reflectance(data_raw, data_field, rad_or_ref)
#print(radiance)


fieldname  = 'EV_500_Aggr1km_RefSB'
data_raw   = get_data(filename, fieldname, 2)
data_field = get_data(filename, fieldname, 1)
data_SD    = get_data(filename, fieldname, 0)
rad_or_ref = False #True for radiance, False for reflectance
radiance_EV_500_Aggr1km_RefSB = get_radiance_or_reflectance(data_raw, data_field, rad_or_ref)


# file = SD('/Users/vllgsbr2/Desktop/MODIS_Training/Data/MOD021KM.A2017245.1635.061.2017258193451.hdf')
# data = file.select('EV_500_Aggr1km_RefSB')
# pprint.pprint(data.attributes()) #tells me scales, offsets and bands
#pprint.pprint(file.datasets()) # shows data fields in file from SD('filename')

#make channels for RGB photo (index 01234 -> band 34567)
image_blue  = radiance_EV_500_Aggr1km_RefSB[0,:,:] #band
image_green = radiance_EV_500_Aggr1km_RefSB[1,:,:] #band
image_red   = radiance_EV_250_Aggr1km_RefSB[0,:,:] #band

#use astropy to normalize radiance values to usable pixel brightness
from astropy.visualization import make_lupton_rgb
image_RGB = make_lupton_rgb(image_red, image_green, image_blue, stretch=0.5)

#plot
plt.imshow(image_RGB)
plt.show()
