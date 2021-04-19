#this is a new simulation which includes both ncdc and usgs data
import sys
import os
import datetime
import calendar

import numpy as np






#import the eslib library
#this library is used to read data and maybe other operations
sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'
print(sPath_library_python)
sys.path.append(sPath_library_python)
from toolbox.reader.text_reader_string import text_reader_string

#global variables
feet2meter = 0.3048
missing_value = -99.0

#this function is used to prepare the parameter files for swat calibration purpose

def swat_prepare_watershed_configuration_and_parameter_file(sFilename_configuration_in_in):
    
    print(type(config) )
    #retrieve the data
    sWorkspace_home = config['sWorkspace_home']
    sWorkspace_scratch = config['sWorkspace_scratch']
    sWorkspace_raw = config['sWorkspace_raw']
    sWorkspace_data_relative = config['sWorkspace_data']

    sWorkspace_calibration_relative = config['sWorkspace_calibration']    
    sWorkspace_simulation_relative = config['sWorkspace_simulation']
    sWorkspace_project_relative = config['sWorkspace_project']

    sRegion = config['sRegion']
    sFilename_ncdc = config['sFilename_ncdc']


    iYear_start = int(config['iYear_start'] )
    #the end year of spinup
    iYear_spinup_end = int(config['iYear_spinup_end'] )
    iYear_end  = int( config['iYear_end'] )

    
    #we need to read some information from the report first
    sWorkspace_data = sWorkspace_scratch + slash + sWorkspace_data_relative
    sWorkspace_data_project = sWorkspace_data + slash + sWorkspace_project_relative

    sWorkspace_simulation = sWorkspace_scratch +  slash  + sWorkspace_simulation_relative
    sWorkspace_calibration = sWorkspace_scratch + slash + sWorkspace_calibration_relative


    sFilename_hru_report = sWorkspace_data_project + slash + 'auxiliary' + slash \
      + 'hru' + slash + 'HRULandUseSoilsReport.txt'
    print(sFilename_hru_report)
    if os.path.isfile(sFilename_hru_report):
        pass
    else:
        print('The file does not exist!')
        return
    ifs=open(sFilename_hru_report,'r')

    #we also need to record the number of subbasin and hru
    #this file will store how many hru are in each subbasin
    #this file will be used to generate model imput files in the calibration process
    sWorkspace_subbasin = sWorkspace_data_project + slash + 'auxiliary' + slash \
      + 'subbasin'
    if not os.path.exists(sWorkspace_subbasin):
        os.makedirs(sWorkspace_subbasin)      
    else:
        pass
    sFilename_watershed_config = sWorkspace_data_project + slash + 'auxiliary' + slash \
      + 'subbasin' + slash + 'watershed_configuration.txt'
    ofs = open( sFilename_watershed_config, 'w' )  

    sLine=ifs.readline()
    while(sLine):
        print(sLine)
        if "Number of Subbasins" in sLine:
            sLine = sLine.rstrip()
            aDummy = sLine.split()
            nsubbasin = int(aDummy[3])
            print(nsubbasin)
            break
        else:
            sLine=ifs.readline()
    #keep reading the hru within each subbasin
    
   
    
    lookup_table1=list()
    lookup_table2=list()
    
    #let's define subbasin starts with one
    iSubbasin = 1
    while( sLine ):
        print(sLine)
        if "SUBBASIN #" in sLine:
            #we found a subbasin
            #start the count of hru 
            iHru = 0
            sLine=ifs.readline()
            while(sLine):
                if "HRUs" in sLine:
                    break
                else:
                    sLine=ifs.readline()
            #we found the hru index now
            sLine=(ifs.readline()).rstrip()
            aDummy = sLine.split()
            sFirst = aDummy[0]
            while( sFirst.isdigit() ):
                #print(aDummy)
                if(len(aDummy)>0):
                    print(aDummy)
                    iHru = iHru + 1
                    sKey = aDummy[3] 
                   
                    if sKey in lookup_table1:
                        pass
                    else:
                        lookup_table1.append(sKey)
                   
                    #lookup table 2    
                    lookup_table2.append(sKey)                        
                    #next line
                    sLine=(ifs.readline()).rstrip()
                    aDummy = sLine.split()
                    
                    if( len(aDummy) > 0) :
                        sFirst = aDummy[0]
                    else:
                        break
                else:
                    break
            
            #now save the count out
            sLine = "{:02d}".format( iSubbasin ) + ', ' + "{:03d}".format( iHru )  + '\n'
            ofs.write(sLine)
            iSubbasin = iSubbasin+1

            continue
        else:
            sLine=ifs.readline()



    ifs.close() #close hru report file
    ofs.close() #save watershed configuration file
    #save it to a file
    #this file store all the existing unique hru type
    sFilename_hru_combination = sWorkspace_data_project + slash +'auxiliary' + slash +'hru' +slash \
     + 'hru_combination.txt'
    ofs = open(sFilename_hru_combination, 'w')
    for item in lookup_table1:
        ofs.write("%s\n" % item)

    ofs.close()

    #this file store all the hru information, some hru belong to the same type
    sFilename_hru_info = sWorkspace_data_project + slash +'auxiliary' + slash + 'hru' + slash \
     +'hru_info.txt'
    ofs = open(sFilename_hru_info, 'w')
    for item in lookup_table2:
        ofs.write("%s\n" % item)
    ofs.close()

    #read existing default parameter
    

    #we will place the parameter in the simulation folder

    #watershed scale parameter
    sFilename_watershed_parameter = sWorkspace_simulation + slash + 'watershed.para'
    ofs = open(sFilename_watershed_parameter, 'w')
    ofs.close()

    #subbasin scale parameter
    sFilename_subbasin_parameter = sWorkspace_simulation + slash + 'subbasin.para'
    ofs = open(sFilename_subbasin_parameter, 'w')
    ofs.close()
    
    #hru scale parameter
    sFilename_hru_parameter = sWorkspace_simulation + slash + 'hru.para'
    ofs = open(sFilename_hru_parameter, 'w')
    sLine = 'hru, cn2\n'
    ofs.write(sLine)
    for iHru_type in range(0, len(lookup_table1)):
        sHru_type = "{:03d}".format( iHru_type + 1)
        sLine = 'hru'+ sHru_type + ', ' + '70' +'\n'
        ofs.write(sLine)
    ofs.close()
    
    print('finished')

if __name__ == '__main__':
    sModel ='swat'
    sCase = 'tr003'
    sTask = 'simulation'
    iFlag_simulation = 1
    iFlag_pest = 0
    if iFlag_pest == 1:
        sTask = 'calibration'

    sFilename_configuration_in = sWorkspace_scratch + slash + '03model' + slash \
            + sModel + slash + sRegion + slash \
            + sTask + slash + sFilename_config
   

      
    
    swat_prepare_watershed_configuration_and_parameter_file(sFilename_configuration_in)
