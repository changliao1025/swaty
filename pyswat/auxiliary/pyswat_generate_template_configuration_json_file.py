import os, sys
#use this function to generate an initial json file for hexwatershed
import json
#once it's generated, you can modify it and use it for different simulations
from pyswat.classes.pycase import swatcase
import numpy as np
def pyswat_generate_template_configuration_json_file(sFilename_json):
   
    if os.path.exists(sFilename_json):         
        os.remove(sFilename_json)

 
    #use a dict to initialize the class
    aConfig = {}
    aConfig['iFlag_flowline'] = 1
    aConfig['iFlag_merge_reach'] = 1
    
    aConfig['iFlag_resample_method'] = 2
    aConfig['lCellID_outlet'] = -1
    aConfig['sFilename_model_configuration']  = sFilename_json

    aConfig['sWorkspace_data'] = '/people/liao313/data'
    aConfig['sWorkspace_scratch'] = '/compyfs/liao313/'
    aConfig['sWorkspace_project'] = '/pyhexwatershed/susquehanna'
    aConfig['sWorkspace_bin'] = '/people/liao313/bin'
    aConfig['sRegion'] = 'susquehanna'
    aConfig['sModel'] = 'pyhexwatershed'

    aConfig['iCase_index'] = 3
    aConfig['sMesh_type'] = 'mpas'

    aConfig['sDate']= '20210713'

    aConfig['sFilename_mesh'] = 'mpas.shp'
    
    aConfig['flowline_info'] = 'flowline_info.json'
    aConfig['sFilename_mesh_info'] = 'mesh_info.json'
    aConfig['sFilename_elevation']  = 'elevation.shp'

    aConfig['sFilename_dem']  = '/qfs/people/liao313/data/hexwatershed/susquehanna/raster/dem/dem_ext.tif'

    aConfig['sFilename_pystream_config'] = '/qfs/people/liao313/workspace/python/pyflowline/pyflowline/config/pystream_susquehanna_mpas.xml'

    aConfig['sFilename_spatial_reference'] = '/qfs/people/liao313/data/hexwatershed/susquehanna/vector/hydrology/boundary_proj.shp'
    

    oModel = swatcase(aConfig)
    
    oModel.export_to_json(sFilename_json)

    return
