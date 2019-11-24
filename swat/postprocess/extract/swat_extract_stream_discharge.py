import sys
import os
import numpy as np
import datetime

from numpy  import array

#import eslib library
sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'
sys.path.append(sPath_library_python)
from toolbox.reader.text_reader_string import text_reader_string

def swat_extract_stream_discharge(sFilename_configuration_in, sCase_in = None, sJob_in = None, sModel_in = None):
    """
    extract discharge from swat model simulation
    """
  
    if sCase_in is not None:
        print(sCase_in)
        sCase = sCase_in
    else:
        #by default, this model will run in steady state
        sCase = 'ss'
    if sJob_in is not None:
        sJob = sJob_in
    else:
        sJob = 'swat'
    if sModel_in is not None:
        print(sModel_in)
        sModel = sModel_in
    else:
        sModel = 'swat' #the default mode is modflow
    
    sWorkspace_scratch = config['sWorkspace_scratch']

    sWorkspace_calibration_relative = config['sWorkspace_calibration']
    sWorkspace_simulation_relative = config['sWorkspace_simulation']

    sWorkspace_simulation = sWorkspace_scratch + slash + sWorkspace_simulation_relative + slash + sCase
    sWorkspace_calibration = sWorkspace_scratch + slash + sWorkspace_calibration_relative + slash + sCase

    sWorkspace_pest_model = sWorkspace_calibration + slash + sModel
    
    iYear_start = int(config['iYear_start'] )
    iYear_spinup_end = int(config['iYear_spinup_end'] )
    iYear_end  = int( config['iYear_end'] )
    nsegment = int( config['nsegment'] )

    dSimulation_start = datetime.datetime(iYear_start, 1, 1)  #year, month, day
    dSimulation_transient_start = datetime.datetime(iYear_spinup_end + 1, 1, 1)  #year, month, day
    dSimulation_end = datetime.datetime(iYear_end, 12, 31)  #year, month, day

    jdStart = julian.to_jd(dSimulation_start, fmt='jd')
    jdEnd = julian.to_jd(dSimulation_end, fmt='jd')

    nstress = int(jdEnd - jdStart + 1)
    
    iFlag_debug = 2
    if(iFlag_debug == 1 ):
        sPath_current = sWorkspace_pest_model + slash + 'beopest1'
    else:
        if iFlag_debug == 2:
            #run from the arcswat directory
            sPath_current = sWorkspace_simulation # + slash  + 'TxtInOut'
        else:
            sPath_current = os.getcwd()
    print('The current path is: ' + sPath_current)
    sWorkspace_slave = sPath_current

    sFilename = sWorkspace_slave + slash + 'output.rch'

    aData = text_reader_string(sFilename, skipline_in=9)
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
    sCase = 'tr003'
    sJob = sCase
    sTask = 'simulation'
    iFlag_simulation = 1
    iFlag_pest = 0
    if iFlag_pest == 1:
        sTask = 'calibration'
    sFilename_configuration = sWorkspace_scratch + slash + '03model' + slash \
              + sModel + slash + sRegion + slash \
              + sTask  + slash + sFilename_config
    swat_extract_stream_discharge(sFilename_configuration,sCase, sJob, sModel)

