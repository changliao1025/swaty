import sys
import os
import numpy as np
from numpy  import array
import datetime

import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook



sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'
print(sPath_library_python)

sys.path.append(sPath_library_python)

from toolbox.reader.text_reader_string import text_reader_string

def swat_evaluate_stream_discharge(sFilename_configuration_in):
    
    sWorkspace_simulation = config['sWorkspace_simulation']
    
    sWorkspace_scratch = config['sWorkspace_scratch']
    sRegion = config['sRegion']
    sFilename_ncdc = config['sFilename_ncdc']
    iYear_start = int(config['iYear_start'] )
    #the end year of spinup
    iYear_spinup_end = int(config['iYear_spinup_end'] )
    iYear_end  = int( config['iYear_end'] )
    nsegment = int( config['nsegment'] )

    sWorkspace_simulation = sWorkspace_scratch + slash + sWorkspace_simulation

    dSimulation_start = datetime.datetime(iYear_start, 1, 1)  #year, month, day
    dSimulation_transient_start = datetime.datetime(iYear_spinup_end+1, 1, 1)  #year, month, day
    dSimulation_end = datetime.datetime(iYear_end, 12,31)  #year, month, day


    jdSimulation_start = julian.to_jd(dSimulation_start, fmt='jd')
    jdSimulation_transient_start = julian.to_jd(dSimulation_transient_start, fmt='jd')
    jdSimulation_end = julian.to_jd(dSimulation_end, fmt='jd')

    nstress_observation = int(jdSimulation_end - jdSimulation_start + 1)
    nstress_simulation = int(jdSimulation_end - jdSimulation_transient_start + 1)
    #print(nstress)
    #print( (68315-9) /17 ) #which means the output does not include the warming up period

    sFilename_observation_discharge = sWorkspace_data + slash + 'swat' + slash + sRegion + slash \
        + 'auxiliary' + slash + 'usgs' + slash + 'discharge' + slash + 'discharge_observation.txt' 
    print(sFilename_observation_discharge)
    aData = text_reader_string(sFilename_observation_discharge)
    aData_all = array( aData ).astype(float)  
    
    aDischarge_observation = aData_all

    aDischarge_observation = np.reshape(aDischarge_observation, nstress_observation)
    aDischarge_observation = aDischarge_observation[ int(jdSimulation_transient_start-jdSimulation_start):  ]
    nan_index = np.where(aDischarge_observation == -9999)
    aDischarge_observation[nan_index] = math.nan

    sFilename = sWorkspace_simulation + slash + 'output.rch'
    #ifs = open(sFilename, 'r')
    aData = text_reader_string(sFilename, skipline_in=9)
    aData_all = array( aData )
    nrow_dummy = len(aData_all)
    ncolumn_dummy = len(aData_all[0,:])

    aData_discharge = aData_all[:, 6].astype(float) 

    aIndex = np.arange(16 , nstress_simulation * nsegment+1, nsegment)
    #for iStress in range(0, nstress):
    print(aIndex)
    aDischarge_simulation = aData_discharge[aIndex]

    #save it to a file

    sFilename = sWorkspace_data + slash + "simulation.txt"
    ofs = open(sFilename, 'w')
    ofs.write(aDischarge_simulation)
    ofs.close()

    
    aDischarge_simulation[nan_index] = math.nan
    aDischarge_observation[nan_index] = math.nan


    #plot simulation
    dates = list()
    for days in range(nstress_simulation):
        dates.append(dSimulation_transient_start + datetime.timedelta(days))
   
    years = mdates.YearLocator()   # every year
    months = mdates.MonthLocator()  # every month
    yearsFmt = mdates.DateFormatter('%Y')
    fig, ax = plt.subplots()
    ax.plot(dates, aDischarge_simulation)
    ax.plot(dates, aDischarge_observation)
    
    
    # format the ticks
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)
    
    # round to nearest years...
    datemin = np.datetime64(dates[0], 'Y')
    datemax = np.datetime64(dates[nstress_simulation-1], 'Y') + np.timedelta64(1, 'Y')
    #ax.set_xlim(datemin, datemax)
    
    
    # format the coords message box
    def price(x):
        return '$%1.2f' % x
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.format_ydata = price
    ax.grid(True)
    
    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()
    
    #plt.show()
    sFilename_out = sWorkspace_data + slash + 'discharge_evaluation.png'
    fig.savefig(sFilename_out)   # save the figure to file
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
    swat_evaluate_stream_discharge(sFilename_configuration_in)

