import sys
import os
import numpy as np
from numpy  import array
import datetime
import calendar
import julian
import platform 




sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'
print(sPath_library_python)

sys.path.append(sPath_library_python)

from toolbox.reader.text_reader_string import text_reader_string

missing_value = -99.0

def swat_prepare_arcswat_ncdc_temperature_file(sFilename_configuration_in):
    
    sFilename_ncdc = config['sFilename_ncdc']
    sRegion = config['sRegion']

    iYear_start = int(config['iYear_start'] )
    iYear_spinup_end = int(config['iYear_spinup_end'] )
    iYear_end  = int( config['iYear_end'] )


    dObservation_start = datetime.datetime(iYear_start, 1, 1)  #year, month, day
    dObservation_end = datetime.datetime(iYear_end, 12,31)  #year, month, day
    jdStart = julian.to_jd(dObservation_start, fmt='jd')
    
    dt_dummy = julian.from_jd(jdStart, fmt='jd')
    jdEnd = julian.to_jd(dObservation_end, fmt='jd')
    nstress = int(jdEnd - jdStart + 1) #this is the data series what will be used.
    #read the ncdc file
    sFilename_ncdc = sWorkspace_scratch + slash + sWorkspace_raw + slash + sFilename_ncdc
        
    aData = text_reader_string(sFilename_ncdc, delimiter_in=',', skipline_in = 1, remove_quota = 1)
    aData_all = array( aData )
    nrow_ncdc = len(aData_all) #this fle contains more than enough data
    ncolumn_ncdc = len(aData_all[0,:])

    aSiteName_all = aData_all[:,0]
    dummy = np.unique(aSiteName_all, return_index=True)[1]
    aSiteName=[aSiteName_all[index] for index in sorted(dummy)]
    nsite = len(aSiteName)

    aLatitude_all  = aData_all[:,3].astype(float)  
    aLongitude_all  = aData_all[:,4].astype(float)
    aElevation_all  = aData_all[:,5].astype(float)

    aDate_ncdc =  aData_all[:,6]
    
    aDate_year = [x[0:4] for x in aDate_ncdc]
    aDate_month = [x[5:7] for x in aDate_ncdc]
    aDate_day = [x[8:10] for x in aDate_ncdc]

    aDate = np.full( nrow_ncdc , 0.0, dtype = float )

    for i in range(0, nrow_ncdc):
        dummy = datetime.datetime(int(aDate_year[i]), int(aDate_month[i]), int(aDate_day[i]))
        aDate[i] = julian.to_jd(dummy, fmt='jd')

    aTmax_dummy = aData_all[:,8]
    aTmin_dummy = aData_all[:,9]

    aLatitude = np.full( nsite , 0.0, dtype = float )
    aLongitude = np.full( nsite , 0.0, dtype = float )
    aElevation = np.full( nsite , 0.0, dtype = float )

    aTmax_ncdc = np.full( nrow_ncdc , missing_value, dtype = float )
    aTmin_ncdc = np.full( nrow_ncdc , missing_value, dtype = float )

    for i in range(0, nrow_ncdc):
        
        tmax = aTmax_dummy[i]
        tmin = aTmin_dummy[i]
        
        if len(tmax) != 0:
            aTmax_ncdc[i]=float(tmax)
        if len(tmin) != 0:
            aTmin_ncdc[i]=float(tmin)
   
    aTmax_new = np.full( (nstress, nsite) , missing_value, dtype=float )
    aTmin_new = np.full( (nstress, nsite) , missing_value, dtype=float )

    for iSite in range(0, nsite):
        sSitename = aSiteName[iSite]
        aIndex = np.where(aSiteName_all == sSitename)

        aLatitude[iSite] = (aLatitude_all[aIndex[0]])[0]
        aLongitude[iSite] = (aLongitude_all[aIndex[0]])[0]
        aElevation[iSite] = (aElevation_all[aIndex[0]])[0]

        aDate_site = aDate[aIndex]
        aTmax_site = aTmax_dummy[aIndex]
        aTmin_site = aTmin_dummy[aIndex]

        for iStress in range(1, nstress):
            jd_dummy1 = jdStart
            jd_dummy =  jd_dummy1 + iStress - 1
            dt_dummy = julian.from_jd(jd_dummy, fmt='jd')

            index_dummy = np.flatnonzero(aDate_site == jd_dummy)
            
            dummy_size = len(index_dummy)
            
            if(dummy_size==1):
                dummy1 =  aTmax_site[index_dummy]  
                if(len(dummy1[0]) > 1 ):
                    tmax_dummy = aTmax_site[index_dummy]                    
                else:
                    tmax_dummy = missing_value  

                dummy2 =  aTmin_site[index_dummy]  
                if(len(dummy2[0]) > 1 ):
                    tmin_dummy = aTmin_site[index_dummy]                    
                else:
                    tmin_dummy = missing_value
            else:
                tmax_dummy = missing_value
                tmin_dummy = missing_value                           
            aTmax_new[iStress-1,iSite] = tmax_dummy
            aTmin_new[iStress-1,iSite] = tmin_dummy
   #write out 
    sFilename = sWorkspace_data + slash +  'swat' + slash + sRegion + slash \
        + 'auxiliary' + slash + 'ncdc' + slash + 'tmp' +  slash +  'ncdc_tmp_site'  + '.txt'  
    ofs = open(sFilename, 'w')

    sLine = 'ID, NAME, LAT, LONG, ELEVATION\n'
    #1,p329959,32.940,-95.938,141.000
    #2,p329956,32.940,-95.625,153.000
    ofs.write(sLine)

    for iSite in range(0, 6):
        sSiteID = "{:02d}".format(iSite+1)  
        sSitename = aSiteName[iSite]
        sLatitude = "{:.3f}".format( aLatitude[iSite] )
        sLongitude = "{:.3f}".format( aLongitude[iSite] )  
        sElevation = "{:05d}".format( int(aElevation[iSite]) )
        sLine = sSiteID + ', ' + sSitename[-8:] + ', ' \
        + sLatitude  + ', '+ sLongitude + ', ' + sElevation + '\n'
        ofs.write(sLine)
    ofs.close()

    for iSite in range(0, 6):
        sSitename = aSiteName[iSite]

        #sFilename = sWorkspace_data + slash + sSitename[-8:] + '.txt'    
        sFilename = sWorkspace_data + slash +  'swat' + slash + sRegion + slash \
        + 'auxiliary' + slash + 'ncdc' + slash + 'tmp' +  slash +  sSitename[-8:]     + '.txt'
        ofs = open(sFilename, 'w')
    
        date_start =  datetime.datetime(iYear_start,1,1)  
        sDate = str(iYear_start)+  "{:02d}".format(1) + "{:02d}".format(1) +'\n'      
        ofs.write(sDate)
        date_start =  datetime.datetime(iYear_start,1,1)   
        jd_start = int(julian.to_jd(date_start, fmt='jd'))
        iStress =1
        for iYear in range(iYear_start, iYear_end+1):
            if (calendar.isleap(iYear)):
                day_in_year = 366
            else:
                day_in_year = 365
            iDay_start =1
            iDay_end = day_in_year
            date1 = datetime.datetime(iYear,1,1)    
            jd1 = julian.to_jd(date1, fmt='jd')
            for iDay in range(iDay_start, iDay_end+1):
                jd2 = jd1 + iDay -1
                dt = julian.from_jd(jd2, fmt='jd')
                        
                sLine  =  "{:05.1f}".format(aTmax_new[iStress-1,iSite]) + ', ' \
                    +"{:05.1f}".format(aTmin_new[iStress-1,iSite]) 
                sLine=sLine+'\n'
                ofs.write( sLine )
                iStress=iStress+1

        ofs.close()
    print('finished')
    return

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
   
    swat_prepare_arcswat_ncdc_temperature_file(sFilename_configuration_in)
    