import sys #append path
import os #check existence
import datetime

import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from numpy  import array



#import the eslib library
sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'
sys.path.append(sPath_library_python)
from toolbox.reader.text_reader_string import text_reader_string


def swat_plot_usgs_precipitation(sFilename_configuration_in):
    """
    plot the precipitation data file
    sFilename_configuration_in
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

    dObservation_start = datetime.datetime(iYear_start, 1, 1)  #year, month, day
    dObservation_end = datetime.datetime(iYear_end, 12, 31)  #year, month, day


    jdStart = julian.to_jd(dObservation_start, fmt='jd')
    jdEnd = julian.to_jd(dObservation_end, fmt='jd')
    nstress = int(jdEnd - jdStart + 1)

    sWorkspace_data = sWorkspace_scratch + slash + sWorkspace_data_relative
    sWorkspace_data_project = sWorkspace_data + slash + sWorkspace_project_relative

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
        aData = text_reader_string(sFilename, skipline_in = 1)
        #convert it float data type
        aPrec  = aData.astype(float)
        iIndex = np.where(aPrec == missing_value)
        aPrec[iIndex] = math.nan

        #plot simulation
        dates = list()
        for days in range(nstress):
            dates.append(dObservation_start + datetime.timedelta(days))
    
        years = mdates.YearLocator()   # every year
        months = mdates.MonthLocator()  # every month
        yearsFmt = mdates.DateFormatter('%Y')
        fig, ax = plt.subplots(figsize=(50, 10))
        ax.plot(dates, aPrec)

        # format the ticks
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(yearsFmt)
        ax.xaxis.set_minor_locator(months)

        # round to nearest years...
        datemin = np.datetime64(dates[0], 'Y')
        datemax = np.datetime64(dates[nstress-1], 'Y') + np.timedelta64(1, 'Y')
        ax.set_xlim(datemin, datemax)


        # format the coords message box
        def time_series(x):
            return '$%1.2f' % x
        ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
        ax.format_ydata = time_series
        ax.grid(True)

        # rotates and right aligns the x labels, and moves the bottom of the
        # axes up to make room for them
        fig.autofmt_xdate()

        plt.show()
        sFilename_out =  sWorkspace_data_project + slash \
                + 'auxiliary' + slash + 'usgs' + slash + 'pcp' + slash \
                + aSiteName[iSite].zfill(8) + '.png' 
        fig.savefig(sFilename_out)   # save the figure to file
        print( sum(aPrec) )


    print('Finished!')
    
if __name__ == '__main__':
    sModel ='swat'
    sRegion = 'tinpan'    
    sCase = 'test'
    sJob = sCase
    sTask = 'simulation'
    iFlag_simulation = 1
    iFlag_pest = 0
    if iFlag_pest == 1:
        sTask = 'calibration'
    sFilename_configuration = sWorkspace_configuration  + slash \
              + sModel + slash + sRegion + slash \
              + sTask  + slash + 'constance_configuration.txt'

    swat_plot_usgs_precipitation(sFilename_configuration_in)