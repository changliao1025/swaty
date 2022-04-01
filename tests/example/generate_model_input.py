import sys
from pathlib import Path
from os.path import realpath
import numpy as np
import argparse
import logging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time swaty simulation started.')


from swaty.classes.swatpara import swatpara
from swaty.swaty_read_model_configuration_file import swaty_read_model_configuration_file
parser = argparse.ArgumentParser()

iFlag_standalone=1
iCase_index = 2
sDate='20220320'

pArgs = parser.parse_args()
if len(sys.argv)> 1:
    iFlag_standalone= pArgs.iFlag_standalone
    iCase_index = pArgs.iCase_index
    sDate = pArgs.sDate
else:
    print(len(sys.argv), 'Missing arguments')
    pass

#set up a parameter
aParameter = list()
aPara_in={}

nsubbasin = 87
nParameter_subbasin=1

#for i in np.arange(nParameter_subbasin):
#    for j in np.arange(1, nsubbasin+1):
#        aPara_in['iParameter_type'] = 2
#        aPara_in['iIndex'] = j
#        aPara_in['sName']= 'CH_K2'
#        aPara_in['dValue_init']=0.0
#        aPara_in['dValue_current']=0.01* j +0.01
#        aPara_in['dValue_lower']=-1
#        aPara_in['dValue_upper']=5
#        pParameter_subbasin = swatpara(aPara_in)
#        aParameter.append(pParameter_subbasin)

nParameter_hru=1
nhru = 2231
for i in range(nParameter_hru):
    for j in np.range(1, nhru):
        aPara_in['iParameter_type'] = 3
        aPara_in['iIndex'] = j
        aPara_in['sName']= 'CN2'
        aPara_in['dValue_init']=0.0
        aPara_in['dValue_current']=0.6
        aPara_in['dValue_lower']=-1
        aPara_in['dValue_upper']=5
        pParameter_hru = swatpara(aPara_in)
        aParameter.append(pParameter_hru)

nsoil_layer = 1
for i in range(nParameter_hru):
    for j in np.range(1, nhru):
        for k in np.arange(1, nsoil_layer+1):
            aPara_in['iParameter_type'] = 3
            aPara_in['iIndex'] = j
            aPara_in['iSoil_layer'] = k
            aPara_in['sName']= 'SOL_ALB'
            aPara_in['dValue_init']=0.0
            aPara_in['dValue_current']=0.6
            aPara_in['dValue_lower']=-1
            aPara_in['dValue_upper']=5
            pParameter_soil = swatpara(aPara_in)
            aParameter.append(pParameter_soil)



sPath = realpath(str( Path().resolve() ))
#this is the temp path which has auxiliray data, not the SWAT input
sWorkspace_data = ( sPath +  '/data/arw' )  

#the actual path to input data
sWorkspace_input = str(Path(sWorkspace_data)  /  'input')
#the desired output workspace
sWorkspace_output = '/global/cscratch1/sd/liao313/04model/swat/arw/simulation'
#where is the swat binary is stored
sPath_bin = str(Path(sPath)  /  'bin')

sFilename_configuration_in = sPath +  '/tests/configurations/template.json'
oSwat = swaty_read_model_configuration_file(sFilename_configuration_in, \
    iFlag_standalone_in=iFlag_standalone,\
        iCase_index_in=iCase_index,\
        sDate_in=sDate, \
            sWorkspace_input_in=sWorkspace_input, \
                sWorkspace_output_in=sWorkspace_output,\
                    aParameter_in = aParameter)

#can change some members

print(oSwat.tojson())

oSwat.setup()


print('Finished')