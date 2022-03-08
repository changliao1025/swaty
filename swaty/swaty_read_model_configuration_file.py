import os 
import sys #used to add system path

import datetime
import json
import numpy as np
import pyearth.toolbox.date.julian as julian
from swaty.classes.pycase import swatcase

pDate = datetime.datetime.today()
sDate_default = "{:04d}".format(pDate.year) + "{:02d}".format(pDate.month) + "{:02d}".format(pDate.day)

def swaty_read_model_configuration_file(sFilename_configuration_in , \
    iCase_index_in = None,\
        iYear_start_in = None,\
            iMonth_start_in = None,\
                iDay_start_in = None, \
        iYear_end_in = None,\
            iMonth_end_in = None,\
                iDay_end_in = None, \
            ):

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
         
    if iCase_index_in is not None:        
        iCase_index = iCase_index_in
    else:       
        iCase_index = int( aConfig['iCase_index'])
        #aConfig['iCase_index'] = int( aConfig['iCase_index'])
    
    if iYear_start_in is not None:        
        iYear_start = iYear_start_in
    else:       
        iYear_start  = int( aConfig['iYear_start'])

    if iMonth_start_in is not None:        
        iMonth_start = iYear_end_in
    else:       
        iMonth_start  = int( aConfig['iMonth_start'])

    if iDay_start_in is not None:        
        iDay_start = iDay_start_in
    else:       
        iDay_start  = int( aConfig['iDay_start'])
    
    if iYear_end_in is not None:        
        iYear_end = iYear_end_in
    else:       
        iYear_end  = int( aConfig['iYear_end'])
    
    if iMonth_end_in is not None:        
        iMonth_end = iMonth_end_in
    else:       
        iMonth_end  = int( aConfig['iMonth_end'])

    if iDay_end_in is not None:
        iDay_end = iDay_end_in
    else:       
        iDay_end  = int( aConfig['iDay_end'])

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
    
    oSwat = swatcase(aConfig)
   
    
    return oSwat