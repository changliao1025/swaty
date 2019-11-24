import sys
import os
import numpy as np
import datetime
import calendar
import julian
import platform 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from pathlib import Path
from numpy  import array


sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'
print(sPath_library_python)

sys.path.append(sPath_library_python)

from toolbox.reader.text_reader_string import text_reader_string


    
def swat_prepare_pest_run_management_file(sFilename_configuration_in):
    
    #strings
    sWorkspace_home = config['sWorkspace_home']
    sWorkspace_data = config['sWorkspace_data']
    sWorkspace_scratch=config['sWorkspace_scratch']
    sWorksapce_raw = config['sWorkspace_raw']    
    sWorkspace_project = config['sWorkspace_project']
    sWorkspace_simulation = config['sWorkspace_simulation']
    
    pest_mode =  config['pest_mode'] 
    sRegion = config['sRegion']

    sWorkspace_data = sWorkspace_data + slash + sWorkspace_project
    sWorkspace_simulation = sWorkspace_scratch +  slash  + sWorkspace_simulation
    sWorkspace_pest = sWorkspace_simulation
    if not os.path.exists(sWorkspace_simulation):
        #os.makedirs(sWorkspace_pest)
        #something is wrong because the simulaiton folder 
        #must exist for calibration
        print("The simulation folder is missing")
        return
    else:
        pass
    

    sFilename_control = sWorkspace_pest + slash + sRegion + '_swat.rmf'
    ofs = open(sFilename_control, 'w')
    ofs.write('prf\n')
    #ofs.write('* control data\n')
    #ofs.write('restart ' + pest_mode  + '\n' ) 
    sLine = '5 0 0 -32'
    ofs.write(sLine)


    ofs.close()

    print('The PEST run management file is prepared successfully!')


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
    swat_prepare_pest_run_management_file(sFilename_configuration_in)
