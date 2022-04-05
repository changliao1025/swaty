import sys
from pathlib import Path
from os.path import realpath
import argparse
import logging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time swaty simulation started.')

from swaty.swaty_generate_template_configuration_file import swaty_generate_template_configuration_file

#used the parser if you want to run this script from the command line 
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

#where do you want to save the configuration file
sFilename_configuration_in = sPath +  '/tests/configurations/template.json'

#the module to generate a confiug file
oSwat = swaty_generate_template_configuration_file(sFilename_configuration_in, \
    sWorkspace_input, \
        sWorkspace_output, sPath_bin, \
            iFlag_standalone_in=iFlag_standalone, iCase_index_in=iCase_index, sDate_in=sDate)




#print the object to check

print(oSwat.tojson())
#after you generate this config, remember to edit it so you can actually use it for simulation

print('Finished')

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time Pyflowline simulation finished.')


