import sys
from pathlib import Path
from os.path import realpath
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
aPara_in['iParameter_type'] = 1
aPara_in['sName']= 'SFTMP'
aPara_in['dValue_init']=0.0
aPara_in['dValue_current']=0.1
aPara_in['dValue_lower']=-1
aPara_in['dValue_upper']=5
pParameter_watershed = swatpara(aPara_in)
aParameter.append(pParameter_watershed)

aPara_in['iParameter_type'] = 1
aPara_in['sName']= 'SMTMP'
aPara_in['dValue_init']=0.0
aPara_in['dValue_current']=0.2
aPara_in['dValue_lower']=-1
aPara_in['dValue_upper']=5
pParameter_watershed = swatpara(aPara_in)
aParameter.append(pParameter_watershed)

aPara_in['iParameter_type'] = 1
aPara_in['sName']= 'ESCO'
aPara_in['dValue_init']=0.0
aPara_in['dValue_current']=0.3
aPara_in['dValue_lower']=-1
aPara_in['dValue_upper']=5
pParameter_watershed = swatpara(aPara_in)
aParameter.append(pParameter_watershed)

aPara_in['iParameter_type'] = 1
aPara_in['sName']= 'SMFMX'
aPara_in['dValue_init']=0.0
aPara_in['dValue_current']=0.4
aPara_in['dValue_lower']=-1
aPara_in['dValue_upper']=5
pParameter_watershed = swatpara(aPara_in)
aParameter.append(pParameter_watershed)

aPara_in['iParameter_type'] = 1
aPara_in['sName']= 'TIMP'
aPara_in['dValue_init']=0.0
aPara_in['dValue_current']=0.5
aPara_in['dValue_lower']=-1
aPara_in['dValue_upper']=5
pParameter_watershed = swatpara(aPara_in)
aParameter.append(pParameter_watershed)

aPara_in['iParameter_type'] = 1
aPara_in['sName']= 'EPCO'
aPara_in['dValue_init']=0.0
aPara_in['dValue_current']=0.6
aPara_in['dValue_lower']=-1
aPara_in['dValue_upper']=5
pParameter_watershed = swatpara(aPara_in)
aParameter.append(pParameter_watershed)




sPath = realpath(str( Path().resolve() ))
#this is the temp path which has auxiliray data, not the SWAT input
sWorkspace_data = ( sPath +  '/data/arw' )  

#the actual path to input data
sWorkspace_input = str(Path(sWorkspace_data)  /  'input')
#the desired output workspace
sWorkspace_output = '/global/cscratch1/sd/liao313/04model/swat/arw/simulation'
#where is the swat binary is stored
sPath_bin = str(Path(sPath)  /  'bin')

sFilename_configuration_in = sPath +  '/tests/configurations/arw.json'
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