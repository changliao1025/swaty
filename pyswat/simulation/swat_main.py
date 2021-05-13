import os 
import sys #used to add system path
import subprocess

from pyearth.system.define_global_variables import *

from pyswat.shared.swat import pyswat

from pyswat.shared.swat_read_model_configuration_file import swat_read_model_configuration_file
from pyswat.simulation.swat_copy_TxtInOut_files import swat_copy_TxtInOut_files
from pyswat.scenarios.swat_prepare_hru_parameter_file import swat_prepare_hru_parameter_file
from pyswat.scenarios.swat_write_hru_input_file import swat_write_hru_input_file
from pyswat.simulation.swat_copy_executable_file import swat_copy_executable_file
from pyswat.simulation.swat_prepare_simulation_bash_file import swat_prepare_simulation_bash_file
from pyswat.simulation.swat_prepare_simulation_job_file import swat_prepare_simulation_job_file

def swat_main(oModel_in):    
    
    
   
    #step 2
    swat_copy_TxtInOut_files(oModel_in)

    #step 3 and 4 are optional
    iFlag_replace = oModel_in.iFlag_replace
    if (iFlag_replace == 1) :
        swat_prepare_hru_parameter_file(oModel_in)
        swat_write_hru_input_file(oModel_in)        
    else:
        pass
    #step 5
    swat_copy_executable_file(oModel_in)
    #step 6
    sFilename_bash = swat_prepare_simulation_bash_file(oModel_in)
    #step 7
    sFilename_job = swat_prepare_simulation_job_file(oModel_in)    
    #step 8 submit
    iFlag_mode = oModel_in.iFlag_mode
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

    
    aVariable = ['cn2']
    aValue = [10]

    sFilename_configuration_in = '/global/homes/l/liao313/workspace/python/pyswat/pyswat/shared/swat_simulation.xml'

    #step 1
    aParameter = swat_read_model_configuration_file(sFilename_configuration_in, aVariable_in = aVariable, aValue_in = aValue)

       # iCase_index_in=iCase_index_in, sJob_in=sJob_in, iFlag_mode_in=iFlag_mode_in)

    aParameter['sFilename_model_configuration'] = sFilename_configuration_in
    oModel = pyswat(aParameter)

    swat_main(oModel)  #, sCase_in = sCase, iFlag_mode_in= iFlag_mode, aVariable_in = aVariable, aValue_in = aValue)