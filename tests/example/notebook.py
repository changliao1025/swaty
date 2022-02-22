import os
from pathlib import Path
from os.path import realpath
from pyswat.classes.pycase import swatcase
from pyswat.pyswat_generate_template_configuration_json_file import pyswat_generate_template_configuration_json_file
from pyswat.pyswat_read_model_configuration_file import pyswat_read_model_configuration_file

iFlag_option = 1
if iFlag_option ==1:
    
    sPath = str(Path(__file__).parent.resolve())
    
    sFilename_configuration_in = realpath( sPath +  '/../configurations/template.json' )
    
    oPyswat = pyswat_generate_template_configuration_json_file(sFilename_configuration_in)
    print(oPyswat.tojson())
    #now you can customize the model object
    oPyswat.iCase_index = 1
    print(oPyswat.tojson())
else: 
    if iFlag_option == 2:
        #an example configuration file is provided with the repository, but you need to update this file based on your own case study
        #linux
        sPath = str(Path(__file__).parent.resolve())
        sFilename_configuration_in = sPath +  '/../tests/configurations/arw.json'
         
        print(sFilename_configuration_in)
        oPyswat = pyswat_read_model_configuration_file(sFilename_configuration_in)
        #print the case information in details
        print(oPyswat.tojson())

   
oPyswat.setup()
oPyswat.run()
oPyswat.evaluate()

print('Finished')