import sys
import os
import numpy as np
import datetime
import calendar


import os, errno
from os.path import isfile, join
from os import listdir

from numpy  import array



sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'
sys.path.append(sPath_library_python)
from toolbox.reader.text_reader_string import text_reader_string

sPath_swat_python = sWorkspace_code +  slash + 'python' + slash + 'swat' + slash + 'swat_python'
sys.path.append(sPath_swat_python)

from swat.pest.swat_slave_copy_swat_executable_file import swat_slave_copy_swat_executable_file
from swat.pest.swat_slave_link_swat_permanent_file import swat_slave_link_swat_permanent_file
 
def swat_prepare_pest_slave_input_file(sFilename_configuration_in, sModel):
    """
    prepare the input files for the slave simulation
    """
   
    #strings
    
    sWorkspace_home = config['sWorkspace_home']
    sWorkspace_scratch=config['sWorkspace_scratch']

    sWorkspace_data_relative = config['sWorkspace_data']  
    sWorkspace_project_relative = config['sWorkspace_project']
    sWorkspace_simulation_relative = config['sWorkspace_simulation']
    sWorkspace_calibration_relative = config['sWorkspace_calibration']

    pest_mode =  config['pest_mode'] 
    sRegion = config['sRegion']

    sWorkspace_data = sWorkspace_scratch + slash + sWorkspace_data_relative
    sWorkspace_data_project = sWorkspace_data + slash + sWorkspace_project_relative

    sWorkspace_simulation = sWorkspace_scratch +  slash  + sWorkspace_simulation_relative
    sWorkspace_calibration = sWorkspace_scratch + slash + sWorkspace_calibration_relative

    sWorkspace_pest_model = sWorkspace_calibration + slash + sModel
    if not os.path.exists(sWorkspace_calibration):
        print("The calibation folder is missing")
        return
    else:
        pass
    
    #get current directory
    sPath_current = os.getcwd()

    if (os.path.normpath(sPath_current)  == os.path.normpath(sWorkspace_pest_model)):
        print('This is the master directory, no need to copy anything')
    else:
        swat_slave_copy_swat_executable_file(sFilename_configuration_in, sModel)
        swat_slave_link_swat_permanent_file(sFilename_configuration_in, sModel)
        print('The swat slave files are prepared successfully!')

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

    swat_prepare_pest_slave_input_file(sFilename_configuration_in, sModel)
