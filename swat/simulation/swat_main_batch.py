import os 
import sys #used to add system path
import numpy as np

sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)
from eslib.system import define_global_variables
from eslib.system.define_global_variables import *


#import package
sPath_swat_python = sWorkspace_code +  slash + 'python' + slash + 'swat' + slash + 'swat_python'
sys.path.append(sPath_swat_python)

from swat.simulation.swat_main import swat_main

iFlag_mode = 0 #just create job file, no run
sModel = 'swat'
sRegion = 'tinpan'
sTask = 'simulation'

sFilename_configuration = sWorkspace_configuration + slash + sModel + slash \
    + sRegion + slash + sTask + slash + sFilename_config 

aCN2 = np.arange(10) * 10 + 5
aAWC = np.arange(10) / 10.0 + 0.05

#start loop
ncase = len(aCN2)
for i in range(ncase):
    #call the create case function
    dCN2 = aCN2[i]
    sCN2 = "{:03d}".format(i)
    aVariable = ['cn2']
    aValue = [dCN2]
    
    sCase = 'CN2_' + sCN2

    swat_main(sFilename_configuration, sCase_in = sCase, iFlag_mode_in= iFlag_mode, aVariable_in = aVariable, aValue_in = aValue)

ncase = len(aAWC)
for i in range(ncase):
    #call the create case function
    dAWC = aAWC[i]
    sAWC = "{:03d}".format(i)
    aVariable = [ 'awc']
    aValue = [ dAWC]
    
    sCase = 'AWC_' + sAWC

    swat_main(sFilename_configuration, sCase_in = sCase, iFlag_mode_in= iFlag_mode, aVariable_in = aVariable, aValue_in = aValue)