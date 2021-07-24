import sys
import os
import numpy as np
import datetime

from shutil import copy2
from numpy  import array

from pyearth.system.define_global_variables import *
from pyearth.toolbox.reader.text_reader_string import text_reader_string
from pyearth.toolbox.data.convert_time_series_daily_to_monthly import convert_time_series_daily_to_monthly

def swat_extract_stream_discharge(oModel_in):
    """
    extract discharge from swat model simulation
    """
  
    
    sModel = oModel_in.sModel
    sRegion = oModel_in.sRegion
    sCase = oModel_in.sCase

    iYear_start = oModel_in.iYear_start
    #iYear_spinup_end = oModel_in.iYear_spinup_end
    iYear_end  = oModel_in.iYear_end
   
    nstress = oModel_in.nstress
    nsegment = oModel_in.nsegment
    sProject = sModel + slash + sRegion
    sWorkspace_data_project = oModel_in.sWorkspace_data_project  
    sWorkspace_simulation_case = oModel_in.sWorkspace_simulation_case
    iFlag_debug = 2
   
    sPath_current = os.getcwd()
    #sPath_current = '/global/cscratch1/sd/liao313/04model/swat/arw/simulation/swat20210723001/'
    print('The current path is: ' + sPath_current)
    

    sFilename = sPath_current + slash + 'output.rch'

    aData = text_reader_string(sFilename, iSkipline_in=9)
    aData_all = array( aData )
    nrow_dummy = len(aData_all)
    ncolumn_dummy = len(aData_all[0,:])

    aData_discharge = aData_all[:, 5].astype(float) 

    aIndex = np.arange(nsegment-1 , nstress * nsegment + 1, nsegment)
    #aIndex = np.arange(nsegment , nstress * nsegment + 1, nsegment)
     
    aDischarge_simulation_daily = aData_discharge[aIndex]

    iYear_start_in = oModel_in.iYear_start
    iMonth_start_in = oModel_in.iMonth_start
    iDay_start_in = oModel_in.iDay_start

    iYear_end_in = oModel_in.iYear_end
    iMonth_end_in = oModel_in.iMonth_end
    iDay_end_in = oModel_in.iDay_end
    
    aDischarge_simulation_monthly = convert_time_series_daily_to_monthly(aDischarge_simulation_daily,\
        iYear_start_in, iMonth_start_in, iDay_start_in, \
      iYear_end_in, iMonth_end_in, iDay_end_in , sType_in = 'sum'  )

    #save it to a text file
    sFilename_out = sPath_current + slash + 'stream_discharge_monthly.txt'

    np.savetxt(sFilename_out, aDischarge_simulation_monthly, delimiter=",")

    sTime  = datetime.datetime.now().strftime("%m%d%Y%H%M%S")

    sFilename_new = sPath_current + slash + 'stream_discharge' + sTime + '.txt'
    copy2(sFilename_out, sFilename_new)
    
    print('Finished extracting stream discharge: ' + sFilename_out)






