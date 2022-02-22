import os 
import sys #used to add system path
import julian
import datetime
import json
import numpy as np


pDate = datetime.datetime.today()
sDate_default = "{:04d}".format(pDate.year) + "{:02d}".format(pDate.month) + "{:02d}".format(pDate.day)

def swaty_read_model_configuration_file(sFilename_configuration_in):


    

    if not os.path.isfile(sFilename_configuration_in):
        print(sFilename_configuration_in + ' does not exist')
        return
    
    # Opening JSON file
    with open(sFilename_configuration_in) as json_file:
        aConfig = json.load(json_file)   


    sModel = aConfig['sModel']  
    sRegion = aConfig['sRegion']

    sWorkspace_data=  aConfig['sWorkspace_data']
    sWorkspace_scratch=  aConfig['sWorkspace_scratch']

    sLine = aConfig['aParameter']
    dummy = sLine.split(',')
    aConfig['aParameter'] =  np.array(dummy) # aConfig['aParameter'].split(',')
            

    sLine = aConfig['aParameter_value']
    dummy = sLine.split(',')
    aConfig['aParameter_value'] =  np.array( dummy  ).astype(float)
            

    sLine = aConfig['aParameter_value_lower']
    dummy = sLine.split(',')
    aConfig['aParameter_value_lower'] =  np.array( dummy  ).astype(float)
           

    sLine = aConfig['aParameter_value_upper']
    dummy = sLine.split(',')
    aConfig['aParameter_value_upper'] =  np.array( dummy  ).astype(float)      

    aConfig['iCase_index'] = int( aConfig['iCase_index'])
    
    iYear_start  = int( aConfig['iYear_start'])
    iMonth_start  = int(  aConfig['iMonth_start'])
    iDay_start  = int(  aConfig['iDay_start'] )
    iYear_end  = int( aConfig['iYear_end'])
    iMonth_end  = int(  aConfig['iMonth_end'])
    iDay_end  = int(  aConfig['iDay_end'])   

    #by default, this system is used to prepare inputs for modflow simulation.
    #however, it can also be used to prepare gsflow simulation inputs.

    #based on global variable, a few variables are calculate once
    #calculate the modflow simulation period
    #https://docs.python.org/3/library/datetime.html#datetime-objects
    
    
    dummy1 = datetime.datetime(iYear_start, iMonth_start, iDay_start)
    dummy2 = datetime.datetime(iYear_end, iMonth_end, iDay_end)
    julian1 = julian.to_jd(dummy1, fmt='jd')
    julian2 = julian.to_jd(dummy2, fmt='jd')

    nstress =int( julian2 - julian1 + 1 )  
    aConfig['lJulian_start'] =  julian1
    aConfig['lJulian_end'] =  julian2
    aConfig['nstress'] =   nstress     
   
    sFilename_swat = aConfig['sFilename_swat']   

    if 'nhru' in aConfig:
        pass
    
    #data
    
    #simulation 
      
    
    return aConfig