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

start_year = 2000
end_year =2017

def swat_prepare_precipitation_file(sFilename_configuration_in):
    
    sFilename_ncdc = config['sFilename_ncdc']


    dObservation_start = datetime.datetime(2000, 1, 1)  #year, month, day
    dObservation_end = datetime.datetime(2017, 12,31)  #year, month, day
    jdStart = julian.to_jd(dObservation_start, fmt='jd')
    
    dt_dummy = julian.from_jd(jdStart, fmt='jd')


    jdEnd = julian.to_jd(dObservation_end, fmt='jd')
    nstress = int(jdEnd - jdStart + 1)

    aData = text_reader_string(sFilename_ncdc, delimiter_in=',', skipline_in=1, remove_quota = 1)
    aData_all = array( aData )
    nrow_dummy = len(aData_all)
    ncolumn_dummy=len(aData_all[0,:])

    aSite_name = aData_all[:,0]
    aLatitude  = aData_all[:,3].astype(float)  
    aLongitude  = aData_all[:,4].astype(float)
    aElevation  = aData_all[:,5].astype(float)

    aDate =  aData_all[:,6]

    aDate_year = [x[0:4] for x in aDate]
    aDate_month = [x[5:7] for x in aDate]
    aDate_day = [x[8:10] for x in aDate]
    for i in range(0, nrow_dummy):
        dummy_start = datetime.datetime(int(aDate_year[i]), int(aDate_month[i]), int(aDate_day[i]))
        aDate[i] =     julian.to_jd(dummy_start, fmt='jd')

    aPrec_dummy = (aData_all[:,7])
    aTmax_dummy = aData_all[:,9]
    aTmin_dummy = aData_all[:,10]

    nrow  = len(aSite_name)
    aPrec = np.full( nrow , 0.0, dtype=float )
    aTmax = np.full( nrow , 0.0, dtype=float )
    aTmin = np.full( nrow , 0.0, dtype=float )

    for i in range(0, nrow):
        prec = aPrec_dummy[i]
        tmax = aTmax_dummy[i]
        tmin = aTmin_dummy[i]
        if len(prec) != 0:
            aPrec[i]=float(prec)
        if len(tmax) != 0:
            aTmax[i]=float(tmax)
        if len(tmin) != 0:
            aTmin[i]=float(tmin)
    #aSite_list = np.unique(aSite_name)
    indexes = np.unique(aSite_name, return_index=True)[1]
    aSite_list=[aSite_name[index] for index in sorted(indexes)]
    nsite = len(aSite_list)

    aLatitude_all = np.full( nsite , 0.0, dtype=float )
    aLongitude_all = np.full( nsite , 0.0, dtype=float )
    aElevation_all=np.full( nsite , 0.0, dtype=float )
   
    aTmax_new = np.full( (nstress, nsite) , 0.0, dtype=float )
    aTmin_new = np.full( (nstress, nsite) , 0.0, dtype=float )

    for iSite in range(0, nsite):
        sSitename = aSite_list[iSite]
        indices = np.where(aSite_name == sSitename)

        aLatitude_all[iSite] = (aLatitude[indices[0]])[0]
        aLongitude_all[iSite] = (aLongitude[indices[0]])[0]
        aElevation_all[iSite] = (aElevation[indices[0]])[0]

        date_site = aDate[indices]

        prec_site = aPrec[indices]
        tmax_site = aTmax[indices]
        tmin_site = aTmin[indices]

        for iStress in range(1, nstress):
            jd_dummy1 = jdStart
            jd_dummy =  jd_dummy1 + iStress - 1
            dt_dummy = julian.from_jd(jd_dummy, fmt='jd')

            index_dummy = np.flatnonzero(date_site == jd_dummy)
            
            #print(index_dummy[0])
            dummy_size = len(index_dummy)
            #print(len(index_dummy))
            
            if(dummy_size==1):
                tmax_dummy = tmax_site[index_dummy]
                tmin_dummy = tmin_site[index_dummy]
            else:
                tmax_dummy = -99
                tmin_dummy = -99
            #print(iSite+1, iStress, jd_dummy, index_dummy,dummy_size, tmax_dummy)
            aTmax_new[iStress-1,iSite] = tmax_dummy
            aTmin_new[iStress-1,iSite] = tmin_dummy


    #write out 
    sFilename_temperature = sWorkspace_data + slash + 'pcp.txt'    
    ofs = open(sFilename_temperature, 'w')

    sLine = 'ID, NAME, LAT, LONG, ELEVATION\n'
    #1,p329959,32.940,-95.938,141.000
    #2,p329956,32.940,-95.625,153.000
    ofs.write(sLine)

    for iSite in range(0, 6):
        sSite = "{:02d}".format(iSite+1)  
        sSitename = aSite_name[iSite]
        sLat = "{:5.1f}".format( aLatitude_all[iSite] )
        sLon = "{:5.1f}".format( aLongitude_all[iSite] )  
        sEle = "{:5.1f}".format( aElevation_all[iSite] )
        sLine = sSite + ', ' + sSitename + ', ' \
        + sLat  + ', '+ sLon + ', ' + sEle + '\n'
        ofs.write(sLine)


    ofs.close()
    sFilename_temperature = sWorkspace_data + slash + 'data.pcp'    
    ofs = open(sFilename_temperature, 'w')
    ofs.write('Just started\n')
    sLine='Lati   '
    for iSite in range(0,6):
        sLine  = sLine + "{:5.1f}".format(aLatitude_all[iSite])  
    sLine=sLine+'\n'
    ofs.write( sLine )
    sLine='Long   '
    for iSite in range(0,6):
        sLine  = sLine + "{:5.1f}".format(aLongitude_all[iSite])     
    sLine=sLine+'\n'
    ofs.write( sLine )
    sLine='Elev   '
    for iSite in range(0,6):
        sLine  = sLine + "{:5d}".format( int( aElevation_all[iSite]) )      
    sLine=sLine+'\n'
    ofs.write( sLine )

 
    
    date_start =  datetime.datetime(start_year,1,1)   
    jd_start = int(julian.to_jd(date_start, fmt='jd'))
    iStress =1
    for iYear in range(start_year, end_year+1):
        if (calendar.isleap(iYear)):
            day_in_year = 366
        else:
            day_in_year = 365
        start_day =1
        end_day = day_in_year
        date1 = datetime.datetime(iYear,1,1)    
        jd1 = julian.to_jd(date1, fmt='jd')
        for iDay in range(start_day, end_day+1):

            
            
            jd2 = jd1 + iDay -1
            dt = julian.from_jd(jd2, fmt='jd')
            #print(dt)
             
            sDate = str(iYear)+  "{:03d}".format(iDay) 
            sLine = sDate           

            for iSite in range(0,6):
                sLine  = sLine + "{:05.1f}".format(aTmax_new[iStress-1,iSite])  \
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
    swat_prepare_precipitation_file(sFilename_configuration_in)
    