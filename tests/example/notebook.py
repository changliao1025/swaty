import os
from pathlib import Path
from os.path import realpath
from swaty.classes.pycase import swatcase
from swaty.swaty_generate_template_configuration_json_file import swaty_generate_template_configuration_json_file
from swaty.swaty_read_model_configuration_file import swaty_read_model_configuration_file

iFlag_option = 1
if iFlag_option ==1:
    
    sPath = str(Path(__file__).parent.resolve())
    
    sFilename_configuration_in = realpath( sPath +  '/../configurations/template.json' )
    
    oswaty = swaty_generate_template_configuration_json_file(sFilename_configuration_in)
    print(oswaty.tojson())
    #now you can customize the model object
    oswaty.iCase_index = 1
    print(oswaty.tojson())
else: 
    if iFlag_option == 2:
        #an example configuration file is provided with the repository, but you need to update this file based on your own case study
        #linux
        sPath = str(Path(__file__).parent.resolve())
        sFilename_configuration_in = sPath +  '/../tests/configurations/arw.json'
         
        print(sFilename_configuration_in)
        oswaty = swaty_read_model_configuration_file(sFilename_configuration_in)
        #print the case information in details
        print(oswaty.tojson())

   
oswaty.setup()
oswaty.run()
oswaty.evaluate()

print('Finished')