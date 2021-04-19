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

from eslib.system.define_global_variables import *

from eslib.toolbox.reader.text_reader_string import text_reader_string
from eslib.visual.plot.plot_time_series_data import plot_time_series_data
from eslib.visual.plot.plot_multiple_time_series_data import plot_multiple_time_series_data

sPath_swat_python = sWorkspace_code +  slash + 'python' + slash + 'swat' + slash + 'swat_python'
sys.path.append(sPath_swat_python)
from swat.shared.swat_read_configuration_file import swat_read_configuration_file
from swat.shared import swat_global


from swat.plot.swat_convert_data_daily_2_monthly import swat_convert_data_daily_2_monthly


def swat_tsplot_multiple_stream_discharge(sFilename_configuration_in, \
    sJob_in = None,\
    sModel_in = None):
    #construct case array
    
    n=10
    iFlag_first = 1
    for i in range(n):
        j = i + 10
        config = swat_read_configuration_file(sFilename_configuration_in,\
            iCase_index_in = j,\
            sDate_in='20191226')
        if iFlag_first ==1:
            sWorkspace_simulation = swat_global.sWorkspace_simulation
            sModel = swat_global.sModel
            sRegion = swat_global.sRegion

            iYear_start = swat_global.iYear_start
            iYear_spinup_end = swat_global.iYear_spinup_end
            iYear_end  = swat_global.iYear_end

            dSimulation_start = swat_global.lJulian_start
            nstress = swat_global.nstress
            aDischarge_simulation_all = np.full((n, nstress), 0.0, dtype=float)
            dates = list()
            dSimulation_start2 = datetime.datetime(iYear_start, 1, 1)  #year, month, day
            for days in range(nstress):
                dates.append(dSimulation_start2 + datetime.timedelta(days))
            sWorkspace_simulation_case = swat_global.sWorkspace_simulation_case 
            sPath_current = sWorkspace_simulation_case   
            print('The current path is: ' + sPath_current)
            sWorkspace_slave = sPath_current
            sFilename = sWorkspace_slave + slash + 'stream_discharge_22.txt'
            aData = text_reader_string(sFilename)
            aDischarge_simulation = array( aData ).astype(float)  
            aDischarge_simulation = aDischarge_simulation * cms2cmd
            aDischarge_simulation.shape = nstress
            aDischarge_simulation_all[i] = aDischarge_simulation
            iFlag_first =0
        else:
            sWorkspace_simulation_case = swat_global.sWorkspace_simulation_case 
            sPath_current = sWorkspace_simulation_case   
            print('The current path is: ' + sPath_current)
            sWorkspace_slave = sPath_current
            sFilename = sWorkspace_slave + slash + 'stream_discharge_22.txt'
            aData = text_reader_string(sFilename)
            aDischarge_simulation = array( aData ).astype(float)  
            aDischarge_simulation = aDischarge_simulation * cms2cmd
            aDischarge_simulation.shape = nstress
            aDischarge_simulation_all[i] = aDischarge_simulation

        

        #dummy1 = np.percentile(aDischarge_simulation, 99)
        #dummy2 = np.where( aDischarge_simulation > dummy1 )
        
    #plot simulation
    aLabel_legend = np.full(n, '',dtype=object)
    sLabel_Y =r'Stream discharge ($m^{3} \, day^{-1}$)' 
    iFlag_cn = 0
    if iFlag_cn ==1:
        sFilename_out = sWorkspace_simulation + slash + 'discharge_cn2_comparison.png'
        aCN2 = np.arange(10) * 10 + 5
        for i in range(n):
            j = n-i-1
            dCN2 = aCN2[j]
            aLabel_legend[i]= 'CN = ' + "{:0.2f}".format(dCN2) 

        plot_multiple_time_series_data(dates, 10, aDischarge_simulation_all, \
            sFilename_out,\
            sTitle_in = '', \
            sLabel_Y_in= sLabel_Y, \
            aLabel_legend_in = aLabel_legend, \
            iSize_X_in = 12, iSize_Y_in = 5)
    #awc
    iFlag_awc = 1
    if iFlag_awc ==1:
        aAWC = np.arange(10) / 10.0 + 0.05
        sFilename_out = sWorkspace_simulation + slash + 'discharge_awc_comparison.png'
        for i in range(n):
            j = i
            dAWC = aAWC[j]
            aLabel_legend[i]= 'AWC = ' + "{:0.2f}".format(dAWC) 

        plot_multiple_time_series_data(dates, 10, aDischarge_simulation_all, \
            sFilename_out,\
            sTitle_in = '', \
            sLabel_Y_in= sLabel_Y, \
            aLabel_legend_in = aLabel_legend, \
            iSize_X_in = 12, iSize_Y_in = 5)


    
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
    swat_tsplot_multiple_stream_discharge(sFilename_configuration)

