import sys
import os
import numpy as np
from numpy  import array
import datetime
import calendar
import julian  #to covert datetime to julian date 
import platform #platform indenpendent
from calendar import monthrange



#import the library
sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'
print(sPath_library_python)
sys.path.append(sPath_library_python)
from toolbox.reader.text_reader_string import text_reader_string

def swat_prepare_csv_file_template(sFilename_configuration_in):
    #check whether the configuration exist or not
    
    sRegion = config['sRegion']
    iYear_start = int(config['iYear_start'] )
    iYear_spinup = int(config['iYear_spinup'] )
    iYear_end  = int( config['iYear_end'] )

    for iYear in range(iYear_start, iYear_end+1):
        sYear =  "{:04d}".format(iYear)
        print(sYear)
        sFilename = sWorkspace_data + slash + 'swat' + slash + sRegion + slash \
             + 'auxiliary' + slash + 'template' + slash + sYear + '_template.csv'
        ofs = open(sFilename, 'w')

        for iMonth in range(1, 13):
            sMonth =  "{:02d}".format(iMonth)
            dummy = monthrange(iYear, iMonth)
            day_in_month = dummy[1]
            for iDay in range(1, day_in_month+1):
                sDay =  "{:02d}".format(iDay)

                sLine = sYear + ', ' + sMonth + ', ' + sDay + '\n'
                ofs.write(sLine)

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
    swat_prepare_csv_file_template(sFilename_configuration_in)