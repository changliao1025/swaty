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
from swat.postprocess.extract.swat_extract_stream_discharge import swat_extract_stream_discharge


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
    for i in range(20):
        iCase =i
        swat_extract_stream_discharge(sFilename_configuration, iCase)

