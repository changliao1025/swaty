import sys
import os
import numpy as np
import datetime
import calendar
import julian
import platform 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook

from numpy  import array



sPath_library_python = sWorkspace_code +  slash + 'python' + slash + 'library' + slash + 'eslib_python'
print(sPath_library_python)

sys.path.append(sPath_library_python)

from toolbox.reader.text_reader_string import text_reader_string
# we do not reply on line count, but instead on string flag
def swat_write_hru_template_file(iSubbasin_in, iHru_in, sFilename_hru_in, sFilename_hru_out):
    ifs=open(sFilename_hru_in, 'rb')   
    line = ifs.readline()
    line = line.decode("utf-8")
    ofs=open(sFilename_hru_out, 'w') 
    ofs.write('ptf $\n')
    while line:

        if "CN2" not in line: 
            ofs.write(line)
        else:
            #deal with it, we need to replace it 
            dummy = 'cn2'+ "{:02}".format(iSubbasin_in) \
            + "{:02}".format(iHru_in) 
            line = '       $' + dummy + '$' + '    | pest parameter CN2 \n'
            ofs.write(line)

        line = ifs.readline() 
        line = line.decode("utf-8")
    ifs.close()
    ofs.close()


#use this function to return a list of hru file
def swat_extract_hru_from_subbasin_file(iSubbasin_in, sWorkspace_simulation_in, sFilename_subbasin_in):
    #print(sFilename_subbasin_in)
    ifs=open(sFilename_subbasin_in, 'rb')   
    line = ifs.readline()
    #print(type(line))
    line = line.decode("utf-8")
    #line = line.split("\r\n")
    while line:
    # in python 2+
    # print line
    # in python 3 print is a builtin function, so
        #print(line)
        dummy = line.strip()
        if(dummy == '| HRU data'):
            line = ifs.readline()
            line = line.decode("utf-8")
            sDummy = line.split()
            nhru = int((sDummy[0]).strip())
        else:
            

        
       
            if(dummy == 'HRU: General'):

                for ihru in range (0, nhru):

                    #this is the subbasin line
                    line = ifs.readline()
                    line = line.decode("utf-8")
                    dummy = line[0:9]
                    sFilename_hru = sWorkspace_simulation_in + slash + dummy + '.mgt'
                    sFilename_hru_out = sWorkspace_simulation_in + slash + dummy + '.mgt.tpl'
                    iHru_in  = ihru + 1
                    swat_write_hru_template_file(iSubbasin_in, iHru_in, sFilename_hru, sFilename_hru_out)
                    #call another function to read 
                    #go to the next subbasin
            else:
                line = ifs.readline() 
                #print(line)
                line = str(line, errors='ignore')
                #line = line.decode("utf-8")
    ifs.close()
    return nhru



#the main function 
def swat_prepare_pest_template_file_old(sFilename_configuration_in):
    
    sWorkspace_home = config['sWorkspace_home']
    sWorkspace_data = config['sWorkspace_data']
    sWorkspace_scratch=config['sWorkspace_scratch']
    sWorksapce_raw = config['sWorkspace_raw']    
    sWorkspace_project = config['sWorkspace_project']
    sWorkspace_simulation = config['sWorkspace_simulation']
    
    pest_mode =  config['pest_mode'] 
    sRegion = config['sRegion']

    sWorkspace_data = sWorkspace_data + slash + sWorkspace_project
    sWorkspace_simulation = sWorkspace_scratch +  slash  + sWorkspace_simulation
    
    sWorkspace_swat_out = sWorkspace_simulation
    sWorkspace_pest = sWorkspace_simulation

    start_year = int(config['start_year'] )
    start_year_spinup = int(config['start_year_spinup'] )
    end_year  = int( config['end_year'] )
   
    nsegment = int( config['nsegment'] )

    #read watershed configuration
    sFilename_fig = sWorkspace_simulation + slash + 'fig.fig'
    #print(sFilename_fig)
    ifs=open(sFilename_fig, 'r')   
    line = ifs.readline()
    sFilename =  sWorkspace_data + slash + 'auxiliary' + slash + 'subbasin' + slash + 'subbasin_hru.ini'
    
    ofs=open(sFilename, 'w')
    iSubbasin = 1
    while line:
    # in python 2+
    # print line
    # in python 3 print is a builtin function, so
        #print(line)
        sDummy = line.split()
        if(len(sDummy) > 0):
            #print(sDummy)
            sDummy = (sDummy[0]).strip()
            if(sDummy == 'subbasin'):
                #this is the subbasin line
                line = ifs.readline()
                sDummy = line.split()
                dummy  = (sDummy[0]).strip()
                sFilename_subbasin = sWorkspace_simulation + slash + dummy
                
                nhru = swat_extract_hru_from_subbasin_file(iSubbasin, sWorkspace_simulation, sFilename_subbasin)
                #print(sFilename_subbasin)

                #write subbasin 
                dummy = str(iSubbasin) + ' ' + str(nhru) + '\n'
                ofs.write(dummy)
                iSubbasin = iSubbasin + 1
                line = ifs.readline()  
                #call another function to read 
                #go to the next subbasin
            else:
                line = ifs.readline()   

        else:
            pass
    # use realine() to read next line


        
        

    ifs.close()
    ofs.close()



    print('The PEST template file is prepared successfully!')
if __name__ == '__main__':
    import os
    cluster = 'snyder'
    if(cluster=='snyder'):
        sFilename_configuration_in = '/scratch/snyder/l/liao46/snyder/03model/swat/purgatoire30/simulation/parallel/purgatoire30.txt'
    else:
        sFilename_configuration_in = '/pic/scratch/liao313/03model/swat/purgatoire30/simulation/parallel/purgatoire30.txt'
    swat_prepare_pest_template_file(sFilename_configuration_in)
