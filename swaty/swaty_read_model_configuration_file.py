
import os

import sys #used to add system path

import datetime
import json
import numpy as np
import pyearth.toolbox.date.julian as julian
from swaty.auxiliary.text_reader_string import text_reader_string
from swaty.classes.pycase import swatcase

pDate = datetime.datetime.today()
sDate_default = "{:04d}".format(pDate.year) + "{:02d}".format(pDate.month) + "{:02d}".format(pDate.day)

def swaty_read_model_configuration_file(sFilename_configuration_in , \
    iFlag_read_discretization_in = None,\
    iFlag_standalone_in=None, \
        iCase_index_in = None, sDate_in = None,\
        iYear_start_in = None,\
            iMonth_start_in = None,\
                iDay_start_in = None, \
        iYear_end_in = None,\
            iMonth_end_in = None,\
                iDay_end_in = None, \
          sWorkspace_input_in =None, \
              sWorkspace_output_in =None ,\
              aParameter_in=None  ):

    if not os.path.isfile(sFilename_configuration_in):
        print(sFilename_configuration_in + ' does not exist')
        return
    
    # Opening JSON file
    with open(sFilename_configuration_in) as json_file:
        aConfig = json.load(json_file)   

    sModel = aConfig['sModel'] 
    sRegion = aConfig['sRegion']

    if sWorkspace_input_in is not None:
        sWorkspace_input = sWorkspace_input_in
    else:
        sWorkspace_input = aConfig['sWorkspace_input']
        pass
    if sWorkspace_output_in is not None:
        sWorkspace_output = sWorkspace_output_in
    else:
        sWorkspace_output = aConfig['sWorkspace_output']
        pass

    if iFlag_read_discretization_in is not None:
        iFlag_read_discretization=1
    else:
        iFlag_read_discretization=0
        pass
    
    if iFlag_standalone_in is not None:        
        iFlag_standalone = iFlag_standalone_in
    else:       
        iFlag_standalone = int( aConfig['iFlag_standalone'])
    if sDate_in is not None:
        sDate = sDate_in
    else:
        sDate = aConfig['sDate']
        pass
    if iCase_index_in is not None:        
        iCase_index = iCase_index_in
    else:       
        iCase_index = int( aConfig['iCase_index'])
        
    
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

    if aParameter_in is not None:
        iFlag_paramter = 1
        aParameter = aParameter_in
    else:       
        iFlag_paramter = 0
        

    #by default, this system is used to prepare inputs for modflow simulation.
    #however, it can also be used to prepare gsflow simulation inputs.

    #based on global variable, a few variables are calculate once
    #calculate the modflow simulation period
    #https://docs.python.org/3/library/datetime.html#datetime-objects
    
    aConfig['iFlag_standalone'] = iFlag_standalone

    aConfig['iFlag_read_discretization'] = iFlag_read_discretization
    aConfig['iCase_index'] = iCase_index
    aConfig['sDate'] = sDate
    aConfig['sWorkspace_input'] = sWorkspace_input
    aConfig['sWorkspace_output'] = sWorkspace_output
    dummy1 = datetime.datetime(iYear_start, iMonth_start, iDay_start)
    dummy2 = datetime.datetime(iYear_end, iMonth_end, iDay_end)
    julian1 = julian.to_jd(dummy1, fmt='jd')
    julian2 = julian.to_jd(dummy2, fmt='jd')

    nstress =int( julian2 - julian1 + 1 )  
    aConfig['lJulian_start'] =  julian1
    aConfig['lJulian_end'] =  julian2
    aConfig['nstress'] =   nstress     
   
    sFilename_swat = aConfig['sFilename_swat']   
    
    #data
    oSwat = swatcase(aConfig)
    

    if iFlag_paramter ==1:
        #oSwat.nParameter_watershed = 0
        #oSwat.nParameter_subbasin = 0
        #oSwat.nParameter_hru = 0
        #oSwat.nParameter_soil = 0
        #oSwat.aParameter_watershed = list()
        #oSwat.aParameter_subbasin = list()
        #oSwat.aParameter_hru = list()
        #oSwat.aParameter_soil = list()
        for i in range(len(aParameter)):
            pParameter = aParameter[i]
            sName = pParameter.sName
            iType = pParameter.iParameter_type
            lIndex_subbasin = pParameter.lIndex_subbasin
            lIndex_hru = pParameter.lIndex_hru
            lIndex_soil_layer = pParameter.lIndex_soil_layer
            dValue = pParameter.dValue_current
            iFlag_found = 0
            if iType == 1:      
                          
                for j in range(oSwat.pWatershed.nParameter_watershed):
                    pPara = oSwat.pWatershed.aParameter_watershed[j]
                    sName1 = pPara.sName
                    if sName.lower() == sName1.lower():
                        #replace
                        oSwat.pWatershed.aParameter_watershed[j].dValue_current = dValue
                        iFlag_found = 1
                        break
                
                #if iFlag_found == 0:
                #    #this one is not in the list yet
                #    pass
                pass    
            else:
                if iType == 2: #subbasin level
                    #get name index
                                       
                    for j in np.arange(oSwat.nsubbasin ):
                        iIndex_name = oSwat.aSubbasin[j].aParameter_subbasin_name.index(sName) 
                        pPara = oSwat.aSubbasin[j].aParameter_subbasin[iIndex_name]
                        sName1 = pPara.sName
                        iIndex1 = pPara.lIndex_subbasin
                        if  lIndex_subbasin == iIndex1:
                            #replace
                            oSwat.aSubbasin[j].aParameter_subbasin[iIndex_name].dValue_current = dValue
                            iFlag_found = 1
                            break
                    pass
                else: #hru level
                    if iType == 3:
                        for j in np.arange(oSwat.nhru_combination ):
                            iIndex_name = oSwat.aHru_combination[j].aParameter_hru_name.index(sName) 
                            pPara = oSwat.aHru_combination[j].aParameter_hru[iIndex_name]
                            sName1 = pPara.sName
                            iIndex1 = pPara.lIndex_hru
                            if  lIndex_hru == iIndex1:
                                #replace
                                oSwat.aHru_combination[j].aParameter_hru[iIndex_name].dValue_current = dValue
                                iFlag_found = 1
                                break
                        pass
                    else: #soil layer
                        for j in np.arange(oSwat.nhru_combination ):
                            for k in np.arange(oSwat.aHru_combination[j].nSoil_layer):
                                iIndex_name = oSwat.aHru_combination[j].aSoil[k].aParameter_soil_name.index(sName) 
                                pPara = oSwat.aHru_combination[j].aSoil[k].aParameter_soil[iIndex_name]
                                sName1 = pPara.sName
                                iIndex0 = pPara.lIndex_hru
                                iIndex1 = pPara.lIndex_soil_layer
                                if lIndex_hru ==iIndex0 and  lIndex_soil_layer == iIndex1:
                                    #replace
                                    oSwat.aHru_combination[j].aSoil[k].aParameter_soil[iIndex_name].dValue_current = dValue
                                    iFlag_found = 1
                                    break
                        pass
                    pass #

            
        pass
    
    
    


   
    oSwat.sFilename_model_configuration = sFilename_configuration_in
    return oSwat