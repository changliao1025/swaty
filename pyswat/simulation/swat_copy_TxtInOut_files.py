#this function is used to copy raw swat simulation files into the calibration folder

import os
import sys
import glob
from shutil import copyfile

sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)
from eslib.system import define_global_variables
from eslib.system.define_global_variables import *

sPath_swat_python = sWorkspace_code +  slash + 'python' + slash + 'swat' + slash + 'swat_python'
sys.path.append(sPath_swat_python)
from swat.shared import swat_global

#from eslib.toolbox.reader.read_configuration_file import read_configuration_file

def swat_copy_TxtInOut_files():
    """
    sFilename_configuration_in
    sModel
    """
    
    
    sWorkspace_simulation_copy = swat_global.sWorkspace_simulation_copy
    sWorkspace_simulation_case = swat_global.sWorkspace_simulation_case  
    sWorkspace_target_case = sWorkspace_simulation_case    

    if not os.path.exists(sWorkspace_simulation_copy):
        print(sWorkspace_simulation_copy)
        print('The simulation copy does not exist!')
        return
    else:      
        pass
    
    
    if not os.path.exists(sWorkspace_target_case):
        os.makedirs(sWorkspace_target_case)
    else:      
        print("The simulation folder already exist")
        #return
    
    
    #the following file will be copied    

    aExtension = ('.pnd','.rte','.sub','.swq','.wgn','.wus',\
            '.chm','.gw','.hru','.mgt','sdr','.sep',\
             '.sol','ATM','bsn','wwq','deg','.cst',\
             'dat','fig','cio','fin','dat','.pcp','.Tmp'  )

    #we need to be careful that Tmp is different in python/linux with tmp
            

    for sExtension in aExtension:

        sRegax = sWorkspace_simulation_copy + slash + '*' + sExtension

        if sExtension == '.Tmp':
            for sFilename in glob.glob(sRegax):
                sBasename_with_extension = os.path.basename(sFilename)
                sFilename_new = sWorkspace_target_case + slash + sBasename_with_extension.lower()
                copyfile(sFilename, sFilename_new)
        else:

            for sFilename in glob.glob(sRegax):
                sBasename_with_extension = os.path.basename(sFilename)
                sFilename_new = sWorkspace_target_case + slash + sBasename_with_extension
                copyfile(sFilename, sFilename_new)


    
    print('Finished copying all input files')


#the main entrance    
if __name__ == '__main__':

    
    
    swat_copy_TxtInOut_files()