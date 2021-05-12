import os 
import sys #used to add system path
from jdcal import gcal2jd, jd2gcal
import datetime



from pyearth.system.define_global_variables import *
from pyearth.toolbox.reader.parse_xml_file import parse_xml_file
from pyearth.toolbox.reader.read_configuration_file import read_configuration_file




pDate = datetime.datetime.today()
sDate_default = "{:04d}".format(pDate.year) + "{:02d}".format(pDate.month) + "{:02d}".format(pDate.day)

def swat_read_model_configuration_file(sFilename_configuration_in,\
     iCase_index_in=None, \
         sJob_in=None,\
          iFlag_mode_in=None, \
         aVariable_in = None, \
             aValue_in = None, \
                 sDate_in = None):


    config = parse_xml_file(sFilename_configuration_in)
    sModel = config['sModel']  
    sRegion = config['sRegion']

    sWorkspace_data=  config['sWorkspace_data']
    sWorkspace_scratch=  config['sWorkspace_scratch']
    


    
    if iFlag_mode_in is not None:
        iFlag_mode = iFlag_mode_in
    else:
        iFlag_mode = 1
    if aVariable_in is not None:
        aVariable = aVariable_in
    else:
        aVariable = None
        pass

    if aValue_in is not None:
        aValue = aValue_in
    else:
        aValue = None
        pass

    if sDate_in is not None:
        sDate = sDate_in
    else:
        sDate = sDate_default
        pass

    if iCase_index_in is not None:        
        iCase_index = iCase_index_in
    else:       
        iCase_index = 1

    

    config['iCase_index'] = iCase_index
    
    #swat_global.aVariable = aVariable
    #swat_global.aValue = aValue
    
    
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
    
    #data
    sWorkspace_data_project = sWorkspace_data + slash + sModel + slash + sRegion
    #simulation
    
    
   
    
    return config