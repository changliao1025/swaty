import os, sys
from pathlib import Path
from os.path import realpath
#use this function to generate an initial json file for hexwatershed
import json
#once it's generated, you can modify it and use it for different simulations
from swaty.classes.pycase import swatcase
#from swaty.classes.basin import pybasin

from swaty.classes.swatpara import swatpara
from swaty.classes.watershed import pywatershed
from swaty.classes.subbasin import pysubbasin
from swaty.classes.hru import pyhru
from swaty.classes.soil import pysoil

def swaty_create_template_configuration_file(sFilename_json,sPath_bin, sWorkspace_input, sWorkspace_output,  \
    iFlag_standalone_in=None, iCase_index_in = None, \
        iFlag_read_discretization_in=None,\
        sDate_in = None, aParameter_in = None):
    if iCase_index_in is not None:        
        iCase_index = iCase_index_in
    else:       
        iCase_index = 1
    
    if iFlag_standalone_in is not None:        
        iFlag_standalone = iFlag_standalone_in
    else:       
        iFlag_standalone = 1
    if iFlag_read_discretization_in is not None:        
        iFlag_read_discretization = iFlag_read_discretization_in
    else:       
        iFlag_read_discretization = 1
    if sDate_in is not None:
        sDate = sDate_in
    else:
        sDate = '20220202'
        pass

    if iFlag_standalone ==1:
        iFlag_simulation =1
        iFlag_calibration =0 
    else:
        iFlag_simulation =0
        iFlag_calibration =1
        
    #use a dict to initialize the class
    aConfig = {}
    aConfig['iFlag_run'] = 1
    aConfig['iFlag_standalone']=iFlag_standalone
    
    aConfig['iFlag_simulation'] = iFlag_simulation
    aConfig['iFlag_calibration'] = iFlag_calibration
    
    aConfig['iFlag_watershed'] = 1  
    aConfig['iFlag_subbasin'] = 1
    aConfig['iFlag_hru'] = 1
    aConfig['iFlag_soil'] = 1

    aConfig['iFlag_mode'] = 1 
    aConfig['iFlag_replace_parameter'] = 1  
        
    #the python bin on your system
    aConfig['sPython']  = '/global/homes/l/liao313/.conda/envs/swatenv/bin/python'
    
    aConfig['sWorkspace_bin'] = sPath_bin 
 
 
    aConfig['sWorkspace_input'] = sWorkspace_input  

    aConfig['sWorkspace_output'] = sWorkspace_output  
    
    aConfig['sRegion'] = 'arw'
    aConfig['sModel'] = 'swat'
    aConfig['sDate'] = sDate
    aConfig['sJob'] = 'swat'
    aConfig['iCase_index'] = iCase_index
    aConfig['iYear_start'] = 1997
    aConfig['iYear_end'] = 2009
    aConfig['iMonth_start'] = 1
    aConfig['iMonth_end'] = 12
    aConfig['iDay_start'] = 1
    aConfig['iDay_end'] = 31
   
    aConfig['nsegment'] = 87
    aConfig['nsubbasin']= 87
    aConfig['nhru']= 2231
    aConfig['sFilename_swat'] = 'swat670'
  
    aConfig['sFilename_observation_discharge'] = 'obs.flow_am.csv'
    aConfig['sWorkspace_simulation_copy'] = '/global/cscratch1/sd/liao313/04model/swat/arw/simulation/TxtInOut/'
    aConfig['sFilename_LandUseSoilsReport'] = 'LandUseSoilsReport.txt'
    aConfig['sFilename_HRULandUseSoilsReport'] = 'HRULandUseSoilsReport.txt'
    
    aConfig['sFilename_hru_combination'] = 'hru_combination.txt'
    aConfig['sFilename_hru_info'] = 'hru_info.txt'
    aConfig['sFilename_watershed_configuration'] = 'watershed_configuration.txt'
    
    oSwat = swatcase(aConfig, iFlag_read_discretization_in=0)

    if aParameter_in is not None:
        aParameter = aParameter_in
        oSwat.pWatershed.nParameter_watershed = 0
        oSwat.nParameter_watershed = 0
        oSwat.nParameter_subbasin=0
        oSwat.nParameter_hru=0
        oSwat.nParameter_soil=0
        oSwat.aParameter_watershed_name=list()
        oSwat.aParameter_subbasin_name=list()
        oSwat.aParameter_hru_name=list()
        oSwat.aParameter_soil_name=list()
        for i in range(len(aParameter)):
            pParameter = aParameter[i]
            sName = pParameter.sName
            iType = pParameter.iParameter_type
            
            iFlag_found = 0
            if iType == 1:   
                if sName.lower() in oSwat.aParameter_watershed_name:
                    pass
                else:
                    oSwat.aParameter_watershed_name.append(sName.lower())
                    oSwat.pWatershed.nParameter_watershed = oSwat.pWatershed.nParameter_watershed + 1      
                    oSwat.nParameter_watershed  =        oSwat.nParameter_watershed+ 1     
                    pass               
                  
            else:
                if iType == 2: #subbasin level
                    #get name index                                         
                    if sName.lower() in oSwat.aParameter_subbasin_name:
                        pass                       
                    else:
                        oSwat.aParameter_subbasin_name.append(sName.lower())
                        oSwat.nParameter_subbasin = oSwat.nParameter_subbasin + 1
                    
                else: #hru level
                    if iType == 3:           
                        if sName.lower() in oSwat.aParameter_hru_name:
                            pass
                        else:
                            oSwat.aParameter_hru_name.append(sName.lower())
                            oSwat.nParameter_hru = oSwat.nParameter_hru + 1   
                            
                    else: #soil layer
                        
                        
                        if sName.lower() in oSwat.aParameter_soil_name:
                            pass
                        else:
                            oSwat.aParameter_soil_name.append(sName.lower())
                            oSwat.nParameter_soil = oSwat.nParameter_soil + 1  
                                
                        pass
                    pass #

        
    else:
        aParameter_watershed=list()
        aParameter_watershed_name=list()
        nParameter_watershed=1
        aName=['SFTMP']
        aValue_lower=[-5]
        aValue_upper=[5]
        aValue_init=[1]
        for iPara in range(nParameter_watershed):
            aPara_in = {}
            aPara_in['iParameter_type']=1
            aPara_in['sName']=aName[iPara].lower()
            aPara_in['dValue_init']=aValue_init[iPara]
            aPara_in['dValue_lower']=aValue_lower[iPara]
            aPara_in['dValue_upper']=aValue_upper[iPara]
            pPara_watershed = swatpara(aPara_in)
            aParameter_watershed.append(pPara_watershed)
            aParameter_watershed_name.append(aName[iPara].lower())

        oSwat.pWatershed.aParameter_watershed=aParameter_watershed
        oSwat.pWatershed.nParameter_watershed = len(aParameter_watershed)
        oSwat.nParameter_watershed = len(aParameter_watershed)

        aName=['CH_K2']
        aValue_lower=[-5]
        aValue_upper=[5]
        aValue_init=[1]
        aParameter_subbasin=list()
        aParameter_subbasin_name=list()
        nParameter_subbasin=1
        for iPara in range(nParameter_subbasin):
            aPara_in = {}
            aPara_in['iParameter_type']=2
            aPara_in['sName']=aName[iPara].lower()
            aPara_in['dValue_init']=aValue_init[iPara]
            aPara_in['dValue_lower']=aValue_lower[iPara]
            aPara_in['dValue_upper']=aValue_upper[iPara]
            pPara_subbasin = swatpara(aPara_in)
            aParameter_subbasin.append(pPara_subbasin)
            aParameter_subbasin_name.append(aName[iPara].lower())

        pdummy = pysubbasin()    
        pdummy.setup_parameter2(aPara_in = aParameter_subbasin)
        pdummy.lIndex = 1
        oSwat.aSubbasin.append(pdummy)
        oSwat.nParameter_subbasin = len(aParameter_subbasin)

        aName=['CN2']
        aValue_lower=[-5]
        aValue_upper=[5]
        aValue_init=[1]
        aParameter_hru=list()
        aParameter_hru_name=list()
        nParameter_hru=1
        for iPara in range(nParameter_hru):
            aPara_in = {}
            aPara_in['iParameter_type']=3
            aPara_in['sName']=aName[iPara].lower()
            aPara_in['dValue_init']=aValue_init[iPara]
            aPara_in['dValue_lower']=aValue_lower[iPara]
            aPara_in['dValue_upper']=aValue_upper[iPara]
            pPara_hru = swatpara(aPara_in)
            aParameter_hru.append(pPara_hru)
            aParameter_hru_name.append(aName[iPara].lower())

        
        aName=['SOL_ALB']
        aValue_lower=[-5]
        aValue_upper=[5]
        aValue_init=[1]
        aParameter_soil=list()
        aParameter_soil_name=list()
        nParameter_soil=1
        for iPara in range(nParameter_soil):
            aPara_in = {}
            aPara_in['iParameter_type']=3
            aPara_in['sName']=aName[iPara].lower()
            aPara_in['dValue_init']=aValue_init[iPara]
            aPara_in['dValue_lower']=aValue_lower[iPara]
            aPara_in['dValue_upper']=aValue_upper[iPara]
            pPara_soil = swatpara(aPara_in)
            aParameter_soil.append(pPara_soil)
            aParameter_soil_name.append(aName[iPara].lower())

        dummy_hru = pyhru()
        dummy_hru.setup_parameter2(aPara_in = aParameter_hru)

        dummy_soil = pysoil()        
        dummy_soil.setup_parameter2(aPara_in = aParameter_soil)
        dummy_hru.aSoil=list()
        dummy_hru.aSoil.append(dummy_soil)  

        oSwat.aHru_combination=list()
        oSwat.aHru_combination.append(dummy_hru)        
        oSwat.nParameter_soil = len(aParameter_soil)
        oSwat.nParameter_hru = len(aParameter_hru)
        oSwat.aParameter_watershed_name = aParameter_watershed_name
        oSwat.aParameter_subbasin_name = aParameter_subbasin_name
        oSwat.aParameter_hru_name = aParameter_hru_name
        oSwat.aParameter_soil_name = aParameter_soil_name

    oSwat.sFilename_model_configuration = sFilename_json

    oSwat.export_config_to_json(sFilename_json)
    return oSwat