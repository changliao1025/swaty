#this is a new simulation which includes both ncdc and usgs data
import sys
import os
import datetime
import calendar
import julian  #to covert datetime to julian date 

import numpy as np
from numpy  import array
from calendar import monthrange #calcuate the number of days in a month

#sProject  ='tinpan'



from pyearth.toolbox.reader.text_reader_string import text_reader_string

#global variables
feet2meter = 0.3048
missing_value = -99.0

#the function to prepare precipition file (with both usgs and ncdc)
#https://confluence.pnnl.gov/confluence/display/SWATMODFL/Using+both+USGS+and+NCDC+data+for+simulation
def swat_prepare_arcswat_usgs_precipitation_file(sFilename_configuration_in):
    """
    prepare the precipitation data file
    """
     
    #retrieve the data
    sWorkspace_home = config['sWorkspace_home']
    sWorkspace_scratch=config['sWorkspace_scratch']

    sWorkspace_data_relative = config['sWorkspace_data']  
    sWorkspace_project_relative = config['sWorkspace_project']
    sWorkspace_simulation_relative = config['sWorkspace_simulation']
    sWorkspace_calibration_relative = config['sWorkspace_calibration']

    sWorkspace_data = sWorkspace_scratch + slash + sWorkspace_data_relative
    sWorkspace_data_project = sWorkspace_data + slash + sWorkspace_project_relative

    sRegion = config['sRegion']
    sFilename_ncdc = config['sFilename_ncdc']
    iYear_start = int(config['iYear_start'] )
    #the end year of spinup
    iYear_spinup_end = int(config['iYear_spinup_end'] )
    iYear_end  = int( config['iYear_end'] )

 
    #the new simulation is 1975-1981
    #read usgs data
    #for usgs data, we prepare the time information ahead, see the templates for details
    #we only have a few years (1979-1981)
    dummy1 = datetime.datetime(iYear_start, 1, 1)
    dummy2 = datetime.datetime(iYear_end, 12, 31)
    julian1 = julian.to_jd(dummy1, fmt='jd')
    julian2 = julian.to_jd(dummy2, fmt='jd')
    julian_start = julian1

    nrow_usgs = int(julian2 - julian1 + 1)

    aSiteName=['c18', 'c19']
    nsite = len(aSiteName)
    for iSite in range(0, nsite):
        #pre-define the container
        aPrec_usgs = np.full( nrow_usgs , missing_value, dtype = float )
        #read data for each year
        for iYear in range(iYear_start, iYear_end+1):
            sYear = "{:04d}".format(iYear)
            sFilename = sWorkspace_data_project + slash \
                + 'auxiliary' + slash + 'usgs' + slash + 'precipitation' + slash \
                + aSiteName[iSite] + slash + sYear + '.csv'
            if os.path.isfile(sFilename):
                aData = text_reader_string(sFilename, delimiter_in=',')
                aData_all = array( aData )
                nrow_dummy = len(aData_all)
                
                aPrec_dummy = aData_all[:,3]
                aPrec_usgs_dummy = np.full( nrow_dummy , missing_value, dtype = float )
                
                for i in range(0, nrow_dummy):
                    dDummy = aPrec_dummy[i]                   
                    if len(dDummy) != 0:
                        aPrec_usgs_dummy[i]=float(dDummy)     
                    else:
                        pass               


                dummy1 = datetime.datetime(iYear, 1, 1)
                dummy2 = datetime.datetime(iYear, 12, 31)

                julian1 = julian.to_jd(dummy1, fmt='jd')
                julian2 = julian.to_jd(dummy2, fmt='jd')

                lIndex1 = int( julian1 - julian_start)
                lIndex2 = int( julian2 - julian_start )
            
                aPrec_usgs[lIndex1 : (lIndex2 + 1)] = aPrec_usgs_dummy


            else:
                print('No precipitation date for this year!')
                #return
            print(iYear)

        
        #write out 
        sFilename = sWorkspace_data + slash +  'swat' + slash + sRegion + slash \
        + 'auxiliary' + slash + 'usgs' + slash + 'pcp' +  slash +  aSiteName[iSite].zfill(8) + '.txt'
        print(sFilename)
        ofs = open(sFilename, 'w')
        date_start =  datetime.datetime(iYear_start,1,1)   
        sDate = str(iYear_start) +  "{:02d}".format(1) + "{:02d}".format(1) +'\n'
        ofs.write(sDate)

        dummy1 = datetime.datetime(iYear_start, 1, 1)
        dummy2 = datetime.datetime(iYear_end, 12, 31)
        julian_start_usgs = julian.to_jd(dummy1, fmt='jd')
        julian_end_usgs = julian.to_jd(dummy2, fmt='jd')       

        #only use usgs data
        
        for iYear in range(iYear_start, iYear_end + 1):
                if (calendar.isleap(iYear)):
                    day_in_year = 366
                else:
                    day_in_year = 365
                iDay_start = 1
                iDay_end = day_in_year

                dummy = datetime.datetime(iYear,1,1)    
                julian1 = julian.to_jd(dummy, fmt='jd')
                for iDay in range(iDay_start, iDay_end+1):
                    julian2 = julian1 + iDay - 1
                    dt = julian.from_jd(julian2, fmt='jd')      

                    lIndex_distance1= int(julian2-julian_start_usgs)
                    lIndex_distance2= int(julian2-julian_end_usgs)

                    #here we assume the usgs data already pre-process with missing data
                    #and all other data are missing if out of range            
                    if(lIndex_distance1>=0 and lIndex_distance2<=0):
                        dDummy = aPrec_usgs[ lIndex_distance1 ]
                    else:
                        dDummy = missing_value

                    sLine  =  "{:06.2f}".format(dDummy) 
                    sLine = sLine+'\n'
                    ofs.write( sLine )

        ofs.close()
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
    swat_prepare_arcswat_usgs_precipitation_file(sFilename_configuration_in)
