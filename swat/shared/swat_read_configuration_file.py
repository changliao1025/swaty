import os 
import sys #used to add system path
from jdcal import gcal2jd, jd2gcal
import datetime

sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)

from eslib.system.define_global_variables import *
from eslib.toolbox.reader.read_configuration_file import read_configuration_file

sPath_swat_python = sWorkspace_code + slash + 'python' + slash + 'swat' + slash + 'swat_python'
sys.path.append(sPath_swat_python)
from swat.shared import swat_global

pDate = datetime.datetime.today()
sDate_default = "{:04d}".format(pDate.year) + "{:02d}".format(pDate.month) + "{:02d}".format(pDate.day)

def swat_read_configuration_file(sFilename_configuration_in,\
     iCase_index_in=None, \
         sJob_in=None,\
          iFlag_mode_in=None, \
         aVariable_in = None, \
             aValue_in = None, \
                 sDate_in = None):
    config = read_configuration_file(sFilename_configuration_in)
    sModel = config['sModel']  
    sRegion = config['sRegion']

    
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
        iCase_index = 0
    sCase_index = "{:03d}".format(iCase_index)
    sCase = sModel + sDate + sCase_index
    if sJob_in is not None:
        sJob = sJob_in
    else:
        sJob = sCase
    
    swat_global.sCase = sCase
    swat_global.sJob = sJob
    swat_global.aVariable = aVariable
    swat_global.aValue = aValue
    swat_global.iFlag_mode = iFlag_mode

    swat_global.iFlag_cluster =  int( config['iFlag_cluster'])
    swat_global.iFlag_simulation =  int( config['iFlag_simulation'])
    swat_global.iFlag_pest_calibration  = int( config['iFlag_pest_calibration'])
    swat_global.iFlag_replace = int(config['iFlag_replace'])
    
    swat_global.iYear_start  = int( config['iYear_start'])
    swat_global.iMonth_start  = int(  config['iMonth_start'])
    swat_global.iDay_start  = int(  config['iDay_start'] )

    swat_global.iYear_end  = int( config['iYear_end'])
    swat_global.iMonth_end  = int(  config['iMonth_end'])
    swat_global.iDay_end  = int(  config['iDay_end'])

    swat_global.iYear_spinup_end  = int( config['iYear_spinup_end'])

    #swat_global.dResolution  = float( config['dResolution'])
    #by default, this system is used to prepare inputs for modflow simulation.
    #however, it can also be used to prepare gsflow simulation inputs.
    

    #based on global variable, a few variables are calculate once
    #calculate the modflow simulation period
    #https://docs.python.org/3/library/datetime.html#datetime-objects
    lJulian_start = gcal2jd(swat_global.iYear_start, swat_global.iMonth_start, swat_global.iDay_start)  #year, month, day
    lJulian_end = gcal2jd(swat_global.iYear_end, swat_global.iMonth_end, swat_global.iDay_end)  #year, month, day
    nstress =int( lJulian_end[1] - lJulian_start[1] + 1 )  
    swat_global.lJulian_start =   lJulian_start[1]
    swat_global.lJulian_end =  lJulian_end[1]
    swat_global.nstress =   nstress
    swat_global.nsegment  = int( config['nsegment'])
    swat_global.sJob = sJob
    
    #swat_global.nsteady =  int( config['nsteady'] )   
    #swat_global.ncolumn =  int( config['ncolumn'])
    #swat_global.nrow =  int( config['nrow'])
    #swat_global.nlayer =  int(config['nlayer'])

    sModel = config['sModel']
    sRegion = config['sRegion']
    sFilename_swat = config['sFilename_swat']
    swat_global.sModel = sModel
    swat_global.sRegion = sRegion
    swat_global.sFilename_swat= sFilename_swat
    
    #data
    sWorkspace_data_project = sWorkspace_data + slash + sModel + slash + sRegion
    #simulation
    sWorkspace_model = sWorkspace_models + slash + sModel
    sWorkspace_region = sWorkspace_model + slash + sRegion
    sWorkspace_simulation =  sWorkspace_region + slash + 'simulation'
    sWorkspace_simulation_case = sWorkspace_simulation + slash + sCase
    sWorkspace_simulation_copy = sWorkspace_simulation + slash + 'TxtInOut'

    swat_global.sWorkspace_data_project = sWorkspace_data_project

    swat_global.sWorkspace_simulation = sWorkspace_simulation
    swat_global.sWorkspace_simulation_case = sWorkspace_simulation_case    
    swat_global.sWorkspace_simulation_in = sWorkspace_simulation_case
    swat_global.sWorkspace_simulation_out = sWorkspace_simulation_case
    swat_global.sWorkspace_simulation_copy = sWorkspace_simulation_copy

    #swat_global.sFilename_elevation =  sWorkspace_data_project + slash + 'raster' + slash + 'elevation' + slash  \
    #    +  config['sFilename_elevation']
    #swat_global.sFilename_boundary =  sWorkspace_data_project + slash + 'raster' + slash + 'elevation' + slash  \
    #    + config['sFilename_boundary']
    #swat_global.sFilename_slope =  sWorkspace_data_project + slash + 'raster' + slash + 'elevation' + slash  \
    #    + config['sFilename_slope']
    #swat_global.sFilename_header_source =  sWorkspace_data_project + slash + 'raster' + slash + 'elevation' + slash  \
    #    + config['sFilename_header_source']
    #swat_global.sFilename_stream_segment = sWorkspace_data_project + slash + 'raster' + slash + 'hydrology' + slash  \
    #    + config['sFilename_stream_segment']
    #swat_global.sFilename_stream_order = sWorkspace_data_project + slash + 'raster' + slash + 'hydrology' + slash  \
    #    + config['sFilename_stream_order']
    #swat_global.sFilename_stream_buffer = sWorkspace_data_project + slash + 'raster' + slash + 'hydrology' + slash  \
    #    + config['sFilename_stream_buffer']
    #swat_global.sFilename_rock_type =  sWorkspace_data_project + slash + 'raster' + slash + 'geology' + slash \
    #    + config['sFilename_rock_type']
    #swat_global.sFilename_subbasin =  sWorkspace_data_project + slash + 'raster' + slash + 'hydrology' + slash  \
    #    +  config['sFilename_subbasin']
    
    swat_global.ncutoff = 200
    swat_global.nstep = 1
    return 1