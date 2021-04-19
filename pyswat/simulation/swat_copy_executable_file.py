#this function is used to copy swat and beopest from linux hpc to calibration folder
import sys
import os
from shutil import copy2

sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)
from eslib.system import define_global_variables
from eslib.system.define_global_variables import *

sPath_swat_python = sWorkspace_code +  slash + 'python' + slash + 'swat' + slash + 'swat_python'
sys.path.append(sPath_swat_python)

from swat.shared import swat_global
#from eslib.toolbox.reader.read_configuration_file import read_configuration_file
    
def swat_copy_executable_file():
    """    
    prepare executable file
    """    
    sFilename_swat = swat_global.sFilename_swat   
    sWorkspace_simulation_case = swat_global.sWorkspace_simulation_case
    
    if not os.path.exists(sWorkspace_simulation_case):
        print("The simiulation folder is missing")
        return
    else:
        pass    

    #copy swat
    sFilename_swat_source = sWorkspace_bin + slash + sFilename_swat
    sFilename_swat_new = sWorkspace_simulation_case + slash + 'swat'
    copy2(sFilename_swat_source, sFilename_swat_new)

    #copy ppest
    #sFilename_beopest_source = sWorkspace_calibration + slash + sFilename_pest
    #sFilename_beopest_new = sWorkspace_pest_model + slash + 'ppest'       
    #copy2(sFilename_beopest_source, sFilename_beopest_new)

    #copy run script?
    #sFilename_run_script = 'run_swat_model'
    #sFilename_run_script_source = sWorkspace_calibration + slash + sFilename_run_script
    #sFilename_run_script_new = sWorkspace_pest_model + slash + sFilename_run_script
    #copy2(sFilename_run_script_source, sFilename_run_script_new)


    print('The swat executable file is copied successfully!')


if __name__ == '__main__':

    
    swat_copy_executable_file()
