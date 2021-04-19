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
import os, errno
from os.path import isfile, join
from os import listdir
from pathlib import Path
from numpy  import array
sPlatform_os = platform.system()

if sPlatform_os=='Windows':
    slash = '\\'
    sWorkspace_code = 'C:' + slash + 'workspace'
else:
    slash ='/'
    home = str(Path.home())
    sWorkspace_code = home + slash + 'workspace'

sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'
print(sPath_library_python)

sys.path.append(sPath_library_python)

from toolbox.reader.text_reader_string import text_reader_string



def symlink_force(target, link_name):
    try:
        os.symlink(target, link_name)
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass
            #os.remove(link_name)
            #os.symlink(target, link_name)
        else:
            raise e
    
def swat_link_swat_permanent_file(sFilename_configuration_in):
    
    #strings
    sWorkspace_home = config['sWorkspace_home']
    sWorkspace_data = config['sWorkspace_data']
    sWorkspace_scratch=config['sWorkspace_scratch']
    sWorksapce_raw = config['sWorkspace_raw']    
    sWorkspace_project = config['sWorkspace_project']
    sWorkspace_simulation = config['sWorkspace_simulation']
    
    pest_mode =  config['pest_mode'] 
    sRegion = config['sRegion']
    nslave = config['nslave']
    sFilename_template = 'purgatoire30_swat.tpl'

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
    
    #get current directory

    sPath_current = os.path.abspath(__file__)
    print(sPath_current)

    for iSlave in range(o, nslave):
        sSlave =  "{:04d}".format(iSlave+1)
        sPath_current = sWorkspace_pest + slash + 'beopest' + sSlave
        os.chdir(sPath_current)
        # This creates a symbolic link on python in tmp directory

        #aFile = os.listdir(sWorkspace_simulation)
        swat_copy_swat_executable(sFilename_configuration_in, iSlave)
        swat_link_swat_permanent_file(sFilename_configuration_in, iSlave)
    
    

    

    print('The swat permanent files are prepared successfully!')


if __name__ == '__main__':
    import os
    print(sPlatform_os)
    if sPlatform_os == 'Darwin':
        sFilename_configuration_in = '/Volumes/mac/03model/swat/purgatoire30/simulation/parallel/purgatoire30.txt'
    else:
        cluster = 'snyder'
        if(cluster=='snyder'):
            sFilename_configuration_in = '/scratch/snyder/l/liao46/snyder/03model/swat/purgatoire30/simulation/parallel/purgatoire30.txt'
        else:
            sFilename_configuration_in = '/pic/scratch/liao313/03model/swat/purgatoire30/simulation/parallel/purgatoire30.txt'
    swat_link_swat_permanent_file(sFilename_configuration_in)
