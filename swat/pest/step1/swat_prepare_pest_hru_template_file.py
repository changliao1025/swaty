import sys
import os
import numpy as np
import datetime
import calendar



from numpy  import array

#import the eslib library
sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'

sys.path.append(sPath_library_python)
from toolbox.reader.text_reader_string import text_reader_string

def swat_prepare_pest_hru_template_file(sFilename_configuration_in, sModel):
    """
    #prepare the pest template file
    """
    

    #strings    

    sWorkspace_data_relative = config['sWorkspace_data']
     
    sWorkspace_project_relative = config['sWorkspace_project']
    sWorkspace_simulation_relative = config['sWorkspace_simulation']
    sWorkspace_calibration_relative = config['sWorkspace_calibration']

    pest_mode =  config['pest_mode'] 
    sRegion = config['sRegion']

    sWorkspace_data = sWorkspace_scratch + slash + sWorkspace_data_relative
    sWorkspace_data_project = sWorkspace_data + slash + sWorkspace_project_relative

    sWorkspace_simulation = sWorkspace_scratch +  slash  + sWorkspace_simulation_relative + slash + sCase
    sWorkspace_calibration = sWorkspace_scratch + slash + sWorkspace_calibration_relative + slash + sCase

    sWorkspace_pest_model = sWorkspace_calibration 
    
    
    #read hru type
    sFilename_hru_combination = sWorkspace_data_project + slash + 'auxiliary' + slash\
     + 'hru' +slash  + 'hru_combination.txt'
    aData_all = text_reader_string(sFilename_hru_combination)
    nhru_type = len(aData_all)


    sFilename_hru_template = sWorkspace_pest_model + slash + 'hru.tpl'
    ofs = open(sFilename_hru_template, 'w')
    sLine = 'ptf $\n'
    ofs.write(sLine)
    #right now we only have one parameter, we can add more later following this format
    sLine = 'hru, cn2\n'
    ofs.write(sLine)
    for iHru_type in range(0, nhru_type):
        sHru_type = "{:03d}".format( iHru_type + 1)
        sLine = 'hru'+ sHru_type + ', ' + '$cn2' + sHru_type +'$\n'
        ofs.write(sLine)
    ofs.close()
    print('hru template is ready!')

    return
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
       
    
    swat_prepare_pest_hru_template_file(sFilename_configuration_in, sModel)