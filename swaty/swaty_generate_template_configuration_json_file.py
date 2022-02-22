import os, sys
from pathlib import Path
from os.path import realpath
#use this function to generate an initial json file for hexwatershed
import json
#once it's generated, you can modify it and use it for different simulations
from swaty.classes.pycase import swatcase
#from swaty.classes.basin import pybasin
#from swaty.classes.basin import pybasin
from swaty.classes.swatpara import swatpara
sPath = str(Path(__file__).parent.resolve())
sPath_data = realpath(sPath +  '/../data/arw/' )
sPath_bin = realpath(sPath +  '/../bin/' )
def swaty_generate_template_configuration_json_file(sFilename_json):
    #use a dict to initialize the class
    aConfig = {}
    aConfig['iFlag_simulation'] = 1
    aConfig['iFlag_calibration'] = 0
    
    aConfig['iFlag_watershed'] = 1   
    aConfig['iFlag_subbasin'] = 0
    aConfig['iFlag_hru'] = 0

    aConfig['iFlag_mode'] = 1 
    aConfig['iFlag_replace_parameter'] = 1 
    
    
    
    #the python bin on your system
    aConfig['sPython']  = '/global/homes/l/liao313/.conda/envs/swatenv/bin/python'
    #aConfig['sWorkspace_home'] = '/global/homes/l/liao313'

    aConfig['sWorkspace_bin'] = sPath_bin 
    #'/global/homes/l/liao313/bin'
 
    aConfig['sWorkspace_data'] = sPath_data
    #'/global/homes/l/liao313/data'
    aConfig['sWorkspace_project'] = '/swat/arw'
    #some output path, should not be within this repository
    aConfig['sWorkspace_scratch'] = '/global/homes/l/liao313/'
    aConfig['sWorkspace_simulation'] = '/global/homes/l/liao313/04model/swat/arw/simulation'
    aConfig['sWorkspace_calibration'] = '/global/homes/l/liao313/04model/swat/arw/calibration'
    aConfig['sRegion'] = 'arw'
    aConfig['sModel'] = 'swat'
    aConfig['sDate'] = '20210902'
    aConfig['sJob'] = 'swat'

    aConfig['iCase_index'] = 1

    aConfig['iYear_start'] = 1997
    aConfig['iYear_end'] = 2009
    aConfig['iMonth_start'] = 1
    aConfig['iMonth_end'] = 12
    aConfig['iDay_start'] = 1
    aConfig['iDay_end'] = 31
   
    aConfig['nsegment'] = 5
    aConfig['nsubbasin']= 5
    aConfig['sFilename_swat'] = 'swat670'
  
    aConfig['sFilename_observation_discharge'] = 'obs.flow_am.csv'
    aConfig['sWorkspace_simulation_copy'] = 'TxtInOut.tar'
    #'/global/homes/l/liao313/04model/swat/arw'

    aConfig['sFilename_hru_combination'] = 'hru_combination.txt'
    aConfig['sFilename_hru_info'] = 'hru_info.txt'
    aConfig['sFilename_watershed_configuration'] = 'watershed_configuration.txt'
    

    oModel = swatcase(aConfig)

    aParameter_watershed=list()
    nParameter_watershed=2
    aName=['SFTMP','SMTMP']
    aValue_init=[0.5,1.0]
    aValue_lower=[-5,-5]
    aValue_upper=[5,5]
    for iPara in range(nParameter_watershed):
        aPara_in = {}
        aPara_in['iParameter_type']=1
        aPara_in['sName']=aName[iPara]
        aPara_in['dValue_init']=aValue_init[iPara]
        aPara_in['dValue_lower']=aValue_lower[iPara]
        aPara_in['dValue_upper']=aValue_upper[iPara]
        pPara_watershed = swatpara(aPara_in)
        aParameter_watershed.append(pPara_watershed)

    oModel.aParameter_watershed=aParameter_watershed
    oModel.nParameter_watershed = len(aParameter_watershed)

    aParameter_subbasin=list()
    nParameter_subbasin=0
    for iPara in range(nParameter_subbasin):
        aPara_in = {}
        aPara_in['iParameter_type']=2
        pPara_subbasin = swatpara(aPara_in)
        aParameter_subbasin.append(pPara_subbasin)

    oModel.aParameter_subbasin=aParameter_subbasin
    oModel.nParameter_subbasin = len(aParameter_subbasin)

    aParameter_hru=list()
    nParameter_hru=0
    for iPara in range(nParameter_hru):
        aPara_in = {}
        aPara_in['iParameter_type']=3
        pPara_hru = swatpara(aPara_in)
        aParameter_hru.append(pPara_hru)

    oModel.aParameter_hru=aParameter_hru
    oModel.nParameter_hru = len(aParameter_hru)

    oModel.export_config_to_json(sFilename_json)
    return oModel