import os , stat
import sys #used to add system path

sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)

from eslib.system.define_global_variables import *

sPath_swat_python = sWorkspace_code +  slash + 'python' + slash + 'swat' + slash + 'swat_python'
sys.path.append(sPath_swat_python)
from swat.simulation import swat_global


def swat_prepare_simulation_bash_file():
    
    sWorkspace_simulation_case = swat_global.sWorkspace_simulation_case

    sFilename_bash = sWorkspace_simulation_case + slash + 'run.sh'
    ifs = open(sFilename_bash, 'w')       
    #end of example
    sLine = '#!/bin/bash' + '\n'
    ifs.write(sLine)    
    sLine = 'module purge' + '\n'
    ifs.write(sLine)    
    sLine = 'module load gcc/5.2.0' + '\n'
    ifs.write(sLine)
    sLine = 'cd ' + sWorkspace_simulation_case + '\n'
    ifs.write(sLine)
    sLine = './swat' + '\n'
    ifs.write(sLine)
    ifs.close()
    #change mod
    os.chmod(sFilename_bash, stat.S_IRWXU )
    print('Bash file is prepared.')
    return sFilename_bash
