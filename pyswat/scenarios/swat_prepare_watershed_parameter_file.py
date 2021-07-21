
import os
import sys

import numpy as np
from pyearth.system.define_global_variables import *
from pyearth.toolbox.reader.text_reader_string import text_reader_string




def swat_prepare_watershed_parameter_file(oModel_in):
    """
    #prepare the pest control file
    """      
    sWorkspace_data_project = oModel_in.sWorkspace_data + slash +  oModel_in.sWorkspace_project
    sWorkspace_simulation_case = oModel_in.sWorkspace_simulation_case    
    sWorkspace_calibration_case = oModel_in.sWorkspace_calibration_case 
    
    iFlag_simulation = oModel_in.iFlag_simulation
    iFlag_watershed = oModel_in.iFlag_watershed
    
    
    aVariable = oModel_in.aVariable
    aValue = oModel_in.aValue
    
    

    if iFlag_simulation == 1:
        sFilename_watershed_template = sWorkspace_simulation_case + slash + 'watershed.para'    
        
    else:
        sFilename_watershed_template = sWorkspace_simulation_case + slash + 'watershed.para'    
   
        pass
    
    if iFlag_watershed ==1:    
        ofs = open(sFilename_watershed_template, 'w')
        nvariable = len(aVariable)
        sLine = 'watershed'
        for i in range(nvariable):
            sVariable = aVariable[i]
            sLine = sLine + ',' + sVariable
        sLine = sLine + '\n'        
        ofs.write(sLine)
    
        
        
        sLine = 'watershed'
        for iVariable in range(nvariable):
            sValue =  "{:5.2f}".format( aValue[iVariable] )            
            sLine = sLine + ', ' + sValue 
        sLine = sLine + '\n'
        ofs.write(sLine)
        ofs.close()
        print('watershed parameter is ready!')
    
    

    return
