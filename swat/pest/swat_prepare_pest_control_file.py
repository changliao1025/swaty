import sys
import os
import numpy as np
import datetime
import calendar


from numpy  import array

            
sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'
sys.path.append(sPath_library_python)
from toolbox.reader.text_reader_string import text_reader_string



def swat_prepare_pest_control_file(sFilename_configuration_in, sModel):
    """
    #prepare the pest control file
    """
    

    
    #strings
    sWorkspace_home = config['sWorkspace_home']
    sWorkspace_scratch = config['sWorkspace_scratch']

    
    sWorkspace_data_relative = config['sWorkspace_data']
    sWorkspace_project_ralative = config['sWorkspace_project']
    sWorkspace_simulation_relative = config['sWorkspace_simulation']
    sWorkspace_calibration_relative = config['sWorkspace_calibration']
    
    pest_mode =  config['pest_mode'] 
    sRegion = config['sRegion']

    sWorkspace_data = sWorkspace_scratch + slash + sWorkspace_data_relative

    sWorkspace_data_project = sWorkspace_data + slash + sWorkspace_project_ralative

    sWorkspace_simulation = sWorkspace_scratch +  slash  + sWorkspace_simulation_relative
    sWorkspace_calibration = sWorkspace_scratch + slash + sWorkspace_calibration_relative

    
    sWorkspace_pest_model = sWorkspace_calibration + slash + sModel
    sWorkspace_simulation_copy = sWorkspace_simulation + slash + 'copy' + slash + 'TxtInOut'

    if not os.path.exists(sWorkspace_simulation_copy):
        print("The simulation folder is missing")
        return
    else:
        pass
    
    #number
    iYear_start = int(config['iYear_start'] )
    #the end year of spinup
    iYear_spinup_end = int(config['iYear_spinup_end'] )
    iYear_end  = int( config['iYear_end'] )
    nsegment = int( config['nsegment'] )
    
    npargp = int(config['npargp'] )
    nprior = int(config['nprior'] )
    nobsgp = int(config['nobsgp'] )

    ntplfile = int(config['ntplfile'] )
    ninsfle = int(config['ninsfle'] )
    sFilename_watershed_configuration = sWorkspace_data_project + slash \
    + 'auxiliary' + slash  + 'subbasin' + slash + 'watershed_configuration.txt'
    if os.path.isfile(sFilename_watershed_configuration):
        pass
    else:
        print(sFilename_watershed_configuration + ' is missing!')
        return
    
    aData_all = text_reader_string(sFilename_watershed_configuration, delimiter_in=',')

    aSubbasin= aData_all[:,0].astype(int)
    aHru = aData_all[:,1].astype(int)
    nsubbasin = len(aSubbasin)

    sFilename_hru_combination =  sWorkspace_data_project + slash \
    + 'auxiliary' + slash + 'hru' + slash + 'hru_combination.txt'
    if os.path.isfile(sFilename_hru_combination):
        pass
    else:
        print(sFilename_hru_combination + ' is missing!')
        return
    
    aData_all=text_reader_string(sFilename_hru_combination, delimiter_in=',')
    nhru = len(aData_all)
    
    npar = nhru

    sFilename = sWorkspace_data_project + slash + 'auxiliary' + slash \
    + 'usgs'+slash+ 'discharge' + slash + 'discharge_observation.txt'
    if os.path.isfile(sFilename):
        pass
    else:
        print(sFilename + ' is missing!')
        return
    
    aData_all = text_reader_string(sFilename, delimiter_in=',')
    obs= array( aData_all).astype(float)
    good_index = np.where(obs != missing_value)
    nobs_with_missing_value = len(obs)
    nobs = len(good_index[0])

    svd = 1
    if svd == 1:
        rlambda1 = 10
        numlam = 9
    else:
        rlambda1 = 0
        numlam = 1
    rlamfac = 3.0 #the rlambda1 change factor
    phiratsuf = 0.3  #the iteration criteria
    phiredlam = 0.01
    relparmax = 3
    facparmax = 3
    facorig = 0.0001
    phiredswh = 0.1
    noptmax = 20       #temination criteria
    phiredstp = 0.005
    nphistp = 5
    nphinored = 4
    relparstp = 0.01
    nrelpar = 4
    icov = 1
    icor = 1
    ieig = 1
    derinc = 0.01
    derinclb = 0.1
    derincmul = 1.5
    inctyp = 'relative'
    forcen = 'switch'
    dermthd = 'parabolic'
    partrans ='none'

    cn2_init = 60
    cn2_min = 10
    cn2_max = 100
    #we need define the input within the configuration file

    sFilename_control = sWorkspace_pest_model + slash + sRegion + '_swat.pst'
    ofs = open(sFilename_control, 'w')
    ofs.write('pcf\n')
    ofs.write('* control data\n')
    ofs.write('restart ' + pest_mode  + '\n' ) 
    #third line
    sLine = "{:0d}".format(npar)  + ' ' \
     +  "{:0d}".format(nobs)  + ' ' \
     +  "{:0d}".format(npargp)  + ' ' \
     +  "{:0d}".format(nprior)  + ' ' \
     +  "{:0d}".format(nobsgp)  + '\n'
    ofs.write(sLine) 
    #fourth line
    sLine = "{:0d}".format(ntplfile)  + ' ' \
     +  "{:0d}".format(ninsfle)  +  ' '\
     + ' double point ' \
     + '1 0 0 \n'
    ofs.write(sLine) 
    #fifth line
    sLine = "{:0.3f}".format(rlambda1)  + ' ' \
     +  "{:0.3f}".format(rlamfac)  + ' ' \
     +  "{:0.3f}".format(phiratsuf)  + ' ' \
     +  "{:0.3f}".format(phiredlam)  + ' ' \
     +  "{:0d}".format(numlam)  + '\n'
    ofs.write(sLine)
    #sixth line
    sLine = "{:0d}".format(relparmax)  + ' ' \
     +  "{:0d}".format(facparmax)  + ' ' \
     +  "{:0.4f}".format(facorig)  + '\n'
    ofs.write(sLine)
    #seventh line
    sLine = "{:0.3f}".format(phiredswh) + '\n'
    ofs.write(sLine)

    sLine = "{:02d}".format(noptmax)  + ' ' \
     +  "{:0.3f}".format(phiredstp)  + ' ' \
     +  "{:0d}".format(nphistp)  + ' ' \
     +  "{:0d}".format(nphinored)  + ' ' \
      +  "{:0.3f}".format(relparstp)  + ' ' \
     +  "{:0d}".format(nrelpar)  + '\n'
    ofs.write(sLine)

    sLine = "{:0d}".format(icov)  + ' ' \
     +  "{:0d}".format(icor)  + ' ' \
     +  "{:0d}".format(ieig)  + '\n'
    ofs.write(sLine)

    ofs.write('* singular value decomposition\n')
    ofs.write('1\n')
    sLine = "{:0d}".format(npar)  + ' ' \
       +  "{:0.4f}".format(1E-4)  + '\n'
    ofs.write(sLine)
    ofs.write('1\n')
    ofs.write( '* parameter groups\n'  )   

    sLine =  'para_gp1 ' \
              + inctyp + ' '\
              + "{:0.3f}".format(derinc)  + ' ' \
              +  "{:0.3f}".format(derinclb)  + ' ' \
              +  forcen  + ' ' \
              +  "{:0.3f}".format(derincmul)  + ' ' \
              +  dermthd  + '\n'
    ofs.write(sLine)

    parchglim = 'relative'
    ofs.write('* parameter data\n')
   
    for ihru_type in range(0, nhru):
        sLine = 'cn2' + "{:03d}".format(ihru_type+1) + ' ' \
          + partrans + ' ' \
          + parchglim + ' '\
          + "{:0.3f}".format(cn2_init) + ' ' \
          + "{:0.3f}".format(cn2_min) + ' ' \
          +"{:0.3f}".format(cn2_max) + ' ' \
          + ' para_gp1 1.0 0.0 1\n'
        ofs.write(sLine)

    ofs.write('* observation groups\n')
    ofs.write( 'discharge\n')
    ofs.write( '* observation data\n')
    
    
    obs = np.reshape(obs, nobs_with_missing_value)
    for i in range(0, nobs_with_missing_value):
        if obs[i] != missing_value:
            sLine = 'discharge' + "{:04d}".format(i+1)   + ' ' \
               + "{:0.4f}".format(obs[i])  + ' 1.0 ' + ' discharge\n'
            ofs.write(sLine)
        else:
            pass

    ofs.write('* model command line\n')

    #run the model
    sLine  = sWorkspace_pest_model + slash + 'run_swat_model\n'
    ofs.write(sLine)

    
    ofs.write('* model input/output\n')

    #sLine1 = sWorkspace_pest_model + slash + 'watershed.tpl'    
    #sLine2 = sWorkspace_pest_model + slash + 'watershed.para\n'
    #sLine = sLine1 + ' ' + sLine2
    #ofs.write(sLine)

    #sLine1 = sWorkspace_pest_model + slash + 'subbasin.tpl'    
    #sLine2 = sWorkspace_pest_model + slash + 'subbasin.para\n'
    #sLine = sLine1 + ' ' + sLine2
    #ofs.write(sLine)

    sLine1 = sWorkspace_pest_model + slash + 'hru.tpl'    
    sLine2 = 'hru.para\n'
    sLine = sLine1 + ' ' + sLine2
    ofs.write(sLine)

    #result
    sFilename_instruction = config['sFilename_instruction']

    sFilename_instruction = sWorkspace_pest_model + slash + sFilename_instruction
    sFilename_result =  config['sFilename_result']
    sLine = sFilename_instruction + ' '  + sFilename_result + '\n'
    ofs.write(sLine)

    phimlim = 1.0
    phimaccept = 1.05 * phimlim
    wfinit = 0.5
    wfmin = 0.1
    wfmax = 10
    wffac = 1.5
    wftol = 0.1
    iregadj = 0


    if pest_mode  == 'estimation' :
        pass
    else:
        ofs.write(' * regularisation\n')
        sLine = "{:0.3f}".format(phimlim) + ' '  \
          + "{:0.3f}".format(phimaccept) + ' '   + '\n'
        ofs.write(sLine)    

        sLine = "{:0.3f}".format(wfinit) + ' '  \
             + "{:0.3f}".format(wfmin) + ' '  \
              + "{:0.3f}".format(wfmax) + ' '  + '\n'
        ofs.write(sLine)    
    
        sLine = "{:0.3f}".format(wffac) + ' '  \
            + "{:0.3f}".format(wftol) + ' ' \
             + "{:0.3f}".format(iregadj) + ' '   + '\n'
        ofs.write(sLine)
        pass


    ofs.close()

    print('The PEST control file is prepared successfully at: ' + sFilename_control)


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
    swat_prepare_pest_control_file(sFilename_configuration_in, sModel)
