#this is a new simulation which includes both ncdc and usgs data
import sys
import os

import numpy as np

from pyearth.system.define_global_variables import *

from pyearth.toolbox.reader.text_reader_string import text_reader_string

from swaty.classes.pycase import swaty

from swaty.swaty_read_model_configuration_file import swat_read_model_configuration_file

#global variables
feet2meter = 0.3048
missing_value = -99.0

#this function is used to prepare the parameter files for swat calibration purpose

def swat_prepare_watershed_configuration_and_parameter_file(oModel_in):
    
    
    #retrieve the data
    
    
    sWorkspace_data = oModel_in.sWorkspace_data

    
    sWorkspace_project = oModel_in.sWorkspace_project

    

    sWorkspace_data_project = sWorkspace_data + slash + sWorkspace_project

    sWorkspace_simulation = oModel_in.sWorkspace_simulation



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
            aDummy = sLine.split() #this is invalid if the line is too long
            #aDummy=np.full(7, '', dtype=string)
            #aDummy[0] = sLine[0,3]
            #aDummy[1] = sLine[3,3]
            #aDummy[2] = sLine[0,3]
            #aDummy[3] = sLine[0,3]
            #aDummy[4] = sLine[0,3]
            #aDummy[5] = sLine[0,3]
            #aDummy[6] = sLine[0,3]
            
            #sFirst = aDummy[ 0 ]
            sLast=aDummy[ len(aDummy)-1 ]
            while( sLast.isdigit() ):
                #print(aDummy)
                if(len(aDummy)>0):
                    print(aDummy)
                    iHru = iHru + 1

                    index = aDummy.index("-->")
                    sKey = aDummy[index+1] 
                   
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
                        #sFirst = aDummy[ len(aDummy)-1 ]
                        sLast = aDummy[ len(aDummy)-1 ]
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


    