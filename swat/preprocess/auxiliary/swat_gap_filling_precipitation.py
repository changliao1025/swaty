import sys #append path
import os #check existence
import datetime

import numpy as np
import calendar

from numpy  import array


#import the eslib library
sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'
sys.path.append(sPath_library_python)
from toolbox.reader.text_reader_string import text_reader_string
from toolbox.math.gap_fill_by_window import gap_fill_by_window


def swat_gap_filling_precipitation(sFilename_configuration_in):
    """
    plot the precipitation data file
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

    sSiteName='c18'
   
    sWorkspace_data = sWorkspace_scratch + slash + sWorkspace_data_relative
    sWorkspace_data_project = sWorkspace_data + slash + sWorkspace_project_relative

    
    sFilename = sWorkspace_data_project + slash \
            + 'auxiliary' + slash + 'usgs' + slash + 'pcp' + slash \
            + sSiteName.zfill(8) + '.txt' 
    if os.path.isfile(sFilename):
        pass
    else:
        print(sFilename)
           
        return
    aData = text_reader_string(sFilename, skipline_in = 1)
    #convert it float data type
    aPrec  = aData.astype(float)
    nan_index = np.where(aPrec == missing_value)
    aPrec[nan_index] = math.nan

    aPrec = aPrec * inch2mm

    # read the discharge data first
    sFilename = sWorkspace_data_project + slash  + 'auxiliary' + slash \
     + 'usgs' + slash + 'discharge' + slash + 'discharge_observation.txt'
    print(sFilename)
    aData = text_reader_string(sFilename)
    aDischarge_observation = array( aData ).astype(float)  
    
    nan_index = np.where(aDischarge_observation == -9999.0 )
    aDischarge_observation[nan_index] = math.nan

    dummy1 = ~np.isnan(aPrec ) 
    dummy2 = aPrec != 0.0
    dummy3 = ~np.isnan(aDischarge_observation ) 
    dummy4 = aDischarge_observation != 0.0
    
    dummy5 = np.where(dummy1 & dummy2 & dummy3 & dummy4)

    aPrec_sub = aPrec[dummy5]
    aDischarge_sub = aDischarge_observation[dummy5]

    dummy1 = np.percentile(aDischarge_sub, 95)
    dummy2= np.where( aDischarge_sub > dummy1 )
    #aDischarge_sub[dummy2] = dummy1
    x = aPrec_sub
    y = aDischarge_sub

    fig, ax = plt.subplots(figsize=(10, 10))
    plt.scatter(x, y,  c="g", alpha=0.5, marker=r'$\clubsuit$',
            label="Precipitation-Discharge relationship")
    plt.xlabel("Precipitation")
    plt.ylabel("Discharge")
    plt.legend(loc='upper left')
    plt.show()
    sFilename_out =  sWorkspace_data_project + slash \
        + 'auxiliary' + slash + 'usgs' + slash + 'pcp' + slash \
        + sSiteName.zfill(8) + '_relation.png'
    fig.savefig(sFilename_out) 

    # now do the gap filling

    #plot simulation
    dates = list()
    for days in range(nstress):
        dates.append(dObservation_start + datetime.timedelta(days))

    years = mdates.YearLocator()   # every year
    months = mdates.MonthLocator()  # every month
    yearsFmt = mdates.DateFormatter('%Y')
    

    # format the coords message box
    def time_series(x):
        return '$%1.2f' % x
    print(  np.nansum(aPrec) )
    for w in range (1, 20):
        aPrec = gap_fill_by_window( aPrec, iWindow_size_in = w)
        
        
        #print(  np.nansum(aPrec) )

    #print(aPrec)

    #now we will duplicate data using neareast date 
    for iStress in range (0, nstress):
        dummy = aPrec[iStress]
        if( math.isnan(dummy)):
            #this data is missing still, and we will search by date
            #get the data by convert from jd to date
            lJd = jdStart + iStress
            dummy_date = julian.from_jd(lJd)
            iYear = dummy_date.year
            iMonth = dummy_date.month
            iDay = dummy_date.day

            # now search
            for iSearch in range (0,10):
                iIndex = pow(-1, iSearch) * (iSearch+1)
                iYear_new = iYear + iIndex
                if (calendar.isleap(iYear) and iMonth == 2 and iDay == 29 ):
                    iDay = 28
                dDate_new = datetime.datetime(iYear_new, iMonth, iDay)  #year, month, day
                
                lJD_new = julian.to_jd(dDate_new, fmt='jd')
                if(  lJD_new >= jdStart and lJD_new <= jdEnd ):
                    #this date is within available date range
                    dummy2 = aPrec[ int(lJD_new - jdStart) ]
                    if( math.isnan(dummy2)):
                        j=1
                    else:
                        #found it
                        aPrec[iStress] = dummy2
                        #print(dummy2)
                        break
                else:
                    j=1

        else:
            j=1
    
    print(aPrec)
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.plot(dates, aPrec)
    # format the ticks
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)
    # round to nearest years...
    datemin = np.datetime64(dates[0], 'Y')
    datemax = np.datetime64(dates[nstress-1], 'Y') + np.timedelta64(1, 'Y')
    ax.set_xlim(datemin, datemax)
    
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.format_ydata = time_series
    ax.grid(True)
    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()
    #plt.show()
    # save the figure to file
    sFilename_out =  sWorkspace_data_project + slash \
        + 'auxiliary' + slash + 'usgs' + slash + 'pcp' + slash \
        + sSiteName.zfill(8) + '_gapfilling.png'
    fig.savefig(sFilename_out)  

    sFilename_precipitation_new =  sWorkspace_data_project + slash \
            + 'auxiliary' + slash + 'usgs' + slash + 'pcp' + slash \
            + sSiteName.zfill(8) + '_new.txt' 
    np.savetxt(sFilename_precipitation_new, aPrec, delimiter=',', fmt='%05.1f') 

    print('finished')

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
    swat_gap_filling_precipitation(sFilename_configuration)