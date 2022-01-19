import os
from pathlib import Path
from pyswat.classes.pycase import swatcase
from pyswat.pyswat_read_model_configuration_file import pyswat_read_model_configuration_file

iFlag_option = 2
if iFlag_option ==1:
    oPyswat=swatcase()
    oPyswat.iCase_index = 1
else: 
    if iFlag_option == 2:
        #an example configuration file is provided with the repository, but you need to update this file based on your own case study
        #linux
        sFilename_configuration_in = str(Path.cwd()) +  '/configurations/pyswat_susquehanna_hexagon.json' 
        print(sFilename_configuration_in)
        oPyswat = pyswat_read_model_configuration_file(sFilename_configuration_in)
        #print the case information in details
        print(oPyswat.tojson())

   
oPyswat.setup()
oPyswat.run()
oPyswat.evaluate()





print('Finished')