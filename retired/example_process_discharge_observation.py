from pyswat.simulation.swat_main import swat_main

from pyswat.pyswat_read_model_configuration_file import swat_read_model_configuration_file
from pyswat.classes.pycase import pyswat
from pyswat.preprocess.auxiliary.swat_prepare_observation_discharge_file import swat_prepare_observation_discharge_file
sFilename_configuration_in = '/global/homes/l/liao313/workspace/python/pyswat/pyswat/shared/swat_simulation.xml'
#step 1
aConfig = swat_read_model_configuration_file(sFilename_configuration_in)
   
# iCase_index_in=iCase_index_in, sJob_in=sJob_in, iFlag_mode_in=iFlag_mode_in)
aConfig['sFilename_model_configuration'] = sFilename_configuration_in
oModel = pyswat(aConfig)
swat_prepare_observation_discharge_file(oModel)