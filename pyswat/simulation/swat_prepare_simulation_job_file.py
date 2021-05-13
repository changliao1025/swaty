import os , stat
import sys #used to add system path



from pyearth.system.define_global_variables import *





def swat_prepare_simulation_job_file(oModel_in):
    
    sWorkspace_simulation_case = oModel_in.sWorkspace_simulation_case
    sJob = oModel_in.sJob

    sFilename_job = sWorkspace_simulation_case + slash + 'submit.job'
    ifs = open(sFilename_job, 'w')   
    
    #end of example
    sLine = '#!/bin/bash' + '\n'
    ifs.write(sLine)
    sLine = '#SBATCH -A br20_liao313' + '\n'
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
    sLine = 'module load gcc/6.1.0' + '\n'
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
