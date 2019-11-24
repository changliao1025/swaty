import os , stat
import sys #used to add system path

sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)
from eslib.system import define_global_variables
from eslib.system.define_global_variables import *

sPath_swat_python = sWorkspace_code +  slash + 'python' + slash + 'swat' + slash + 'swat_python'
sys.path.append(sPath_swat_python)
from swat.simulation import swat_global
from swat.simulation.swat_global import *

def swat_prepare_simulation_job_file():
    
    sWorkspace_simulation_case = swat_global.sWorkspace_simulation_case
    sJob = swat_global.sJob

    sFilename_job = sWorkspace_simulation_case + slash + 'submit.job'
    ifs = open(sFilename_job, 'w')   
    
    #end of example
    sLine = '#!/bin/bash' + '\n'
    ifs.write(sLine)
    sLine = '#SBATCH -A inversion' + '\n'
    ifs.write(sLine)
    sLine = '#SBATCH -t 0:10:00' + '\n'
    ifs.write(sLine)
    sLine = '#SBATCH -p short' + '\n'
    ifs.write(sLine)
    sLine = '#SBATCH -N 1' + '\n'
    ifs.write(sLine)
    sLine = '#SBATCH -n 2' + '\n'
    ifs.write(sLine)
    sLine = '#SBATCH -J ' + sJob + '' + '\n'
    ifs.write(sLine)
    sLine = '#SBATCH -o out.out' + '\n'
    ifs.write(sLine)
    sLine = '#SBATCH -e err.err' + '\n'
    ifs.write(sLine)
    sLine = '#SBATCH --mail-type=ALL' + '\n'
    ifs.write(sLine)
    sLine = '#SBATCH --mail-user=chang.liao@pnnl.gov' + '\n'
    ifs.write(sLine)
    sLine = 'cd $SLURM_SUBMIT_DIR' + '\n'
    ifs.write(sLine)
    sLine = 'module purge' + '\n'
    ifs.write(sLine)    
    sLine = 'module load gcc/5.2.0' + '\n'
    ifs.write(sLine)
    sLine = 'cd ' + sWorkspace_simulation_case+ '\n'
    ifs.write(sLine)
    sLine = './swat' + '\n'
    ifs.write(sLine)
    ifs.close()
    os.chmod(sFilename_job, stat.S_IRWXU )

    #alaso need sbatch to submit it

    print('Job file is prepared.')
    return sFilename_job
