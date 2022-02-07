
import os
import sys

import numpy as np
from pyearth.system.define_global_variables import *
from pyearth.toolbox.reader.text_reader_string import text_reader_string




def swat_prepare_hru_parameter_file(oSwat_in):
    """
    #prepare the pest control file
    """      
    sWorkspace_data_project = oSwat_in.sWorkspace_data + slash +  oSwat_in.sWorkspace_project
    sWorkspace_simulation_case = oSwat_in.sWorkspace_simulation_case    
    sWorkspace_calibration_case = oSwat_in.sWorkspace_calibration_case 
    
    iFlag_simulation = oSwat_in.iFlag_simulation
    iFlag_watershed = oSwat_in.iFlag_watershed
    iFlag_subbasin = oSwat_in.iFlag_subbasin
    iFlag_hru = oSwat_in.iFlag_hru
    
    aParameter_hru = oSwat_in.aParameter_hru
    aParameter_value_hru = oSwat_in.aParameter_value_hru
    nParameter_hru = oSwat_in.nParameter_hru
    
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
        
        sFilename_hru_template = sWorkspace_simulation_case + slash + 'hru.para'    
        pass
    
    
    
    

    if iFlag_hru ==1:    
        ofs = open(sFilename_hru_template, 'w')
        
        sLine = 'hru'
        for i in range(nParameter_hru):
            sVariable = aParameter_hru[i]
            sLine = sLine + ',' + sVariable
        sLine = sLine + '\n'        
        ofs.write(sLine)

        for iHru_type in range(0, nhru_type):
            sHru_type = "{:03d}".format( iHru_type + 1)
            sLine = 'hru'+ sHru_type 
            for i in range(nParameter_hru):
                sValue =  "{:5.2f}".format( aParameter_value_hru[i] )            
                sLine = sLine + ', ' + sValue 
            sLine = sLine + '\n'
            ofs.write(sLine)
        ofs.close()
        print('hru parameter is ready!')

    return
