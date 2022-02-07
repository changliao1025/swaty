import sys
import os
import numpy as np
import datetime
import calendar

from numpy  import array



from pyearth.toolbox.reader.text_reader_string import text_reader_string

def swat_extract_et(sFilename_configuration_in, sCase_in = None, sModel_in = None):
    """
    extract discharge from swat model simulation
    """
    
    if sCase_in is not None:
        print(sCase_in)
        sCase = sCase_in
    else:
        #by default, this model will run in steady state
        sCase = 'ss'

    sWorkspace_scratch = config['sWorkspace_scratch']

    sWorkspace_calibration_relative = config['sWorkspace_calibration']
    sWorkspace_simulation_relative = config['sWorkspace_simulation']

    sWorkspace_simulation = sWorkspace_scratch + slash + sWorkspace_simulation_relative  + slash  + sCase
    sWorkspace_calibration = sWorkspace_scratch + slash + sWorkspace_calibration_relative  + slash  + sCase

    sWorkspace_pest_model = sWorkspace_calibration + slash + sModel
    
    iYear_start = int(config['iYear_start'] )
    iYear_spinup_end = int(config['iYear_spinup_end'] )
    iYear_end  = int( config['iYear_end'] )
    nsegment = int( config['nsegment'] )
    nhru = int( config['nhru'] )

    dSimulation_start = datetime.datetime(iYear_start, 1, 1)  #year, month, day
    dSimulation_transient_start = datetime.datetime(iYear_spinup_end + 1, 1, 1)  #year, month, day
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
            sPath_current = sWorkspace_simulation
        else:
            sPath_current = os.getcwd()
    print('The current path is: ' + sPath_current)
    sWorkspace_slave = sPath_current

    sFilename_in = sWorkspace_slave + slash + 'output.hru'

    ifs = open(sFilename_in, "r")
    #read the unused line
    for i in range(8):
        sLine=(ifs.readline()).rstrip()
        print(sLine)
    
    #read the head line
    sLine=(ifs.readline()).rstrip()
    print(sLine)
    #now read the actual data
    aPet = np.full( nstress , 0.0, dtype = float )
    aEt = np.full( nstress , 0.0, dtype = float )


    #sFilename_pet = sWorkspace_simulation + slash + 'tinpan_pet.txt'
    #ofs = open(sFilename_pet, 'w')

    aIndex = [383, 384]
    for i in range(nstress):
        aPet1 = np.full( 13 , 0.0, dtype = float )
        for j  in range(nhru):
            sLine=(ifs.readline()).rstrip()
            sDummy = sLine.split()
            pet = sDummy[10]
            et =  sDummy[11]
            if(j == 383):
                aPet1[0] = pet
            if(j == 384):
                aPet1[1] = pet
            if(j == 386):
                aPet1[2] = pet
            if(j == 387):
                aPet1[3] = pet
            if(j == 388):
                aPet1[4] = pet
            if(j == 389):
                aPet1[5] = pet
            if(j == 390):
                aPet1[6] = pet
            if(j == 391):
                aPet1[7] = pet
            if(j == 392):
                aPet1[8] = pet
            if(j == 393):
                aPet1[9] = pet
            if(j == 397):
                aPet1[10] = pet
            if(j == 398):
                aPet1[10] = pet
            if(j == 399):
                aPet1[11] = pet
        
        aPet[i] = np.mean(aPet1)
        #sLine_out =  "{:03f}".format( aPet[i]) + '\n'
        #ofs.write(sLine_out)
            
            
    #save to a file
    ifs.close()


    #save it to a text file
    sFilename_out = sWorkspace_simulation + slash + 'tinpan_pet.txt'

    np.savetxt(sFilename_out, aPet, delimiter=",")
    
    print('finished extracting et')



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

    swat_extract_et(sFilename_configuration, sCase, sModel)

