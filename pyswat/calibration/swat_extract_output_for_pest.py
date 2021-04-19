import sys
import os
import datetime
import calendar

import numpy as np
from numpy  import array

from calendar import monthrange #calcuate the number of days in a month

#make sure the program is platform independent


#import the eslib library
#this library is used to read data and maybe other operations
sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'
sys.path.append(sPath_library_python)
from toolbox.reader.text_reader_string import text_reader_string

sPath_swat_python = sWorkspace_code +  slash + 'python' + slash + 'swat' + slash + 'swat_python'
sys.path.append(sPath_swat_python)
from swat.postprocess.swat_extract_stream_discharge import swat_extract_stream_discharge


def swat_extract_output_for_pest(sFilename_configuration_in, sModel):
    """
    sFilename_configuration_in
    """
    #stream discharge
    swat_extract_stream_discharge(sFilename_configuration_in, sModel)


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

    



    swat_extract_output_for_pest(sFilename_configuration_in, sCase, sJob, sModel)
   
