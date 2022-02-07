
import os
import sys
import glob
import numpy as np
from pathlib import Path
from shutil import copyfile
from abc import ABCMeta, abstractmethod
import datetime
from shutil import copy2
import json
from json import JSONEncoder

from pyswat.auxiliary.text_reader_string import text_reader_string
from pyswat.auxiliary.line_count import line_count


pDate = datetime.datetime.today()
sDate_default = "{:04d}".format(pDate.year) + "{:02d}".format(pDate.month) + "{:02d}".format(pDate.day)

class CaseClassEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.float32):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, list):
            pass  
        
       
            
        return JSONEncoder.default(self, obj)

class swatcase(object):
    __metaclass__ = ABCMeta
    iCase_index=0
    iSiteID=0
    iFlag_simulation=1
    iFlag_calibration=0
    iFlag_watershed=0
    iFlag_subbasin=0
    iFlag_hru=0
    iFlag_mode=0
    iYear_start=0
    iYear_end=0
    iMonth_start=0
    iMonth_end=0
    iDay_start=0
    iDay_end=0
    nstress=0
    nsegment =0
    nhru=0

    aConfig_in=None
    aParameter_watershed = None
    aParameter_subbasin = None
    aParameter_hru = None

    aParameter_value=None
    aParameter_value_watershed = None
    aParameter_value_subbasin = None
    aParameter_value_hru = None

    aParameter_value_lower_watershed = None
    aParameter_value_lower_subbasin = None
    aParameter_value_lower_hru       = None

    aParameter_value_upper_watershed = None
    aParameter_value_upper_subbasin = None
    aParameter_value_upper_hru       = None

    nParameter=0
    nParameter_watershed=0
    nParameter_subbasin=0
    nParameter_hru=0

    sFilename_model_configuration=''
    sWorkspace_data=''
    sWorkspace_scratch=''    
    sWorkspace_project=''    
    sWorkspace_simulation=''
    sWorkspace_simulation_case=''
    sWorkspace_calibration=''
    sWorkspace_calibration_case=''
    sFilename_model_configuration=''
    sFilename_observation_discharge=''
    sRegion=''
    sModel=''
    sCase=''
    sDate=''
    sSiteID=''
    sDate_start =''
    sDate_end=''

    def __init__(self, aConfig_in):
        self.sFilename_model_configuration    = aConfig_in[ 'sFilename_model_configuration']
        self.sWorkspace_home = aConfig_in[ 'sWorkspace_home']
        self.sWorkspace_data = aConfig_in[ 'sWorkspace_data']
       
        self.sWorkspace_scratch    = aConfig_in[ 'sWorkspace_scratch']
        sWorkspace_scratch = self.sWorkspace_scratch
        sWorkspace_data=self.sWorkspace_data
        self.sRegion               = aConfig_in[ 'sRegion']
        self.sModel                = aConfig_in[ 'sModel']
        self.sPython               = aConfig_in[ 'sPython']
        #self.sDate_start              = aConfig_in[ 'sDate_start']
        #self.sDate_end                = aConfig_in[ 'sDate_end']
        self.nsegment = int( aConfig_in[ 'nsegment'] )
        self.nsubbasin = int (aConfig_in[ 'nsubbasin'])

        self.sWorkspace_project= aConfig_in[ 'sWorkspace_project']
        self.sWorkspace_bin= aConfig_in[ 'sWorkspace_bin']

        self.sWorkspace_simulation = str(Path(self.sWorkspace_scratch ) / self.sModel / self.sRegion / 'simulation')
        
        sPath = self.sWorkspace_simulation
        Path(sPath).mkdir(parents=True, exist_ok=True)

        self.sWorkspace_calibration = str(Path(self.sWorkspace_scratch ) / self.sModel / self.sRegion / 'calibration')
        sPath = self.sWorkspace_calibration
        Path(sPath).mkdir(parents=True, exist_ok=True)

        iCase_index = int(aConfig_in['iCase_index'])
        sCase_index = "{:03d}".format( iCase_index )
        sDate   = aConfig_in[ 'sDate']
        if sDate is not None:
            self.sDate= sDate
        else:
            self.sDate = sDate_default
        self.iCase_index =   iCase_index
        sCase = self.sModel + self.sDate + sCase_index
        self.sCase = sCase
        

        self.sWorkspace_simulation_case = str(Path(self.sWorkspace_simulation ) / sCase )
        sPath = self.sWorkspace_simulation_case
        Path(sPath).mkdir(parents=True, exist_ok=True)

        self.sWorkspace_calibration_case = str(Path(self.sWorkspace_calibration ) / sCase )
        sPath = self.sWorkspace_calibration_case
        Path(sPath).mkdir(parents=True, exist_ok=True)

        self.iFlag_calibration =  int(aConfig_in['iFlag_calibration']) 
        self.iFlag_simulation =  int(aConfig_in['iFlag_simulation']) 
        self.iFlag_watershed =  int(aConfig_in['iFlag_watershed']) 
        self.iFlag_subbasin =  int(aConfig_in['iFlag_subbasin']) 
        self.iFlag_hru =  int(aConfig_in['iFlag_hru']) 
        self.sFilename_observation_discharge = aConfig_in[ 'sFilename_observation_discharge']
        self.sFilename_swat = aConfig_in[ 'sFilename_swat']
        

        self.iYear_start  = int( aConfig_in['iYear_start'] )
        self.iYear_end    = int( aConfig_in['iYear_end']   )
        self.iMonth_start = int( aConfig_in['iMonth_start'])
        self.iMonth_end   = int( aConfig_in['iMonth_end']  ) 
        self.iDay_start   = int( aConfig_in['iDay_start']  )
        self.iDay_end     = int( aConfig_in['iDay_end']    )
        self.nstress      = int( aConfig_in['nstress']     )

        iMonth_count = 0
        for iYear in range( self.iYear_start, self.iYear_end +1):
            if iYear == self.iYear_start:
                iMonth_start = self.iMonth_start
            else:
                iMonth_start = 1

            if iYear == self.iYear_end :
                iMonth_end = self.iMonth_end
            else:
                iMonth_end = 12

            for iMonth in range(iMonth_start, iMonth_end+1):
                iMonth_count = iMonth_count  + 1
                pass
        
        self.sWorkspace_data_project = str(Path(self.sWorkspace_data ) / self.sWorkspace_project )
        #read hru type
        if 'nhru' in aConfig_in:
            nhru = int( aConfig_in['nhru']) 
            if nhru > 1:
                self.nhru = nhru
            else:
                self.nhru=9
        
        

        self.nstress_month = iMonth_count

        self.iFlag_mode   = int( aConfig_in['iFlag_mode']) 
        self.iFlag_replace_parameter= int( aConfig_in['iFlag_replace_parameter'] ) 

        #for replace and calibration
        self.aParameter_value =  aConfig_in['aParameter_value'] #this should be a variable sized array
        self.aParameter_value_lower =  aConfig_in['aParameter_value_lower'] #this should be a variable sized array
        self.aParameter_value_upper =  aConfig_in['aParameter_value_upper'] #this should be a variable sized array
        self.aParameter =  aConfig_in['aParameter']  #list

        if self.aParameter is not None:
            self.aParameter_watershed, self.aParameter_subbasin, self.aParameter_hru,\
                self.aParameter_value_watershed, self.aParameter_value_subbasin, self.aParameter_value_hru, \
                self.aParameter_value_lower_watershed, self.aParameter_value_lower_subbasin, self.aParameter_value_lower_hru, \
                  self.aParameter_value_upper_watershed, self.aParameter_value_upper_subbasin, self.aParameter_value_upper_hru \
               = self.define_parameter(self.aParameter, self.aParameter_value, self.aParameter_value_lower, self.aParameter_value_upper)
        
            self.nParameter_watershed = self.aParameter_watershed.size
            self.nParameter_subbasin = self.aParameter_subbasin.size
            self.nParameter_hru = self.aParameter_hru.size

            self.nParameter = self.nParameter_watershed \
                + self.nParameter_subbasin * self.nsubbasin \
                    + self.nParameter_hru  *  self.nhru
            pass

        self.sJob =  aConfig_in['sJob'] 

        

        #self.sWorkspace_simulation_copy = self.sWorkspace_data  + aConfig_in['sWorkspace_simulation_copy']
        self.sWorkspace_simulation_copy =  str(Path(self.sWorkspace_calibration ) / 'TxtInOut' )
        #self.sFilename_hru_combination = self.sWorkspace_data_project + slash + 'auxiliary' + slash\
        # + 'hru' + slash   + 'hru_combination.txt'       
        self.sFilename_hru_combination =   aConfig_in['hru_combination_file'] 
        self.sFilename_watershed_configuration = aConfig_in['sFilename_watershed_configuration'] 
        self.sFilename_hru_info = aConfig_in['sFilename_hru_info'] 

        return

    def define_parameter(self, aParameter_in, aValue_in, aValue_lower_in, aValue_upper_in):

        aParameter_watershed_all = np.array(['SFTMP','SMTMP','AI0'])
        aParameter_subbasin_all = np.array(['CH_K2','CH_N2'])
        aParameter_hru_all = np.array(['CN2'])

        aParameter_watershed = list()
        aParameter_subbasin     = list()
        aParameter_hru       = list()
        aParameter_value_watershed = list()
        aParameter_value_lower_watershed = list()
        aParameter_value_upper_watershed = list()

        aParameter_value_subbasin     = list()
        aParameter_value_lower_subbasin = list()
        aParameter_value_upper_subbasin = list()
        aParameter_value_hru       = list()
        aParameter_value_lower_hru  = list()
        aParameter_value_upper_hru  = list()

        aParameter_in= np.array(aParameter_in)
        nParameter  = aParameter_in.size


        for i in range(nParameter):
            sParameter  = aParameter_in[i]
            aValue = aValue_in[i]
            aValue_lower = aValue_lower_in[i]
            aValue_upper = aValue_upper_in[i]
            if sParameter in aParameter_watershed_all:
                aParameter_watershed.append(sParameter)
                aParameter_value_watershed.append(aValue)
                aParameter_value_lower_watershed.append(aValue_lower)
                aParameter_value_upper_watershed.append(aValue_upper)
            else: 
                if sParameter in aParameter_subbasin_all:
                    aParameter_subbasin.append(sParameter)
                    aParameter_value_subbasin.append(aValue)
                    aParameter_value_lower_subbasin.append(aValue_lower)
                    aParameter_value_upper_subbasin.append(aValue_upper)
                else:
                    if sParameter in aParameter_hru_all:
                        aParameter_hru.append(sParameter)
                        aParameter_value_hru.append(aValue)
                        aParameter_value_lower_hru.append(aValue_lower)
                        aParameter_value_upper_hru.append(aValue_upper)

            pass

        aParameter_watershed = np.array(aParameter_watershed)
        aParameter_subbasin = np.array(aParameter_subbasin)
        aParameter_hru = np.array(aParameter_hru)

        aParameter_value_watershed = np.array(aParameter_value_watershed)
        aParameter_value_subbasin =     np.array(aParameter_value_subbasin)
        aParameter_value_hru =       np.array(aParameter_value_hru)

        aParameter_value_lower_watershed = np.array(aParameter_value_lower_watershed)
        aParameter_value_lower_subbasin =     np.array(aParameter_value_lower_subbasin)
        aParameter_value_lower_hru =       np.array(aParameter_value_lower_hru)

        aParameter_value_upper_watershed = np.array(aParameter_value_upper_watershed)
        aParameter_value_upper_subbasin =     np.array(aParameter_value_upper_subbasin)
        aParameter_value_upper_hru =       np.array(aParameter_value_upper_hru)


        return aParameter_watershed, aParameter_subbasin, aParameter_hru,\
            aParameter_value_watershed,aParameter_value_subbasin,aParameter_value_hru,\
                aParameter_value_lower_watershed, aParameter_value_lower_subbasin,  aParameter_value_lower_hru,\
                aParameter_value_upper_watershed, aParameter_value_upper_subbasin, aParameter_value_upper_hru       
        

    def copy_TxtInOut_files(self):
        """
        sFilename_configuration_in
        sModel
        """
              
        sWorkspace_simulation_copy = self.sWorkspace_simulation_copy
        sWorkspace_simulation_case = self.sWorkspace_simulation_case      

        if self.iFlag_calibration == 1:
            sWorkspace_target_case = os.getcwd()
        else:
            sWorkspace_target_case = sWorkspace_simulation_case   


        if not os.path.exists(sWorkspace_simulation_copy):
            print(sWorkspace_simulation_copy)
            print('The simulation copy does not exist!')
            return
        else:      
            pass
        
        Path(sWorkspace_target_case).mkdir(parents=True, exist_ok=True)
        #the following file will be copied    

        aExtension = ('.pnd','.rte','.sub','.swq','.wgn','.wus',\
                '.chm','.gw','.hru','.mgt','sdr','.sep',\
                 '.sol','ATM','bsn','wwq','deg','.cst',\
                 'dat','fig','cio','fin','dat','.pcp','.tmp'  )

        #we need to be careful that Tmp is different in python/linux with tmp


        for sExtension in aExtension:
            sDummy = '*' + sExtension
            sRegax = os.path.join(str(Path(sWorkspace_simulation_copy)  ) ,  sDummy  )

            #sRegax = sWorkspace_simulation_copy + slash + '*' + sExtension

            if sExtension == '.tmp':
                for sFilename in glob.glob(sRegax):
                    sBasename_with_extension = os.path.basename(sFilename)
                    sFilename_new = os.path.join(str(Path(sWorkspace_target_case)) ,  sBasename_with_extension.lower()  )
                    #sFilename_new = sWorkspace_target_case + slash + sBasename_with_extension.lower()
                    copyfile(sFilename, sFilename_new)
            else:

                for sFilename in glob.glob(sRegax):
                    sBasename_with_extension = os.path.basename(sFilename)
                    sFilename_new = os.path.join(str(Path(sWorkspace_target_case)) ,  sBasename_with_extension  )
                    #sFilename_new = sWorkspace_target_case + slash + sBasename_with_extension
                    copyfile(sFilename, sFilename_new)



        print('Finished copying all input files')

    
    def setup(self):

        self.copy_TxtInOut_files()
        self.define_parameter()

        #replace parameter using parameter files
        if (self.iFlag_replace_parameter == 1) :
            self.pyswat_prepare_watershed_parameter_file()
            self.pyswat_write_watershed_input_file()    
            self.pyswat_prepare_subbasin_parameter_file()
            self.pyswat_write_subbasin_input_file()      
            self.pyswat_prepare_hru_parameter_file()
            self.pyswat_write_hru_input_file()        
        else:
            pass

        #step 5
        self.pyswat_copy_executable_file()
        #step 6
        sFilename_bash = self.pyswat_prepare_simulation_bash_file()
        #step 7
        sFilename_job = self.pyswat_prepare_simulation_job_file() 


        return

    def run(self):
        

        return    

    def evaluate(self):
        return
    
    def pyswat_prepare_watershed_parameter_file(self):
        """
        #prepare the pest control file
        """      
        sWorkspace_simulation_case = self.sWorkspace_simulation_case    
        sWorkspace_calibration_case = self.sWorkspace_calibration_case 

        iFlag_simulation = self.iFlag_simulation
        iFlag_watershed = self.iFlag_watershed


        aParameter_watershed = self.aParameter_watershed
        aParameter_value_watershed = self.aParameter_value_watershed

        nParameter_watershed = aParameter_watershed.size

        if iFlag_simulation == 1:
            sFilename_watershed_template = os.path.join(str(Path(sWorkspace_simulation_case)) ,  'watershed.para' )     
        else:
            sFilename_watershed_template = os.path.join(str(Path(sWorkspace_calibration_case)) ,  'watershed.para' )    
            pass
        
        if iFlag_watershed ==1:    
            ofs = open(sFilename_watershed_template, 'w')

            sLine = 'watershed'
            for i in range(nParameter_watershed):
                sVariable = aParameter_watershed[i]
                sLine = sLine + ',' + sVariable
            sLine = sLine + '\n'        
            ofs.write(sLine)

            sLine = 'watershed'
            for i in range(nParameter_watershed):
                sValue =  "{:5.2f}".format( aParameter_value_watershed[i] )            
                sLine = sLine + ', ' + sValue 
                print('watershed parameter: '+ sLine)

            sLine = sLine + '\n'
            ofs.write(sLine)
            ofs.close()
            print('watershed parameter is ready!')



        return

    def pyswat_prepare_subbasin_parameter_file(self):
        """
        #prepare the pest control file
        """      
        
        sWorkspace_simulation_case = self.sWorkspace_simulation_case    
        sWorkspace_calibration_case = self.sWorkspace_calibration_case 

        iFlag_simulation = self.iFlag_simulation
        iFlag_watershed = self.iFlag_watershed
        iFlag_subbasin = self.iFlag_subbasin
        iFlag_hru = self.iFlag_hru
        nsubbasin = self.nsubbasin

    
        aParameter_subbasin = self.aParameter_subbasin
        aParameter_value_subbasin = self.aParameter_value_subbasin
        nParameter_subbasin = self.nParameter_subbasin

        if iFlag_simulation == 1:
            sFilename_subbasin_template = os.path.join(str(Path(sWorkspace_simulation_case)) ,  'subbasin.para' )  
            #sFilename_subbasin_template = sWorkspace_simulation_case + slash + 'subbasin.para'   
    
        else:
            sFilename_subbasin_template = os.path.join(str(Path(sWorkspace_calibration_case)) ,  'subbasin.para' )  
            #sFilename_subbasin_template = sWorkspace_simulation_case + slash + 'basin.para'   

            pass
        
        
        
        if iFlag_subbasin ==1:    
            ofs = open(sFilename_subbasin_template, 'w')

            sLine = 'subbasin'
            for i in range(nParameter_subbasin):
                sVariable = aParameter_subbasin[i]
                sLine = sLine + ',' + sVariable
            sLine = sLine + '\n'        
            ofs.write(sLine)

            for iSubbasin in range(0, nsubbasin):
                sSubbasin = "{:03d}".format( iSubbasin + 1)
                sLine = 'subbasin' + sSubbasin 
                for i in range(nParameter_subbasin):
                    sValue =  "{:5.2f}".format( aParameter_value_subbasin[i] )            
                    sLine = sLine + ', ' + sValue 
                sLine = sLine + '\n'
                ofs.write(sLine)
            ofs.close()
            print('subbasin parameter is ready!')



        return

    def pyswat_prepare_hru_parameter_file(self):
        """
        #prepare the pest control file
        """      
   
        sWorkspace_simulation_case = self.sWorkspace_simulation_case    
        sWorkspace_calibration_case = self.sWorkspace_calibration_case 

        iFlag_simulation = self.iFlag_simulation
        iFlag_watershed = self.iFlag_watershed
        iFlag_subbasin = self.iFlag_subbasin
        iFlag_hru = self.iFlag_hru

        aParameter_hru = self.aParameter_hru
        aParameter_value_hru = self.aParameter_value_hru
        nParameter_hru = self.nParameter_hru

        #read hru type
        
        if os.path.isfile(self.sFilename_hru_combination):
            pass
        else:
            print('The file does not exist!')
            return
        aData_all = text_reader_string(self.sFilename_hru_combination)
        nhru_type = len(aData_all)

        if iFlag_simulation == 1:
            sFilename_hru_template = os.path.join(str(Path(sWorkspace_simulation_case)) ,  'hru.para' )  
            #sFilename_hru_template = sWorkspace_simulation_case + slash + 'hru.para'   
        else:
            sFilename_hru_template = os.path.join(str(Path(sWorkspace_calibration_case)) ,  'hru.para' )  
            #sFilename_hru_template = sWorkspace_simulation_case + slash + 'hru.para'    
            pass
       

        if iFlag_hru ==1:    
            ofs = open(sFilename_hru_template, 'w')

            sLine = 'hru'
            for i in range(nParameter_hru):
                sVariable = aParameter_hru[i]
                sLine = sLine + ',' + sVariable
            sLine = sLine + '\n'        
            ofs.write(sLine)

            for iHru_type in range(0, nhru_type):
                sHru_type = "{:03d}".format( iHru_type + 1)
                sLine = 'hru'+ sHru_type 
                for i in range(nParameter_hru):
                    sValue =  "{:5.2f}".format( aParameter_value_hru[i] )            
                    sLine = sLine + ', ' + sValue 
                sLine = sLine + '\n'
                ofs.write(sLine)
            ofs.close()
            print('hru parameter is ready!')

        return

    def pyswat_write_watershed_input_file(self):
        """
        write the input files from the new parameter generated by PEST to each hru file
        """
        aParameter_watershed = self.aParameter_watershed

        nParameter_watershed = self.nParameter_watershed
        if(nParameter_watershed<1):        
            print("There is no watershed parameter to be updated!")
            return
        else:
            pass    
        
        iFlag_simulation = self.iFlag_simulation
        iFlag_calibration = self.iFlag_calibration


        sWorkspace_simulation_case = self.sWorkspace_simulation_case
        sWorkspace_simulation_copy =  self.sWorkspace_simulation_copy

        sWorkspace_calibration_case = self.sWorkspace_calibration_case
        sWorkspace_pest_model = sWorkspace_calibration_case
        print('sWorkspace_simulation_copy: ' + sWorkspace_simulation_copy)


        # we need to identify a list of files that are HRU defined, you can add others later
        #for watershed parameter, only one file extension is used so far
        aExtension = ['.bsn','.wwq']
        aBSN=['SFTMP','SMTMP']
        aWWQ=['AI0']


        aExtension = np.asarray(aExtension)
        nFile_type= len(aExtension)

        #the parameter is located in the different files
        aParameter_table = np.empty( (nFile_type)  , dtype = object )

        #need a better way to control this 
        for iVariable in range(nParameter_watershed):
            sParameter_watershed = aParameter_watershed[iVariable]

            if sParameter_watershed in aBSN:
                if( aParameter_table[0] is None  ):
                    aParameter_table[0] = np.array(sParameter_watershed)
                else:
                    aParameter_table[0] = np.append(aParameter_table[0],sParameter_watershed)
                    #aParameter_table[0].append(sParameter_watershed) 
                pass
            else:
                if sParameter_watershed in aWWQ:
                    if( aParameter_table[1] is None  ):
                        aParameter_table[1] = sParameter_watershed
                    else:
                        aParameter_table[1].append(sParameter_watershed) 
                    pass
                pass


        aParameter_user = np.full( (nFile_type) , None , dtype = np.dtype(object) )
        aParameter_count = np.full( (nFile_type) , 0 , dtype = int )
        aParameter_flag = np.full( (nFile_type) , 0 , dtype = int )
        aParameter_index = np.full( (nFile_type) , -1 , dtype = np.dtype(object) )
    
        #then we need to define what parameters may be calibrated
        #this list should include all possible parameters in the parameter file
    
        #read parameter file
        if iFlag_simulation == 1:
            sFilename_parameter = os.path.join(str(Path(sWorkspace_simulation_case)) ,  'watershed.para' )  
            #sFilename_parameter = sWorkspace_simulation_case + slash + 'watershed.para'
        else:
            iFlag_debug = 0
            sPath_current = os.getcwd()
            sFilename_parameter = os.path.join(str(Path(sPath_current)) ,  'watershed.para' )  
            #sFilename_parameter = sPath_current + slash + 'watershed.para'

        print(sFilename_parameter)
        #check whetheher the file exist or not
        if os.path.isfile(sFilename_parameter):
            pass
        else:
            print('The file does not exist: '+sFilename_parameter)
            return

        aData_all = text_reader_string(sFilename_parameter, cDelimiter_in =',')
        aDummy = aData_all[0,:]
        nParameter = len(aDummy) - 1
        aParameter_list = aDummy[1: nParameter+1]

        aParameter_value = (aData_all[1,1: nParameter+1]).astype(float)
        aParameter_value = np.array(aParameter_value)
        print(aParameter_value)

        for p in range(0, nParameter):
            para = aParameter_list[p]
            for i in range(0, nFile_type):
                aParameter_tmp = aParameter_table[i]
                if aParameter_tmp is not None:
                    if para in aParameter_tmp:
                        aParameter_count[i]= aParameter_count[i]+1
                        aParameter_flag[i]=1

                        if(aParameter_count[i] ==1):
                            aParameter_index[i] = [p]
                            aParameter_user[i]= [para]
                        else:
                            aParameter_index[i] = np.append(aParameter_index[i],[p])
                            aParameter_user[i] = np.append(aParameter_user[i],[para])
                        continue

                    
        if iFlag_simulation == 1:
            sWorkspace_source_case = sWorkspace_simulation_copy
            sWorkspace_target_case = sWorkspace_simulation_case
            pass
        else:
            sPath_current = os.getcwd()
            if (os.path.normpath(sPath_current)  == os.path.normpath(sWorkspace_pest_model)):
                print('this is the parent, no need to copy anything')
                return
            else:
                print('this is a child')
                sWorkspace_source_case = sWorkspace_simulation_copy
                sWorkspace_target_case = sPath_current

        for iFile_type in range(0, nFile_type):
            sExtension = aExtension[iFile_type]
            iFlag = aParameter_flag[iFile_type]
            if( iFlag == 1):
                #there should be only one for each extension       

                sFilename = 'basins' + sExtension
                sFilename_watershed = os.path.join(str(Path(sWorkspace_source_case)) ,  sFilename )  
                #sFilename_watershed = sWorkspace_source_case + slash + sFilename

                #open the file to read

                nline = line_count(sFilename_watershed)
                ifs=open(sFilename_watershed, 'rb')   

                #open the new file to write out
                #sFilename_watershed_out = sWorkspace_target_case + slash + sFilename    
                sFilename_watershed_out = os.path.join(str(Path(sWorkspace_target_case)) ,  sFilename )         

                if os.path.exists(sFilename_watershed_out):                
                    os.remove(sFilename_watershed_out)

                ofs=open(sFilename_watershed_out, 'w') 
                aValue = aParameter_value[:]
                for iLine in range(nline):
                    sLine0=(ifs.readline())
                    if len(sLine0) < 1:
                        continue
                    sLine0=sLine0.rstrip()
                    #print(sLine0)
                    sLine= sLine0.decode("utf-8", 'ignore')


                    for i in range(0, aParameter_count[iFile_type]):
                        aParameter_indices = np.array(aParameter_index[iFile_type])
                        aParameter_filetype = np.array(aParameter_user[iFile_type])
                        if 'sftmp' in sLine.lower() and 'SFTMP' in aParameter_filetype : 
                            dummy = 'SFTMP'   
                            dummy_index1 = np.where(aParameter_filetype == dummy)
                            dummy_index2 = aParameter_indices[dummy_index1][0]
                            sLine_new = "{:16.3f}".format(  aValue[dummy_index2]  )     + '    | pest parameter SFTMP' + '\n'
                            ofs.write(sLine_new)
                            print(sLine_new)
                            break #important
                        else:
                            if 'smtmp' in sLine.lower() and 'SMTMP' in aParameter_filetype: 
                                dummy = 'SMTMP'                             
                                dummy_index1 = np.where(aParameter_filetype == dummy)
                                dummy_index2 = aParameter_indices[dummy_index1][0]
                                sLine_new = "{:16.3f}".format(  aValue[dummy_index2]  )     + '    | pest parameter SMTMP' + '\n'
                                ofs.write(sLine_new)
                                print(sLine_new)
                                break  #important
                            else:
                                sLine = sLine + '\n'
                                ofs.write(sLine)
                                break  #important


                            
                            
                ifs.close()
                ofs.close()

        print('Finished writing watershed file!')
        return    

    def pyswat_write_subbasin_input_file(self):
        """
        write the input files from the new parameter generated by PEST to each hru file
        """
        aParameter_subbasin = self.aParameter_subbasin
        nvariable = aParameter_subbasin.size
        if(nvariable<1):
            #there is nothing to be replaced at all
            print("There is no subbasin parameter to be updated!")
            return
        else:
            pass    
        
        iFlag_simulation = self.iFlag_simulation
        iFlag_calibration = self.iFlag_calibration


        sWorkspace_simulation_case = self.sWorkspace_simulation_case
        sWorkspace_simulation_copy =  self.sWorkspace_simulation_copy

        sWorkspace_calibration_case = self.sWorkspace_calibration_case
        sWorkspace_pest_model = sWorkspace_calibration_case

        sWorkspace_data_project = self.sWorkspace_data_project
    
        nsubbasin = self.nsubbasin
    
        # we need to identify a list of files that are HRU defined, you can add others later
        aExtension = ['.rte', '.sub']
        #now we can add corresponding possible variables

        aRTE =['CH_K2','CH_N2' ]
        aSUB=[]

        aExtension = np.asarray(aExtension)
        nFile_type= aExtension.size

        #the parameter is located in the different files
        aParameter_table = np.empty( (nFile_type)  , dtype = object )

        #need a better way to control this 
        for iVariable in range(nvariable):
            sParameter_subbasin = aParameter_subbasin[iVariable]

            if sParameter_subbasin in aRTE:

                if( aParameter_table[0] is None  ):
                    aParameter_table[0] = np.array(sParameter_subbasin)
                else:
                    aParameter_table[0]= np.append(aParameter_table[0],sParameter_subbasin)            
            else:
                if sParameter_subbasin in aSUB:
                    pass
                pass


        aParameter_user = np.full( (nFile_type) , None , dtype = np.dtype(object) )
        aParameter_count = np.full( (nFile_type) , 0 , dtype = int )
        aParameter_flag = np.full( (nFile_type) , 0 , dtype = int )
        aParameter_index = np.full( (nFile_type) , -1 , dtype = np.dtype(object) )
    
        #then we need to define what parameters may be calibrated
        #this list should include all possible parameters in the parameter file
    
        #read parameter file
        #os.chdir('/global/cscratch1/sd/liao313/04model/swat/arw/calibration/swat20210723011/child3')
        #iFlag_simulation=0

        if iFlag_simulation == 1:
            #sFilename_parameter = sWorkspace_simulation_case + slash + 'subbasin.para'
            sFilename_parameter = os.path.join(str(Path(sWorkspace_simulation_case)) ,  'subbasin.para' )   
        else:
            iFlag_debug = 0        
            sPath_current = os.getcwd()
            #sFilename_parameter = sPath_current + slash + 'subbasin.para'
            sFilename_parameter = os.path.join(str(Path(sPath_current)) ,  'subbasin.para' )   

        print(sFilename_parameter)
        #check whetheher the file exist or not
        if os.path.isfile(sFilename_parameter):
            pass
        else:
            print('The file does not exist: '+sFilename_parameter)
            return

        aData_all = text_reader_string(sFilename_parameter, cDelimiter_in =',')
        aDummy = aData_all[0,:]
        nParameter = len(aDummy) - 1
        aParameter_list = aDummy[1: nParameter+1]

        aParameter_value = (aData_all[1:(nsubbasin+1),1: nParameter+1]).astype(float)
        aParameter_value = np.asarray(aParameter_value)

        for p in range(0, nParameter):
            para = aParameter_list[p]
            for i in range(0, nFile_type):
                aParameter_tmp = aParameter_table[i]
                if aParameter_tmp is not None:
                    if para in aParameter_tmp:
                        aParameter_count[i]= aParameter_count[i]+1
                        aParameter_flag[i]=1

                        if(aParameter_count[i] ==1):
                            aParameter_index[i] = [p]
                            aParameter_user[i]= [para]
                        else:
                            aParameter_index[i] = np.append(aParameter_index[i],[p])
                            aParameter_user[i] = np.append(aParameter_user[i],[para])
                        continue

                    
        if iFlag_simulation == 1:
            pass
        else:
            sPath_current = os.getcwd()
            if (os.path.normpath(sPath_current)  == os.path.normpath(sWorkspace_pest_model)):
                print('this is the parent, no need to copy anything')
                return
            else:
                print('this is a child')
                sWorkspace_source_case = sWorkspace_simulation_copy
                sWorkspace_target_case = sPath_current

        #iHru_index = 0 
        for iSubbasin in range(0, nsubbasin):
            #subbasin string
            sSubbasin = "{:05d}".format( iSubbasin + 1)

            #loop through all basin in this subbasin

            for iFile_type in range(0, nFile_type):
                #check whether these is parameter chanage or not
                sExtension = aExtension[iFile_type]
                iFlag = aParameter_flag[iFile_type]
                sFilename = sSubbasin + '0000' + sExtension


                if( iFlag == 1):

                    #sFilename_subbasin = sWorkspace_source_case  + slash + sFilename 
                    sFilename_subbasin = os.path.join(str(Path(sWorkspace_source_case)) ,  sFilename )   
                    #open the file to read
                    ifs=open(sFilename_subbasin, 'rb')   
                    sLine=(ifs.readline()).rstrip().decode("utf-8", 'ignore')
                    #open the new file to write out
                    #sFilename_subbasin_out = sWorkspace_target_case + slash + sFilename     
                    sFilename_subbasin_out = os.path.join(str(Path(sWorkspace_target_case)) ,  sFilename )
                    if os.path.exists(sFilename_subbasin_out):                 
                        os.remove(sFilename_subbasin_out)

                    print(sFilename_subbasin_out)

                    ofs=open(sFilename_subbasin_out, 'w') 
                    #because of the python interface, pest will no longer interact with model files directly
                    #starting from here we will                             
                    aValue = aParameter_value[iSubbasin, :]
                    while sLine:
                    
                        for i in range(0, aParameter_count[iFile_type]):
                            aParameter_indices = np.array(aParameter_index[iFile_type])
                            aParameter_filetype = np.array(aParameter_user[iFile_type])
                            if 'ch_k2' in sLine.lower()  and 'CH_K2' in aParameter_filetype:    
                                dummy_index1 = np.where(aParameter_filetype == 'CH_K2')                            
                                dummy_index2 = aParameter_indices[dummy_index1][0]
                                sLine_new = "{:14.5f}".format(  aValue[dummy_index2]  )     + '    | pest parameter ch_k2 \n'
                                ofs.write(sLine_new)                            
                                break                            
                            else:
                                if 'ch_n2' in sLine.lower() and 'CH_N2' in aParameter_filetype:                                
                                    dummy_index1 = np.where(aParameter_filetype == 'CH_N2')                               
                                    dummy_index2 = aParameter_indices[dummy_index1][0]
                                    sLine_new = "{:14.5f}".format(  aValue[dummy_index2]  )     + '    | pest parameter ch_n2 \n'
                                    ofs.write(sLine_new)    
                                    break
                                else:
                                    sLine = sLine + '\n'
                                    ofs.write(sLine)
                                    break

                        sLine0=(ifs.readline()).rstrip()
                        #print(sLine0)
                        sLine= sLine0.decode("utf-8", 'ignore')
                    #close files
                    ifs.close()
                    ofs.close()
                else:
                    #this file does not need to changed
                    pass

        print('Finished writing subbasin file!')
        return

    def pyswat_write_hru_input_file(self):
        """
        write the input files from the new parameter generated by PEST to each hru file
        """
        aParameter_hru = self.aParameter_hru
        nvariable = aParameter_hru.size
        if(nvariable<1):
            #there is nothing to be replaced at all
            print("There is no hru parameter to be updated!")
            return
        else:
            pass    
        
        iFlag_simulation = self.iFlag_simulation
        iFlag_calibration = self.iFlag_calibration


        sWorkspace_simulation_case = self.sWorkspace_simulation_case
        sWorkspace_simulation_copy =  self.sWorkspace_simulation_copy

        sWorkspace_calibration_case = self.sWorkspace_calibration_case
        sWorkspace_pest_model = sWorkspace_calibration_case

        sWorkspace_data_project = self.sWorkspace_data_project
    
        sFilename_watershed_configuration = self.sFilename_watershed_configuration
        sFilename_hru_info = self.sFilename_hru_info
        #sFilename_watershed_configuration = sWorkspace_data_project + slash \
        #+ 'auxiliary' + slash  + 'subbasin' + slash \
        #+ 'watershed_configuration.txt'

        #check whether file exist
        if os.path.isfile(sFilename_watershed_configuration):
            pass
        else:
            print('The file does not exist: ' + sFilename_watershed_configuration)
            return
        aSubbasin_hru  = text_reader_string( sFilename_watershed_configuration, cDelimiter_in = ',' )

        aSubasin = aSubbasin_hru[:,0].astype(int)
        aHru = aSubbasin_hru[:,1].astype(int)

        nsubbasin = len(aSubasin)
        nhru = sum(aHru)

        #sFilename_hru_info = sWorkspace_data_project + slash + 'auxiliary' + slash \
        #  + 'hru' + slash + 'hru_info.txt'
        if os.path.isfile(sFilename_hru_info):
            pass
        else:
            print('The file does not exist: ')
            return
        aHru_info = text_reader_string(sFilename_hru_info)
        aHru_info = np.asarray(aHru_info)
        nhru = len(aHru_info)
        aHru_info= aHru_info.reshape(nhru)

        #sFilename_hru_combination = sWorkspace_data_project + slash + 'auxiliary' + slash \
        #  + 'hru' + slash + 'hru_combination.txt'
        sFilename_hru_combination = self.sFilename_hru_combination
        if os.path.isfile(sFilename_hru_combination):
            pass
        else:
            print('The file does not exist: ')
            return
        aHru_combination = text_reader_string(sFilename_hru_combination)
        aHru_combination = np.asarray(aHru_combination)

        nhru_type = len(aHru_combination)
        aHru_combination= aHru_combination.reshape(nhru_type)

        # we need to identify a list of files that are HRU defined, you can add others later
        aExtension = ('.chm','.gw','.hru','.mgt','.sdr', '.sep', '.sol')
        #now we can add corresponding possible variables


        aCHM =[]
        aGW = []
        aHRU =[]
        aMGT = ['CN2']
        aSDR = []
        aSEP =[]
        aSOL=['AWC']

        aExtension = np.asarray(aExtension)
        nFile_type= len(aExtension)

        #the parameter is located in the different files
        aParameter_table = np.empty( (nFile_type)  , dtype = object )

        #need a better way to control this 
        for iVariable in range(nvariable):
            sVariable = aParameter_hru[iVariable]

            if sVariable in aCHM:
                pass
            else:
                if sVariable in aGW:
                    pass
                else:
                    if sVariable in aHRU:
                        pass
                    else:
                        if sVariable in aMGT:
                            if( aParameter_table[3] is None  ):
                                aParameter_table[3] = sVariable
                            else:
                                aParameter_table[3].append(sVariable)                             
                        else:
                            if sVariable in aSDR:
                                pass
                            else: 
                                if sVariable in aSEP:
                                    pass
                                else:
                                    if sVariable in aSOL:
                                        if( aParameter_table[6] is None  ):
                                            aParameter_table[6] = sVariable
                                        else:
                                            aParameter_table[6].append(sVariable) 
                                    else:
                                        pass
                                    
                                    

                                    

        aParameter_user = np.full( (nFile_type) , None , dtype = np.dtype(object) )
        aParameter_count = np.full( (nFile_type) , 0 , dtype = int )
        aParameter_flag = np.full( (nFile_type) , 0 , dtype = int )
        aParameter_index = np.full( (nFile_type) , -1 , dtype = np.dtype(object) )
    
        #then we need to define what parameters may be calibrated
        #this list should include all possible parameters in the parameter file
    
        #read parameter file
        if iFlag_simulation == 1:
            #sFilename_parameter = sWorkspace_simulation_case + slash + 'hru.para'
            sFilename_parameter = os.path.join(str(Path(sWorkspace_simulation_case)) ,  'hru.para' )  
        else:
            iFlag_debug = 0
            sPath_current = os.getcwd()
            #sFilename_parameter = sPath_current + slash + 'hru.para'
            sFilename_parameter = os.path.join(str(Path(sPath_current)) ,  'hru.para' )  
        #check whetheher the file exist or not
        if os.path.isfile(sFilename_parameter):
            pass
        else:
            print('The file does not exist: '+sFilename_parameter)
            return

        aData_all = text_reader_string(sFilename_parameter, cDelimiter_in =',')
        aDummy = aData_all[0,:]
        nParameter = len(aDummy) - 1
        aParameter_list = aDummy[1: nParameter+1]

        aParameter_value = (aData_all[1:(nhru+1),1: nParameter+1]).astype(float)
        aParameter_value = np.asarray(aParameter_value)

        for p in range(0, nParameter):
            para = aParameter_list[p]
            for i in range(0, nFile_type):
                aParameter_tmp = aParameter_table[i]
                if aParameter_tmp is not None:
                    if para in aParameter_tmp:
                        aParameter_count[i]= aParameter_count[i]+1
                        aParameter_flag[i]=1

                        if(aParameter_count[i] ==1):
                            aParameter_index[i] = [p]
                            aParameter_user[i]= [para]
                        else:
                            aParameter_index[i] = np.append(aParameter_index[i],[p])
                            aParameter_user[i] = np.append(aParameter_user[i],[para])
                        continue

        sWorkspace_source_case = sWorkspace_simulation_copy
        sWorkspace_target_case = sWorkspace_simulation_case
        if iFlag_simulation == 1:
            pass
        else:
            sPath_current = os.getcwd()
            if (os.path.normpath(sPath_current)  == os.path.normpath(sWorkspace_pest_model)):
                print('this is the parent, no need to copy anything')
                return
            else:
                print('this is a child')
                sWorkspace_source_case = sWorkspace_simulation_copy
                sWorkspace_target_case = sWorkspace_simulation_case

        iHru_index = 0 
        for iSubbasin in range(0, nsubbasin):
            #subbasin string
            sSubbasin = "{:05d}".format( iSubbasin + 1)
            nhru = aHru[ iSubbasin]
            #loop through all hru in this subbasin
            for iHru in range(0, nhru):
                #hru string
                sHru = "{:04d}".format( iHru + 1)
                #find the hry type 
                sHru_code = aHru_info[iHru_index]
                iIndex = np.where(aHru_combination == sHru_code)
                iHru_index = iHru_index + 1
                for iFile_type in range(0, nFile_type):
                    #check whether these is parameter chanage or not
                    sExtension = aExtension[iFile_type]
                    iFlag = aParameter_flag[iFile_type]
                    if( iFlag == 1):
                        sFilename = sSubbasin + sHru + sExtension
                        sFilename_hru = sWorkspace_source_case +  slash + sFilename 
                        #open the file to read
                        ifs=open(sFilename_hru, 'rb')   
                        sLine=(ifs.readline()).rstrip().decode("utf-8", 'ignore')

                        #open the new file to write out
                        sFilename_hru_out = sWorkspace_target_case + slash + sFilename
                        #do we need to remove linnk first, i guess it's better to do so
                        if os.path.exists(sFilename_hru_out):                
                            os.remove(sFilename_hru_out)

                        ofs=open(sFilename_hru_out, 'w') 
                        #because of the python interface, pest will no longer interact with model files directly
                        #starting from here we will                             
                        aValue = aParameter_value[iIndex[0], :]
                        while sLine:
                            aParameter = aParameter_user[iFile_type]

                            for i in range(0, aParameter_count[iFile_type]):
                                #sKey = aParameter[i]
                                if 'cn2' in sLine.lower() : 
                                    dummy = 'CN2' + "{:02d}".format(iSubbasin) \
                                    + "{:02d}".format(iHru) 
                                    dummy1 = np.array(aParameter_index[iFile_type])
                                    dummy2 = np.array(aParameter_user[iFile_type])
                                    dummy_index1 = np.where(dummy2 == 'CN2')
                                    dummy_index2 = dummy1[dummy_index1][0]
                                    sLine_new = "{:16.2f}".format(  aValue[0][dummy_index2]  )     + '    | pest parameter CN2 \n'
                                    ofs.write(sLine_new)
                                    break
                                else:
                                    if ' Ave. AW Incl. Rock' in sLine :
                                         #get substring
                                        sLine_sub = sLine[27:]
                                        dummy = sLine_sub.split()                
                                        nSoil_layer  = len(dummy)
                                        sLine_new = '{0: <27}'.format(' Ave. AW Incl. Rock: ')
                                        dummy1 = np.array(aParameter_index[iFile_type])
                                        dummy2 = np.array(aParameter_user[iFile_type])
                                        dummy_index1 = np.where(dummy2 == 'AWC')
                                        dummy_index2 = dummy1[dummy_index1][0]
                                        for j in range(nSoil_layer):
                                            sLine_new = sLine_new +  "{:12.2f}".format(  aValue[0][dummy_index2]  ) 
                                        sLine_new = sLine_new + '\n'
                                        ofs.write(sLine_new)
                                        break
                                    else:
                                        sLine = sLine + '\n'
                                        ofs.write(sLine)
                                        break
                            sLine0=(ifs.readline()).rstrip()
                            #print(sLine0)
                            sLine= sLine0.decode("utf-8", 'ignore')
                        #close files
                        ifs.close()
                        ofs.close()
                    else:
                        #this file does not need to changed
                        pass

        print('Finished writing hru file!')
        return
         
    def pyswat_copy_executable_file(self):
        """    
        prepare executable file
        """    
        sWorkspace_bin = self.sWorkspace_bin 
        sFilename_swat = self.sFilename_swat   
        sWorkspace_simulation_case = self.sWorkspace_simulation_case
        sWorkspace_calibration_case = self.sWorkspace_calibration_case    
        sWorkspace_pest_model = sWorkspace_calibration_case
        #copy swat
        #sFilename_swat_source = sWorkspace_bin + slash + sFilename_swat
        sFilename_swat_source = os.path.join(str(Path(sWorkspace_bin)) ,  sFilename_swat )

        sPath_current = os.getcwd()
        #sPath_current = sWorkspace_simulation_case
        #sFilename_swat_new = sPath_current + slash + 'swat'
        sFilename_swat_new = os.path.join(str(Path(sPath_current)) ,  'swat' )

        print(sFilename_swat_source)
        print(sFilename_swat_new)
        copy2(sFilename_swat_source, sFilename_swat_new)



    

        #copy ppest
        #sFilename_beopest_source = sWorkspace_calibration + slash + sFilename_pest
        #sFilename_beopest_new = sWorkspace_pest_model + slash + 'ppest'       
        #copy2(sFilename_beopest_source, sFilename_beopest_new)

        #copy run script?
        #sFilename_run_script = 'run_swat_model'
        #sFilename_run_script_source = sWorkspace_calibration + slash + sFilename_run_script
        #sFilename_run_script_new = sWorkspace_pest_model + slash + sFilename_run_script
        #copy2(sFilename_run_script_source, sFilename_run_script_new)


        print('The swat executable file is copied successfully!')
    
    def export_to_json(self, sFilename_output):
        with open(sFilename_output, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f,sort_keys=True, \
                ensure_ascii=False, \
                indent=4, cls=CaseClassEncoder)
        return