import os,sys
from pathlib import Path
from os.path import realpath
import numpy as np
import argparse
import logging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time swaty simulation started.')


from swaty.auxiliary.text_reader_string import text_reader_string
from swaty.classes.swatpara import swatpara
from swaty.swaty_read_model_configuration_file import swaty_read_model_configuration_file
parser = argparse.ArgumentParser()

iFlag_standalone=1
iCase_index = 1
sDate='20220504'



sPath = realpath(str( Path().resolve() ))
#this is the temp path which has auxiliray data, not the SWAT input
sWorkspace_data = ( sPath +  '/data/arw' )  

#the actual path to input data
sWorkspace_input = str(Path(sWorkspace_data)  /  'input')

#to extract the parameter, we need to know the name of parameter for watershed, subbasin and hru, soil
aParameter=list()
aPara_in=dict()

aParemeter_watershed = np.array(['esco','ai0', 'sftmp','smtmp','timp','epco'])
nParameter_watershed = len(aParemeter_watershed)


for j in np.arange(1, nParameter_watershed+1):
    aPara_in['iParameter_type'] = 1
    aPara_in['iIndex_subbasin'] = j
    aPara_in['sName']= aParemeter_watershed[j-1]
    aPara_in['dValue_init']=0.0
    aPara_in['dValue_current']=0.01* j +0.01
    aPara_in['dValue_lower']=-1
    aPara_in['dValue_upper']=5
    pParameter = swatpara(aPara_in)
    aParameter.append(    pParameter )


aParemeter_subbasin = np.array(['ch_n2','ch_k2','plaps','tlaps'])
nParameter_subbasin = len(aParemeter_subbasin)
for j in np.arange(1, nParameter_subbasin+1):
    aPara_in['iParameter_type'] = 2
    aPara_in['iIndex_subbasin'] = j
    aPara_in['sName']= aParemeter_subbasin[j-1]
    aPara_in['dValue_init']=0.0
    aPara_in['dValue_current']=0.01* j +0.01
    aPara_in['dValue_lower']=-1
    aPara_in['dValue_upper']=5
    pParameter = swatpara(aPara_in)
    aParameter.append(pParameter)

aParemeter_hru = np.array(['cn2','rchrg_dp','gwqmn','gw_revap','revapmn','gw_delay','alpha_bf','ov_n'])
nParameter_hru = len(aParemeter_hru)
for j in np.arange(1, nParameter_hru+1):
    aPara_in['iParameter_type'] = 3
    aPara_in['iIndex_hru'] = j
    aPara_in['sName']= aParemeter_hru[j-1]
    aPara_in['dValue_init']=0.0
    aPara_in['dValue_current']=0.01* j +0.01
    aPara_in['dValue_lower']=-1
    aPara_in['dValue_upper']=5
    pParameter = swatpara(aPara_in)
    aParameter.append(pParameter)



aParemeter_soil = np.array(['sol_k','sol_awc','sol_alb','sol_bd'])
nParameter_soil = len(aParemeter_soil)
for j in np.arange(1, nParameter_soil+1):
    aPara_in['iParameter_type'] = 4
    aPara_in['lIndex_soil_layer'] = j
    aPara_in['sName']= aParemeter_soil[j-1]
    aPara_in['dValue_init']=0.0
    aPara_in['dValue_current']=0.01* j +0.01
    aPara_in['dValue_lower']=-1
    aPara_in['dValue_upper']=5
    pParameter = swatpara(aPara_in)
    aParameter.append(pParameter)



#the desired output workspace
sWorkspace_output = '/global/cscratch1/sd/liao313/04model/swat/arw/simulation'
#where is the swat binary is stored
sPath_bin = str(Path(sPath)  /  'bin')

sFilename_configuration_in = sPath +  '/tests/configurations/template.json'
oSwat = swaty_read_model_configuration_file(sFilename_configuration_in, \
    iFlag_read_discretization_in=1,\
    iFlag_standalone_in=iFlag_standalone,\
        iCase_index_in=iCase_index,\
        sDate_in=sDate, \
            sWorkspace_input_in=sWorkspace_input, \
                sWorkspace_output_in=sWorkspace_output)

#can change some members

print(oSwat.tojson())

#oSwat.extract_default_parameter_value(aParameter)
oSwat.generate_parameter_bounds()


print('Finished')