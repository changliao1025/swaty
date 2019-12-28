
import os
import sys

sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)
from eslib.system import define_global_variables
from eslib.system.define_global_variables import *
from eslib.toolbox.reader.text_reader_string import text_reader_string

sPath_swat_python = sWorkspace_code +  slash + 'python' + slash + 'swat' + slash + 'swat_python'
sys.path.append(sPath_swat_python)
from swat.shared import swat_global

def swat_prepare_hru_parameter_file():
    """
    #prepare the pest control file
    """      
    sWorkspace_data_project = swat_global.sWorkspace_data_project    
    sWorkspace_simulation_case = swat_global.sWorkspace_simulation_case    
    
    iFlag_simulation = swat_global.iFlag_simulation
    iFlag_pest_calibration = swat_global.iFlag_pest_calibration      
    aVariable = swat_global.aVariable
    aValue = swat_global.aValue
    
    if not os.path.exists(sWorkspace_simulation_case):
        os.makedirs(sWorkspace_simulation_case)      
    else:
        pass

    #read hru type
    sFilename_hru_combination = sWorkspace_data_project + slash + 'auxiliary' + slash\
     + 'hru' + slash   + 'hru_combination.txt'
    if os.path.isfile(sFilename_hru_combination):
        pass
    else:
        print('The file does not exist!')
        return
    aData_all = text_reader_string(sFilename_hru_combination)
    nhru_type = len(aData_all)

    if iFlag_simulation == 1:
        sFilename_hru_template = sWorkspace_simulation_case + slash + 'hru.para'    
    else:
        #sFilename_hru_template = sWorkspace_calibration_case + slash + 'hru.para'
        pass

    ofs = open(sFilename_hru_template, 'w')
    nvariable = len(aVariable)
    sLine = 'hru'
    for i in range(nvariable):
        sVariable = aVariable[i]
        sLine = sLine + ',' + sVariable
    sLine = sLine + '\n'        
    ofs.write(sLine)

    for iHru_type in range(0, nhru_type):
        sHru_type = "{:03d}".format( iHru_type + 1)
        sLine = 'hru'+ sHru_type 
        for iVariable in range(nvariable):
            sValue =  "{:5.2f}".format( aValue[iVariable])            
            sLine = sLine + ', ' + sValue 
        sLine = sLine + '\n'
        ofs.write(sLine)
    ofs.close()
    print('hru parameter is ready!')

    return
if __name__ == '__main__':
    
    
    
    
    swat_prepare_hru_parameter_file()