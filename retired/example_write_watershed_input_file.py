

from pyswat.pyswat_read_model_configuration_file import swat_read_model_configuration_file
from pyswat.classes.pycase import pyswat
from pyswat.scenarios.swat_write_watershed_input_file    import swat_write_watershed_input_file
sFilename_configuration_in = '/global/homes/l/liao313/workspace/python/pyswat/pyswat/shared/swat_simulation.xml'
#step 1
aConfig = swat_read_model_configuration_file(sFilename_configuration_in)
   
# iCase_index_in=iCase_index_in, sJob_in=sJob_in, iFlag_mode_in=iFlag_mode_in)
aConfig['sFilename_model_configuration'] = sFilename_configuration_in
oModel = pyswat(aConfig)
swat_write_watershed_input_file(oModel)