import sys
import os

import numpy as np
from numpy  import array
import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from matplotlib.ticker import FuncFormatter
ftsz = 18
plt.rcParams['xtick.labelsize']=ftsz
plt.rcParams['ytick.labelsize']=ftsz
plt.rcParams['axes.labelsize']=ftsz
plt.rcParams['axes.titlesize']=ftsz 
sPlatform_os = platform.system()


sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'
sys.path.append(sPath_library_python)

from toolbox.reader.text_reader_string import text_reader_string

sPath_swat_python = sWorkspace_code +  slash + 'python' + slash + 'swat' + slash + 'swat_python'
sys.path.append(sPath_swat_python)

from swat.plot.swat_convert_data_daily_2_monthly import swat_convert_data_daily_2_monthly
# format the coords message box
def time_series(x, position):

        return '%4.1f' % x
def swat_tsplot_pet(sFilename_configuration_in, sCase_in = None, sJob_in = None, sModel_in = None):
    
    
    if sCase_in is not None:
        print(sCase_in)
        sCase = sCase_in
    else:
        #by default, this model will run in steady state
        sCase = 'ss'
    if sJob_in is not None:
        sJob = sJob_in
    else:
        sJob = 'modflow'
    if sModel_in is not None:
        print(sModel_in)
        sModel = sModel_in
    else:
        sModel = 'modflow' #the default mode is modflow
    
    sWorkspace_scratch = config['sWorkspace_scratch']

    sWorkspace_calibration_relative = config['sWorkspace_calibration']
    sWorkspace_simulation_relative = config['sWorkspace_simulation']

    sWorkspace_simulation = sWorkspace_scratch + slash + sWorkspace_simulation_relative + slash + sCase
    sWorkspace_calibration = sWorkspace_scratch + slash + sWorkspace_calibration_relative + slash + sCase

    sWorkspace_pest_model = sWorkspace_calibration + slash + sModel

    sRegion = config['sRegion']
    sFilename_ncdc = config['sFilename_ncdc']
    iYear_start = int(config['iYear_start'] )
    iYear_spinup_end = int(config['iYear_spinup_end'] )
    iYear_end  = int( config['iYear_end'] )
    dSimulation_start = datetime.datetime(iYear_start, 1, 1)  #year, month, day
    dSimulation_end = datetime.datetime(iYear_end, 12, 31)  #year, month, day


    jdStart = julian.to_jd(dSimulation_start, fmt='jd')
    jdEnd = julian.to_jd(dSimulation_end, fmt='jd')
    nstress = int(jdEnd - jdStart + 1)

    
    iFlag_debug = 2
    if(iFlag_debug == 1 ):
        sPath_current = sWorkspace_pest_model + slash + 'beopest1'
    else:
        if iFlag_debug == 2:
            #run from the arcswat directory
            sPath_current = sWorkspace_simulation #+ slash  + 'TxtInOut'
        else:
            sPath_current = os.getcwd()
    print('The current path is: ' + sPath_current)
    sWorkspace_slave = sPath_current
    sFilename = sWorkspace_slave + slash + 'tinpan_pet.txt'
    aData = text_reader_string(sFilename)
    aDischarge_simulation = array( aData ).astype(float)  

    dummy1 = np.percentile(aDischarge_simulation, 99)
    dummy2 = np.where( aDischarge_simulation > dummy1 )
    #aDischarge_simulation[dummy2] = 0.01
    #plot simulation
    dates = list()
    for days in range(nstress):
        dates.append(dSimulation_start + datetime.timedelta(days))
   
    years = mdates.YearLocator()   # every year
    months = mdates.MonthLocator()  # every month
    yearsFmt = mdates.DateFormatter('%Y')
    fig, ax = plt.subplots(1, 1, figsize=(12, 9))
    ax.plot(dates, aDischarge_simulation)
    
    # format the ticks
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)

    ax.set_xlabel('Time')
    ax.set_ylabel('Potential Evapotranspiration (units: mm/day)')
    
    # round to nearest years...
    datemin = np.datetime64(dates[0], 'Y')
    datemax = np.datetime64(dates[nstress-1], 'Y') + np.timedelta64(1, 'Y')
    #ax.set_ylim(0.0, max(aDischarge_simulation) * 0.3 )
    ax.set_xlim(datemin, datemax)
    
    
    
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.format_ydata = time_series
    ax.grid(True)
    
    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()
    
    #plt.show()
    sFilename_out = sWorkspace_simulation + slash + 'tinpan_pet.png'
    fig.savefig(sFilename_out)   # save the figure to file
    #plt.close(fig) 


    aDischarge_monthly = swat_convert_data_daily_2_monthly( aDischarge_simulation, \
         jdEnd, jdStart, iFlag_mean_or_total_in =1 ) 
    dates = list()
    nyear = iYear_end - iYear_start + 1
    for iYear in range(iYear_start, iYear_end+1):
        for iMonth in range(1,13):
            dSimulation = datetime.datetime(iYear, iMonth, 15) 
            dates.append(dSimulation )

    fig, ax = plt.subplots(1, 1, figsize=(12, 9))
    aDischarge_monthly.shape = (12* nyear)
    ax.plot(dates, aDischarge_monthly)
    
    # format the ticks
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)

    ax.set_xlabel('Time')
    #ax.set_ylabel('Stream discharge (units: cubic meter)')
    ax.set_ylabel('Potential Evapotranspiration (unit: mm)')
    
    # round to nearest years...
    #datemin = np.datetime64(dates[0], 'Y')
    #datemax = np.datetime64(dates[nstress-1], 'Y') + np.timedelta64(1, 'Y')
    #ax.set_ylim(0.0, max(aDischarge_simulation) * 0.3 )
    #ax.set_xlim(datemin, datemax)
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')

    formatter = FuncFormatter(time_series)
    ax.yaxis.set_major_formatter(formatter)
    
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    #ax.fmt_ydata  = time_series
    ax.grid(True)
    
    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()
    
    #plt.show()
    sFilename_out = sWorkspace_simulation + slash + 'pet_monthly.png'
    fig.savefig(sFilename_out)   # save the figure to file
    print("finished")



if __name__ == '__main__':
    sRegion = 'tinpan'
    sModel ='swat'
    sCase = 'tr003'
    sJob = sCase
    sTask = 'simulation'
    iFlag_simulation = 1
    iFlag_pest = 0
    if iFlag_pest == 1:
        sTask = 'calibration'
    sFilename_configuration = sWorkspace_scratch + slash + '03model' + slash \
              + sModel + slash + sRegion + slash \
              + sTask  + slash + sFilename_config
    swat_tsplot_pet(sFilename_configuration, sCase, sJob, sModel)

