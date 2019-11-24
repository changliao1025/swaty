#this function is used to copy the swat from calibration folder to the current slave folder
import sys
import os
import datetime
import calendar

import glob

import numpy as np
from numpy  import array
from shutil import copyfile, copy2
from calendar import monthrange #calcuate the number of days in a month



#import the eslib library
sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'
sys.path.append(sPath_library_python)
from toolbox.reader.text_reader_string import text_reader_string


def swat_slave_copy_swat_executable_file(sFilename_configuration_in, sModel):
    """
    copy swat to local slave directory
    """
    

    

    sWorkspace_calibration_relative = config['sWorkspace_calibration']
    sWorkspace_calibration = sWorkspace_scratch + slash + sWorkspace_calibration_relative
    sWorkspace_pest_model = sWorkspace_calibration + slash + sModel
    
    sFilename_swat =  sWorkspace_pest_model + slash + 'swat'     

    iFlag_debug = 0
    if(iFlag_debug == 1 ):
        sPath_current = sWorkspace_pest_model + slash + 'beopest1'
    else:
        sPath_current = os.getcwd()
    print('The current slave path is: ' + sPath_current)
    sWorkspace_slave = sPath_current

    sFilename_new = sPath_current + slash + 'swat'
    copy2(sFilename_swat, sFilename_new)
    
    print('Finished copying swat in slave directory')


#the main entrance    
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
   
    swat_slave_copy_swat_executable_file(sFilename_configuration_in, sModel)