from swaty.simulation.swat_main import swat_main

from swaty.swaty_read_model_configuration_file import swat_read_model_configuration_file
from swaty.classes.pycase import swaty
from swaty.preprocess.auxiliary.swat_prepare_observation_discharge_file import swat_prepare_observation_discharge_file
sFilename_configuration_in = '/global/homes/l/liao313/workspace/python/swaty/swaty/shared/swat_simulation.xml'
#step 1
aConfig = swat_read_model_configuration_file(sFilename_configuration_in)
   
# iCase_index_in=iCase_index_in, sJob_in=sJob_in, iFlag_mode_in=iFlag_mode_in)
aConfig['sFilename_model_configuration'] = sFilename_configuration_in
oModel = swaty(aConfig)
swat_prepare_observation_discharge_file(oModel)