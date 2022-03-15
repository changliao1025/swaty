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

parser = argparse.ArgumentParser()
iFlag_option = 1
sPath = str( Path().resolve() )
sWorkspace_data = realpath( sPath +  '/data/arw' )
sWorkspace_input = realpath( sWorkspace_data +  '/input' )
sWorkspace_output = '/global/cscratch1/sd/liao313/04model/swat/arw/simulation'
sPath_bin = realpath( sPath +  '/bin' )

sFilename_configuration_in = realpath( sPath +  '/tests/configurations/template.json' ) 
oSwat = swaty_generate_template_configuration_file(sFilename_configuration_in, sWorkspace_input,sWorkspace_output, sPath_bin, iFlag_standalone_in=1, iCase_index_in=3, sDate_in='20220308')
print(oSwat.tojson())


