import sys
import os

import numpy as np
from numpy  import array
import datetime


import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook





from pyearth.toolbox.reader.text_reader_string import text_reader_string
def price(x):
        return '$%1.2f' % x


def swat_plot_usgs_stream_discharge(sFilename_configuration_in):
    
    

    sWorkspace_data_relative = config['sWorkspace_data']  
    sWorkspace_project_relative = config['sWorkspace_project']
    sWorkspace_simulation_relative = config['sWorkspace_simulation']
    sWorkspace_calibration_relative = config['sWorkspace_calibration']

    sRegion = config['sRegion']
    iYear_start = int(config['iYear_start'] )
    iYear_spinup_end = int(config['iYear_spinup_end'] )
    iYear_end  = int( config['iYear_end'] )
    nsegment = int( config['nsegment'] )

    dSimulation_start = datetime.datetime(iYear_start, 1, 1)  #year, month, day
    dSimulation_transient_start = datetime.datetime(iYear_spinup_end+1, 1, 1)  #year, month, day
    dSimulation_end = datetime.datetime(iYear_end, 12,31)  #year, month, day

    dObservation_start = datetime.datetime(iYear_start, 1, 1)  #year, month, day
    dObservation_end = datetime.datetime(iYear_end, 12, 31)  #year, month, day

    jdSimulation_start = julian.to_jd(dSimulation_start, fmt='jd')
    jdSimulation_transient_start = julian.to_jd(dSimulation_transient_start, fmt='jd')
    jdSimulation_end = julian.to_jd(dSimulation_end, fmt='jd')

    jdStart = julian.to_jd(dObservation_start, fmt='jd')
    jdEnd = julian.to_jd(dObservation_end, fmt='jd')
    nstress = int(jdEnd - jdStart + 1)

    nstress_observation = int(jdSimulation_end - jdSimulation_start + 1)
    sWorkspace_data = sWorkspace_scratch + slash + sWorkspace_data_relative
    sWorkspace_data_project = sWorkspace_data + slash + sWorkspace_project_relative

    sFilename = sWorkspace_data_project + slash   + 'auxiliary' + slash \
     + 'usgs' + slash + 'discharge' + slash + 'discharge_observation.txt'
    print(sFilename)
    aData = text_reader_string(sFilename)
    aData_all = array( aData ).astype(float)  
    
    aDischarge_observation = aData_all

    nan_index = np.where(aDischarge_observation == -9999)
    aDischarge_observation[nan_index] = math.nan

    #plot simulation
    dates = list()
    for days in range(nstress_observation):
        dates.append(dObservation_start + datetime.timedelta(days))
   
    years = mdates.YearLocator()   # every year
    months = mdates.MonthLocator()  # every month
    yearsFmt = mdates.DateFormatter('%Y')
    fig, ax = plt.subplots()
    ax.plot(dates, aDischarge_observation)
    
    # format the ticks
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)
    
    # round to nearest years...
    datemin = np.datetime64(dates[0], 'Y')
    datemax = np.datetime64(dates[nstress_observation-1], 'Y') + np.timedelta64(1, 'Y')
    ax.set_xlim(datemin, datemax)
    
    # format the coords message box
    
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.format_ydata = price
    ax.grid(True)
    
    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()
    
    #plt.show()
    sFilename_out = sWorkspace_data_project  + slash        + 'auxiliary' + slash \
    + 'usgs' + slash + 'discharge'+slash+ 'discharge_observation.png'
    fig.savefig(sFilename_out)   # save the figure to file
    print(sFilename_out)
    plt.close(fig) 
    print("finished")


if __name__ == '__main__':
    
    sRegion = 'tinpan'
    sModel ='swat'
    sCase = 'test'
    sJob = sCase
    sTask = 'simulation'
    iFlag_simulation = 1
    iFlag_pest = 0
    if iFlag_pest == 1:
        sTask = 'calibration'
    sFilename_configuration = sWorkspace_scratch + slash + '03model' + slash \
              + sModel + slash + sRegion + slash \
              + sTask  + slash + sFilename_config
    swat_plot_usgs_stream_discharge(sFilename_configuration_in)

