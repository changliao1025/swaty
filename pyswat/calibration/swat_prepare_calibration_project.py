#this will be the head quarter of the calibration

import sys
import os
import datetime
import calendar


import numpy as np

from numpy  import array
from calendar import monthrange #calcuate the number of days in a month



#import the eslib library
#this library is used to read data and maybe other operations
sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'
sys.path.append(sPath_library_python)
from toolbox.reader.text_reader_string import text_reader_string

#import swat library

sPath_swat_python = sWorkspace_code +  slash + 'python' + slash + 'swat' + slash + 'swat_python'
sys.path.append(sPath_swat_python)

from swat.calibration.swat_prepare_calibration_workspace import swat_prepare_calibration_workspace
from swat.calibration.swat_prepare_input_copy_file import swat_prepare_input_copy_file
from swat.calibration.swat_prepare_executable_file import swat_prepare_executable_file
from swat.calibration.swat_prepare_calibration_job_file import swat_prepare_calibration_job_file

from swat.pest.swat_prepare_pest_run_script import swat_prepare_pest_run_script
from swat.pest.swat_prepare_pest_control_file import swat_prepare_pest_control_file
from swat.pest.swat_prepare_pest_instruction_file import swat_prepare_pest_instruction_file
from swat.pest.swat_prepare_pest_template_file import swat_prepare_pest_template_file

def swat_prepare_calibration_project(sFilename_configuration_in, sPlatform_os):
    """
    The head quarter
    """
    

    
    #retrieve user input
    iID = int(sys.argv[1])
    sID = "{:03d}".format( iID )
    sModel = 'beopest' + sID

    swat_prepare_calibration_workspace(sFilename_configuration_in, sModel)

    #the following steps/files will be created one by one
    #now we start to call other functions
    iFlag_copy_swat_file = int(sys.argv[2])
    if (iFlag_copy_swat_file == 1 ):
        swat_prepare_input_copy_file(sFilename_configuration_in, sModel)

    #step #1: copy swat executable file to the master folder
    #copy the beopest to the master folder only when it is on linux
    if (sPlatform_os=='Linux'):
        swat_prepare_executable_file(sFilename_configuration_in, sModel)
        swat_prepare_pest_run_script(sFilename_configuration_in, sModel)
        swat_prepare_calibration_job_file(sFilename_configuration_in, sModel)
    
    #step # create pest control file
    swat_prepare_pest_control_file(sFilename_configuration_in, sModel)
    #step # create pest instruction file
    swat_prepare_pest_instruction_file(sFilename_configuration_in, sModel)
    #step # create pest template file
    swat_prepare_pest_template_file(sFilename_configuration_in, sModel)

    print('the pest calibration project is prepared successfully!')
    return

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
    
    swat_prepare_calibration_project(sFilename_configuration_in, sPlatform_os)
