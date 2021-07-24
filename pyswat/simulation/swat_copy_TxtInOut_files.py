#this function is used to copy raw swat simulation files into the calibration folder

import os
import sys
import glob
from shutil import copyfile


from pyearth.system.define_global_variables import *



#from pyearth.toolbox.reader.read_configuration_file import read_configuration_file

def swat_copy_TxtInOut_files(oSwat_in):
    """
    sFilename_configuration_in
    sModel
    """
    sWorkspace_data= oSwat_in.sWorkspace_data
    sWorkspace_data_project = sWorkspace_data+ slash+ oSwat_in.sWorkspace_project
    sWorkspace_simulation_copy = oSwat_in.sWorkspace_simulation_copy
    
    
    sWorkspace_simulation_case = oSwat_in.sWorkspace_simulation_case  
    sWorkspace_calibration_case = oSwat_in.sWorkspace_calibration_case  

    if oSwat_in.iFlag_calibration ==1:
        sWorkspace_target_case = os.getcwd()
        
    else:
        sWorkspace_target_case = sWorkspace_simulation_case   
        

    if not os.path.exists(sWorkspace_simulation_copy):
        print(sWorkspace_simulation_copy)
        print('The simulation copy does not exist!')
        return
    else:      
        pass
    
    Path(sWorkspace_target_case).mkdir(parents=True, exist_ok=True)
    
    
    
    #the following file will be copied    

    aExtension = ('.pnd','.rte','.sub','.swq','.wgn','.wus',\
            '.chm','.gw','.hru','.mgt','sdr','.sep',\
             '.sol','ATM','bsn','wwq','deg','.cst',\
             'dat','fig','cio','fin','dat','.pcp','.tmp'  )

    #we need to be careful that Tmp is different in python/linux with tmp
            

    for sExtension in aExtension:

        sRegax = sWorkspace_simulation_copy + slash + '*' + sExtension

        if sExtension == '.tmp':
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