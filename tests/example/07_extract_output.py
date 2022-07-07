import os,sys
from pathlib import Path
from os.path import realpath
import numpy as np

import logging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time swaty simulation started.')


from swaty.auxiliary.text_reader_string import text_reader_string
from swaty.classes.swatpara import swatpara
from swaty.swaty_read_model_configuration_file import swaty_read_model_configuration_file


iFlag_standalone=1
iCase_index = 1
sDate='20220504'
iCase_index = 1
sDate = '20220615'

sPath = realpath(str( Path().resolve() ))
#this is the temp path which has auxiliray data, not the SWAT input
sWorkspace_data = ( sPath +  '/data/arw' )  

#the actual path to input data
sWorkspace_input = str(Path(sWorkspace_data)  /  'input')
sWorkspace_input = '/global/homes/l/liao313/workspace/python/pypest/data/arw/input'

#the desired output workspace
sWorkspace_output = '/global/cscratch1/sd/liao313/04model/pest/arw/calibration/pest20220615001/swat'
#where is the swat binary is stored
sPath_bin = str(Path(sPath)  /  'bin')

sFilename_configuration_in = sPath +  '/tests/configurations/template.json'
sFilename_configuration_in = '/global/homes/l/liao313/workspace/python/pypest/examples/swat/swat_new.json'
oSwat = swaty_read_model_configuration_file(sFilename_configuration_in, \
    iFlag_read_discretization_in=1,\
    iFlag_standalone_in=0,\
        iCase_index_in=iCase_index,\
        sDate_in=sDate, \
            sWorkspace_input_in=sWorkspace_input, \
                sWorkspace_output_in=sWorkspace_output)

#can change some members

print(oSwat.tojson())
oSwat.analyze()