import sys #append path
import os #check existence
import datetime
import numpy as np
from numpy  import array

from pyearth.toolbox.reader.text_reader_string import text_reader_string


def swat_plot_usgs_precipitation(sFilename_configuration_in):
    """
    plot the precipitation data file
    """
    if os.path.isfile(sFilename_configuration_in):
        pass
    else:
        print('The model configuration file does not exist!')
        return
    #read the configuration into a dictionary    

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