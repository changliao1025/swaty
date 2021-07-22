#this function is used to copy swat and beopest from linux hpc to calibration folder
import sys
import os
from shutil import copy2


from pyearth.system.define_global_variables import *


#from pyearth.toolbox.reader.read_configuration_file import read_configuration_file
    
def swat_copy_executable_file(oModel_in):
    """    
    prepare executable file
    """    
    sWorkspace_bin = oModel_in.sWorkspace_bin 
    sFilename_swat = oModel_in.sFilename_swat   
    sWorkspace_simulation_case = oModel_in.sWorkspace_simulation_case
    sWorkspace_calibration_case = oModel_in.sWorkspace_calibration_case
   
    sWorkspace_pest_model = sWorkspace_calibration_case


    #copy swat
    sFilename_swat_source = sWorkspace_bin + slash + sFilename_swat

    #sPath_current = os.getcwd()
    sPath_current = sWorkspace_simulation_case
    sFilename_swat_new = sPath_current + slash + 'swat'

    
      

    print(sFilename_swat_source)
    print(sFilename_swat_new)
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
