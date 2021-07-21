from pyswat.simulation.swat_main import swat_main

from pyswat.shared.swat_read_model_configuration_file import swat_read_model_configuration_file
from pyswat.shared.swat import pyswat


    
aVariable_hru = ['cn2']
aVariable_watershed = ('SFTMP')
aVariable_basin = ('CH_K2','CH_N2')

aValue = [1.0,2.0]

sFilename_configuration_in = '/global/homes/l/liao313/workspace/python/pyswat/pyswat/shared/swat_simulation.xml'
#step 1
aParameter = swat_read_model_configuration_file(sFilename_configuration_in, \
    aVariable_in = aVariable_basin, \
        aValue_in = aValue)
# iCase_index_in=iCase_index_in, sJob_in=sJob_in, iFlag_mode_in=iFlag_mode_in)
aParameter['sFilename_model_configuration'] = sFilename_configuration_in
oModel = pyswat(aParameter)
swat_main(oModel)  #, sCase_in = sCase, iFlag_mode_in= iFlag_mode, aVariable_in = aVariable, aValue_in = aValue)