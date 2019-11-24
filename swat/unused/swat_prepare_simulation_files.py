import os 
import sys #used to add system path


sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)
from eslib.system import define_global_variables
from eslib.system.define_global_variables import *
from eslib.toolbox.reader.read_configuration_file import read_configuration_file

#import package
sPath_swat_python = sWorkspace_code +  slash + 'python' + slash + 'swat' + slash + 'swat_python'
sys.path.append(sPath_swat_python)
from swat.simulation.swat_copy_TxtInOut_files import swat_copy_TxtInOut_files
from swat.simulation.swat_copy_executable_file import swat_copy_executable_file
from swat.simulation.swat_prepare_simulation_bash_file import swat_prepare_simulation_bash_file
from swat.simulation.swat_prepare_simulation_job_file import swat_prepare_simulation_job_file

def swat_prepare_simulation_files(sFilename_configuration_in, sCase_in=None, sJob_in=None):
    config = read_configuration_file(sFilename_configuration_in)
    if sCase_in is not None:
        print(sCase_in)
        sCase = sCase_in
    else:
        #by default, this model will run in steady state
        sCase = 'test'
    if sJob_in is not None:
        sJob = sJob_in
    else:
        sJob = sCase
    
    #read configuration file
    sModel  =config['sModel']
    sRegion = config['sRegion']
    
    sWorkspace_model = sWorkspace_models + slash + sModel
    sWorkspace_region = sWorkspace_model + slash + sRegion
    sWorkspace_simulation =  sWorkspace_region + slash + 'simulation'
    sWorkspace_simulation_case = sWorkspace_simulation + slash + sCase

    if not os.path.isdir(sWorkspace_simulation_case):
        print(sWorkspace_simulation_case)
        os.makedirs(sWorkspace_simulation_case)

    #
    #copy exsting data
    swat_copy_TxtInOut_files(sFilename_configuration_in, sCase_in =sCase)
    swat_copy_executable_file(sFilename_configuration_in, sCase_in =sCase)

    swat_prepare_simulation_bash_file(sFilename_configuration_in, sCase_in =sCase)
    swat_prepare_simulation_job_file(sFilename_configuration_in, sCase_in =sCase, sJob_in =sJob)     
    

    print('Finished case: ' + sCase)
    return sFilename_bash, sFilename_job
if __name__ == '__main__':
    iFlag_mode = 0
    sModel = 'swat'
    sRegion = 'tinpan'
    sTask = 'simulation'
    sCase = 'test'
    sFilename_configuration = sWorkspace_configuration + slash + sModel + slash \
        + sRegion + slash \
        + sTask + slash + sFilename_config 

    swat_run_simulation(sFilename_configuration, sCase_in = sCase)