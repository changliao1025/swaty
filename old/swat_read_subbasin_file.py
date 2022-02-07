import sys
import os


import numpy as np
from numpy  import array
from calendar import monthrange #calcuate the number of days in a month




from pyearth.toolbox.reader.text_reader_string import text_reader_string



def swat_prepare_subbasin_configuration_file(iSubbasin, sWorkspace_simulation_model_in, sFilename_subbasin_in):
    """
    Test
    """

    
    ifs=open(sFilename_subbasin_in, 'rb')   
    line = ifs.readline()
    
    dummy = line.strip()
    if(dummy == '| HRU data'):
        line = ifs.readline()
        line = line.decode("utf-8")
        sDummy = line.split()
        nhru = int((sDummy[0]).strip())
    else:        
       
        if(dummy == 'HRU: General'):

            for ihru in range (0, nhru):

                #this is the subbasin line
                line = ifs.readline()
                line = line.decode("utf-8")
                dummy = line[0:9]
                sFilename_hru = sWorkspace_simulation_model_in + slash + dummy + '.mgt'
                sFilename_hru_out = sWorkspace_simulation_model_in + slash + dummy + '.mgt.tpl'
                iHru_in  = ihru + 1
                swat_write_hru_template_file(iSubbasin_in, iHru_in, sFilename_hru, sFilename_hru_out)
                #call another function to read 
                #go to the next subbasin
        else:
            line = ifs.readline() 
            #print(line)
            line = str(line, errors='ignore')
            #line = line.decode("utf-8")
    ifs.close()
    return nhru

