import sys
import os

import numpy as np
from numpy  import array
import datetime
import calendar


import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from matplotlib.ticker import FuncFormatter


from swaty.swaty_read_model_configuration_file import swat_read_model_configuration_file
from swaty.classes.pycase import swaty
from pyearth.system.define_global_variables import *
from pyearth.toolbox.reader.text_reader_string import text_reader_string
from pyearth.visual.timeseries.plot_time_series_data import plot_time_series_data

from pyearth.visual.scatter.scatter_plot_data import scatter_plot_data

#ftsz = 18
#plt.rcParams['xtick.labelsize']=ftsz
#plt.rcParams['ytick.labelsize']=ftsz
#plt.rcParams['axes.labelsize']=ftsz
#plt.rcParams['axes.titlesize']=ftsz 




#from swaty.plot.swat_convert_data_daily_2_monthly import swat_convert_data_daily_2_monthly


def swat_tsplot_stream_discharge(oSwat_in):
  
    iYear_start = oSwat_in.iYear_start
    iYear_end = oSwat_in.iYear_end
    nstress_month = oSwat_in.nstress_month
    
    sWorkspace_simulation_case = oSwat_in.sWorkspace_simulation_case


    sFilename1 = '/global/u1/l/liao313/data/swat/arw/auxiliary/usgs/discharge/stream_discharge_monthly.txt'
    
    aData = text_reader_string(sFilename1)
    aDischarge_obs = np.array( aData ).astype(float)  
    aDischarge_obs = aDischarge_obs.flatten() * cms2cmd

    sFilename2 = sWorkspace_simulation_case + slash + 'stream_discharge_monthly.txt'
    
    aData = text_reader_string(sFilename2)
    aDischarge_simulation1 = np.array( aData ).astype(float)  
    aDischarge_simulation1 = aDischarge_simulation1.flatten() * cms2cmd

    sFilename3 =  '/global/u1/l/liao313/data/swat/arw/auxiliary/usgs/discharge/stream_discharge_monthly_opt.txt'
    
    aData = text_reader_string(sFilename3)
    aDischarge_simulation2 = array( aData ).astype(float)  
    aDischarge_simulation2 = aDischarge_simulation2.flatten() * cms2cmd

    #dummy1 = np.percentile(aDischarge_simulation, 99)
    #dummy2 = np.where( aDischarge_simulation > dummy1 )

    
    #plot simulation
    dates = list()
    for iYear in range(iYear_start, iYear_end+1):
        for iMonth in range(1,13):
            dSimulation = datetime.datetime(iYear, iMonth, 1)
            dates.append(dSimulation)
   
    
    
    sLabel_Y =r'Stream discharge ($m^{3} \, day^{-1}$)' 
    sLabel_legend = 'Simulated stream discharge'


    aDate= np.tile( dates , (3,1))
    aData = np.array([aDischarge_obs , aDischarge_simulation1,aDischarge_simulation2])

    aLabel_legend = ['Default','Initial','Calibrated']
    aColor_in = ['black', 'red', 'blue']

    sFilename_out = sWorkspace_simulation_case + slash + 'discharge_monthly_scatter1.png'

    scatter_plot_data(aDischarge_obs,aDischarge_simulation1,sFilename_out,\
        iFlag_scientific_notation_x_in=1,\
                      iFlag_scientific_notation_y_in=1,\
                          dMin_x_in = 0.0, \
                              dMax_x_in = 1E7, \
                                   dMin_y_in = 0.0, \
                              dMax_y_in = 1E7, \
     iSize_x_in = 8, \
                      iSize_y_in = 8,\
                          sLabel_legend_in = 'Initial',\
                               sLabel_x_in = r'Observed discharge ($m^{3} \, day^{-1}$)',\
                      sLabel_y_in = r'Simulated discharge ($m^{3} \, day^{-1}$)' )

    sFilename_out = sWorkspace_simulation_case + slash + 'discharge_monthly_scatter2.png'
    scatter_plot_data(aDischarge_obs,aDischarge_simulation2,sFilename_out,\
         iFlag_scientific_notation_x_in=1,\
                      iFlag_scientific_notation_y_in=1,\
                           dMin_x_in = 0.0, \
                              dMax_x_in = 1E7, \
                                   dMin_y_in = 0.0, \
                              dMax_y_in = 1E7, \
         iSize_x_in = 8, \
                      iSize_y_in = 8,\
                          sLabel_legend_in = 'Calibrated',\
                               sLabel_x_in =r'Observed discharge ($m^{3} \, day^{-1}$)',\
                      sLabel_y_in = r'Calibrated discharge ($m^{3} \, day^{-1}$)' )

    sFilename_out = sWorkspace_simulation_case + slash + 'discharge_monthly.png'
    plot_time_series_data(aDate, aData,\
         sFilename_out,\
         sTitle_in = '', \
             sLabel_y_in= sLabel_Y,\
                 aColor_in =aColor_in,\
              aLabel_legend_in = aLabel_legend, \
            iSize_x_in = 12,\
                 iSize_y_in = 5)
    


    
    print("finished")



if __name__ == '__main__':

    
    sFilename_configuration_in = '/global/homes/l/liao313/workspace/python/swaty/swaty/shared/swat_simulation.xml'
    aConfig = swat_read_model_configuration_file(sFilename_configuration_in)
   
    # iCase_index_in=iCase_index_in, sJob_in=sJob_in, iFlag_mode_in=iFlag_mode_in)
    aConfig['sFilename_model_configuration'] = sFilename_configuration_in
    oSwat = swaty(aConfig)
    swat_tsplot_stream_discharge(oSwat)

