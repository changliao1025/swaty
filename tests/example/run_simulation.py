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
iFlag_option = 1
sPath = str( Path().resolve() )
sWorkspace_data = realpath( sPath +  '/data/arw' )
sWorkspace_input = realpath( sWorkspace_data +  '/input' )
sWorkspace_output = '/global/cscratch1/sd/liao313/04model/swat/arw/simulation'
sPath_bin = realpath( sPath +  '/bin' )

sFilename_configuration_in = sPath +  '/tests/configurations/arw.json'
oSwat = swaty_read_model_configuration_file(sFilename_configuration_in, iFlag_standalone_in=1,iCase_index_in=2,sDate_in='20220308', sWorkspace_input_in=sWorkspace_input, sWorkspace_output_in=sWorkspace_output)
print(oSwat.tojson())

oSwat.setup()
oSwat.run()
oSwat.analyze()
oSwat.evaluate()

print('Finished')