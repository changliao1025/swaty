
import os
import sys

import numpy as np
from pyearth.system.define_global_variables import *
from pyearth.toolbox.reader.text_reader_string import text_reader_string




def swat_prepare_hru_parameter_file(oModel_in):
    """
    #prepare the pest control file
    """      
    sWorkspace_data_project = oModel_in.sWorkspace_data + slash +  oModel_in.sWorkspace_project
    sWorkspace_simulation_case = oModel_in.sWorkspace_simulation_case    
    sWorkspace_calibration_case = oModel_in.sWorkspace_calibration_case 
    
    iFlag_simulation = oModel_in.iFlag_simulation
    
    aVariable = oModel_in.aVariable
    aValue = oModel_in.aValue
    
    #read hru type
    sFilename_hru_combination = sWorkspace_data_project + slash + 'auxiliary' + slash\
     + 'hru' + slash   + 'hru_combination.txt'
    if os.path.isfile(sFilename_hru_combination):
        pass
    else:
        print('The file does not exist!')
        return
    aData_all = text_reader_string(sFilename_hru_combination)
    nhru_type = len(aData_all)

    if iFlag_simulation == 1:
        sFilename_hru_template = sWorkspace_simulation_case + slash + 'hru.para'    
    else:
        sFilename_hru_template = sWorkspace_calibration_case + slash + 'hru.para'
        pass

    ofs = open(sFilename_hru_template, 'w')
    nvariable = len(aVariable)
    sLine = 'hru'
    for i in range(nvariable):
        sVariable = aVariable[i]
        sLine = sLine + ',' + sVariable
    sLine = sLine + '\n'        
    ofs.write(sLine)

    for iHru_type in range(0, nhru_type):
        sHru_type = "{:03d}".format( iHru_type + 1)
        sLine = 'hru'+ sHru_type 
        for iVariable in range(nvariable):
            sValue =  "{:5.2f}".format( aValue[iVariable] )            
            sLine = sLine + ', ' + sValue 
        sLine = sLine + '\n'
        ofs.write(sLine)
    ofs.close()
    print('hru parameter is ready!')

    return
