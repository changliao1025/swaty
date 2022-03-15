import sys
from pathlib import Path
from os.path import realpath
import argparse
import logging
import numpy as np 
import ray
ray.init()

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time swaty simulation started.')
from swaty.classes.swatpara import swatpara
from swaty.swaty_read_model_configuration_file import swaty_read_model_configuration_file
from swaty.auxiliary.text_reader_string import text_reader_string
parser = argparse.ArgumentParser()

sFilename_para = '/global/u1/l/liao313/data/swat/arw/auxiliary/parameter_ensemble_SWAT_25_46000real.csv'
aParameter_dummy = text_reader_string(sFilename_para, iSkipline_in= 1, cDelimiter_in=',')
aSFTMP = np.array(aParameter_dummy[:, 14] ).astype(float)

aSMTMP= np.array(aParameter_dummy[:, 15] ).astype(float)
 

nEnsemble = len(aSFTMP)
#read excel file for parameter list

sPath = str( Path().resolve() )
sWorkspace_data = realpath( sPath +  '/data/arw' )
sWorkspace_input = realpath( sWorkspace_data +  '/input' )
sWorkspace_output = '/global/cscratch1/sd/liao313/04model/swat/arw/simulation'
sPath_bin = realpath( sPath +  '/bin' )

sFilename_configuration_in = sPath +  '/tests/configurations/arw.json'

#for i in range(20):

@ray.remote
def generate_model_input(i):
    aParameter = list()
    aPara_in={}

    aPara_in['iParameter_type'] = 1
    aPara_in['sName'] = 'SFTMP'
    aPara_in['dValue_init']=0.0
    aPara_in['dValue_current']=aSFTMP[i]
    aPara_in['dValue_lower']=-1
    aPara_in['dValue_upper']=5
    pParameter_watershed = swatpara(aPara_in)    
    aParameter.append(pParameter_watershed)

    aPara_in['sName'] = 'SMTMP'
    aPara_in['dValue_init']=0.0
    aPara_in['dValue_current']=aSMTMP[i]
    aPara_in['dValue_lower']=-1
    aPara_in['dValue_upper']=5
    pParameter_watershed = swatpara(aPara_in)    
    aParameter.append(pParameter_watershed)

    oSwat = swaty_read_model_configuration_file(sFilename_configuration_in, \
        iFlag_standalone_in=1,\
            iCase_index_in= i+1 ,\
                sDate_in='20220314', \
            sWorkspace_input_in=sWorkspace_input, \
                sWorkspace_output_in=sWorkspace_output,\
            aParameter_in = aParameter)

    oSwat.setup()

futures = [generate_model_input.remote(i) for i in range(10)]
print(ray.get(futures))

print('Finished')