import sys
import os
import numpy as np

import datetime
import calendar

from numpy import array



sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'
print(sPath_library_python)

sys.path.append(sPath_library_python)

from toolbox.reader.text_reader_string import text_reader_string



def swat_prepare_observation_discharge_file(sFilename_configuration_in):
      
    sWorkspace_home = config['sWorkspace_home']
    sWorkspace_scratch = config['sWorkspace_scratch']
   
    sWorkspace_data_relative = config['sWorkspace_data']
    sWorkspace_project_ralative = config['sWorkspace_project']

    sFilename_observation_discharge = config['sFilename_observation_discharge']
    iYear_start = int(config['iYear_start'] )
    iYear_end  = int( config['iYear_end'] )
    iYear_spinup_end = int(config['iYear_spinup_end'] )
    sRegion = config['sRegion']

    dObservation_start = datetime.datetime(iYear_start, 1, 1)  #year, month, day
    
    dObservation_end = datetime.datetime(iYear_end, 12,31)  #year, month, day

    jdStart = julian.to_jd(dObservation_start, fmt='jd')
    
    jdEnd = julian.to_jd(dObservation_end, fmt='jd')
    nstress = int(jdEnd - jdStart + 1)
    
    print(nstress )

    
    sWorkspace_data = sWorkspace_scratch + slash + sWorkspace_data_relative

    sWorkspace_data_project = sWorkspace_data + slash + sWorkspace_project_ralative

    sFilename_discharge = sWorkspace_data_project + slash + sFilename_observation_discharge
    aData_dummy = text_reader_string(sFilename_discharge, delimiter_in=',', skipline_in=1)
    print(sFilename_discharge)
    aData = array( aData_dummy )
    aYear =  aData[:,0] 
    aMonth =  aData[:,1] 
    aDay =  aData[:,2] 
    aDischarge = aData[:, 4] #unit is cms because it is convected in excel
    nobs = len(aDischarge  )
  
    #save a txt file for other purpose
    sFilename_observation_discharge_out = sWorkspace_data + slash + 'swat' + slash + sRegion + slash \
    + 'auxiliary' + slash + 'usgs' + slash + 'discharge' + slash + 'discharge_observation.txt' 
    #ofs= open(sFilename_observation_discharge_out, 'w')
    aDischarge_observation = np.full( (nstress), missing_value, dtype=float )
    for i in range(0, nobs):
        iYear = int(aYear[i])
        iMonth = int( aMonth[i])
        iDay = int(aDay[i])
        dDischarge = float(aDischarge[i])
        date_dummy = datetime.datetime(iYear, iMonth, iDay)
        jd_dummy = julian.to_jd(date_dummy, fmt='jd')
        lIndex = jd_dummy - jdStart

        aDischarge_observation[ int(lIndex)] = dDischarge
    #ofs.write(aDischarge_observation)
    #ofs.close()
    np.savetxt(sFilename_observation_discharge_out, aDischarge_observation, delimiter=',', fmt='%0.6f') 
    print('finished')

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
    
    swat_prepare_observation_discharge_file(sFilename_configuration_in)