#this function is used to copy swat and beopest from linux hpc to calibration folder
import sys
import os
import numpy as np
import datetime
import calendar

import errno
from os.path import isfile, join
from os import listdir

from numpy  import array
from shutil import copyfile, copy2



#import library
sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'
sys.path.append(sPath_library_python)

from toolbox.reader.text_reader_string import text_reader_string

    
def swat_prepare_calibration_job_file(sFilename_configuration_in, sModel_in = None):
    """
    prepare the job submission file
    """
   
    
    #strings
    sWorkspace_home = config['sWorkspace_home']
    sWorkspace_scratch=config['sWorkspace_scratch']

    sWorkspace_data_relative = config['sWorkspace_data']  
    sWorkspace_project_relative = config['sWorkspace_project']
    sWorkspace_simulation_relative = config['sWorkspace_simulation']
    sWorkspace_calibration_relative = config['sWorkspace_calibration']

    
    pest_mode =  config['pest_mode'] 
    sRegion = config['sRegion']
    sFilename_swat = config['sFilename_swat']
    sFilename_pest = config['sFilename_pest']

    
    sWorkspace_calibration = sWorkspace_scratch + slash + sWorkspace_calibration_relative

    sWorkspace_pest_model = sWorkspace_calibration + slash + sModel

    sFilename_job = sWorkspace_pest_model + slash + 'job.submit'
    ifs = open(sFilename_job, 'w')
    #example
    #!/bin/bash
    #SBATCH -A inversion
    #SBATCH -t 100:00:00
    #SBATCH -N 1
    #SBATCH -n 1
    #SBATCH -J child
    #SBATCH -o stdout.out
    #SBATCH -e stderr.err
    #SBATCH --mail-type=ALL
    #SBATCH --mail-user=chang.liao@pnnl.gov
    #cd $SLURM_SUBMIT_DIR
    #module purge
    #module load gcc/5.2.0
    #module load python/anaconda3.6
    #end of example
    sLine = '#!/bin/bash\n'
    ifs.write(sLine)

    sLine = '#SBATCH -A inversion\n'
    ifs.write(sLine)

    sLine = '#SBATCH -t 100:00:00\n'
    ifs.write(sLine)

    sLine = '#SBATCH -N 3\n'
    ifs.write(sLine)

    sLine = '#SBATCH -n 36\n'
    ifs.write(sLine)

    sLine = '#SBATCH -J ' + sModel + '\n'
    ifs.write(sLine)

    sLine = '#SBATCH -o out.out\n'
    ifs.write(sLine)

    sLine = '#SBATCH -e err.err\n'
    ifs.write(sLine)

    sLine = '#SBATCH --mail-type=ALL\n'
    ifs.write(sLine)

    sLine = '#SBATCH --mail-user=chang.liao@pnnl.gov\n'
    ifs.write(sLine)

    sLine = 'cd $SLURM_SUBMIT_DIR\n'
    ifs.write(sLine)

    sLine = 'module purge\n'
    ifs.write(sLine)

    sLine = 'module load python/anaconda3.6\n'
    ifs.write(sLine)

    sLine = 'module load gcc/5.2.0\n'
    ifs.write(sLine)

    sLine = 'module load openmpi/1.8.3\n'
    ifs.write(sLine)

    sLine = 'mpirun -np 36 ppest ' + sWorkspace_pest_model+slash+sRegion + '_swat /M slave\n'
    ifs.write(sLine)

    ifs.close()


    print('The pest job file is copied successfully!')


if __name__ == '__main__':
    sRegion = 'tinpan'
    sModel ='swat'
    sCase = 'test'
    sJob = sCase
    sTask = 'simulation'
    iFlag_simulation = 1
    iFlag_pest = 0
    if iFlag_pest == 1:
        sTask = 'calibration'
    sFilename_configuration = sWorkspace_scratch + slash + '03model' + slash \
              + sModel + slash + sRegion + slash \
              + sTask  + slash + sFilename_config
            
    swat_prepare_calibration_job_file(sFilename_configuration_in, sModel)
