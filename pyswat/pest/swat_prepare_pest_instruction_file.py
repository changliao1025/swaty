import sys
import os
import numpy as np
import datetime

from numpy  import array


sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'
sys.path.append(sPath_library_python)
from toolbox.reader.text_reader_string import text_reader_string



def swat_prepare_pest_instruction_file(sFilename_configuration_in, sModel):
    """
    prepare pest instruction file
    """
    
    
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
    sWorkspace_simulation_copy = sWorkspace_simulation + slash + 'copy' + slash + 'TxtInOut'

    iYear_start = int(config['iYear_start'] )
    iYear_spinup_end = int(config['iYear_spinup_end'] )
    iYear_end  = int( config['iYear_end'] )
    nsegment = int( config['nsegment'] )

    dSimulation_start = datetime.datetime(iYear_start, 1, 1)  #year, month, day
    dSimulation_transient_start = datetime.datetime(iYear_spinup_end + 1, 1, 1)  #year, month, day
    dSimulation_end = datetime.datetime(iYear_end, 12, 31)  #year, month, day

    jdStart = julian.to_jd(dSimulation_transient_start, fmt='jd')
    jdEnd = julian.to_jd(dSimulation_end, fmt='jd')
    nstress = int(jdEnd - jdStart + 1)

    sFilename_observation = sWorkspace_data_project + slash + 'auxiliary' + slash \
        + 'usgs' + slash + 'discharge' + slash + 'discharge_observation.txt'
    if os.path.isfile(sFilename_observation):
        pass
    else:
        print(sFilename_observation + ' is missing!')
        return
    aData = text_reader_string(sFilename_observation)
    aDischarge_observation = array( aData ).astype(float) 
    nobs_with_missing_value = len(aDischarge_observation)
    
    aDischarge_observation = np.reshape(aDischarge_observation, nobs_with_missing_value)
    nan_index = np.where(aDischarge_observation == missing_value)

    #write instruction
    sFilename_instruction = sWorkspace_pest_model + slash + sRegion + '_swat.ins'    
    ofs= open(sFilename_instruction,'w')
    ofs.write('pif $\n')

    #we need to consider that there is missing value in the observations
    for i in range(0, nstress):
        dDummy = aDischarge_observation[i]
        if( dDummy != missing_value  ):
            sLine = 'l1' + ' !discharge' + "{:04d}".format(i+1) + '!\n'
        else:
            sLine = 'l1' + ' !dum' + '!\n'
        ofs.write(sLine)
            
    ofs.close()
    print('The instruction file is prepared successfully!')

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
    swat_prepare_pest_instruction_file(sFilename_configuration_in, sModel)