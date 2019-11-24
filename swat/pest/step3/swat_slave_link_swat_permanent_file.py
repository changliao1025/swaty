import sys
import os
import numpy as np
import datetime
import calendar

import glob
import errno
from os.path import isfile, join
from os import listdir

from numpy  import array


sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'
sys.path.append(sPath_library_python)
from toolbox.reader.text_reader_string import text_reader_string


def create_symlink(source, target_link):
    """
    """
    try:
        os.symlink(source, target_link)
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass
            os.remove(target_link)
            os.symlink(source, target_link)
        else:
            raise e


def swat_slave_link_swat_permanent_file(sFilename_configuration_in, sModel):
    """
    create sym limk of swat files
    """
    
    #strings
    

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
    
    iFlag_debug = 0
    if(iFlag_debug == 1 ):
        sPath_current = sWorkspace_pest_model + slash + 'beopest1'
    else:
        sPath_current = os.getcwd()
    
    sWorkspace_slave = sPath_current

    #we will use a tuple
    aExtension = ('.pnd','.rte','.sub','.swq','.wgn','.wus',\
            '.chm','.gw','.hru','.mgt','sdr','.sep',\
             '.sol','ATM','bsn','wwq','deg','.cst',\
             'dat','fig','cio','fin','dat','.pcp','.tmp'  )
            
    for sExtension in aExtension:
        sRegax = sWorkspace_pest_model + slash + '*' + sExtension
        for sFilename in glob.glob(sRegax):
            sBasename_with_extension = os.path.basename(sFilename)
            sLink = sWorkspace_slave + slash + sBasename_with_extension
            create_symlink(sFilename, sLink)   

    print('The swat permanent files are prepared successfully!')


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
    swat_slave_link_swat_permanent_file(sFilename_configuration_in, sModel)
