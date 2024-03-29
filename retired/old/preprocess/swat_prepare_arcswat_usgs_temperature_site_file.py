import sys
import os
import numpy as np
from numpy  import array
import datetime
import calendar
import julian  #to covert datetime to julian date 
import platform #platform indenpendent
from calendar import monthrange




from pyearth.toolbox.reader.text_reader_string import text_reader_string

feet2meter = 0.3048

def swat_prepare_arcswat_usgs_temperature_site_file(sFilename_configuration_in):
    #check whether the configuration exist or not
       
    #retrieve the data
    sWorkspace_home = config['sWorkspace_home']
    sWorkspace_data = config['sWorkspace_data']
    sRegion = config['sRegion']
    iYear_start = int(config['iYear_start'] )
    iYear_spinup_end = int(config['iYear_spinup_end'] )
    iYear_end  = int( config['iYear_end'] )

    #write out 
    sFilename = sWorkspace_data + slash +  'swat' + slash + sRegion + slash \
    + 'auxiliary' + slash + 'usgs' + slash + 'usgs_tmp_site.txt'    
    print(sFilename)
    ofs = open(sFilename, 'w')

    sLine = 'ID, NAME, LAT, LONG, ELEVATION\n'
    #1,p329959,32.940,-95.938,141.000
    #2,p329956,32.940,-95.625,153.000
    ofs.write(sLine)

     #C-18 Upper Molino Canyon,
    sSiteID = "{:02d}".format(2)  
    sSiteName = 'c17'.zfill(8)
    dLatitude = 37 + 10/60.0 + 37/3600.0 
    dLongitude = 104 + 47/60.0 + 59/3600.0
    dElevation = 6980 * feet2meter

    sLatitude =  "{:.3f}".format(dLatitude)
    sLongitude = "{:.3f}".format(dLongitude)
    sElevation = "{:05d}".format( int(dElevation ) ) 

    sLine = sSiteID + ', ' + sSiteName + ', ' \
    + sLatitude  + ', '+ sLongitude + ', ' + sElevation + '\n'
    ofs.write(sLine)
   
    ofs.close()

    print('finished')
   

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
    swat_prepare_arcswat_usgs_temperature_site_file(sFilename_configuration_in)
