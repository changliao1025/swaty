import sys #append path
import os #check existence
import datetime

import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_toolkits.axes_grid1 import AxesGrid

from numpy  import array

sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)

from pyearth.system.define_global_variables import *
from pyearth.toolbox.reader.read_configuration_file import read_configuration_file
from pyearth.toolbox.reader.text_reader_string import text_reader_string
from pyearth.visual.plot.plot_time_series_data import plot_time_series_data

sPath_swat_python = sWorkspace_code +  slash + 'python' + slash + 'swat' + slash + 'swat_python'
sys.path.append(sPath_swat_python)
from swat.shared.swat_read_configuration_file import swat_read_configuration_file
from swat.shared import swat_global


missing_value1  = -99
def swat_plot_usgs_precipitation(sFilename_configuration_in):
    """
    plot the precipitation data file
    sFilename_configuration_in
    """
    config = swat_read_configuration_file(sFilename_configuration_in)
    sModel = swat_global.sModel
    sRegion = swat_global.sRegion
    #sFilename_ncdc = config['sFilename_ncdc']
    iYear_start = swat_global.iYear_start
    iYear_spinup_end = swat_global.iYear_spinup_end
    iYear_end  = swat_global.iYear_end
    dObservation_start = datetime.datetime(iYear_start, 1, 1)  #year, month, day
    dObservation_end = datetime.datetime(iYear_end, 12, 31)  #year, month, day   
    nstress = swat_global.nstress
    sProject = sModel + slash + sRegion
    sWorkspace_data_project = sWorkspace_data + slash + sProject

    aSiteName=['c18']
    nsite = len(aSiteName)

    for iSite in range(0, nsite):
        sFilename = sWorkspace_data_project + slash \
                + 'auxiliary' + slash + 'usgs' + slash + 'pcp' + slash \
                + aSiteName[iSite].zfill(8) + '.txt' 
        if os.path.isfile(sFilename):
            pass
        else:
            print(sFilename)
               
            return
        aData = text_reader_string(sFilename, iSkipline_in = 1)
        #convert it float data type
        aPrec  = aData.astype(float)
        iIndex = np.where(aPrec == missing_value1)
        aPrec[iIndex] = math.nan

        #plot simulation
        dates = list()
        for days in range(nstress):
            dates.append(dObservation_start + datetime.timedelta(days))

        sFilename_jpg = sWorkspace_data_project + slash \
                + 'auxiliary' + slash + 'usgs' + slash + 'pcp' + slash \
                + aSiteName[iSite].zfill(8) +    sExtension_jpg 
        print('start ploting')
        inch2mm = 25.4
        aPrec = aPrec * inch2mm

        sLabel_Y = r'Precipitation ($mm \, day^{-1}$)'
        plot_time_series_data(dates, aPrec, sFilename_jpg,\
             sTitle_in = '', sLabel_Y_in= sLabel_Y ,\
            iSize_X_in = 12, iSize_Y_in = 5)
        


    print('Finished!')

if __name__ == '__main__':
    sModel ='swat'
    #because we do not have precipitation data at the tin pan site, the actual data is from the calibration site
    sRegion = 'tinpan'    
    sRegion = 'purgatoire30'
    sCase = 'test'
    sJob = sCase
    sTask = 'simulation'
    iFlag_simulation = 1
    iFlag_pest = 0
    if iFlag_pest == 1:
        sTask = 'calibration'
    sFilename_configuration = sWorkspace_configuration  + slash \
              + sModel + slash + sRegion + slash \
              + sTask  + slash + 'marianas_configuration.txt'

    swat_plot_usgs_precipitation(sFilename_configuration)