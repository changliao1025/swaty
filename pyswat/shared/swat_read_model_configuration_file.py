import os 
import sys #used to add system path
from jdcal import gcal2jd, jd2gcal
import datetime

import numpy as np

from pyearth.system.define_global_variables import *
from pyearth.toolbox.reader.parse_xml_file import parse_xml_file
from pyearth.toolbox.reader.read_configuration_file import read_configuration_file
from pyearth.toolbox.reader.text_reader_string import text_reader_string


pDate = datetime.datetime.today()
sDate_default = "{:04d}".format(pDate.year) + "{:02d}".format(pDate.month) + "{:02d}".format(pDate.day)

def swat_read_model_configuration_file(sFilename_configuration_in):


    config = parse_xml_file(sFilename_configuration_in)
    sModel = config['sModel']  
    sRegion = config['sRegion']

    sWorkspace_data=  config['sWorkspace_data']
    sWorkspace_scratch=  config['sWorkspace_scratch']
    


    
    sLine = config['aParameter']
    dummy = sLine.split(',')
    config['aParameter'] =  np.array(dummy) # config['aParameter'].split(',')
            

    sLine = config['aParameter_value']
    dummy = sLine.split(',')
    config['aParameter_value'] =  np.array( dummy  ).astype(float)
            

    sLine = config['aParameter_value_lower']
    dummy = sLine.split(',')
    config['aParameter_value_lower'] =  np.array( dummy  ).astype(float)
           

    sLine = config['aParameter_value_upper']
    dummy = sLine.split(',')
    config['aParameter_value_upper'] =  np.array( dummy  ).astype(float)
            

    

    config['iCase_index'] = int( config['iCase_index'])
    

    
    iYear_start  = int( config['iYear_start'])
    iMonth_start  = int(  config['iMonth_start'])
    iDay_start  = int(  config['iDay_start'] )
    iYear_end  = int( config['iYear_end'])
    iMonth_end  = int(  config['iMonth_end'])
    iDay_end  = int(  config['iDay_end'])   

    
    #by default, this system is used to prepare inputs for modflow simulation.
    #however, it can also be used to prepare gsflow simulation inputs.
    

    #based on global variable, a few variables are calculate once
    #calculate the modflow simulation period
    #https://docs.python.org/3/library/datetime.html#datetime-objects
    lJulian_start = gcal2jd(iYear_start, iMonth_start, iDay_start)  #year, month, day
    lJulian_end = gcal2jd(iYear_end, iMonth_end, iDay_end)  #year, month, day
    nstress =int( lJulian_end[1] - lJulian_start[1] + 1 )  
    config['lJulian_start'] =   lJulian_start[1]
    config['lJulian_end'] =  lJulian_end[1]
    config['nstress'] =   nstress 

    
   
    sFilename_swat = config['sFilename_swat']   

    if 'nhru' in config:
        pass
    
    #data
    
    #simulation
    
    
   
    
    return config