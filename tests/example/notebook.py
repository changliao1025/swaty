import sys
from pathlib import Path
from os.path import realpath
import argparse
import logging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time swaty simulation started.')
def is_module_available(module_name):
    if sys.version_info < (3, 0):
        # python 2
        import importlib
        torch_loader = importlib.find_loader(module_name)
    elif sys.version_info <= (3, 3):
        # python 3.0 to 3.3
        import pkgutil
        torch_loader = pkgutil.find_loader(module_name)
    elif sys.version_info >= (3, 4):
        # python 3.4 and above
        import importlib
        torch_loader = importlib.util.find_spec(module_name)

    return torch_loader is not None

iFlag = is_module_available('swaty')

from swaty.classes.pycase import swatcase
from swaty.swaty_generate_template_configuration_json_file import swaty_generate_template_configuration_json_file
from swaty.swaty_read_model_configuration_file import swaty_read_model_configuration_file
parser = argparse.ArgumentParser()
iFlag_option = 1
sPath = str( Path().resolve() )
if iFlag_option ==1:
    
    sFilename_configuration_in = realpath( sPath +  '/tests/configurations/template.json' ) 
    sWorkspace_data = realpath( sPath +  '/data/arw' )
    sWorkspace_input = realpath( sWorkspace_data +  '/input' )

    sWorkspace_output = realpath( sWorkspace_data +  '/output' )

    sPath_bin = realpath( sPath +  '/bin' )
    oSwat = swaty_generate_template_configuration_json_file(sFilename_configuration_in, sWorkspace_input,sWorkspace_output, sPath_bin)
    oSwat.iCase_index = 1
    print(oSwat.tojson())
else: 
    if iFlag_option == 2:
        #an example configuration file is provided with the repository, but you need to update this file based on your own case study
        #linux
        
        sFilename_configuration_in = sPath +  '/tests/configurations/arw.json'
     
        oSwat = swaty_read_model_configuration_file(sFilename_configuration_in)
        
        print(oSwat.tojson())


oSwat.setup()
oSwat.run()
oSwat.analyze()
oSwat.evaluate()

print('Finished')