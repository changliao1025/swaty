import sys
import os

import numpy as np
from numpy  import array
import datetime
import calendar


import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from matplotlib.ticker import FuncFormatter

sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)

from pyearth.system.define_global_variables import *
from pyearth.toolbox.reader.text_reader_string import text_reader_string
from pyearth.visual.plot.plot_time_series_data import plot_time_series_data

#ftsz = 18
#plt.rcParams['xtick.labelsize']=ftsz
#plt.rcParams['ytick.labelsize']=ftsz
#plt.rcParams['axes.labelsize']=ftsz
#plt.rcParams['axes.titlesize']=ftsz 


sPath_swat_python = sWorkspace_code +  slash + 'python' + slash + 'swat' + slash + 'swat_python'
sys.path.append(sPath_swat_python)
from swat.shared.swat_read_configuration_file import swat_read_configuration_file
from swat.shared import swat_global


from swat.plot.swat_convert_data_daily_2_monthly import swat_convert_data_daily_2_monthly


def swat_plot_stream_discharge(sFilename_configuration_in, iCase_index_in = None, sJob_in = None, sModel_in = None):
  
    config = swat_read_configuration_file(sFilename_configuration_in, \
        iCase_index_in = iCase_index_in,\
         sDate_in = '20191219')
    sModel = swat_global.sModel
    sRegion = swat_global.sRegion
   
    iYear_start = swat_global.iYear_start
    iYear_spinup_end = swat_global.iYear_spinup_end
    iYear_end  = swat_global.iYear_end
   
    dSimulation_start = swat_global.lJulian_start
    nstress = swat_global.nstress
    
    sWorkspace_simulation_case = swat_global.sWorkspace_simulation_case
    
    iFlag_debug = 2
    if(iFlag_debug == 1 ):
        sPath_current = sWorkspace_pest_model + slash + 'beopest1'
    else:
        if iFlag_debug == 2:
            #run from the arcswat directory
            sPath_current = sWorkspace_simulation_case #+ slash  + 'TxtInOut'
        else:
            sPath_current = os.getcwd()
    print('The current path is: ' + sPath_current)
    sWorkspace_slave = sPath_current
    sFilename = sWorkspace_slave + slash + 'stream_discharge_22.txt'
    aData = text_reader_string(sFilename)
    aDischarge_simulation = array( aData ).astype(float)  
    aDischarge_simulation = aDischarge_simulation * cms2cmd

    dummy1 = np.percentile(aDischarge_simulation, 99)
    dummy2 = np.where( aDischarge_simulation > dummy1 )
    dSimulation_start = datetime.datetime(iYear_start, 1, 1)  #year, month, day
    #plot simulation
    dates = list()
    for days in range(nstress):
        dates.append(dSimulation_start + datetime.timedelta(days))
   
    sFilename_out = sWorkspace_simulation_case + slash + 'discharge_daily.png'
    
    sLabel_Y =r'Stream discharge ($m^{3} \, day^{-1}$)' 
    sLabel_legend = 'Simulated stream discharge'

    plot_time_series_data(dates, aDischarge_simulation,\
         sFilename_out,\
         sTitle_in = '', \
             sLabel_Y_in= sLabel_Y,\
              sLabel_legend_in = sLabel_legend, \
            iSize_X_in = 12,\
                 iSize_Y_in = 5)
    


    
    print("finished")



if __name__ == '__main__':
    
    sModel ='swat'
    
    sRegion = 'tinpan'
    iCase = 0
   
    sTask = 'simulation'
    iFlag_simulation = 1
    iFlag_pest = 0
    if iFlag_pest == 1:
        sTask = 'calibration'
    sFilename_configuration = sWorkspace_configuration+ slash \
              + sModel + slash + sRegion + slash \
              + sTask  + slash + 'marianas_configuration.txt'
    swat_tsplot_stream_discharge(sFilename_configuration, iCase)

