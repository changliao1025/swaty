import sys
from pathlib import Path
from os.path import realpath
import argparse
import logging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time swaty simulation started.')

from swaty.classes.pycase import swatcase

from swaty.swaty_read_model_configuration_file import swaty_read_model_configuration_file
parser = argparse.ArgumentParser()
parser.add_argument("--iCase_index", help = "iCase_index",  type = int)
parser.add_argument("--iFlag_standalone", help = "iFlag_standalone",  type = int)
parser.add_argument("--sDate", help = "sDate",  type = str)

###========================
# the default setting
###========================
iFlag_standalone=1
iCase_index = 1
sDate='20220320'

pArgs = parser.parse_args()
if len(sys.argv)> 1:
    iFlag_standalone= pArgs.iFlag_standalone
    iCase_index = pArgs.iCase_index
    sDate = pArgs.sDate
else:
    print(len(sys.argv), 'Missing arguments')
    pass

sPath = realpath(str( Path().resolve() ))
#this is the temp path which has auxiliray data, not the SWAT input
sWorkspace_data = ( sPath +  '/data/arw' )  

#the actual path to input data
sWorkspace_input = str(Path(sWorkspace_data)  /  'input')
#the desired output workspace
sWorkspace_output = '/global/cscratch1/sd/liao313/04model/swat/arw/simulation'
#where is the swat binary is stored
sPath_bin = str(Path(sPath)  /  'bin')


#path to the configuration file
sFilename_configuration_in = sPath +  '/tests/configurations/arw.json'


oSwat = swaty_read_model_configuration_file(sFilename_configuration_in, iFlag_standalone_in=iFlag_standalone,iCase_index_in=iCase_index, sDate_in=sDate, sWorkspace_input_in=sWorkspace_input, sWorkspace_output_in=sWorkspace_output)

#print configure again
print(oSwat.tojson())

#oSwat.setup()
#oSwat.run()
oSwat.analyze()
oSwat.evaluate()

print('Finished')