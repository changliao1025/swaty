import sys
import os
import datetime
import calendar
import julian  #to covert datetime to julian date 
import platform #platform independent
import numpy as np
from numpy  import array
from calendar import monthrange #calcuate the number of days in a month



#import the eslib library
#this library is used to read data and maybe other operations
sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'
print(sPath_library_python)
sys.path.append(sPath_library_python)
from toolbox.reader.text_reader_string import text_reader_string

#global variables
feet2meter = 0.3048
missing_value = -99.0

def swat_prepare_watershed_configuration_file(sFilename_configuration_in):
    #check whether the configuration exist or not
      
    print(type(config) )
    #retrieve the data
    sWorkspace_home = config['sWorkspace_home']
    sWorkspace_data = config['sWorkspace_data']
    sWorkspace_raw = config['sWorkspace_raw']
    sWorkspace_scratch = config['sWorkspace_scratch']
    sWorkspace_simulation = config['sWorkspace_simulation']
    sRegion = config['sRegion']
    sFilename_ncdc = config['sFilename_ncdc']
    iYear_start = int(config['iYear_start'] )
    #the end year of spinup
    iYear_spinup_end = int(config['iYear_spinup_end'] )
    iYear_end  = int( config['iYear_end'] )

    
    #we need to read some information from the report first
    sWorkspace_data_model = sWorkspace_data + slash + 'swat' + slash + sRegion 
    sWorkspace_simulation_model = sWorkspace_scratch + slash + sWorkspace_simulation


    #read watershed configuration
    sFilename_fig = sWorkspace_simulation_model + slash + 'fig.fig'
    #print(sFilename_fig)
    ifs=open(sFilename_fig, 'r')   
    sLine = ifs.readline()

    #the file to be write will be in the data folder
    sFilename =  sWorkspace_data + slash + 'auxiliary' + slash + 'subbasin' + slash + 'subbasin_hru.ini'
    ofs=open(sFilename, 'w')
    iSubbasin = 1
    while (sLine):
   
        #print(sLine)
        aDummy = sLine.split()
        if(len(aDummy) > 0):
            #print(sDummy)
            sDummy = (aDummy[0]).strip()
            if(sDummy == 'subbasin'):
                #this is the subbasin sLine
                #read one more line
                sLine = ifs.readline()
                aDummy = sLine.split()
                sDummy  = (aDummy[0]).strip()
                sFilename_subbasin = sWorkspace_simulation_model + slash + sDummy
                #print(sFilename_subbasin)

                #read the subbasin file 
                nhru = swat_read_subbasin_file(iSubbasin, sWorkspace_simulation_model, sFilename_subbasin)
                

                #write subbasin 
                dummy = str(iSubbasin) + ' ' + str(nhru) + '\n'
                ofs.write(dummy)

                
                iSubbasin = iSubbasin + 1
                sLine = ifs.readline()  
                #call another function to read 
                #go to the next subbasin
            else:
                sLine = ifs.readline()   

        else:
            pass
    # use realine() to read next sLine


        
        

    ifs.close()
    ofs.close()

if __name__ == '__main__':
    
    swat_prepare_watershed_configuration_file(sFilename_configuration_in)