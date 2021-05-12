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
    

    print('Finished!')
if __name__ == '__main__':
    sModel = 'beopest001'
    sFilename_configuration_in = sWorkspace_scratch + slash + '03model' + slash \
            + 'swat' + slash + 'purgatoire30' + slash \
            + 'calibration'  + slash + sFilename_config
            
    swat_plot_usgs_precipitation(sFilename_configuration_in)