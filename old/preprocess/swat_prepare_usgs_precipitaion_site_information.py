import sys
import os
import numpy as np
from numpy  import array


from pyearth.toolbox.reader.text_reader_string import text_reader_string

def swat_prepare_precipitation_site_information(sFilename_configuration_in):
     #check whether the configuration exist or not
    
    
    sRegion = config['sRegion']
   

    sFilename_precipiation_site = sWorkspace_data + slash + 'swat' + slash + sRegion + slash \
    + 'auxiliary' + slash + 'precipiation_site.txt'
    print(sFilename_precipiation_site)
    ofs = open(sFilename_precipiation_site, 'w')

    sLine='name, long, lat\n'
    ofs.write(sLine)
    #in our study area, there are only a free precipiation site from the report
    sName = 'C2'
    dLatitude = 37 + 13/60.0 + 0/3600.0 
    dLongitude = 105 + 3/60.0 + 0/3600.0
    sLine = sName + ', ' +  "{:0.6f}".format(-dLongitude) + ', ' \
       +  "{:0.6f}".format(dLatitude) + '\n'
    ofs.write(sLine)

    #C-18 Upper Molino Canyon,
    sName = 'C18' 
    dLatitude = 37 + 11/60.0 + 11/3600.0 
    dLongitude = 104 + 49/60.0 + 48/3600.0
    sLine = sName + ', ' +  "{:0.6f}".format(-dLongitude) + ', ' \
       +  "{:0.6f}".format(dLatitude) + '\n'
    ofs.write(sLine)

    #C-19 Lower Molino Canyon,
    sName = 'C19'
    dLatitude = 37 + 7/60.0 + 56/3600.0 
    dLongitude = 104 + 48/60.0 + 35/3600.0
    sLine = sName + ', ' +  "{:0.6f}".format(-dLongitude) + ', ' \
       +  "{:0.6f}".format(dLatitude) + '\n'
    ofs.write(sLine)
    ofs.close()

    return

if __name__ == '__main__':
    sRegion = 'tinpan'
    sModel ='swat'
    sCase = 'test'
    sJob = sCase
    sTask = 'simulation'
    iFlag_simulation = 1
    iFlag_pest = 0
    if iFlag_pest == 1:
        sTask = 'calibration'
    sFilename_configuration = sWorkspace_scratch + slash + '03model' + slash \
              + sModel + slash + sRegion + slash \
              + sTask  + slash + sFilename_config
    swat_prepare_precipitation_site_information(sFilename_configuration_in)
    