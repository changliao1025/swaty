import sys
import os
import numpy as np
import datetime

from numpy  import array

#import eslib library
sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)

from eslib.toolbox.reader.text_reader_string import text_reader_string
from eslib.system.define_global_variables import *
from eslib.toolbox.reader.read_configuration_file import read_configuration_file

sPath_swat_python = sWorkspace_code +  slash + 'python' + slash + 'swat' + slash + 'swat_python'
sys.path.append(sPath_swat_python)
from swat.shared.swat_read_configuration_file import swat_read_configuration_file
from swat.shared import swat_global

def swat_extract_stream_discharge(sFilename_configuration_in, iCase_index_in = None):
    """
    extract discharge from swat model simulation
    """
  
    config = swat_read_configuration_file(sFilename_configuration_in, iCase_index_in)
    sModel = swat_global.sModel
    sRegion = swat_global.sRegion
    sCase = swat_global.sCase

    iYear_start = swat_global.iYear_start
    iYear_spinup_end = swat_global.iYear_spinup_end
    iYear_end  = swat_global.iYear_end
   
    nstress = swat_global.nstress
    nsegment = swat_global.nsegment
    sProject = sModel + slash + sRegion
    sWorkspace_data_project = swat_global.sWorkspace_data_project  
    sWorkspace_simulation_case = swat_global.sWorkspace_simulation_case
    iFlag_debug = 2
    if(iFlag_debug == 1 ):
        sPath_current = sWorkspace_pest_model + slash + 'beopest1'
    else:
        if iFlag_debug == 2:
            #run from the arcswat directory
            sPath_current = sWorkspace_simulation_case # + slash  + 'TxtInOut'
        else:
            sPath_current = os.getcwd()
    print('The current path is: ' + sPath_current)
    sWorkspace_slave = sPath_current

    sFilename = sWorkspace_slave + slash + 'output.rch'

    aData = text_reader_string(sFilename, iSkipline_in=9)
    aData_all = array( aData )
    nrow_dummy = len(aData_all)
    ncolumn_dummy = len(aData_all[0,:])

    aData_discharge = aData_all[:, 6].astype(float) 

    aIndex = np.arange(nsegment-1 , nstress * nsegment + 1, nsegment)
    aIndex = np.arange(nsegment-2 , nstress * nsegment + 1, nsegment)
    
    aDischarge_simulation = aData_discharge[aIndex]

    #save it to a text file
    sFilename_out = sWorkspace_slave + slash + 'stream_discharge_22.txt'

    np.savetxt(sFilename_out, aDischarge_simulation, delimiter=",")
    
    print('finished extracting stream discharge')



if __name__ == '__main__':
   
    sRegion = 'tinpan'
    sModel ='swat'
    iCase = 0
    
    sTask = 'simulation'
    iFlag_simulation = 1
    iFlag_pest = 0
    if iFlag_pest == 1:
        sTask = 'calibration'
    sFilename_configuration = sWorkspace_configuration  + slash \
              + sModel + slash + sRegion + slash \
              + sTask  + slash + 'marianas_configuration.txt'
    swat_extract_stream_discharge(sFilename_configuration, iCase)

