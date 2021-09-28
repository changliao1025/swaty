import os 
import sys #used to add system path
import subprocess

from pyearth.system.define_global_variables import *

from pyswat.shared.swat import pyswat

from pyswat.simulation.swat_copy_TxtInOut_files import swat_copy_TxtInOut_files
from pyswat.scenarios.swat_prepare_watershed_parameter_file import swat_prepare_watershed_parameter_file
from pyswat.scenarios.swat_prepare_subbasin_parameter_file import swat_prepare_subbasin_parameter_file
from pyswat.scenarios.swat_prepare_hru_parameter_file import swat_prepare_hru_parameter_file

from pyswat.scenarios.swat_write_watershed_input_file import swat_write_watershed_input_file
from pyswat.scenarios.swat_write_subbasin_input_file import swat_write_subbasin_input_file
from pyswat.scenarios.swat_write_hru_input_file import swat_write_hru_input_file

from pyswat.simulation.swat_copy_executable_file import swat_copy_executable_file
from pyswat.simulation.swat_prepare_simulation_bash_file import swat_prepare_simulation_bash_file
from pyswat.simulation.swat_prepare_simulation_job_file import swat_prepare_simulation_job_file

def swat_main(oSwat_in):        
    
    #swat_copy_TxtInOut_files(oSwat_in)

    #step 3 and 4 are optional
    iFlag_replace = oSwat_in.iFlag_replace
    if (iFlag_replace == 1) :
        swat_prepare_watershed_parameter_file(oSwat_in)
        swat_write_watershed_input_file(oSwat_in)      

        swat_prepare_subbasin_parameter_file(oSwat_in)
        swat_write_subbasin_input_file(oSwat_in)      

        swat_prepare_hru_parameter_file(oSwat_in)
        swat_write_hru_input_file(oSwat_in)        
    else:
        pass
    #step 5
    swat_copy_executable_file(oSwat_in)
    #step 6
    sFilename_bash = swat_prepare_simulation_bash_file(oSwat_in)
    #step 7
    sFilename_job = swat_prepare_simulation_job_file(oSwat_in)    
    #step 8 submit
    iFlag_mode = oSwat_in.iFlag_mode
    print('Finished')
    
     

 