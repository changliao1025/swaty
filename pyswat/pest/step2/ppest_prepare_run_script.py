#this function is used to copy swat and beopest from linux hpc to calibration folder
import sys
import os, stat
import numpy as np
import datetime
import calendar



import errno
from os.path import isfile, join
from os import listdir

from numpy  import array
from shutil import copyfile, copy2


sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'
sys.path.append(sPath_library_python)
from toolbox.reader.text_reader_string import text_reader_string

    
def ppest_prepare_run_script(sFilename_configuration_in, sModel):
    """
    prepare the job submission file
    """
    
    
    #strings
    

    sWorkspace_data_relative = config['sWorkspace_data']  
    sWorkspace_project_relative = config['sWorkspace_project']
    sWorkspace_simulation_relative = config['sWorkspace_simulation']
    sWorkspace_calibration_relative = config['sWorkspace_calibration']

    sWorkspace_calibration = sWorkspace_scratch + slash + sWorkspace_calibration_relative

    sWorkspace_pest_model = sWorkspace_calibration + slash + sModel

    sFilename_script = sWorkspace_pest_model + slash + 'run_swat_model'
    ifs = open(sFilename_script, 'w')
    #example
    #!/bin/bash
    #echo "Started to prepare python scripts"
    #
    #cat << EOF > pyscript1.py
    ##!/share/apps/python/anaconda3.6/bin/python
    #from swat_prepare_pest_slave_input_file import *
    #sFilename_configuration_in='/pic/scratch/liao313/03model/swat/purgatoire30/calibration/linux_config.txt'
    #swat_prepare_pest_slave_input_file(sFilename_configuration_in)
    #EOF
    #
    #cat << EOF > pyscript2.py
    ##!/share/apps/python/anaconda3.6/bin/python
    #from swat_prepare_input_from_pest import *
    #sFilename_configuration_in='/pic/scratch/liao313/03model/swat/purgatoire30/calibration/linux_config.txt'
    #swat_prepare_input_from_pest(sFilename_configuration_in)
    #EOF
    #
    #cat << EOF > pyscript3.py
    ##!/share/apps/python/anaconda3.6/bin/python
    #from swat_extract_output_for_pest import *
    #sFilename_configuration_in='/pic/scratch/liao313/03model/swat/purgatoire30/calibration/linux_config.txt'
    #swat_extract_output_for_pest(sFilename_configuration_in)
    #EOF
    #
    #chmod 755 pyscript1.py
    #chmod 755 pyscript2.py
    #chmod 755 pyscript3.py
    #echo "Finished preparing python scripts"
    #
    #echo "Started to prepare SWAT inputs"
    ##step 1: prepare inputs
    #./pyscript1.py
    #./pyscript2.py
    #echo "Finished preparing SWAT simulation"
    #
    ##step 2: run swat model
    #echo "Started to run SWAT simulation"
    #./swat
    #echo "Finished running SWAT simulation"
    #
    ##step 3: extract SWAT output
    #echo "Started to extract SWAT simulation outputs"
    #./pyscript3.py
    #echo "Finished extracting SWAT simulation outputs"
    #end of example
    sLine = '#!/bin/bash\n'
    ifs.write(sLine)

    sLine = 'echo "Started to prepare python scripts"\n'
    ifs.write(sLine)
    #the first one
    sLine = 'cat << EOF > pyscript1.py\n'
    ifs.write(sLine)

    sLine = '#!/share/apps/python/anaconda3.6/bin/python\n'
    ifs.write(sLine)

    sLine = 'from swat_prepare_pest_slave_input_file import *\n'
    ifs.write(sLine)

    sLine = 'sFilename_configuration_in = ' + '"' + sFilename_configuration_in + '"\n'
    ifs.write(sLine)

    sLine = 'sModel = ' + '"' + sModel + '"\n'
    ifs.write(sLine)
    sLine = 'swat_prepare_pest_slave_input_file(sFilename_configuration_in, sModel)\n'
    ifs.write(sLine)

    sLine = 'EOF\n'
    ifs.write(sLine)
    #the second 
    sLine = 'cat << EOF > pyscript2.py\n'
    ifs.write(sLine)

    sLine = '#!/share/apps/python/anaconda3.6/bin/python\n'
    ifs.write(sLine)

    sLine = 'from swat_prepare_input_from_pest import *\n'
    ifs.write(sLine)

    sLine = 'sFilename_configuration_in = ' + '"' + sFilename_configuration_in + '"\n'
    ifs.write(sLine)

    sLine = 'sModel = ' + '"' + sModel + '"\n'
    ifs.write(sLine)
    sLine = 'swat_prepare_input_from_pest(sFilename_configuration_in, sModel)\n'
    ifs.write(sLine)

    sLine = 'EOF\n'
    ifs.write(sLine)
    #the third one
    sLine = 'cat << EOF > pyscript3.py\n'
    ifs.write(sLine)

    sLine = '#!/share/apps/python/anaconda3.6/bin/python\n'
    ifs.write(sLine)

    sLine = 'from swat_extract_output_for_pest import *\n'
    ifs.write(sLine)

    sLine = 'sFilename_configuration_in = ' + '"' + sFilename_configuration_in + '"\n'
    ifs.write(sLine)

    sLine = 'sModel = ' + '"' + sModel + '"\n'
    ifs.write(sLine)
    sLine = 'swat_extract_output_for_pest(sFilename_configuration_in, sModel)\n'
    ifs.write(sLine)

    sLine = 'EOF\n'
    ifs.write(sLine)
    #end of python

    sLine = 'chmod 755 pyscript1.py\n'
    ifs.write(sLine)

    sLine = 'chmod 755 pyscript2.py\n'
    ifs.write(sLine)

    sLine = 'chmod 755 pyscript3.py\n'
    ifs.write(sLine)

    sLine = 'echo "Finished preparing python scripts"\n'
    ifs.write(sLine)

    sLine = 'echo "Started to prepare SWAT inputs"\n'
    ifs.write(sLine)
    #step 1: prepare inputs
    sLine = './pyscript1.py\n'
    ifs.write(sLine)
    
    sLine = './pyscript2.py\n'
    ifs.write(sLine)

    sLine = 'echo "Finished preparing SWAT simulation"\n'
    ifs.write(sLine)
    #step 2: run swat model
    sLine = 'echo "Started to run SWAT simulation"\n'
    ifs.write(sLine)
    sLine = './swat\n'
    ifs.write(sLine)
    sLine = 'echo "Finished running SWAT simulation"\n'
    ifs.write(sLine)

    #step 3: extract SWAT output
    sLine = 'echo "Started to extract SWAT simulation outputs"\n'
    ifs.write(sLine)
    sLine = './pyscript3.py\n'
    ifs.write(sLine)
    sLine = 'echo "Finished extracting SWAT simulation outputs"\n'
    ifs.write(sLine)


    ifs.close()

    os.chmod(sFilename_script, stat.S_IREAD | stat.S_IWRITE | stat.S_IXUSR)


    print('The pest run model file is prepared successfully!')


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
    ppest_prepare_run_script(sFilename_configuration, sModel)
