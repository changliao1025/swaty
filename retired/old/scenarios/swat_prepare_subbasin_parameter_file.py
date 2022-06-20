
import os
import sys

import numpy as np
from pyearth.system.define_global_variables import *
from pyearth.toolbox.reader.text_reader_string import text_reader_string




def swat_prepare_subbasin_parameter_file(oSwat_in):
    """
    #prepare the pest control file
    """      
    sWorkspace_simulation_case = oSwat_in.sWorkspace_simulation_case           
    iFlag_simulation = oSwat_in.iFlag_simulation 
    iFlag_subbasin = oSwat_in.iFlag_subbasin 
    nsubbasin = oSwat_in.nsubbasin      
    aParameter_subbasin = oSwat_in.aParameter_subbasin
    aParameter_value_subbasin = oSwat_in.aParameter_value_subbasin
    nParameter_subbasin = oSwat_in.nParameter_subbasin             
    sFilename_subbasin_template = sWorkspace_simulation_case + slash + 'subbasin.para'       
    
    if iFlag_subbasin ==1:    
        ofs = open(sFilename_subbasin_template, 'w')
        
        sLine = 'subbasin'
        for i in range(nParameter_subbasin):
            sVariable = aParameter_subbasin[i]
            sLine = sLine + ',' + sVariable
        sLine = sLine + '\n'        
        ofs.write(sLine)
    
        for iSubbasin in range(0, nsubbasin):
            sSubbasin = "{:03d}".format( iSubbasin + 1)
            sLine = 'subbasin' + sSubbasin 
            for i in range(nParameter_subbasin):
                sValue =  "{:5.2f}".format( aParameter_value_subbasin[i] )            
                sLine = sLine + ', ' + sValue 
            sLine = sLine + '\n'
            ofs.write(sLine)
        ofs.close()
        print('subbasin parameter is ready!')

    

    return
