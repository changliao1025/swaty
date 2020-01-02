import os 
import sys #used to add system path
import subprocess

sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)
from eslib.system import define_global_variables
from eslib.system.define_global_variables import *


sPath_swat_python = sWorkspace_code +  slash + 'python' + slash + 'swat' + slash + 'swat_python'
sys.path.append(sPath_swat_python)

from swat.shared import swat_global

from swat.shared.swat_read_configuration_file import swat_read_configuration_file
from swat.simulation.swat_copy_TxtInOut_files import swat_copy_TxtInOut_files
from swat.scenarios.swat_prepare_hru_parameter_file import swat_prepare_hru_parameter_file
from swat.scenarios.swat_write_hru_input_file import swat_write_hru_input_file
from swat.simulation.swat_copy_executable_file import swat_copy_executable_file
from swat.simulation.swat_prepare_simulation_bash_file import swat_prepare_simulation_bash_file
from swat.simulation.swat_prepare_simulation_job_file import swat_prepare_simulation_job_file

def swat_main(sFilename_configuration_in, iCase_index_in=None, sJob_in=None, iFlag_mode_in=None, aVariable_in = None, aValue_in = None):    
    
    #step 1
    swat_read_configuration_file(sFilename_configuration_in, \
        iCase_index_in=iCase_index_in, sJob_in=sJob_in, iFlag_mode_in=iFlag_mode_in, aVariable_in = aVariable_in, aValue_in = aValue_in)
   
    #step 2
    #swat_copy_TxtInOut_files()

    #step 3 and 4 are optional
    iFlag_replace = swat_global.iFlag_replace
    if (iFlag_replace == 1) :
        swat_prepare_hru_parameter_file()
        swat_write_hru_input_file()        
    else:
        pass
    #step 5
    swat_copy_executable_file()
    #step 6
    sFilename_bash = swat_prepare_simulation_bash_file()
    #step 7
    sFilename_job = swat_prepare_simulation_job_file()    
    #step 8 submit
    iFlag_mode = swat_global.iFlag_mode
    print('Finished')
    return
    if( iFlag_mode == 1):
        #run local
        subprocess.call(sFilename_bash, shell=True, executable=sFilename_interactive_bash )

    else:
        #run job
        sLine = 'sbatch ' + sFilename_job
        # cannot run on marianas
        subprocess.call(sLine, shell=True, executable=sFilename_interactive_bash )  

    
if __name__ == '__main__':
    iFlag_mode = 1
    sModel = 'swat'
    sRegion = 'tinpan'
    sTask = 'simulation'
    sCase = 'test'
    sFilename_configuration = sWorkspace_configuration + slash + sModel + slash \
        + sRegion + slash \
        + sTask + slash + sFilename_config 
    aVariable = ['cn2']
    aValue = [10]

    swat_main(sFilename_configuration, sCase_in = sCase, iFlag_mode_in= iFlag_mode, aVariable_in = aVariable, aValue_in = aValue)