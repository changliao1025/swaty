import sys #append path
import os #check existence
import datetime
import julian  #to covert datetime to julian date 
import platform #platform independent
import numpy as np
from pathlib import Path
from numpy  import array

#import the eslib library
sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'
sys.path.append(sPath_library_python)
from toolbox.reader.text_reader_string import text_reader_string

feet2meter = 0.3048
missing_value = -99.0
def swat_plot_usgs_precipitation(sFilename_configuration_in):
    """
    plot the precipitation data file
    """
    

    sWorkspace_data_relative = config['sWorkspace_data']  
    sWorkspace_project_relative = config['sWorkspace_project']
    sWorkspace_simulation_relative = config['sWorkspace_simulation']
    sWorkspace_calibration_relative = config['sWorkspace_calibration']

    sRegion = config['sRegion']
    sFilename_ncdc = config['sFilename_ncdc']
    iYear_start = int(config['iYear_start'] )
    iYear_spinup_end = int(config['iYear_spinup_end'] )
    iYear_end  = int( config['iYear_end'] )

    print('Finished!')
if __name__ == '__main__':
    sModel = 'beopest001'
    sFilename_configuration_in = sWorkspace_scratch + slash + '03model' + slash \
            + 'swat' + slash + 'purgatoire30' + slash \
            + 'calibration'  + slash + sFilename_config
    swat_plot_usgs_precipitation(sFilename_configuration_in)