
import os,stat
import sys
import glob
import shutil

import numpy as np
from pathlib import Path
import tarfile
import subprocess
from shutil import copyfile
from abc import ABCMeta, abstractmethod
import datetime
from shutil import copy2
import json
from json import JSONEncoder
from pyearth.system.define_global_variables import *
import pyearth.toolbox.date.julian as julian
from pyearth.toolbox.data.convert_time_series_daily_to_monthly import convert_time_series_daily_to_monthly
from pyearth.visual.timeseries.plot_time_series_data import plot_time_series_data
from pyearth.visual.scatter.scatter_plot_data import scatter_plot_data

from swaty.auxiliary.text_reader_string import text_reader_string
from swaty.auxiliary.line_count import line_count
from swaty.classes.watershed import pywatershed
from swaty.classes.subbasin import pysubbasin
from swaty.classes.hru import pyhru
from swaty.classes.soil import pysoil
from swaty.classes.swatpara import swatpara

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
        if isinstance(obj, pywatershed):
            return json.loads(obj.tojson())

        if isinstance(obj, pysubbasin):
            return json.loads(obj.tojson())

        if isinstance(obj, pyhru):
            return json.loads(obj.tojson())
         
        if isinstance(obj, pysoil):
            return json.loads(obj.tojson())

        if isinstance(obj, swatpara):
            return json.loads(obj.tojson()) 
       
        if isinstance(obj, list):
            pass  
        return JSONEncoder.default(self, obj)

class swatcase(object):
    __metaclass__ = ABCMeta
    iCase_index=0
    iSiteID=0
    iFlag_run =0
    iFlag_standalone=1
    iFlag_simulation=1
    iFlag_initialization=1
    iFlag_calibration=0
    iFlag_watershed=0
    iFlag_subbasin=0
    iFlag_hru=0
    iFlag_soil=0
    iFlag_mode=0
    iYear_start=0
    iYear_end=0
    iMonth_start=0
    iMonth_end=0
    iDay_start=0
    iDay_end=0
    nstress=0
    nsegment =0
    nhru=0 #total nhru
    nhru_combination=0  #unique hru
    nsoil_combination =0
    aConfig_in=None

    aParameter_watershed_name = None    
    aParameter_subbasin_name = None
    aParameter_hru_name = None
    aParameter_soil_name = None

    pWatershed = None
    aSubbasin=None
    aHru=None
    aHru_combination=None
    aSoil_combinaiton = None

    nParameter=0
    nParameter_watershed=0
    nParameter_subbasin=0
    nParameter_hru=0
    nParameter_soil=0

    sFilename_swat_current = ''
    sFilename_model_configuration=''
    sWorkspace_input=''
    sWorkspace_output=''   
 
    sTime_step_calibration=''
    sFilename_observation_discharge=''
    sFilename_LandUseSoilsReport=''
    sFilename_HRULandUseSoilsReport=''
    sRegion=''
    sModel=''
    sCase=''
    sDate=''
    sSiteID=''
    sDate_start =''
    sDate_end=''

    def __init__(self, aConfig_in,\
        iFlag_read_discretization_in=None,\
        iFlag_standalone_in= None,\
        sDate_in=None, sWorkspace_output_in=None, aParameter_in = None):

        if 'iFlag_run' in aConfig_in:
            self.iFlag_run =  int(aConfig_in['iFlag_run']) 
        if iFlag_standalone_in is not None:
            self.iFlag_standalone = iFlag_standalone_in
        else:
            if 'iFlag_standalone' in aConfig_in:
                self.iFlag_standalone = int(aConfig_in['iFlag_standalone'])
            else:
                self.iFlag_standalone=1

        if iFlag_read_discretization_in is not None:
            self.iFlag_read_discretization = int(iFlag_read_discretization_in)
        else:
            if 'iFlag_read_discretization' in aConfig_in:
                self.iFlag_read_discretization =int(aConfig_in['iFlag_read_discretization'])
            else:
                self.iFlag_read_discretization=0

        
        if 'iFlag_initialization' in aConfig_in:
            self.iFlag_initialization =  int(aConfig_in['iFlag_initialization']) 
        
        if 'iFlag_calibration' in aConfig_in:
            self.iFlag_calibration =  int(aConfig_in['iFlag_calibration']) 
        if 'iFlag_simulation' in aConfig_in:
            self.iFlag_simulation =  int(aConfig_in['iFlag_simulation']) 
        if 'iFlag_watershed' in aConfig_in:
            self.iFlag_watershed =  int(aConfig_in['iFlag_watershed']) 
        if 'iFlag_subbasin' in aConfig_in:
            self.iFlag_subbasin =  int(aConfig_in['iFlag_subbasin']) 
        if 'iFlag_hru' in aConfig_in:
            self.iFlag_hru =  int(aConfig_in['iFlag_hru']) 
        if 'iFlag_soil' in aConfig_in:
            self.iFlag_soil =  int(aConfig_in['iFlag_soil']) 
            
        
        if 'iFlag_mode' in aConfig_in:
            self.iFlag_mode   = int( aConfig_in['iFlag_mode']) 
        if 'iFlag_replace_parameter' in aConfig_in:
            self.iFlag_replace_parameter= int( aConfig_in['iFlag_replace_parameter'] ) 
        
        if 'iYear_start' in aConfig_in:
            self.iYear_start  = int( aConfig_in['iYear_start'] )
        if 'iYear_end' in aConfig_in:
            self.iYear_end    = int( aConfig_in['iYear_end']   )
        if 'iMonth_start' in aConfig_in:
            self.iMonth_start = int( aConfig_in['iMonth_start'])
        if 'iMonth_end' in aConfig_in:
            self.iMonth_end   = int( aConfig_in['iMonth_end']  ) 
        if 'iDay_start' in aConfig_in:
            self.iDay_start   = int( aConfig_in['iDay_start']  )
        if 'iDay_end' in aConfig_in:
            self.iDay_end     = int( aConfig_in['iDay_end']    )
        if 'nstress' in aConfig_in:
            self.nstress      = int( aConfig_in['nstress']     )
        else:
            pass

        

        if 'sRegion' in aConfig_in:
            self.sRegion               = aConfig_in[ 'sRegion']
        if 'sModel' in aConfig_in:
            self.sModel                = aConfig_in[ 'sModel']
        if 'sPython' in aConfig_in:
            self.sPython               = aConfig_in[ 'sPython']
        if 'sFilename_model_configuration' in aConfig_in:
            self.sFilename_model_configuration    = aConfig_in[ 'sFilename_model_configuration']
        
       
        if 'sWorkspace_input' in aConfig_in:
            self.sWorkspace_input = aConfig_in[ 'sWorkspace_input']
       
        if sWorkspace_output_in is not None:
            self.sWorkspace_output = sWorkspace_output_in
        else:
            if 'sWorkspace_output' in aConfig_in:
                self.sWorkspace_output = aConfig_in[ 'sWorkspace_output']
                #the model can be run as part of hexwatershed or standalone
        

        if 'sWorkspace_bin' in aConfig_in:
            self.sWorkspace_bin= aConfig_in[ 'sWorkspace_bin']

        if 'iCase_index' in aConfig_in:
            iCase_index = int(aConfig_in['iCase_index'])
        else:
            iCase_index=1
        sCase_index = "{:03d}".format( iCase_index )

        if sDate_in is not None:
            self.sDate= sDate_in
        else:
            if 'sDate' in aConfig_in:
                self.sDate   = aConfig_in[ 'sDate']
            else:
                self.sDate = sDate_default

        self.iCase_index =   iCase_index
        sCase = self.sModel + self.sDate + sCase_index
        self.sCase = sCase
        if self.iFlag_standalone == 1:
            #in standalone case, will add case information 
            sPath = str(Path(self.sWorkspace_output)  /  sCase)
            self.sWorkspace_output = sPath
            
        else:
            #use specified output path, also do not add output or input tag
            sPath = self.sWorkspace_output

        Path(sPath).mkdir(parents=True, exist_ok=True)    
        
        if 'sJob' in aConfig_in:
            self.sJob =  aConfig_in['sJob'] 
        else:
            self.sJob = 'swat'

        if 'sWorkspace_simulation_copy' in aConfig_in:
            self.sWorkspace_simulation_copy= aConfig_in[ 'sWorkspace_simulation_copy']
            if (os.path.exists(self.sWorkspace_simulation_copy)):
                pass
            else:
                self.sWorkspace_simulation_copy = os.path.join(self.sWorkspace_input, self.sWorkspace_simulation_copy )
                pass
        else:
            self.sWorkspace_simulation_copy='TxtInOut.tar'
            self.sWorkspace_simulation_copy = os.path.join(self.sWorkspace_input,  self.sWorkspace_simulation_copy )

        if 'sFilename_LandUseSoilsReport' in aConfig_in:
            self.sFilename_LandUseSoilsReport = aConfig_in[ 'sFilename_LandUseSoilsReport']
        else:
            self.sFilename_LandUseSoilsReport = 'LandUseSoilsReport.txt'
        self.sFilename_LandUseSoilsReport =  os.path.join(self.sWorkspace_input,  self.sFilename_LandUseSoilsReport )

        if 'sFilename_HRULandUseSoilsReport' in aConfig_in:
            self.sFilename_HRULandUseSoilsReport = aConfig_in[ 'sFilename_HRULandUseSoilsReport']
        else:
            self.sFilename_HRULandUseSoilsReport = 'HRULandUseSoilsReport.txt'
        self.sFilename_HRULandUseSoilsReport =  os.path.join(self.sWorkspace_input,  self.sFilename_HRULandUseSoilsReport )

        if 'sFilename_parameter_bounds' in aConfig_in:
            self.sFilename_parameter_bounds = aConfig_in[ 'sFilename_parameter_bounds']
        else:
            self.sFilename_parameter_bounds = 'parameter_bounds.txt'
        self.sFilename_parameter_bounds =  os.path.join(self.sWorkspace_input,  self.sFilename_parameter_bounds )
        
        self.sFilename_hru_combination = os.path.join(self.sWorkspace_output,  'hru_combination.txt' )
                        
        self.sFilename_watershed_configuration = os.path.join(self.sWorkspace_output, 'watershed_configuration.txt' )
        
        self.sFilename_hru_info = os.path.join(self.sWorkspace_output,  'hru_info.txt' )

        #soil
        self.sFilename_soil_combination = os.path.join(self.sWorkspace_output, 'soil_combination.txt')
        self.sFilename_soil_info = os.path.join(self.sWorkspace_output, 'soil_info.txt')

        #set up instance
        self.pWatershed = pywatershed()
        
        if self.iFlag_read_discretization == 1:
            #read basin
            dummy = text_reader_string(self.sFilename_watershed_configuration, cDelimiter_in=',')
            dummy1 = np.array(dummy[:,0])
            aSubbasin_info = dummy1.astype(int)
            self.nsubbasin = aSubbasin_info.shape[0]
            self.nsegment = self.nsubbasin

            self.aSubbasin=list()
            for i in range(1, self.nsubbasin+1):
                pdummy = pysubbasin()    
                pdummy.lIndex_subbasin = i
                self.aSubbasin.append(pdummy)

            #read hru
            aHru_combination = text_reader_string(self.sFilename_hru_combination, cDelimiter_in=',')
            self.nhru_combination = len(aHru_combination)


            aHru_info = text_reader_string(self.sFilename_hru_info, cDelimiter_in=',')
            self.nhru = len(aHru_info)
            aHru_info= np.reshape(aHru_info, (self.nhru))

            #read soil
            aSoil_info = text_reader_string(self.sFilename_soil_info, cDelimiter_in=',')
            aSoil_info = np.array(aSoil_info)            

            aSoil_combinaiton = text_reader_string(self.sFilename_soil_combination, cDelimiter_in=',')
            self.nsoil_combination = len(aSoil_combinaiton)
            self.aSoil_combinaiton= aSoil_combinaiton


            self.aHru_combination=list()
            for iHru_combination in range(1, self.nhru_combination+1):
                pdummy = pyhru()
                pdummy.lIndex_hru = iHru_combination

                sHru = aHru_combination[iHru_combination-1]
                dummy_index = np.where(aHru_info == sHru)
                dummy_index2= dummy_index[0][0]
                dummy = aSoil_info[dummy_index2,:]

                pdummy.nSoil_layer= int( dummy[1])
                pdummy.sSoil_type = dummy[0].strip()
                pdummy.aSoil=list()
                for j in range(1, pdummy.nSoil_layer+1):
                    dummy_soil = pysoil()
                    dummy_soil.lIndex_hru = iHru_combination
                    dummy_soil.lIndex_soil_layer = j
                    dummy_soil.sSoil_type = pdummy.sSoil_type
                    pdummy.aSoil.append(dummy_soil)

                self.aHru_combination.append(pdummy)

        else:
            if 'nsegment' in aConfig_in:
                self.nsegment = int( aConfig_in[ 'nsegment'] )
            if 'nsubbasin' in aConfig_in:
                self.nsubbasin = int (aConfig_in[ 'nsubbasin'])
                self.aSubbasin=list()
                for i in range(self.nsubbasin):
                    pdummy = pysubbasin()    
                    pdummy.lIndex = i+1
                    self.aSubbasin.append(pdummy)
            if 'nhru' in aConfig_in:
                nhru = int( aConfig_in['nhru']) 
                
        if 'sFilename_observation_discharge' in aConfig_in: 
            self.sFilename_observation_discharge = aConfig_in['sFilename_observation_discharge']
        
        if 'sTime_step_calibration' in aConfig_in: 
            self.sTime_step_calibration = aConfig_in['sTime_step_calibration']
        else:
            self.sTime_step_calibration = 'daily'
        

        if 'sFilename_swat' in aConfig_in:
            self.sFilename_swat = aConfig_in[ 'sFilename_swat']

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

        self.nstress_month = iMonth_count    
      
            
        
        if self.iFlag_read_discretization == 1:
            if 'aParameter_watershed_name' in aConfig_in:
                dummy = aConfig_in['aParameter_watershed_name']
                self.pWatershed.aParameter_watershed_name = dummy
                self.aParameter_watershed_name = dummy
                aParameter_watershed=list()
                for i in range(len(self.aParameter_watershed_name)):
                    aPara_in = {}
                    aPara_in['iParameter_type']=1
                    aPara_in['sName']=self.aParameter_watershed_name[i]
                    aPara_in['dValue_init']=0
                    aPara_in['dValue_lower']=0
                    aPara_in['dValue_upper']=0
                    pPara_watershed = swatpara(aPara_in)
                    aParameter_watershed.append(pPara_watershed)
                
                self.pWatershed.aParameter_watershed=aParameter_watershed
                self.pWatershed.nParameter_watershed=len(aParameter_watershed)
                    
    
            if 'aParameter_subbasin_name' in aConfig_in:
                dummy = aConfig_in['aParameter_subbasin_name']
                self.aParameter_subbasin_name = dummy
                aPara_in = {}
                for i in range(1, self.nsubbasin+1):                    
                    self.aSubbasin[i-1].aParameter_subbasin_name = dummy
                    aParameter_subbasin=list()
                    for j in range(len(self.aParameter_subbasin_name)):
                        aPara_in['iParameter_type']=2
                        aPara_in['lIndex_subbasin']=i
                        aPara_in['sName']=self.aParameter_subbasin_name[j]
                        aPara_in['dValue_init']=0.0
                        aPara_in['dValue_lower']=0.0
                        aPara_in['dValue_upper']=0.0
                        pPara_subbasin = swatpara(aPara_in)
                        aParameter_subbasin.append(pPara_subbasin) 

                    self.aSubbasin[i-1].aParameter_subbasin = aParameter_subbasin     
                    self.aSubbasin[i-1].nParameter_subbasin = len(aParameter_subbasin )             
                
            if 'aParameter_hru_name' in aConfig_in:
                dummy = aConfig_in['aParameter_hru_name']
                self.aParameter_hru_name = dummy
                aPara_in = {}
                for i in range(1, self.nhru_combination+1):      
                    aParameter_hru=list()
                    for j in range(len(self.aParameter_hru_name)):
                        aPara_in['lIndex_hru']=i
                        aPara_in['iParameter_type']=3
                        aPara_in['sName']=self.aParameter_hru_name[j]
                        aPara_in['dValue_init']=0.0
                        aPara_in['dValue_lower']=0.0
                        aPara_in['dValue_upper']=0.0
                        pPara_hru = swatpara(aPara_in)
                        aParameter_hru.append(pPara_hru)
                    self.aHru_combination[i-1].aParameter_hru_name = dummy
                    self.aHru_combination[i-1].aParameter_hru = aParameter_hru  
                    self.aHru_combination[i-1].nParameter_hru = len(aParameter_hru)  

            if 'aParameter_soil_name' in aConfig_in:
                dummy = aConfig_in['aParameter_soil_name']
                self.aParameter_soil_name = dummy
                for i in range(1, self.nhru_combination+1):
                    nSoil_layer = self.aHru_combination[i-1].nSoil_layer
                    for j in range(1, nSoil_layer+1):    
                        aParameter_soil=list()
                        for k in range(len(self.aParameter_soil_name)):
                            aPara_in = {}
                            aPara_in['iParameter_type']=4
                            aPara_in['lIndex_hru']=i
                            aPara_in['lIndex_soil_layer']=j
                            aPara_in['sName']=self.aParameter_soil_name[k]
                            aPara_in['dValue_init']=0.0
                            aPara_in['dValue_lower']=0.0
                            aPara_in['dValue_upper']=0.0
                            pPara_hru = swatpara(aPara_in)
                            aParameter_soil.append(pPara_hru)                     
                        self.aHru_combination[i-1].aSoil[j-1].aParameter_soil_name = dummy
                        self.aHru_combination[i-1].aSoil[j-1].aParameter_soil = aParameter_soil
                        self.aHru_combination[i-1].aSoil[j-1].nParameter_soil = len(aParameter_soil)

            if aParameter_in is not None:                                  
                pass
            else:            
                if 'nParameter_watershed' in aConfig_in:
                    self.nParameter_watershed = int(aConfig_in['nParameter_watershed'] )
                else:
                    self.nParameter_watershed = 0
                if 'nParameter_subbasin' in aConfig_in:
                    self.nParameter_subbasin = int(aConfig_in['nParameter_subbasin'] )
                else:
                    self.nParameter_subbasin = 0
    
                if 'nParameter_hru' in aConfig_in:
                    self.nParameter_hru = int(aConfig_in['nParameter_hru'] )
                else:
                    self.nParameter_hru = 0
                
                if 'nParameter_soil' in aConfig_in:
                    self.nParameter_soil = int(aConfig_in['nParameter_soil'] )
                else:
                    self.nParameter_soil = 0

            
        else:
            if aParameter_in is not None:                                      
                pass
            else:            
                if 'nParameter_watershed' in aConfig_in:
                    self.nParameter_watershed = int(aConfig_in['nParameter_watershed'] )
                else:
                    self.nParameter_watershed = 0
                if 'nParameter_subbasin' in aConfig_in:
                    self.nParameter_subbasin = int(aConfig_in['nParameter_subbasin'] )
                else:
                    self.nParameter_subbasin = 0

                if 'nParameter_hru' in aConfig_in:
                    self.nParameter_hru = int(aConfig_in['nParameter_hru'] )
                else:
                    self.nParameter_hru = 0

                if 'nParameter_soil' in aConfig_in:
                    self.nParameter_soil = int(aConfig_in['nParameter_soil'] )
                else:
                    self.nParameter_soil = 0
        return


    def copy_TxtInOut_files(self):
        """
        sFilename_configuration_in
        sModel
        """        
        
        sWorkspace_target_case = self.sWorkspace_output   

        Path(sWorkspace_target_case).mkdir(parents=True, exist_ok=True)

        if not os.path.exists(self.sWorkspace_simulation_copy):
            print(self.sWorkspace_simulation_copy)
            print('The simulation copy does not exist!')
            return
        else:      
            #we might need to extract 
            if os.path.isfile(self.sWorkspace_simulation_copy):  
                sBasename = Path(self.sWorkspace_simulation_copy).stem
                #delete previous folder
                sTarget_path = str(Path(self.sWorkspace_output) /sBasename)
                if os.path.exists(sTarget_path):
                    shutil.rmtree(sTarget_path)
                    pass
                
                pTar = tarfile.open(self.sWorkspace_simulation_copy)
                pTar.extractall(self.sWorkspace_output) # specify which folder to extract to
                pTar.close()
                
                self.sWorkspace_simulation_copy = sTarget_path
            else:
                #this is a folder
                pass
        

        sWorkspace_simulation_copy= self.sWorkspace_simulation_copy
        
        
        #the following file will be copied    

        aExtension = ('.pnd','.rte','.sub','.swq','.wgn','.wus',\
                '.chm','.gw','.hru','.mgt','sdr','.sep',\
                 '.sol','ATM','bsn','wwq','deg','.cst',\
                 'dat','fig','cio','fin','dat','.pcp','.tmp','.slr','.hmd'  )

        #we need to be careful that Tmp is different in python/linux with tmp

        nsubbasin = self.nsubbasin
        sFilename_watershed_configuration = self.sFilename_watershed_configuration
        sFilename_hru_info = self.sFilename_hru_info     
        aSubbasin_hru  = text_reader_string( sFilename_watershed_configuration, cDelimiter_in = ',' )
        aHru_configuration = aSubbasin_hru[:,1].astype(int)  

        aExtension_watershed = ( '.fin','.cio','.fig','.dat','.cst','.wwq', '.bsn','.deg','.slr' )
        aExtension_subbasin = ('.wus','.sub','.swq','.pnd','.rte','.wgn'  )
        aExtension_hru = ( '.chm','.gw','.hru','.mgt','.sdr','.sep','.sol'  )
        aExtension_other = ('ATM','.pcp','.tmp','.hmd'  )

        for sExtension in aExtension_watershed:
            sDummy = '*'+ sExtension
            sRegax = os.path.join(str(Path(sWorkspace_simulation_copy)  ) ,  sDummy  )
            for sFilename in glob.glob(sRegax):
                sBasename_with_extension = os.path.basename(sFilename)
                sFilename_new = os.path.join(str(Path(sWorkspace_target_case)) ,   sBasename_with_extension )     
                print(sFilename, sFilename_new)               
                #copyfile(sFilename, sFilename_new)      
                if (os.path.exists(sFilename_new)): 
                    sCommand = 'rm -rf  ' + sFilename_new
                    status = subprocess.call(sCommand, shell=True)  
                sCommand = 'cp ' + sFilename + ' ' + sFilename_new
                status = subprocess.call(sCommand, shell=True)  
        
        for iSubbasin in range(1, nsubbasin+1):
            sSubbasin = "{:05d}".format( iSubbasin )            
            for sExtension in aExtension_subbasin:
                sDummy = sSubbasin + '0000' + sExtension
                sFilename = os.path.join(str(Path(sWorkspace_simulation_copy)  ) ,  sDummy  )              
              
                #sBasename_with_extension = os.path.basename(sFilename)
                sFilename_new = os.path.join(str(Path(sWorkspace_target_case)) ,  sDummy  )   
                print(sFilename, sFilename_new)                 
                #copyfile(sFilename, sFilename_new)
                if (os.path.exists(sFilename_new)): 
                    sCommand = 'rm -rf  ' + sFilename_new
                    status = subprocess.call(sCommand, shell=True) 
                sCommand = 'cp ' + sFilename + ' ' + sFilename_new
                status = subprocess.call(sCommand, shell=True)


        for iSubbasin in range(1, nsubbasin+1):
            sSubbasin = "{:05d}".format( iSubbasin )
            nhru_subbasin = aHru_configuration[ iSubbasin-1]
            for iHru in range(1, nhru_subbasin+1):
                sHru = "{:04d}".format( iHru)
                print(sSubbasin + sHru) 
                for sExtension in aExtension_hru:
                       
                    sDummy = sSubbasin + sHru + sExtension
                    sFilename = os.path.join(str(Path(sWorkspace_simulation_copy)  ) ,  sDummy  )
                    
                    #else:
                    #start = datetime.datetime.now()
                    #for sFilename in glob.glob(sRegax):
                    #sBasename_with_extension = os.path.basename(sFilename)
                    sFilename_new = os.path.join(str(Path(sWorkspace_target_case)) ,  sDummy  )   
                                 
                    #copyfile(sFilename, sFilename_new)
                    if (os.path.exists(sFilename_new)): 
                        sCommand = 'rm -rf  ' + sFilename_new
                        status = subprocess.call(sCommand, shell=True) 
                    sCommand = 'cp ' + sFilename + ' ' + sFilename_new
                    status = subprocess.call(sCommand, shell=True)

                    #finish = datetime.datetime.now()
                    #print("Time elapsed: ", finish-start) # CPU seconds elapsed (floating point)

        for sExtension in aExtension_other:
            if sExtension == '.tmp':
                sDummy = '*'+ sExtension
                sRegax = os.path.join(str(Path(sWorkspace_simulation_copy)  ) ,  sDummy  )
                for sFilename in glob.glob(sRegax):
                    sBasename_with_extension = os.path.basename(sFilename)
                    sFilename_new = os.path.join(str(Path(sWorkspace_target_case)) ,  sBasename_with_extension.lower()  )                    
                    #copyfile(sFilename, sFilename_new)
                    if (os.path.exists(sFilename_new)): 
                        sCommand = 'rm -rf  ' + sFilename_new
                        status = subprocess.call(sCommand, shell=True) 
                    sCommand = 'cp ' + sFilename + ' ' + sFilename_new
                    status = subprocess.call(sCommand, shell=True)  
            else:
                sDummy = '*'+ sExtension
                sRegax = os.path.join(str(Path(sWorkspace_simulation_copy)  ) ,  sDummy  )
                for sFilename in glob.glob(sRegax):
                    sBasename_with_extension = os.path.basename(sFilename)
                    sFilename_new = os.path.join(str(Path(sWorkspace_target_case)) ,  sBasename_with_extension  )                    
                    #copyfile(sFilename, sFilename_new)
                    sCommand = 'rm -rf  ' + sFilename_new
                    status = subprocess.call(sCommand, shell=True) 
                    sCommand = 'cp ' + sFilename + ' ' + sFilename_new
                    status = subprocess.call(sCommand, shell=True)  


        print('Finished copying all input files')
    
    def prepare_pest_template_files(self):

        self.swaty_prepare_watershed_template_file()
        self.swaty_prepare_subbasin_template_file()
        self.swaty_prepare_hru_template_file()
        self.swaty_prepare_soil_template_file()

        return

    def setup(self):
        """
        Set up a SWAT case
        """
        

        if (self.iFlag_initialization ==1):
            self.copy_TxtInOut_files()                       
            #self.swaty_prepare_watershed_parameter_file()
            #self.swaty_prepare_subbasin_parameter_file()
            #self.swaty_prepare_hru_parameter_file()
            #self.swaty_prepare_soil_parameter_file()
            #actual update parameter                 
               
            self.swaty_copy_executable_file()
            sFilename_bash = self.swaty_prepare_simulation_bash_file()
            sFilename_job = self.swaty_prepare_simulation_job_file() 
            pass
        else: #during calibration
            #an inital simulation is needed?

            #self.convert_pest_parameter_to_model_input()   #this step only construct object
            if (self.iFlag_replace_parameter == 1):                           
                #actual update parameter
                self.swaty_write_watershed_input_file()                
                self.swaty_write_subbasin_input_file()                 
                self.swaty_write_hru_input_file()        
            else:
                pass               
                      
            
           
            pass

        
        
        

        
        
        return

    def convert_pest_parameter_to_model_input(self, \
        
        sFilename_pest_parameter_watershed_in = None,\
        sFilename_watershed_parameter_default_in = None,\
        sFilename_watershed_parameter_bounds_in = None,\

        sFilename_pest_parameter_subbasin_in = None,\
        sFilename_subbasin_parameter_default_in = None,\
            sFilename_subbasin_parameter_bounds_in = None,\
            
        sFilename_pest_parameter_hru_in = None,\
        sFilename_hru_parameter_default_in = None,\
            sFilename_hru_parameter_bounds_in = None,\
            
        sFilename_pest_parameter_soil_in = None,\
        sFilename_soil_parameter_bounds_in = None, \
            sWorkspace_soil_parameter_default_in = None ):

        self.convert_pest_parameter_to_actual_parameter(\
        
        sFilename_pest_parameter_watershed_in = sFilename_pest_parameter_watershed_in,\
        sFilename_watershed_parameter_default_in = sFilename_watershed_parameter_default_in,\
            sFilename_watershed_parameter_bounds_in = sFilename_watershed_parameter_bounds_in,\

        sFilename_pest_parameter_subbasin_in = sFilename_pest_parameter_subbasin_in,\
        sFilename_subbasin_parameter_default_in = sFilename_subbasin_parameter_default_in,\
            sFilename_subbasin_parameter_bounds_in = sFilename_subbasin_parameter_bounds_in,\
            
        sFilename_pest_parameter_hru_in = sFilename_pest_parameter_hru_in,\
        sFilename_hru_parameter_default_in = sFilename_hru_parameter_default_in,\
            sFilename_hru_parameter_bounds_in = sFilename_hru_parameter_bounds_in,\
            
        sFilename_pest_parameter_soil_in = sFilename_pest_parameter_soil_in,\
        sFilename_soil_parameter_bounds_in = sFilename_soil_parameter_bounds_in,\
            sWorkspace_soil_parameter_default_in = sWorkspace_soil_parameter_default_in )

        #build object


        return

    def convert_pest_parameter_to_actual_parameter(self, \
        
        sFilename_pest_parameter_watershed_in = None,\
        sFilename_watershed_parameter_default_in = None,\
            sFilename_watershed_parameter_bounds_in = None,\

        sFilename_pest_parameter_subbasin_in = None,\
        sFilename_subbasin_parameter_default_in = None,\
            sFilename_subbasin_parameter_bounds_in = None,\
            
        sFilename_pest_parameter_hru_in = None,\
        sFilename_hru_parameter_default_in = None,\
            sFilename_hru_parameter_bounds_in = None,\
            
        sFilename_pest_parameter_soil_in = None,\
        sFilename_soil_parameter_bounds_in = None,\
            sWorkspace_soil_parameter_default_in = None    ):
        
        self.convert_pest_watershed_parameter_to_actual_parameter(sFilename_pest_parameter_watershed_in = sFilename_pest_parameter_watershed_in,\
        sFilename_watershed_parameter_default_in = sFilename_watershed_parameter_default_in,sFilename_watershed_parameter_bounds_in = sFilename_watershed_parameter_bounds_in)
        
        self.convert_pest_subbasin_parameter_to_actual_parameter(sFilename_pest_parameter_subbasin_in = sFilename_pest_parameter_subbasin_in,\
        sFilename_subbasin_parameter_default_in = sFilename_subbasin_parameter_default_in,sFilename_subbasin_parameter_bounds_in = sFilename_subbasin_parameter_bounds_in)        
        
        self.convert_pest_hru_parameter_to_actual_parameter(sFilename_pest_parameter_hru_in = sFilename_pest_parameter_hru_in,\
        sFilename_hru_parameter_default_in = sFilename_hru_parameter_default_in,sFilename_hru_parameter_bounds_in = sFilename_hru_parameter_bounds_in)
        
        self.convert_pest_soil_parameter_to_actual_parameter(sFilename_pest_parameter_soil_in = sFilename_pest_parameter_soil_in,\
        sFilename_soil_parameter_bounds_in = sFilename_soil_parameter_bounds_in,sWorkspace_soil_parameter_default_in= sWorkspace_soil_parameter_default_in)

        return

    def convert_pest_watershed_parameter_to_actual_parameter(self, sFilename_pest_parameter_watershed_in = None,\
        sFilename_watershed_parameter_default_in = None,sFilename_watershed_parameter_bounds_in = None ):

        #read the default parameter value
        if sFilename_pest_parameter_watershed_in is None:
            sFilename_pest_parameter_watershed = os.path.join( self.sWorkspace_output, 'watershed.para' )
        else:
            sFilename_pest_parameter_watershed = sFilename_pest_parameter_watershed_in
        
        sTime  = datetime.datetime.now().strftime("%m%d%Y%H%M%S")
        sFilename_new = os.path.join(os.path.dirname(sFilename_pest_parameter_watershed_in), 'watershed_parameter' + sTime + '.txt')
        copy2(sFilename_pest_parameter_watershed_in, sFilename_new)

        aData_dummy0 = text_reader_string(sFilename_pest_parameter_watershed, cDelimiter_in=',')

        #read pest default parameter value
        if sFilename_watershed_parameter_default_in is None:
            sFilename_watershed_parameter_default = os.path.join( self.sWorkspace_output, 'watershed_parameter_default.txt' )
        else:
            sFilename_watershed_parameter_default = sFilename_watershed_parameter_default_in
        aData_dummy1 = text_reader_string(sFilename_watershed_parameter_default, cDelimiter_in=',')

        #read the bound        
        if sFilename_watershed_parameter_bounds_in is None:
            sFilename_watershed_parameter_bounds = os.path.join(self.sWorkspace_output,  'watershed_parameter_bounds.txt' )
        else:
            sFilename_watershed_parameter_bounds = sFilename_watershed_parameter_bounds_in

        aData_dummy2 = text_reader_string(sFilename_watershed_parameter_bounds, cDelimiter_in=',')

        #replace watershed by writing into a new file
        sFilename_watershed_out = os.path.join( self.sWorkspace_output, 'watershed_updated.para' )
        ofs=open(sFilename_watershed_out, 'w') 

        #assume the paramete may be out of bound because of the ratio operations
        #maintain the order of the parameter

        sLine_header = aData_dummy0[0,:]
        nParameter_watershed  = sLine_header.shape[0] - 1
        sLine_header = ','.join(sLine_header)
        sLine = sLine_header + '\n'
        ofs.write(sLine)
        
        aData_dummy00 = aData_dummy0[0,1:(nParameter_watershed+1)]
        aData_dummy01 = aData_dummy0[1,1:(nParameter_watershed+1)]
        #self.nParameter_watershed = nParameter_watershed
        sLine = 'watershed'
        for i in range(nParameter_watershed):
            # we assume the order are the same as well, because the default parameter should be extracted using the same configuration
            # we must verify that the bounds have a same order 
            sName = aData_dummy00[i] #not used since no ratio consider
            iIndex_name = self.pWatershed.aParameter_watershed_name.index(sName)
            
            dValue = float(aData_dummy01[i].strip())
            dValue_lower = float(aData_dummy2[i,1].strip())
            dValue_upper = float(aData_dummy2[i,2].strip())
            if dValue < dValue_lower:
                dValue = dValue_lower
            if dValue > dValue_upper:
                dValue = dValue_upper

            self.pWatershed.aParameter_watershed[iIndex_name].dValue_current = dValue
            sLine = sLine + ',' + "{:0f}".format( dValue )
    
            pass
        sLine = sLine + '\n'
        ofs.write(sLine)
        ofs.close()
        
        
        return
    
    def convert_pest_subbasin_parameter_to_actual_parameter(self,  sFilename_pest_parameter_subbasin_in = None,\
        sFilename_subbasin_parameter_default_in = None,sFilename_subbasin_parameter_bounds_in = None):
        sWorkspace_output = self.sWorkspace_output
        #subbasin
        #read the default parameter value
        if sFilename_pest_parameter_subbasin_in is None:
            sFilename_pest_subbasin = os.path.join( sWorkspace_output, 'subbasin.para' )
        else:
            sFilename_pest_parameter_subbasin = sFilename_pest_parameter_subbasin_in

        sTime  = datetime.datetime.now().strftime("%m%d%Y%H%M%S")
        sFilename_new = os.path.join(os.path.dirname(sFilename_pest_parameter_subbasin_in), 'subbasin_parameter' + sTime + '.txt')
        copy2(sFilename_pest_parameter_subbasin_in, sFilename_new)

        aData_dummy0 = text_reader_string(sFilename_pest_parameter_subbasin, cDelimiter_in=',')

        #read pest default parameter value
        if sFilename_subbasin_parameter_default_in is None:
            sFilename_subbasin_parameter_default = os.path.join( sWorkspace_output, 'subbasin_parameter_default.txt' )
        else:
            sFilename_subbasin_parameter_default = sFilename_subbasin_parameter_default_in
        aData_dummy1 = text_reader_string(sFilename_subbasin_parameter_default, cDelimiter_in=',')

        #read the bound        
        if sFilename_subbasin_parameter_bounds_in is None:
            sFilename_subbasin_parameter_bounds = os.path.join(sWorkspace_output,  'subbasin_parameter_bounds.txt' )
        else:
            sFilename_subbasin_parameter_bounds = sFilename_subbasin_parameter_bounds_in
        aData_dummy2 = text_reader_string(sFilename_subbasin_parameter_bounds, cDelimiter_in=',')

        #replace subbasin by writing into a new file
        sFilename_subbasin_out = os.path.join( sWorkspace_output, 'subbasin_updated.para' )
        ofs=open(sFilename_subbasin_out, 'w') 

        #assume the paramete may be out of bound because of the ratio operations
        #maintain the order of the parameter

        sLine_header = aData_dummy0[0,:]
        nParameter_subbasin  = sLine_header.shape[0] - 1
        sLine_header = ','.join(sLine_header)
        sLine = sLine_header + '\n'
        ofs.write(sLine)
        
        aData_dummy00 = aData_dummy0[0,1:(nParameter_subbasin+1)]
        aData_dummy01 = aData_dummy0[1,1:(nParameter_subbasin+1)]
        self.nParameter_subbasin = nParameter_subbasin
        
        for iSubbasin in range(1, self.nsubbasin):
            sSubbasin = "{:05d}".format( iSubbasin )   
            sLine = sSubbasin
            for j in range(nParameter_subbasin):
                # we assume the order are the same as well, because the default parameter should be extracted using the same configuration

                # we must verify that the bounds have a same order 
                sName = aData_dummy00[j].strip()
                iIndex_name = self.aSubbasin[iSubbasin-1].aParameter_subbasin_name.index(sName)
                dValue = float(aData_dummy01[j].strip())
                dValue_lower = float(aData_dummy2[j,1].strip())
                dValue_upper = float(aData_dummy2[j,2].strip())
                if dValue < dValue_lower:
                    dValue = dValue_lower
                if dValue > dValue_upper:
                    dValue = dValue_upper
                
                self.aSubbasin[iSubbasin-1].aParameter_subbasin[iIndex_name].dValue_current = dValue

                sLine = sLine + ',' + "{:0f}".format( dValue )

                pass
            sLine = sLine + '\n'
            ofs.write(sLine)
        ofs.close()
        
        return
    
    def convert_pest_hru_parameter_to_actual_parameter(self, sFilename_pest_parameter_hru_in = None,\
        sFilename_hru_parameter_default_in = None,sFilename_hru_parameter_bounds_in = None):

        
        #subbasin
        #read the default parameter value
        if sFilename_pest_parameter_hru_in is None:
            sFilename_pest_parameter_hru = os.path.join(  self.sWorkspace_output, 'hru.para' )
        else:
            sFilename_pest_parameter_hru = sFilename_pest_parameter_hru_in
        
        sTime  = datetime.datetime.now().strftime("%m%d%Y%H%M%S")
        sFilename_new = os.path.join(os.path.dirname(sFilename_pest_parameter_hru_in), 'hru_parameter' + sTime + '.txt')
        copy2(sFilename_pest_parameter_hru_in, sFilename_new)

        aData_dummy0 = text_reader_string(sFilename_pest_parameter_hru, cDelimiter_in=',')
        #read pest default parameter value
        if sFilename_hru_parameter_default_in is None:
            sFilename_hru_parameter_default = os.path.join(  self.sWorkspace_output, 'hru_parameter_default.txt' )
        else:
            sFilename_hru_parameter_default = sFilename_hru_parameter_default_in
        aData_dummy1 = text_reader_string(sFilename_hru_parameter_default, cDelimiter_in=',')
        #read the bound        
        if sFilename_hru_parameter_bounds_in is None:
            sFilename_hru_parameter_bounds = os.path.join(self.sWorkspace_output,  'hru_parameter_bounds.txt' )
        else:
            sFilename_hru_parameter_bounds = sFilename_hru_parameter_bounds_in
        aData_dummy2 = text_reader_string(sFilename_hru_parameter_bounds, cDelimiter_in=',')  

        sFilename_hru_out = os.path.join(  self.sWorkspace_output, 'hru_updated.para' )
        ofs=open(sFilename_hru_out, 'w') 
        #assume the paramete may be out of bound because of the ratio operations
        #maintain the order of the parameter

        sLine_header = aData_dummy0[0,:]
        nParameter_hru  = sLine_header.shape[0] - 1
        sLine_header = ','.join(sLine_header)
        sLine = sLine_header + '\n'
        ofs.write(sLine)
        
        aData_dummy00 = aData_dummy0[0,1:(nParameter_hru+1)]
        aData_dummy01 = aData_dummy0[1:,1:(nParameter_hru+1)]
        self.nParameter_hru = nParameter_hru

        aName_ratio= ['cn2','ov_n']
        
        for iHru in range(1, self.nhru_combination):
            sHRU = "{:04d}".format( iHru )   
            sLine = sHRU
            for j in range(nParameter_hru):
                # we assume the order are the same as well, because the default parameter should be extracted using the same configuration
                # we must verify that the bounds have a same order

                sName = aData_dummy00[j].strip()

                iIndex_name = self.aHru_combination[iHru-1].aParameter_hru_name.index(sName)
                if sName in aName_ratio:
                    dValue_default = float(aData_dummy1[iHru,j+1].strip())
                    dRatio = float(aData_dummy01[0][j].strip())
                    #dValue =  dValue_default * dRatio #chang (0-10)
                    dValue =  dValue_default * (1 + dRatio) #khong (-1,1)
                else:
                    dRatio = 1.0
                    dValue = float(aData_dummy01[0][j].strip()) * dRatio

                dValue_lower = float(aData_dummy2[j,1].strip())
                dValue_upper = float(aData_dummy2[j,2].strip())
                if dValue < dValue_lower:
                    dValue = dValue_lower
                if dValue > dValue_upper:
                    dValue = dValue_upper

                self.aHru_combination[iHru-1].aParameter_hru[iIndex_name].dValue_current = dValue

                sLine = sLine + ',' + "{:0f}".format( dValue )
                pass
            sLine = sLine + '\n'
            ofs.write(sLine)
        ofs.close()

        return
    
    def convert_pest_soil_parameter_to_actual_parameter(self, sFilename_pest_parameter_soil_in = None,\
        sFilename_soil_parameter_bounds_in = None,sWorkspace_soil_parameter_default_in = None ):
        sWorkspace_simulation_case = self.sWorkspace_output
        #subbasin
        #read the default parameter value
        if sFilename_pest_parameter_soil_in is None:
            sFilename_pest_parameter_soil = os.path.join( sWorkspace_simulation_case, 'soil.para' )
        else: 
            sFilename_pest_parameter_soil= sFilename_pest_parameter_soil_in

        sTime  = datetime.datetime.now().strftime("%m%d%Y%H%M%S")
        #save history
        sFilename_new = os.path.join(os.path.dirname(sFilename_pest_parameter_soil), 'soil_parameter' + sTime + '.txt')
        copy2(sFilename_pest_parameter_soil, sFilename_new)

        if sWorkspace_soil_parameter_default_in is None:
            sWorkspace_soil_parameter_default = self.sWorkspace_output
        else:
            sWorkspace_soil_parameter_default = sWorkspace_soil_parameter_default_in
        
        

        aData_dummy0 = text_reader_string(sFilename_pest_parameter_soil, cDelimiter_in=',')
        sFilename_soil_combination = self.sFilename_soil_combination
        nsoil_combination = self.nsoil_combination
        aSoil_combination = text_reader_string(sFilename_soil_combination, cDelimiter_in = ',')
        aSoil_combination = np.asarray(aSoil_combination)
        aSoil_combination= aSoil_combination.reshape(nsoil_combination, 2) 
        aName_ratio= ['sol_k','sol_awc','sol_alb','sol_bd']

        #read the bound        
        if sFilename_soil_parameter_bounds_in is None :    
            sFilename_soil_parameter_bounds = os.path.join(self.sWorkspace_input,  'soil_parameter_bounds.txt' )
        else:
            sFilename_soil_parameter_bounds = sFilename_soil_parameter_bounds_in
        aData_dummy2 = text_reader_string(sFilename_soil_parameter_bounds, cDelimiter_in=',')

        aDate_out= list()
        for iSoil_type in range(1, nsoil_combination+1 ):

            sSoil_type = "{:02d}".format( iSoil_type )
            sSoil_code = aSoil_combination[iSoil_type-1,0]
            nSoil_layer = int(aSoil_combination[iSoil_type-1,1])            
            sFilename_soil_default_parameter = os.path.join( sWorkspace_soil_parameter_default, 'soiltype' + sSoil_type + '_parameter_default.txt' )
            aData_dummy1 = text_reader_string(sFilename_soil_default_parameter, cDelimiter_in=',')
            sFilename_soiltype_out = os.path.join( sWorkspace_simulation_case, 'soiltype' + sSoil_type + '.para' )
            ofs=open(sFilename_soiltype_out, 'w') 
            #assume the paramete may be out of bound because of the ratio operations
            #maintain the order of the parameter
            sLine_header = aData_dummy0[0,:]
            nParameter_soil  = sLine_header.shape[0] - 1

            aData_soil_layer = np.full( (nSoil_layer,nParameter_soil ), -9999, dtype=float )
            sLine_header = ','.join(sLine_header)
            sLine = sLine_header + '\n'
            ofs.write(sLine)
            aData_dummy00 = aData_dummy0[0,1:(nParameter_soil+1)]
            aData_dummy01 = aData_dummy0[1,1:(nParameter_soil+1)]
            #self.nParameter_soil = nParameter_soil

            #only replace the first line/soil layer
            sSoil_layer = "{:02d}".format( 1 ) 
            sLine = 'soillayer'+sSoil_layer
            for j in range(nParameter_soil):
                # we assume the order are the same as well, because the default parameter should be extracted using the same configuration
                # we must verify that the bounds have a same order 
                sName = aData_dummy00[j].strip()
                if sName in aName_ratio:
                    dValue_default = float(aData_dummy1[1,j+1].strip())
                    dRatio = float(aData_dummy01[j].strip())
                    dValue =  dValue_default * dRatio
                else:
                    dRatio = 1.0
                    dValue = float(aData_dummy01[j].strip()) * dRatio
                
                dValue_lower = float(aData_dummy2[j,1].strip())
                dValue_upper = float(aData_dummy2[j,2].strip())
                if dValue < dValue_lower:
                    dValue = dValue_lower
                if dValue > dValue_upper:
                    dValue = dValue_upper
                sLine = sLine + ',' + "{:0f}".format( dValue )

                aData_soil_layer[0, j] = dValue
                pass
            sLine = sLine + '\n'
            ofs.write(sLine)

            for iSoil_layer in range(2, nSoil_layer + 1):
                sSoil_layer = "{:02d}".format( iSoil_layer )   
                sLine = 'soillayer'+sSoil_layer
                for j in range(1, nParameter_soil+1):
                    # we assume the order are the same as well, because the default parameter should be extracted using the same configuration
                    # we must verify that the bounds have a same order 
                    dValue = float(aData_dummy1[iSoil_layer, j])                  
                    sLine = sLine + ',' + "{:0f}".format( dValue )

                    aData_soil_layer[iSoil_layer-1, j-1] = dValue
                    pass
                sLine = sLine + '\n'
                ofs.write(sLine)
            ofs.close()

            aDate_out.append(aData_soil_layer)

        #update hru soil parameter
        aSoil_type = aSoil_combination[:,0]
        aSoil_type = np.reshape(aSoil_type, len(aSoil_type))
        aSoil_type = list(aSoil_type)
        for iHru in range(1, self.nhru_combination):
            sSoil_type = self.aHru_combination[iHru-1].sSoil_type
            iSoil_index =  aSoil_type.index(sSoil_type)
            nSoil_layer = self.aHru_combination[iHru-1].nSoil_layer
            nParameter_soil = self.aHru_combination[iHru-1].aSoil[0].nParameter_soil
            for iSoil_layer in range(1, nSoil_layer+1):
                for i in range(nParameter_soil):
                    dummy = aDate_out[iSoil_index]
                    self.aHru_combination[iHru-1].aSoil[iSoil_layer-1].aParameter_soil[i].dValue_current= dummy[iSoil_layer-1, i]

        
        

        return

    def run(self):
        if (self.iFlag_run ==1):            
            sFilename_bash = os.path.join(self.sWorkspace_output,  'run_swat.sh' )
            if (os.path.exists(sFilename_bash)):
                os.chdir(self.sWorkspace_output)
                sCommand = './run_swat.sh '
                print(sCommand)
                p = subprocess.Popen(sCommand, shell= True)
                p.wait()
            pass
        else:
            pass

        

        return    

    def analyze(self, sFilename_output_in=None):
        self.swaty_extract_stream_discharge(sFilename_output_in = sFilename_output_in )
        
        return
    
    def evaluate(self):
        self.swaty_tsplot_stream_discharge()
        return

    def swaty_generate_model_structure_files(self):
        #the files from this step should be saved at the output folder instead of input folder
        self.swaty_prepare_watershed_configuration()
        self.swaty_retrieve_soil_info()

        #update?

        return
    
    def generate_parameter_bounds(self, sFilename_watershed_parameter_bounds_in = None,\
        sFilename_subbasin_parameter_bounds_in = None,\
        sFilename_hru_parameter_bounds_in = None,\
            sFilename_soil_parameter_bounds_in = None      ):

        sFilename_parameter_bounds = self.sFilename_parameter_bounds
        aData_dummy = text_reader_string(sFilename_parameter_bounds, cDelimiter_in=',', iSkipline_in=1)

        aName = aData_dummy[:, 1]
        aLower = aData_dummy[:, 2]
        aUpper = aData_dummy[:, 3]

        nParameter = aName.size

        aParameter_watershed = ['sftmp','smtmp','esco','smfmx','timp','epco']
        aParameter_subbasin = ['ch_k2','ch_n2','plaps','tlaps']
        aParameter_hru = ['cn2', 'rchrg_dp', 'gwqmn', 'gw_revap','revapmn','gw_delay','alpha_bf','ov_n']
        aParameter_soil = ['sol_awc','sol_k','sol_alb','sol_bd']
        #split into different group?

        aData_out_watershed = list()
        aData_out_subbasin = list()
        aData_out_hru = list()
        aData_out_soil = list()
        for i in range(nParameter):
            sPara = aName[i].lower().strip()
            dValue_lower = aLower[i]
            dValue_upper = aUpper[i]
            #sLower = "{:0f}".format( dValue_lower )
            #sUpper = "{:0f}".format( dValue_upper )

            if sPara in aParameter_watershed:
                sLine = sPara + ',' + dValue_lower + ',' + dValue_upper
                aData_out_watershed.append(sLine)
                pass
            else:
                if sPara in aParameter_subbasin:
                    sLine = sPara + ',' + dValue_lower + ',' + dValue_upper
                    aData_out_subbasin.append(sLine)
                    pass
                else:
                    if sPara in aParameter_hru:
                        sLine = sPara + ',' + dValue_lower + ',' + dValue_upper
                        aData_out_hru.append(sLine)
                        pass
                    else:
                        sLine = sPara + ',' + dValue_lower + ',' + dValue_upper
                        aData_out_soil.append(sLine)
                        pass

                    pass
                pass
            pass

        #export
        if sFilename_watershed_parameter_bounds_in is None:
            sFilename_watershed_parameter_bounds = os.path.join(self.sWorkspace_output,  'watershed_parameter_bounds.txt' )
        else:
            sFilename_watershed_parameter_bounds = sFilename_watershed_parameter_bounds_in
        ofs=open(sFilename_watershed_parameter_bounds, 'w') 
        for i in aData_out_watershed:
            ofs.write(i + '\n')
        ofs.close()

        if sFilename_subbasin_parameter_bounds_in is None:
            sFilename_subbasin_parameter_bounds = os.path.join(self.sWorkspace_output,  'subbasin_parameter_bounds.txt' )
        else:
            sFilename_subbasin_parameter_bounds =sFilename_subbasin_parameter_bounds_in
        ofs=open(sFilename_subbasin_parameter_bounds, 'w') 
        for i in aData_out_subbasin:
            ofs.write(i + '\n')
        ofs.close()

        if sFilename_hru_parameter_bounds_in is None:
            sFilename_hru_parameter_bounds = os.path.join(self.sWorkspace_output,  'hru_parameter_bounds.txt' )
        else:
            sFilename_hru_parameter_bounds = sFilename_hru_parameter_bounds_in
        ofs=open(sFilename_hru_parameter_bounds, 'w') 
        for i in aData_out_hru:
            ofs.write(i + '\n')
        ofs.close()

        if sFilename_soil_parameter_bounds_in is None:
            sFilename_soil_parameter_bounds = os.path.join(self.sWorkspace_output,  'soil_parameter_bounds.txt' )
        else:
            sFilename_soil_parameter_bounds = sFilename_soil_parameter_bounds_in
        ofs=open(sFilename_soil_parameter_bounds, 'w') 
        for i in aData_out_soil:
            ofs.write(i + '\n')
        ofs.close()


        return

    def extract_default_parameter_value(self, aParameter_in, sFilename_watershed_in= None,\
        sFilename_subbasin_in = None,\
        sFilename_hru_in = None,\
        sWorkspace_soil_in = None        ):




        #watershed
        aParameter = list()
        for p in aParameter_in:
            if p.iParameter_type == 1:
               aParameter.append(p) 
        self.extract_default_parameter_value_watershed(aParameter, sFilename_watershed_in= sFilename_watershed_in)
        #subbasin
        aParameter.clear()
        for p in aParameter_in:
            if p.iParameter_type == 2:
               aParameter.append(p)
        self.extract_default_parameter_value_subbasin(aParameter, sFilename_subbasin_in=sFilename_subbasin_in)
        #hru
        aParameter.clear()
        for p in aParameter_in:
            if p.iParameter_type == 3:
               aParameter.append(p)
        self.extract_default_parameter_value_hru(aParameter, sFilename_hru_in= sFilename_hru_in)
        #soil
        aParameter.clear()
        for p in aParameter_in:
            if p.iParameter_type == 4:
               aParameter.append(p)
        self.extract_default_parameter_value_soil(aParameter, sWorkspace_soil_in=sWorkspace_soil_in)

        return

    def extract_default_parameter_value_watershed(self, aParameter_watershed, sFilename_watershed_in = None):
        sWorkspace_source_case = self.sWorkspace_simulation_copy
        sWorkspace_target_case = self.sWorkspace_output
        nParameter_watershed = len(aParameter_watershed)
        if nParameter_watershed < 1:
            return

        #open the new file to write out
        if sFilename_watershed_in is None:
            sFilename  = 'watershed_parameter_default.txt'
            sFilename_watershed_out = os.path.join(str(Path(sWorkspace_target_case)) ,  sFilename )   
        else:
            sFilename_watershed_out = sFilename_watershed_in

        if os.path.exists(sFilename_watershed_out):                
            os.remove(sFilename_watershed_out)

        ofs=open(sFilename_watershed_out, 'w') 
        
        #we need to save the array and output them in the last step
        aData_out = np.full(nParameter_watershed, -9999, dtype=float)
        
    
        aExtension = ['.bsn','.wwq']
        aBSN=['sftmp','smtmp','esco','smfmx','timp','epco']
        aWWQ=['ai0']
        aExtension = np.asarray(aExtension)
        nFile_type= len(aExtension)

        #the parameter is located in the different files
        aParameter_table = np.empty( (nFile_type)  , dtype = object )

        #need a better way to control this 
        for iVariable in range(nParameter_watershed):
            sParameter_watershed = aParameter_watershed[iVariable].sName

            if sParameter_watershed in aBSN:
                if( aParameter_table[0] is None  ):
                    aParameter_table[0] = np.array(sParameter_watershed)
                else:
                    aParameter_table[0] = np.append(aParameter_table[0],sParameter_watershed)
                    
                pass
            else:
                if sParameter_watershed in aWWQ:
                    if( aParameter_table[1] is None  ):
                        aParameter_table[1] = np.array(sParameter_watershed)
                    else:
                        aParameter_table[1]=np.append(aParameter_table[1],sParameter_watershed)
                    pass
                pass

        aParameter_user = np.full( (nFile_type) , None , dtype = np.dtype(object) )
        aParameter_count = np.full( (nFile_type) , 0 , dtype = int )
        aParameter_flag = np.full( (nFile_type) , 0 , dtype = int )
        aParameter_index = np.full( (nFile_type) , -1 , dtype = np.dtype(object) )
        for p in range(0, nParameter_watershed):
            para = aParameter_watershed[p].sName
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

  
        #write the head
        sLine = 'watershed'
        for iFile_type in range(0, nFile_type):
            sExtension = aExtension[iFile_type]
            iFlag = aParameter_flag[iFile_type]
            if( iFlag == 1):
                aParameter_indices = np.array(aParameter_index[iFile_type])
                for i in range(len(aParameter_indices)):
                    dummy_index  = aParameter_indices[i]
                    pParameter = aParameter_watershed[dummy_index]       
                    sVariable = pParameter.sName
                    sLine = sLine + ',' + sVariable
        sLine = sLine + '\n'        
        ofs.write(sLine)

        aDate_out = np.full(nParameter_watershed, -9999, dtype=float)

        #write value
        for iFile_type in range(0, nFile_type):
            sExtension = aExtension[iFile_type]
            iFlag = aParameter_flag[iFile_type]
            if( iFlag == 1):
                #there should be only one for each extension       
                sFilename = 'basins' + sExtension
                sFilename_watershed = os.path.join(str(Path(sWorkspace_source_case)) ,  sFilename )             
                nline = line_count(sFilename_watershed)
                ifs=open(sFilename_watershed, 'rb')                   
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
                        if 'sftmp' in sLine.lower() and 'sftmp' in aParameter_filetype : 
                            
                            #this one may not in the same order as shown in the actual fil
                            sValue = (sLine.split('|'))[0].strip()
                            dValue = float(sValue)
                            dummy_index  = np.where( aParameter_filetype=='sftmp' )
                            dummy_index2 = aParameter_indices[dummy_index]
                            aData_out[dummy_index2] = dValue
                            break #important
                        else:
                            if 'smtmp' in sLine.lower() and 'smtmp' in aParameter_filetype: 
                                sValue = (sLine.split('|'))[0].strip()
                                dValue = float(sValue)
                                dummy_index  = np.where( aParameter_filetype=='smtmp' )
                                dummy_index2 = aParameter_indices[dummy_index]
                                aData_out[dummy_index2] = dValue                                
                                break  #important
                            else:

                                if 'esco' in sLine.lower() and 'esco' in aParameter_filetype: 
                                    sValue = (sLine.split('|'))[0].strip()
                                    dValue = float(sValue)
                                    dummy_index  = np.where( aParameter_filetype=='esco' )
                                    dummy_index2 = aParameter_indices[dummy_index]
                                    aData_out[dummy_index2] = dValue
                                    break  #important
                                else:
                                    if 'smfmx' in sLine.lower() and 'smfmx' in aParameter_filetype: 
                                        sValue = (sLine.split('|'))[0].strip()
                                        dValue = float(sValue)
                                        dummy_index  = np.where( aParameter_filetype=='smfmx' )
                                        dummy_index2 = aParameter_indices[dummy_index]
                                        aData_out[dummy_index2] = dValue
                                        break  #important
                                    else:
                                        if 'timp' in sLine.lower() and 'timp' in aParameter_filetype: 
                                            sValue = (sLine.split('|'))[0].strip()
                                            dValue = float(sValue)
                                            dummy_index  = np.where( aParameter_filetype=='timp' )
                                            dummy_index2 = aParameter_indices[dummy_index]
                                            aData_out[dummy_index2] = dValue
                                            break  #important
                                        else:
                                            if 'epco' in sLine.lower() and 'epco' in aParameter_filetype: 
                                                sValue = (sLine.split('|'))[0].strip()
                                                dValue = float(sValue)
                                                dummy_index  = np.where( aParameter_filetype=='epco' )
                                                dummy_index2 = aParameter_indices[dummy_index]
                                                aData_out[dummy_index2] = dValue
                                                break  #important
                                            else:
                                                if 'ai0' in sLine.lower() and 'ai0' in aParameter_filetype: 
                                                    sValue = (sLine.split('|'))[0].strip()
                                                    dValue = float(sValue)
                                                    dummy_index  = np.where( aParameter_filetype=='ai0' )
                                                    dummy_index2 = aParameter_indices[dummy_index]
                                                    aData_out[dummy_index2] = dValue
                                                    break  #important
                                                else:
                                                    pass

                                                pass
                                break  #important


                            
                            
                ifs.close()

        #write parameter value      
        sLine = 'watershed'

        for p in range(0, nParameter_watershed):
            dValue = aData_out[p]

            sValue =  ',' + "{:0f}".format( dValue ) 
            sLine = sLine + sValue

        ofs.write(sLine)
        ofs.close()

        print('Finished writing watershed default parameter file!')
        



        return
    
    def extract_default_parameter_value_subbasin(self, aParameter_subbasin, sFilename_subbasin_in = None):
        sWorkspace_source_case = self.sWorkspace_simulation_copy
        sWorkspace_target_case = self.sWorkspace_output
   
        nParameter_subbasin = len(aParameter_subbasin)
        if(nParameter_subbasin<1):
            #there is nothing to be replaced at all
            print("There is no subbasin parameter to be updated!")
            return
        else:
            pass     
    
        #open the new file to write out
        if sFilename_subbasin_in is None:
            sFilename  = 'subbasin_parameter_default.txt'
            sFilename_subbasin_out = os.path.join(str(Path(sWorkspace_target_case)) ,  sFilename )    
        else:
            sFilename_subbasin_out = sFilename_subbasin_in

        if os.path.exists(sFilename_subbasin_out):                
            os.remove(sFilename_subbasin_out)

        ofs=open(sFilename_subbasin_out, 'w') 
    
        nsubbasin = self.nsubbasin
    
        # we need to identify a list of files that are HRU defined, you can add others later
        aExtension = ['.rte', '.sub']
        #now we can add corresponding possible variables

        aRTE =['ch_k2','ch_n2' ]
        aSUB=['plaps','tlaps']

        aExtension = np.asarray(aExtension)
        nFile_type= aExtension.size

        #the parameter is located in the different files
        aParameter_table = np.empty( (nFile_type)  , dtype = object )

        #need a better way to control this 
        for iVariable in range(nParameter_subbasin):
            sParameter_subbasin = aParameter_subbasin[iVariable].sName

            if sParameter_subbasin in aRTE:

                if( aParameter_table[0] is None  ):
                    aParameter_table[0] = np.array(sParameter_subbasin)
                else:
                    aParameter_table[0]= np.append(aParameter_table[0],sParameter_subbasin)            
            else:
                if sParameter_subbasin in aSUB:
                    if( aParameter_table[1] is None  ):
                        aParameter_table[1] = np.array(sParameter_subbasin)
                    else:
                        aParameter_table[1]= np.append(aParameter_table[1],sParameter_subbasin)   
                    pass
                pass


        aParameter_user = np.full( (nFile_type) , None , dtype = np.dtype(object) )
        aParameter_count = np.full( (nFile_type) , 0 , dtype = int )
        aParameter_flag = np.full( (nFile_type) , 0 , dtype = int )
        aParameter_index = np.full( (nFile_type) , -1 , dtype = np.dtype(object) )
            

        for p in range(0, nParameter_subbasin):
            para = aParameter_subbasin[p].sName
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

        #write the head
        aData_out = np.full((nParameter_subbasin), '', dtype=object)  
        for iFile_type in range(0, nFile_type):
            sExtension = aExtension[iFile_type]
            iFlag = aParameter_flag[iFile_type]
            if( iFlag == 1):
                aParameter_indices = np.array(aParameter_index[iFile_type])
                for i in range(len(aParameter_indices)):
                    dummy_index  = aParameter_indices[i]
                    pParameter = aParameter_subbasin[dummy_index]    
                    sVariable = pParameter.sName   
                    aData_out[dummy_index]= sVariable
                    
        sLine = 'subbasin'            
        for i in range(1, nParameter_subbasin+1):    
            sLine = sLine + ',' + aData_out[i-1]            
        sLine = sLine + '\n'     
             
        ofs.write(sLine)

        #write value
        aData_out = np.full((nsubbasin, nParameter_subbasin), -9999, dtype=float)
        
        for iSubbasin in range(1, nsubbasin+1):
            #subbasin string
            sSubbasin = "{:05d}".format( iSubbasin )    
            for iFile_type in range(0, nFile_type):                
                sExtension = aExtension[iFile_type]
                iFlag = aParameter_flag[iFile_type]
                sFilename = sSubbasin + '0000' + sExtension
                if( iFlag == 1):
                    sFilename_subbasin = os.path.join(str(Path(sWorkspace_source_case)) ,  sFilename )   
                    #open the file to read
                    nline = line_count(sFilename_subbasin)
                    ifs=open(sFilename_subbasin, 'rb')   
                    sLine=(ifs.readline()).rstrip().decode("utf-8", 'ignore')                        
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
                            if 'ch_k2' in sLine.lower()  and 'ch_k2' in aParameter_filetype:
                                sValue = (sLine.split('|'))[0].strip()
                                dValue = float(sValue)
                                dummy_index  = np.where( aParameter_filetype=='ch_k2' )
                                dummy_index2 = aParameter_indices[dummy_index]
                                aData_out[iSubbasin-1, dummy_index2] = dValue    
                                                          
                                break                            
                            else:
                                if 'ch_n2' in sLine.lower() and 'ch_n2' in aParameter_filetype:                                
                                    sValue = (sLine.split('|'))[0].strip()
                                    dValue = float(sValue)
                                    dummy_index  = np.where( aParameter_filetype=='ch_n2' )
                                    dummy_index2 = aParameter_indices[dummy_index]
                                    aData_out[iSubbasin-1, dummy_index2] = dValue   
                                    break
                                else:
                                    if 'plaps' in sLine.lower() and 'plaps' in aParameter_filetype:                                
                                        sValue = (sLine.split('|'))[0].strip()
                                        dValue = float(sValue)
                                        dummy_index  = np.where( aParameter_filetype=='plaps' )
                                        dummy_index2 = aParameter_indices[dummy_index]
                                        aData_out[iSubbasin-1, dummy_index2] = dValue   
                                        break
                                    else:
                                        if 'tlaps' in sLine.lower() and 'tlaps' in aParameter_filetype:                                
                                            sValue = (sLine.split('|'))[0].strip()
                                            dValue = float(sValue)
                                            dummy_index  = np.where( aParameter_filetype=='tlaps' )
                                            dummy_index2 = aParameter_indices[dummy_index]
                                            aData_out[iSubbasin-1, dummy_index2] = dValue   
                                            break
                                        else:
                                            break     
                        
                    #close files
                    ifs.close()
                    
                else:
                    #this file does not need to changed
                    pass
            pass
        
        #write parameter value    
        for iSubbasin in range(1, nsubbasin+1):
            sSubbasin = "{:05d}".format( iSubbasin )   
            sLine = 'subbasin'+sSubbasin 
            for p in range(0, nParameter_subbasin):
                dValue = aData_out[iSubbasin-1, p]

                sValue = ',' + "{:0f}".format( dValue ) 
                sLine = sLine + sValue
            
            sLine = sLine + '\n'

            ofs.write(sLine)
        ofs.close()
        print('Finished writing subbasin default parameter file!')
        return

    def extract_default_parameter_value_hru(self, aParameter_hru, sFilename_hru_in = None):
        sWorkspace_source_case = self.sWorkspace_simulation_copy
        sWorkspace_target_case = self.sWorkspace_output
        nParameter_hru = len(aParameter_hru)
       
        if(nParameter_hru<1):
            #there is nothing to be replaced at all
            print("There is no subbasin parameter to be updated!")
            return
        else:
            pass   
        #open the new file to write out
        if sFilename_hru_in is None:
            sFilename  = 'hru_parameter_default.txt'
            sFilename_hru_out = os.path.join(str(Path(sWorkspace_target_case)) ,  sFilename )    
        else:
            sFilename_hru_out = sFilename_hru_in

        if os.path.exists(sFilename_hru_out):                
            os.remove(sFilename_hru_out)

        ofs=open(sFilename_hru_out, 'w') 
        nsubbasin = self.nsubbasin
        nhru=self.nhru
        nhru_combination = self.nhru_combination
        iFlag_simulation = self.iFlag_simulation    
        sWorkspace_output = self.sWorkspace_output
        sWorkspace_simulation_copy =  self.sWorkspace_simulation_copy    
        sWorkspace_pest_model = sWorkspace_output    
        sFilename_watershed_configuration = self.sFilename_watershed_configuration
        sFilename_hru_info = self.sFilename_hru_info     
        aSubbasin_hru  = text_reader_string( sFilename_watershed_configuration, cDelimiter_in = ',' )
        aHru_configuration = aSubbasin_hru[:,1].astype(int)     
        aHru_info = text_reader_string(sFilename_hru_info)
        aHru_info = np.asarray(aHru_info)      
        aHru_info= aHru_info.reshape( nhru )
        sFilename_hru_combination = self.sFilename_hru_combination        
        aHru_combination = text_reader_string(sFilename_hru_combination)
        aHru_combination = np.asarray(aHru_combination)
        aHru_combination= aHru_combination.reshape(nhru_combination)

        # we need to identify a list of files that are HRU defined, you can add others later
        aExtension = ('.chm','.gw','.hru','.mgt','.sdr', '.sep')
        #now we can add corresponding possible variables
        aCHM =[]
        aGW = ['rchrg_dp', 'gwqmn', 'gw_revap','revapmn','gw_delay','alpha_bf']
        aHRU =['ov_n']
        aMGT = ['cn2']
        aSDR = []
        aSEP =[]
        #aSOL=['sol_awc','sol_k','sol_alb','sol_bd'] 

        aExtension = np.asarray(aExtension)
        nFile_type= len(aExtension)

        #the parameter is located in the different files
        aParameter_table = np.empty( (nFile_type)  , dtype = object )

        #hru level
        for iVariable in range(nParameter_hru):
            sParameter_hru = aParameter_hru[iVariable].sName

            if sParameter_hru in aCHM:
                pass
            else:
                if sParameter_hru in aGW:
                    if( aParameter_table[1] is None  ):
                        aParameter_table[1] = sParameter_hru
                    else:
                        aParameter_table[1]= np.append(aParameter_table[1],sParameter_hru)  
                    pass
                else:
                    if sParameter_hru in aHRU:
                        if( aParameter_table[2] is None  ):
                            aParameter_table[2] = sParameter_hru
                        else:
                            aParameter_table[2]= np.append(aParameter_table[2],sParameter_hru) 
                        pass
                    else:
                        if sParameter_hru in aMGT:
                            if( aParameter_table[3] is None  ):
                                aParameter_table[3] = sParameter_hru
                            else:
                                aParameter_table[3]= np.append(aParameter_table[3],sParameter_hru)                           
                        else:
                            if sParameter_hru in aSDR:
                                pass
                            else: 
                                if sParameter_hru in aSEP:
                                    pass
                                else:                                    
                                    pass           

        aParameter_user = np.full( (nFile_type) , None , dtype = np.dtype(object) ) #list of parameter actually used in this file type
        aParameter_count = np.full( (nFile_type) , 0 , dtype = int ) #how many parameter in this file type
        aParameter_flag = np.full( (nFile_type) , 0 , dtype = int )  #whether there is parameter in this file type
        aParameter_index = np.full( (nFile_type) , -1 , dtype = np.dtype(object) ) #the index of each parameter in this file type
    
        for p in range(0, nParameter_hru):
            para = aParameter_hru[p].sName
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
        

        #write the head
        aData_out = np.full((nParameter_hru), '', dtype=object)    
        
        for iFile_type in range(0, nFile_type):
            sExtension = aExtension[iFile_type]
            iFlag = aParameter_flag[iFile_type]
            if( iFlag == 1):
                aParameter_indices = np.array(aParameter_index[iFile_type])
                for i in range(len(aParameter_indices)):
                    dummy_index  = aParameter_indices[i]
                    pParameter = aParameter_hru[dummy_index]    
                    sVariable = pParameter.sName   
                    aData_out[dummy_index]= sVariable
                    
        sLine = 'hru'            
        for i in range(1, nParameter_hru+1):                
            sValue =  ',' + aData_out[i-1] 
            sLine = sLine +   sValue    
        sLine = sLine + '\n'             
        ofs.write(sLine)       

        #write value
        aData_out = np.full((nhru_combination, nParameter_hru), -9999, dtype=float)         
       
        iHru_index = 0 
        for iSubbasin in range(1, nsubbasin+1):
            sSubbasin = "{:05d}".format( iSubbasin )
            nhru_subbasin = aHru_configuration[ iSubbasin-1]
            for iHru in range(1, nhru_subbasin+1):
                #hru string
                sHru = "{:04d}".format( iHru)
                #find the hry type 
                sHru_code = aHru_info[iHru_index]
                iIndex = np.where(aHru_combination == sHru_code)
                iHru_index = iHru_index + 1
                for iFile_type in range(0, nFile_type):
                    #check whether these is parameter chanage or not
                    sExtension = aExtension[iFile_type]
                    iFlag = aParameter_flag[iFile_type]
                    if( iFlag == 1):
                        if sExtension == '.gw':                         
                            sFilename = sSubbasin + sHru + sExtension
                            sFilename_hru = os.path.join(sWorkspace_source_case , sFilename )                            
                            nline = line_count(sFilename_hru)
                            ifs=open(sFilename_hru, 'rb')   
                            sLine=(ifs.readline()).rstrip().decode("utf-8", 'ignore')                        
                            for iLine in range(nline):    
                                sLine0=(ifs.readline())
                                if len(sLine0) < 1:
                                    continue
                                sLine0=sLine0.rstrip()                                
                                sLine= sLine0.decode("utf-8", 'ignore')                                                            
                                for i in range(0, aParameter_count[iFile_type]):       
                                    aParameter_indices = np.array(aParameter_index[iFile_type])
                                    aParameter_filetype = np.array(aParameter_user[iFile_type])                        
                                    if 'rchrg_dp' in sLine.lower() and 'rchrg_dp' in aParameter_filetype:                                      
                                        sValue = (sLine.split('|'))[0].strip()
                                        dValue = float(sValue)
                                        dummy_index  = np.where( aParameter_filetype=='rchrg_dp' )
                                        dummy_index2 = aParameter_indices[dummy_index]
                                        aData_out[iIndex, dummy_index2] = dValue  
                                        pass                                        
                                    else:
                                        if 'gwqmn' in sLine.lower() and 'gwqmn' in aParameter_filetype:                                         
                                            sValue = (sLine.split('|'))[0].strip()
                                            dValue = float(sValue)
                                            dummy_index  = np.where( aParameter_filetype=='gwqmn' )
                                            dummy_index2 = aParameter_indices[dummy_index]
                                            aData_out[iIndex, dummy_index2] = dValue  
                                            pass
                                        else:
                                            if 'gw_revap' in sLine.lower() and 'gw_revap' in aParameter_filetype:                                         
                                                sValue = (sLine.split('|'))[0].strip()
                                                dValue = float(sValue)
                                                dummy_index  = np.where( aParameter_filetype=='gw_revap' )
                                                dummy_index2 = aParameter_indices[dummy_index]
                                                aData_out[iIndex, dummy_index2] = dValue  
                                                pass
                                            else:
                                                if 'revapmn' in sLine.lower() and 'revapmn' in aParameter_filetype:                                         
                                                    sValue = (sLine.split('|'))[0].strip()
                                                    dValue = float(sValue)
                                                    dummy_index  = np.where( aParameter_filetype=='revapmn' )
                                                    dummy_index2 = aParameter_indices[dummy_index]
                                                    aData_out[iIndex, dummy_index2] = dValue  
                                                    pass
                                                else:
                                                    if 'alpha_bf' in sLine.lower() and 'alpha_bf' in aParameter_filetype:                                         
                                                        sValue = (sLine.split('|'))[0].strip()
                                                        dValue = float(sValue)
                                                        dummy_index  = np.where( aParameter_filetype=='alpha_bf' )
                                                        dummy_index2 = aParameter_indices[dummy_index]
                                                        aData_out[iIndex, dummy_index2] = dValue  
                                                        pass
                                                    else:
                                                        if 'gw_delay' in sLine.lower() and 'gw_delay' in aParameter_filetype:                                         
                                                            sValue = (sLine.split('|'))[0].strip()
                                                            dValue = float(sValue)
                                                            dummy_index  = np.where( aParameter_filetype=='gw_delay' )
                                                            dummy_index2 = aParameter_indices[dummy_index]
                                                            aData_out[iIndex, dummy_index2] = dValue  
                                                            pass
                                                        else:
                                                            break
                                        
                                                                       
                            #close files
                            ifs.close()
                         
                            pass
                        else:
                            if sExtension == '.hru':
                                sFilename = sSubbasin + sHru + sExtension
                                sFilename_hru = os.path.join(sWorkspace_source_case , sFilename )
                                sFilename_hru = os.path.join(sWorkspace_source_case , sFilename )                            
                                nline = line_count(sFilename_hru)
                                ifs=open(sFilename_hru, 'rb')   
                                sLine=(ifs.readline()).rstrip().decode("utf-8", 'ignore')                                                       
                                for iLine in range(nline):    
                                    sLine0=(ifs.readline())
                                    if len(sLine0) < 1:
                                        continue
                                    sLine0=sLine0.rstrip()                                
                                    sLine= sLine0.decode("utf-8", 'ignore')  
                                    for i in range(0, aParameter_count[iFile_type]):       
                                        aParameter_indices = np.array(aParameter_index[iFile_type])
                                        aParameter_filetype = np.array(aParameter_user[iFile_type])                                                                        
                                        if 'ov_n' in sLine.lower() and 'ov_n' in aParameter_filetype: 
                                            sValue = (sLine.split('|'))[0].strip()
                                            dValue = float(sValue)
                                            dummy_index  = np.where( aParameter_filetype=='ov_n' )
                                            dummy_index2 = aParameter_indices[dummy_index]
                                            aData_out[iIndex, dummy_index2] = dValue  
                                            break
                                        else:                                                                                       
                                            break
                                pass
                            else: #mgt
                                sFilename = sSubbasin + sHru + sExtension
                                sFilename_hru = os.path.join(sWorkspace_source_case , sFilename )
                                sFilename_hru = os.path.join(sWorkspace_source_case , sFilename )                            
                                nline = line_count(sFilename_hru)
                                ifs=open(sFilename_hru, 'rb')   
                                sLine=(ifs.readline()).rstrip().decode("utf-8", 'ignore')                                                       
                                for iLine in range(nline):    
                                    sLine0=(ifs.readline())
                                    if len(sLine0) < 1:
                                        continue
                                    sLine0=sLine0.rstrip()                                
                                    sLine= sLine0.decode("utf-8", 'ignore')  
                                    for i in range(0, aParameter_count[iFile_type]):       
                                        aParameter_indices = np.array(aParameter_index[iFile_type])
                                        aParameter_filetype = np.array(aParameter_user[iFile_type])                                                                        
                                        if 'cn2' in sLine.lower() and 'cn2' in aParameter_filetype: 
                                            sValue = (sLine.split('|'))[0].strip()
                                            dValue = float(sValue)
                                            dummy_index  = np.where( aParameter_filetype=='cn2' )
                                            dummy_index2 = aParameter_indices[dummy_index]
                                            aData_out[iIndex, dummy_index2] = dValue  

                                            break
                                        else:
                                                                                       
                                            break
                               
                           
                                ifs.close()
                           
                    else:
                        #this file does not need to changed
                        pass

                pass
        
        #write parameter value    
        for iHru in range(1, nhru_combination+1):
            sHru = "{:05d}".format( iHru )   
            sLine = 'hru' +sHru 
            for p in range(0, nParameter_hru):
                dValue = aData_out[iHru-1, p]
                sValue = ',' + "{:0f}".format( dValue ) 
                sLine = sLine + sValue
            
            sLine = sLine + '\n'
            ofs.write(sLine)
        ofs.close()
        print('Finished writing hru default parameter file!')
        return

    def extract_default_parameter_value_soil(self, aParameter_soil, sWorkspace_soil_in = None):
        sWorkspace_source_case = self.sWorkspace_simulation_copy
        sWorkspace_target_case = self.sWorkspace_output
        nParameter_soil = len(aParameter_soil)
        if(nParameter_soil<1):
            #there is nothing to be replaced at all
            print("There is no subbasin parameter to be updated!")
            return
        else:
            pass   

        #get soil layer info
        nsubbasin = self.nsubbasin
        nhru=self.nhru
        nhru_combination = self.nhru_combination
        nsoil_combination = self.nsoil_combination
        iFlag_simulation = self.iFlag_simulation    
        sWorkspace_output = self.sWorkspace_output
        sWorkspace_simulation_copy =  self.sWorkspace_simulation_copy    
        sWorkspace_pest_model = sWorkspace_output    
        sFilename_watershed_configuration = self.sFilename_watershed_configuration
        sFilename_hru_info = self.sFilename_hru_info     
        aSubbasin_hru  = text_reader_string( sFilename_watershed_configuration, cDelimiter_in = ',' )
        aHru_configuration = aSubbasin_hru[:,1].astype(int)     
        aHru_info = text_reader_string(sFilename_hru_info)
        aHru_info = np.asarray(aHru_info)      
        aHru_info= aHru_info.reshape( nhru )
        sFilename_hru_combination = self.sFilename_hru_combination        
        aHru_combination = text_reader_string(sFilename_hru_combination)
        aHru_combination = np.asarray(aHru_combination)
        aHru_combination= aHru_combination.reshape(nhru_combination)
        sFilename_soil_combination = self.sFilename_soil_combination
        aSoil_combination = text_reader_string(sFilename_soil_combination, cDelimiter_in = ',')
        aSoil_combination = np.asarray(aSoil_combination)
        aSoil_combination= aSoil_combination.reshape(nsoil_combination, 2) 
        aSoil_combination_dummy= aSoil_combination[:,0]
        sFilename_soil_info = self.sFilename_soil_info
        aSoil_info = text_reader_string(sFilename_soil_info, cDelimiter_in = ',')
        aSoil_info = np.array(aSoil_info)[:,0]
        aSoil_info= aSoil_info.reshape(nhru) 
        aSOL=['sol_awc','sol_k','sol_alb','sol_bd'] 
        aExtension = np.array(['.sol'])
        nFile_type= (aExtension).size

        #hru level
        #the parameter is located in the different files
        aParameter_table = np.empty( (nFile_type)  , dtype = object )
        for iVariable in range(nParameter_soil):
            sParameter_hru = aParameter_soil[iVariable].sName                
            if sParameter_hru in aSOL:
                if( aParameter_table[0] is None  ):
                    aParameter_table[0] = sParameter_hru
                else:
                    aParameter_table[0]= np.append(aParameter_table[0],sParameter_hru)  
                pass
            else:
                pass           
        aParameter_user = np.full( (nFile_type) , None , dtype = np.dtype(object) ) #list of parameter actually used in this file type
        aParameter_count = np.full( (nFile_type) , 0 , dtype = int ) #how many parameter in this file type
        aParameter_flag = np.full( (nFile_type) , 0 , dtype = int )  #whether there is parameter in this file type
        aParameter_index = np.full( (nFile_type) , -1 , dtype = np.dtype(object) ) #the index of each parameter in this file type
        for p in range(0, nParameter_soil):
            para = aParameter_soil[p].sName
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

        for iSoil in range(1, nsoil_combination+1):
            sSoil_type =  "{:02d}".format( iSoil )
            #open the new file to write out
            sFilename  = 'soiltype' + sSoil_type + '_parameter_default.txt'
            if sWorkspace_soil_in is None:                
                sFilename_soil_out = os.path.join(str(Path(sWorkspace_target_case)) ,  sFilename ) 
            else:
                sFilename_soil_out = os.path.join(sWorkspace_soil_in ,  sFilename ) 
                
            ssoil_code = aSoil_combination[iSoil-1,0]
            nSoil_layer = int(aSoil_combination[iSoil-1,1])
            if os.path.exists(sFilename_soil_out):                
                os.remove(sFilename_soil_out)

            ofs=open(sFilename_soil_out, 'w')          

            #write the head
            aData_out = np.full((nParameter_soil), '', dtype=object)    

            for iFile_type in range(0, nFile_type):
                sExtension = aExtension[iFile_type]
                iFlag = aParameter_flag[iFile_type]
                if( iFlag == 1):
                    aParameter_indices = np.array(aParameter_index[iFile_type])
                    for i in range(len(aParameter_indices)):
                        dummy_index  = aParameter_indices[i]
                        pParameter = aParameter_soil[dummy_index]    
                        sVariable = pParameter.sName   
                        aData_out[dummy_index]= sVariable

            sLine = 'soillayer'            
            for i in range(1, nParameter_soil+1):    
                sLine = sLine + ', ' + aData_out[i-1]            
            sLine = sLine + '\n'             
            ofs.write(sLine)      

            #write value
            aData_out = np.full((nSoil_layer, nParameter_soil), -9999, dtype=float) 

            iHru_index = 0 
            for iSubbasin in range(1, nsubbasin+1):
                sSubbasin = "{:05d}".format( iSubbasin )
                nhru_subbasin = aHru_configuration[ iSubbasin-1]
                for iHru in range(1, nhru_subbasin+1):
                    #hru string
                    sHru = "{:04d}".format( iHru)
                    #find the hry type 
                    #sHru_code = aHru_info[iHru_index]
                    sSoil_code = aSoil_info[iHru_index]
                    iHru_index = iHru_index + 1
                    if ssoil_code != sSoil_code:
                        #print(sSoil_code, ssoil_code)
                        continue                    
                    iIndex = np.where(aSoil_combination_dummy == sSoil_code)                    
                    for iFile_type in range(0, nFile_type):
                        #check whether these is parameter chanage or not
                        sExtension = aExtension[iFile_type]
                        iFlag = aParameter_flag[iFile_type]
                        if( iFlag == 1):
                            if sExtension == '.sol':                         
                                sFilename = sSubbasin + sHru + sExtension
                                sFilename_hru = os.path.join(sWorkspace_source_case , sFilename )                            
                                nline = line_count(sFilename_hru)
                                ifs=open(sFilename_hru, 'rb')   
                                sLine=(ifs.readline()).rstrip().decode("utf-8", 'ignore')                        
                                for iLine in range(nline):    
                                    sLine0=(ifs.readline())
                                    if len(sLine0) < 1:
                                        continue
                                    sLine0=sLine0.rstrip()                                
                                    sLine= sLine0.decode("utf-8", 'ignore')                                                            
                                    for i in range(0, aParameter_count[iFile_type]):       
                                        aParameter_indices = np.array(aParameter_index[iFile_type])
                                        aParameter_filetype = np.array(aParameter_user[iFile_type])                        
                                        if 'ave. aw incl. rock' in sLine.lower() and 'sol_awc' in aParameter_filetype:                                      
                                            sValue = (sLine.split(':'))[1].strip()
                                            aValue = np.array(sValue.split()).astype(float)   
                                            aValue = np.reshape(aValue, (nSoil_layer,1))                                                     
                                            dummy_index  = np.where( aParameter_filetype=='sol_awc' )
                                            dummy_index2 = aParameter_indices[dummy_index]
                                            aData_out[:, dummy_index2] = aValue
                                            pass                                        
                                        else:
                                            if 'ksat.' in sLine.lower() and 'sol_k' in aParameter_filetype:                                         
                                                sValue = (sLine.split(':'))[1].strip()
                                                aValue = np.array(sValue.split()).astype(float)   
                                                aValue = np.reshape(aValue, (nSoil_layer,1))                                                     
                                                dummy_index  = np.where( aParameter_filetype=='sol_k' )
                                                dummy_index2 = aParameter_indices[dummy_index]
                                                aData_out[:, dummy_index2] = aValue 
                                                pass
                                            else:
                                                if 'soil albedo' in sLine.lower() and 'sol_alb' in aParameter_filetype:                                         
                                                    sValue = (sLine.split(':'))[1].strip()
                                                    aValue = np.array(sValue.split()).astype(float)   
                                                    aValue = np.reshape(aValue, (nSoil_layer,1))                                                     
                                                    dummy_index  = np.where( aParameter_filetype=='sol_alb' )
                                                    dummy_index2 = aParameter_indices[dummy_index]
                                                    aData_out[:, dummy_index2] = aValue 
                                                    pass
                                                else:
                                                    if 'bulk density moist' in sLine.lower() and 'sol_bd' in aParameter_filetype:                                         
                                                        sValue = (sLine.split(':'))[1].strip()
                                                        aValue = np.array(sValue.split()).astype(float)   
                                                        aValue = np.reshape(aValue, (nSoil_layer,1))                                                     
                                                        dummy_index  = np.where( aParameter_filetype=='sol_bd' )
                                                        dummy_index2 = aParameter_indices[dummy_index]
                                                        aData_out[:, dummy_index2] = aValue  
                                                        break
                                                    else:
                                                        pass
                                                

                                #close files
                                ifs.close()

            
            for iSoil_layer in range(1, nSoil_layer+1):
                sSoil_layer = "{:02d}".format( iSoil_layer )
                sLine = 'soillayer'+sSoil_layer 
                for i in range(0, nParameter_soil):
                    dValue = aData_out[iSoil_layer-1, i]
                    sValue =  ',' + "{:0f}".format( dValue ) 
                    sLine = sLine  + sValue

                sLine = sLine + '\n'
                ofs.write(sLine)

            ofs.close()
            print('Finished writing soil default parameter file!')
            pass
            
            
        return

    def swaty_prepare_watershed_configuration(self):
        #process hru report if needed
        if(os.path.isfile(self.sFilename_hru_info) \
            and os.path.isfile(self.sFilename_hru_combination) \
                and os.path.isfile(self.sFilename_watershed_configuration)):
            return
    

        sFilename_hru_report = self.sFilename_HRULandUseSoilsReport
        print(sFilename_hru_report)
        if os.path.isfile(sFilename_hru_report):
            pass
        else:
            print('The HRU report file does not exist!')
            return
        ifs=open(sFilename_hru_report,'r')

        #we also need to record the number of subbasin and hru
        #this file will store how many hru are in each subbasin
        #this file will be used to generate model imput files in the calibration process
        
        ofs = open( self.sFilename_watershed_configuration, 'w' )  

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
                sLine = "{:05d}".format( iSubbasin ) + ', ' + "{:04d}".format( iHru )  + '\n'
                ofs.write(sLine)
                iSubbasin = iSubbasin+1

                continue
            else:
                sLine=ifs.readline()


        ifs.close() #close hru report file
        ofs.close() #save watershed configuration file
        #save it to a file
        #this file store all the existing unique hru type        
        ofs = open(self.sFilename_hru_combination, 'w')
        for item in lookup_table1:
            ofs.write("%s\n" % item)
        ofs.close()

        #this file store all the hru information, some hru belong to the same type        
        ofs = open(self.sFilename_hru_info, 'w')
        for item in lookup_table2:
            ofs.write("%s\n" % item)
        ofs.close()   
        print('finished')    

    def swaty_retrieve_soil_info(self):
        sWorkspace_source_case = self.sWorkspace_simulation_copy
        sWorkspace_target_case = self.sWorkspace_output
        sFilename_watershed_configuration = self.sFilename_watershed_configuration
        sFilename_hru_info = self.sFilename_hru_info
        
        aSoil_name=list()
        aSoil_layer=list()
        aSoil_info_name = list()
        aSoil_info_layer = list()
        #check whether file exist
        if os.path.isfile(sFilename_watershed_configuration):
            pass
        else:
            print('The file does not exist: ' + sFilename_watershed_configuration)
            return
        aSubbasin_hru  = text_reader_string( sFilename_watershed_configuration, cDelimiter_in = ',' )
        aHru = aSubbasin_hru[:,1].astype(int)
        nhru = sum(aHru)
        #find how many soil layer in each hru
        sExtension='.sol'
        for iSubbasin in range(1, self.nsubbasin+1):
            
            sSubbasin = "{:05d}".format( iSubbasin )
            nhru = aHru[ iSubbasin-1]
            #loop through all hru in this subbasin
            for iHru in range(1, nhru+1):
                #hru string
                sHru = "{:04d}".format( iHru )
                sFilename = sSubbasin + sHru + sExtension
                sFilename_hru = os.path.join(sWorkspace_source_case , sFilename )
                ifs=open(sFilename_hru, 'rb')   
                sLine=(ifs.readline()).rstrip().decode("utf-8", 'ignore')
                while sLine:
                            
                    if 'soil name' in sLine.lower() : 
                        #print(sLine)
                        dummy = sLine.split(':')  
                        dummy_soil=dummy[1].rstrip()

                        sLine=(ifs.readline()).rstrip().decode("utf-8", 'ignore')
                        while sLine:
                            if 'bulk density moist' in sLine.lower():
                                dummy = sLine.split(':')  
                                dummy1=dummy[1].rstrip()
                                dummy2=dummy1.split()
                                nSoil_layer=len(dummy2)
                                
                                #sLine=(ifs.readline()).rstrip().decode("utf-8", 'ignore')
                                break
                            else:
                                sLine=(ifs.readline()).rstrip().decode("utf-8", 'ignore')
                        

                        if dummy_soil not in aSoil_name:
                            aSoil_name.append(dummy_soil)
                            aSoil_layer.append(nSoil_layer)
                        else:
                            #sLine=(ifs.readline()).rstrip().decode("utf-8", 'ignore')
                            pass

                        aSoil_info_name.append(dummy_soil)
                        aSoil_info_layer.append(nSoil_layer)
                                
                    else:
                        sLine=(ifs.readline()).rstrip().decode("utf-8", 'ignore')


            pass
        #save 
        ofs = open(self.sFilename_soil_combination, 'w')
        nsoil = len(aSoil_name)
        for i in range(nsoil):
            sLine = aSoil_name[i].strip() + ',' + "{:0d}".format( aSoil_layer[i]) + '\n'
            ofs.write(sLine)
        ofs.close()

        ofs = open(self.sFilename_soil_info, 'w')
        nsoil = len(aSoil_info_layer)
        for i in range(nsoil):
            sLine = aSoil_info_name[i].strip() + ','  + "{:0d}".format( aSoil_info_layer[i]) + '\n'
            ofs.write(sLine)
        ofs.close()
        return
    
    def swaty_prepare_watershed_parameter_file(self):
        """
        #prepare the pest control file
        """      
        sWorkspace_output = self.sWorkspace_output    

        iFlag_simulation = self.iFlag_simulation
        iFlag_watershed = self.iFlag_watershed

        aParameter_watershed = self.pWatershed.aParameter_watershed
        nParameter_watershed = self.pWatershed.nParameter_watershed

        sFilename_watershed_template = os.path.join(str(Path(sWorkspace_output)), 'watershed.para' )     
        
        if iFlag_watershed ==1:    
            ofs = open(sFilename_watershed_template, 'w')

            sLine = 'watershed'
            for i in range(nParameter_watershed):
                sVariable = aParameter_watershed[i].sName
                sLine = sLine + ',' + sVariable
            sLine = sLine + '\n'        
            ofs.write(sLine)

            sLine = 'watershed'
            for i in range(nParameter_watershed):
                sValue =  "{:5.2f}".format( aParameter_watershed[i].dValue_init )            
                sLine = sLine + ', ' + sValue 
                #print('watershed parameter: '+ sLine)

            sLine = sLine + '\n'
            ofs.write(sLine)
            ofs.close()
            print('watershed parameter is ready!')



        return

    def swaty_prepare_watershed_template_file(self, sFilename_watershed_template_in=None):
        """
        #prepare the pest control file
        """      
        sWorkspace_output = self.sWorkspace_output    

        iFlag_simulation = self.iFlag_simulation
        iFlag_watershed = self.iFlag_watershed

        aParameter_watershed = self.pWatershed.aParameter_watershed
        nParameter_watershed = self.pWatershed.nParameter_watershed
        if sFilename_watershed_template_in is None:
            sFilename_watershed_template = os.path.join(str(Path(sWorkspace_output)), 'watershed.tpl' )     
        else:
            sFilename_watershed_template = sFilename_watershed_template_in

        if iFlag_watershed ==1:    
            ofs = open(sFilename_watershed_template, 'w')
            sLine = 'ptf $\n'
            ofs.write(sLine)
            sLine = 'watershed'
            for i in range(nParameter_watershed):
                sVariable = aParameter_watershed[i].sName
                sLine = sLine + ',' + sVariable
            sLine = sLine + '\n'        
            ofs.write(sLine)

            sLine = 'watershed'
            for i in range(nParameter_watershed):
                sValue =   aParameter_watershed[i].sName            
                sValue = ' $' +  sValue    + '$'     
                sLine = sLine + ', ' + sValue                

            sLine = sLine + '\n'
            ofs.write(sLine)
            ofs.close()
            print('watershed template is ready!')



        return
    
    def swaty_prepare_subbasin_parameter_file(self):
        """
        #prepare the pest control file
        """      
        sWorkspace_output = self.sWorkspace_output    
        
        iFlag_subbasin = self.iFlag_subbasin
        
        nsubbasin = self.nsubbasin

        
        
        sFilename_subbasin_template = os.path.join(str(Path(sWorkspace_output)) ,  'subbasin.para' )  
        
        if iFlag_subbasin ==1:    
            ofs = open(sFilename_subbasin_template, 'w')

           
            aParameter_subbasin_name = self.aSubbasin[0].aParameter_subbasin_name
            nParameter_subbasin = self.aSubbasin[0].nParameter_subbasin

            sLine = 'subbasin'

            for i in range(nParameter_subbasin):
                sVariable = aParameter_subbasin_name[i]
                sLine = sLine + ',' + sVariable
            sLine = sLine + '\n'        
            ofs.write(sLine)

            for iSubbasin in range(1, nsubbasin+1):

                aParameter_subbasin = self.aSubbasin[iSubbasin-1].aParameter_subbasin
                nParameter_subbasin = self.aSubbasin[iSubbasin-1].nParameter_subbasin
                sSubbasin = "{:05d}".format( iSubbasin )
                sLine = 'subbasin' + sSubbasin 
                for i in range(nParameter_subbasin):
                    sValue =  "{:5.2f}".format( aParameter_subbasin[i].dValue_init ) 
                    #sIndex + "{:05d}".format( iSubbasin + 1)

                    sLine = sLine + ', ' + sValue 
                sLine = sLine + '\n'
                ofs.write(sLine)
            ofs.close()
            print('subbasin parameter is ready!')



        return

    def swaty_prepare_subbasin_template_file(self, sFilename_subbasin_template_in=None):
        """
        #prepare the pest control file
        """      
        sWorkspace_output = self.sWorkspace_output    
        
        iFlag_subbasin = self.iFlag_subbasin
        
        nsubbasin = self.nsubbasin

        if sFilename_subbasin_template_in is None:
        
            sFilename_subbasin_template = os.path.join(str(Path(sWorkspace_output)) ,  'subbasin.tpl' )  
        else:
            sFilename_subbasin_template = sFilename_subbasin_template_in

        if iFlag_subbasin ==1:    
            ofs = open(sFilename_subbasin_template, 'w')
            sLine = 'ptf $\n'
            ofs.write(sLine)
           
            aParameter_subbasin_name = self.aSubbasin[0].aParameter_subbasin_name
            nParameter_subbasin = self.aSubbasin[0].nParameter_subbasin

            sLine = 'subbasin'

            for i in range(nParameter_subbasin):
                sVariable = aParameter_subbasin_name[i]
                sLine = sLine + ',' + sVariable
            sLine = sLine + '\n'        
            ofs.write(sLine)

            sLine = 'subbasin'
            for i in range(nParameter_subbasin):                
                sValue =   aParameter_subbasin_name[i]          
                sValue = ' $' +  sValue    + '$'                 
                sLine = sLine + ', ' + sValue 
            sLine = sLine + '\n'
            ofs.write(sLine)
            ofs.close()
            print('subbasin template is ready!')



        return

    def swaty_prepare_hru_parameter_file(self):
        """
        #prepare the pest control file
        """      
   
        sWorkspace_output = self.sWorkspace_output    
        iFlag_simulation = self.iFlag_simulation    
        iFlag_hru = self.iFlag_hru
        aParameter_hru_name=self.aHru_combination[0].aParameter_hru_name
        if os.path.isfile(self.sFilename_hru_combination):
            pass
        else:
            print('The file does not exist!')
            return
        aData_all = text_reader_string(self.sFilename_hru_combination)
        nhru_type = len(aData_all)
        sFilename_hru_template = os.path.join(str(Path(sWorkspace_output)) ,  'hru.para' )  
        
        if iFlag_hru ==1:    
            ofs = open(sFilename_hru_template, 'w')
            nParameter_hru = self.aHru_combination[0].nParameter_hru
            sLine = 'hru'
            for i in range(nParameter_hru):
                sVariable = aParameter_hru_name[i]
                sLine = sLine + ',' + sVariable
            sLine = sLine + '\n'        
            ofs.write(sLine)

            for iHru_type in range(0, nhru_type):
                sHru_type = "{:04d}".format( iHru_type + 1)
                sLine = 'hru'+ sHru_type 

                nParameter_hru = self.aHru_combination[iHru_type].nParameter_hru
                aParameter_hru = self.aHru_combination[iHru_type].aParameter_hru


                for i in range(nParameter_hru):
                    sValue =  "{:5.2f}".format( aParameter_hru[i].dValue_init )            
                    sLine = sLine + ', ' + sValue 
                sLine = sLine + '\n'
                ofs.write(sLine)
            ofs.close()
            print('hru parameter is ready!')

        return

    def swaty_prepare_hru_template_file(self, sFilename_hru_template_in = None):
        """
        #prepare the pest control file
        """      
   
        sWorkspace_output = self.sWorkspace_output    
        iFlag_simulation = self.iFlag_simulation    
        iFlag_hru = self.iFlag_hru
        aParameter_hru_name=self.aHru_combination[0].aParameter_hru_name
        if os.path.isfile(self.sFilename_hru_combination):
            pass
        else:
            print('The file does not exist!')
            return
        aData_all = text_reader_string(self.sFilename_hru_combination)
        nhru_type = len(aData_all)

        if sFilename_hru_template_in is None:
            sFilename_hru_template = os.path.join(str(Path(sWorkspace_output)) ,  'hru.tpl' )  
        else:
            sFilename_hru_template = sFilename_hru_template_in
        
        if iFlag_hru ==1:    
            ofs = open(sFilename_hru_template, 'w')
            sLine = 'ptf $\n'
            ofs.write(sLine)
            nParameter_hru = self.aHru_combination[0].nParameter_hru
            sLine = 'hru'
            for i in range(nParameter_hru):
                sVariable = aParameter_hru_name[i]
                sLine = sLine + ',' + sVariable
            sLine = sLine + '\n'        
            ofs.write(sLine)

            sLine = 'hru'
            for i in range(nParameter_hru):
                sValue = aParameter_hru_name[i]    
                sValue = ' $' +  sValue    + '$'       
                sLine = sLine + ', ' + sValue 
            sLine = sLine + '\n'
            ofs.write(sLine)
            ofs.close()
            print('hru template is ready!')

        return

    def swaty_prepare_soil_parameter_file(self):
        sWorkspace_output = self.sWorkspace_output    
        iFlag_simulation = self.iFlag_simulation    
        iFlag_hru = self.iFlag_hru
        aParameter_hru_name=self.aHru_combination[0].aParameter_hru_name
        if os.path.isfile(self.sFilename_hru_combination):
            pass
        else:
            print('The file does not exist!')
            return
        aData_all = text_reader_string(self.sFilename_hru_combination)
        nhru_type = len(aData_all)
        
        sFilename_soil_combination = self.sFilename_soil_combination
        aSoil_combination = text_reader_string(sFilename_soil_combination, cDelimiter_in = ',')
        aSoil_combination = np.asarray(aSoil_combination)
        nsoil_combination = self.nsoil_combination
        aSoil_combination= aSoil_combination.reshape(nsoil_combination, 2) 
        aSoil_combination_dummy= aSoil_combination[:,0]
        sFilename_soil_info = self.sFilename_soil_info
        aSoil_info = text_reader_string(sFilename_soil_info, cDelimiter_in = ',')
        aSoil_info = np.array(aSoil_info)[:,0]
        

        if iFlag_hru ==1:       

            #single para for testing  
            sFilename_soil_template = os.path.join(str(Path(sWorkspace_output)) ,  'soil.para' )  
            ofs = open(sFilename_soil_template, 'w')
            nParameter_soil = self.aHru_combination[0].aSoil[0].nParameter_soil
            aParameter_soil_name = self.aHru_combination[0].aSoil[0].aParameter_soil_name
            sLine = 'soil'
            for i in range(1,nParameter_soil+1):
                sVariable = aParameter_soil_name[i-1]
                sLine = sLine + ',' + sVariable
            sLine = sLine + '\n'        
            ofs.write(sLine)      
            
            sSoil_layer = "{:02d}".format( 1 )      
            sLine = 'soillayer'+ sSoil_layer           
            aParameter_soil = self.aHru_combination[0].aSoil[0].aParameter_soil
            for i in range(nParameter_soil):
                sValue =  "{:5.2f}".format( aParameter_soil[i].dValue_init )            
                sLine = sLine + ',' + sValue 
            sLine = sLine + '\n'
            ofs.write(sLine)


            for iSoil_type in range(1, nsoil_combination+1):
                sSoil_type = "{:02d}".format( iSoil_type )
                ssoil_code = aSoil_combination[iSoil_type-1,0]
                nSoil_layer = int(aSoil_combination[iSoil_type-1,1])
                sFilename_soil_template = os.path.join(str(Path(sWorkspace_output)) ,  'soiltype'+sSoil_type+ '.para' )  
                ofs = open(sFilename_soil_template, 'w')
                nParameter_soil = self.aHru_combination[0].aSoil[0].nParameter_soil
                aParameter_soil_name = self.aHru_combination[0].aSoil[0].aParameter_soil_name
                sLine = 'soillayer'
                for i in range(1,nParameter_soil+1):
                    sVariable = aParameter_soil_name[i-1]
                    sLine = sLine + ',' + sVariable
                sLine = sLine + '\n'        
                ofs.write(sLine)  
                
                           
                for iSoil_layer in range(1, nSoil_layer + 1):  
                    sSoil_layer = "{:02d}".format( iSoil_layer )      
                    sLine = 'soillayer'+ sSoil_layer           
                    aParameter_soil = self.aHru_combination[0].aSoil[0].aParameter_soil
                    for i in range(nParameter_soil):
                        sValue =  "{:5.2f}".format( aParameter_soil[i].dValue_init )            
                        sLine = sLine + ',' + sValue 
                    sLine = sLine + '\n'
                    ofs.write(sLine)
            ofs.close()
            print('soil parameter is ready!')

        return

    def swaty_prepare_soil_template_file(self, sFilename_soil_template_in = None):
        sWorkspace_output = self.sWorkspace_output    
        iFlag_simulation = self.iFlag_simulation    
        iFlag_hru = self.iFlag_hru
        aParameter_hru_name=self.aHru_combination[0].aParameter_hru_name
        if os.path.isfile(self.sFilename_hru_combination):
            pass
        else:
            print('The file does not exist!')
            return
        aData_all = text_reader_string(self.sFilename_hru_combination)
        nhru_type = len(aData_all)
        
        sFilename_soil_combination = self.sFilename_soil_combination
        aSoil_combination = text_reader_string(sFilename_soil_combination, cDelimiter_in = ',')
        aSoil_combination = np.asarray(aSoil_combination)
        nsoil_combination = self.nsoil_combination
        aSoil_combination= aSoil_combination.reshape(nsoil_combination, 2) 
        aSoil_combination_dummy= aSoil_combination[:,0]
        sFilename_soil_info = self.sFilename_soil_info
        aSoil_info = text_reader_string(sFilename_soil_info, cDelimiter_in = ',')
        aSoil_info = np.array(aSoil_info)[:,0]
        

        if iFlag_hru ==1:                
            if sFilename_soil_template_in is None:
                sFilename_soil_template = os.path.join(str(Path(sWorkspace_output)) ,  'soil.tpl' )  
            else:
                sFilename_soil_template = sFilename_soil_template_in
            ofs = open(sFilename_soil_template, 'w')
            sLine = 'ptf $\n'
            ofs.write(sLine)
            nParameter_soil = self.aHru_combination[0].aSoil[0].nParameter_soil
            aParameter_soil_name = self.aHru_combination[0].aSoil[0].aParameter_soil_name                 
            sLine='soil'  
            for i in range(nParameter_soil):
                sValue =  aParameter_soil_name[i]       
                sLine = sLine + ', ' + sValue 
            sLine = sLine + '\n'
            ofs.write(sLine)

            sLine='soil' 
            for i in range(nParameter_soil):
                sValue =  aParameter_soil_name[i]   
                sValue = ' $' +  sValue    + '$'     
                sLine = sLine + ', ' + sValue 
            sLine = sLine + '\n'
            ofs.write(sLine)

             
            
            ofs.close()
            print('soil template is ready!')

        return

    def swaty_create_pest_instruction_file(self, sFilename_instruction):
        """
        prepare pest instruction file
        """            
        nstress_month = self.nstress_month

        sFilename_observation = os.path.join( self.sWorkspace_input,'discharge_observation_monthly.txt' )
        if os.path.isfile(sFilename_observation):
            pass
        else:
            print(sFilename_observation + ' is missing!')
            return
        aData = text_reader_string(sFilename_observation)
        aDischarge_observation = np.array( aData ).astype(float) 
        nobs_with_missing_value = len(aDischarge_observation)

        aDischarge_observation = np.reshape(aDischarge_observation, nobs_with_missing_value)
        nan_index = np.where(aDischarge_observation == missing_value)

        #write instruction
    
        ofs= open(sFilename_instruction,'w')
        ofs.write('pif $\n')

        #we need to consider that there is missing value in the observations
        #changed from daily to monthly
        for i in range(0, nstress_month):
            dDummy = aDischarge_observation[i]
            if( dDummy != missing_value  ):
                sLine = 'l1' + ' !discharge' + "{:04d}".format(i+1) + '!\n'
            else:
                sLine = 'l1' + ' !dum' + '!\n'
            ofs.write(sLine)

        ofs.close()
        print('The instruction file is prepared successfully!')
        return
    
    def swaty_write_watershed_input_file(self):
        """
        write the input files from the new parameter generated by PEST to each hru file
        """
        aParameter_watershed = self.pWatershed.aParameter_watershed
        nParameter_watershed = self.pWatershed.nParameter_watershed
        if(nParameter_watershed<1):        
            print("There is no watershed parameter to be updated!")
            return
        else:
            pass    
        
        iFlag_simulation = self.iFlag_simulation
        sWorkspace_output = self.sWorkspace_output
        sWorkspace_simulation_copy =  self.sWorkspace_simulation_copy
        sWorkspace_pest_model = sWorkspace_output
        
        aExtension = ['.bsn','.wwq']
        aBSN=['sftmp','smtmp','esco','smfmx','timp','epco']
        aWWQ=['ai0']


        aExtension = np.asarray(aExtension)
        nFile_type= len(aExtension)

        #the parameter is located in the different files
        aParameter_table = np.empty( (nFile_type)  , dtype = object )

        #need a better way to control this 
        for iVariable in range(nParameter_watershed):
            sParameter_watershed = aParameter_watershed[iVariable].sName

            if sParameter_watershed in aBSN:
                if( aParameter_table[0] is None  ):
                    aParameter_table[0] = np.array(sParameter_watershed)
                else:
                    aParameter_table[0] = np.append(aParameter_table[0],sParameter_watershed)
                    
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
      

        for p in range(0, nParameter_watershed):
            para = aParameter_watershed[p].sName
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
            sWorkspace_target_case = sWorkspace_output
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
                            sLine_new = "{:16.3f}".format(  aParameter_watershed[dummy_index2].dValue_current  )     + '    | pest parameter SFTMP' + '\n'
                            ofs.write(sLine_new)
                            print(sLine_new)
                            break #important
                        else:
                            if 'smtmp' in sLine.lower() and 'SMTMP' in aParameter_filetype: 
                                dummy = 'SMTMP'                             
                                dummy_index1 = np.where(aParameter_filetype == dummy)
                                dummy_index2 = aParameter_indices[dummy_index1][0]
                                sLine_new = "{:16.3f}".format(  aParameter_watershed[dummy_index2].dValue_current  )     + '    | pest parameter SMTMP' + '\n'
                                ofs.write(sLine_new)
                                print(sLine_new)
                                break  #important
                            else:

                                if 'esco' in sLine.lower() and 'esco' in aParameter_filetype: 
                                    dummy = 'esco'                             
                                    dummy_index1 = np.where(aParameter_filetype == dummy)
                                    dummy_index2 = aParameter_indices[dummy_index1][0]
                                    sLine_new = "{:16.3f}".format(  aParameter_watershed[dummy_index2].dValue_current   )     + '    | pest parameter ESCO' + '\n'
                                    ofs.write(sLine_new)
                                    print(sLine_new)
                                else:
                                    if 'smfmx' in sLine.lower() and 'smfmx' in aParameter_filetype: 
                                        dummy = 'smfmx'                             
                                        dummy_index1 = np.where(aParameter_filetype == dummy)
                                        dummy_index2 = aParameter_indices[dummy_index1][0]
                                        sLine_new = "{:16.3f}".format(  aParameter_watershed[dummy_index2].dValue_current   )     + '    | pest parameter SMFMX' + '\n'
                                        ofs.write(sLine_new)
                                        print(sLine_new)
                                    else:
                                        if 'timp' in sLine.lower() and 'timp' in aParameter_filetype: 
                                            dummy = 'timp'                             
                                            dummy_index1 = np.where(aParameter_filetype == dummy)
                                            dummy_index2 = aParameter_indices[dummy_index1][0]
                                            sLine_new = "{:16.3f}".format(  aParameter_watershed[dummy_index2].dValue_current   )     + '    | pest parameter TIMP' + '\n'
                                            ofs.write(sLine_new)
                                            print(sLine_new)
                                        else:
                                            if 'epco' in sLine.lower() and 'epco' in aParameter_filetype: 
                                                dummy = 'epco'                             
                                                dummy_index1 = np.where(aParameter_filetype == dummy)
                                                dummy_index2 = aParameter_indices[dummy_index1][0]
                                                sLine_new = "{:16.3f}".format(  aParameter_watershed[dummy_index2].dValue_current   )     + '    | pest parameter EPCO' + '\n'
                                                ofs.write(sLine_new)
                                                print(sLine_new)
                                            else:
                                                sLine = sLine + '\n'
                                                ofs.write(sLine)
                                break  #important


                            
                            
                ifs.close()
                ofs.close()

        print('Finished writing watershed file!')
        return    

    def swaty_write_subbasin_input_file(self):
        """
        write the input files from the new parameter generated by PEST to each hru file
        """
        #aParameter_subbasin = self.aParameter_subbasin
        aParameter_subbasin_name= self.aSubbasin[0].aParameter_subbasin_name
        nParameter_subbasin = self.aSubbasin[0].nParameter_subbasin
        if(nParameter_subbasin<1):
            #there is nothing to be replaced at all
            print("There is no subbasin parameter to be updated!")
            return
        else:
            pass    
        
        iFlag_simulation = self.iFlag_simulation
        sWorkspace_output = self.sWorkspace_output
        sWorkspace_simulation_copy =  self.sWorkspace_simulation_copy       
        sWorkspace_pest_model = sWorkspace_output
        #sWorkspace_data_project = self.sWorkspace_data_project
    
        nsubbasin = self.nsubbasin
    
        # we need to identify a list of files that are HRU defined, you can add others later
        aExtension = ['.rte', '.sub']
        #now we can add corresponding possible variables

        aRTE =['ch_k2','ch_n2' ]
        aSUB=['plaps','tlaps']

        aExtension = np.asarray(aExtension)
        nFile_type= aExtension.size

        #the parameter is located in the different files
        aParameter_table = np.empty( (nFile_type)  , dtype = object )

        #need a better way to control this 
        for iVariable in range(nParameter_subbasin):
            sParameter_subbasin = aParameter_subbasin_name[iVariable]

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
    
        

        for p in range(0, nParameter_subbasin):
            para = aParameter_subbasin_name[p]
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
            sWorkspace_target_case = sWorkspace_output
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

        
        for iSubbasin in range(1, nsubbasin+1):
            #subbasin string
            sSubbasin = "{:05d}".format( iSubbasin )
            aParameter_subbasin = self.aSubbasin[iSubbasin-1].aParameter_subbasin

            #loop through all basin in this subbasin

            for iFile_type in range(0, nFile_type):
                #check whether these is parameter chanage or not
                sExtension = aExtension[iFile_type]
                iFlag = aParameter_flag[iFile_type]
                sFilename = sSubbasin + '0000' + sExtension

                if( iFlag == 1):

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
                    aValue  = np.array(aParameter_subbasin)
                    #aValue = dummy_data[:]
                    while sLine:
                    
                        for i in range(0, aParameter_count[iFile_type]):
                            aParameter_indices = np.array(aParameter_index[iFile_type])
                            aParameter_filetype = np.array(aParameter_user[iFile_type])
                            if 'ch_k2' in sLine.lower()  and 'ch_k2' in aParameter_filetype:    
                                dummy_index1 = np.where(aParameter_filetype == 'ch_k2')                            
                                dummy_index2 = aParameter_indices[dummy_index1][0]
                                sLine_new = "{:14.5f}".format(  aValue[dummy_index2].dValue_current  )     + '    | pest parameter ch_k2 \n'
                                ofs.write(sLine_new)                            
                                break                            
                            else:
                                if 'ch_n2' in sLine.lower() and 'ch_n2' in aParameter_filetype:                                
                                    dummy_index1 = np.where(aParameter_filetype == 'ch_n2')                               
                                    dummy_index2 = aParameter_indices[dummy_index1][0]
                                    sLine_new = "{:14.5f}".format(  aValue[dummy_index2].dValue_current  )     + '    | pest parameter ch_n2 \n'
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

    def swaty_write_hru_input_file(self):
        """
        write the input files from the new parameter generated by PEST to each hru file
        """
    
        #aParameter_hru = self.aParameter_hru
        
        nParameter_hru = self.aHru_combination[0].nParameter_hru
        aParameter_hru_name = self.aHru_combination[0].aParameter_hru_name

        nParameter_soil= self.aHru_combination[0].aSoil[0].nParameter_soil
        aParameter_soil_name = self.aHru_combination[0].aSoil[0].aParameter_soil_name

        nsubbasin = self.nsubbasin
        nhru = self.nhru
        nhru_combination = self.nhru_combination
        if(nParameter_hru<1):
            #there is nothing to be replaced at all
            print("There is no hru parameter to be updated!")
            return
        else:
            pass    
        
        iFlag_simulation = self.iFlag_simulation    
        sWorkspace_output = self.sWorkspace_output
        sWorkspace_simulation_copy =  self.sWorkspace_simulation_copy    
        sWorkspace_pest_model = sWorkspace_output    
        sFilename_watershed_configuration = self.sFilename_watershed_configuration
        sFilename_hru_info = self.sFilename_hru_info     
        aSubbasin_hru  = text_reader_string( sFilename_watershed_configuration, cDelimiter_in = ',' )
        aHru_configuration = aSubbasin_hru[:,1].astype(int)     
        aHru_info = text_reader_string(sFilename_hru_info)
        aHru_info = np.asarray(aHru_info)      
        aHru_info= aHru_info.reshape( nhru )
        sFilename_hru_combination = self.sFilename_hru_combination        
        aHru_combination = text_reader_string(sFilename_hru_combination)
        aHru_combination = np.asarray(aHru_combination)
        aHru_combination= aHru_combination.reshape(nhru_combination)

        # we need to identify a list of files that are HRU defined, you can add others later
        aExtension = ('.chm','.gw','.hru','.mgt','.sdr', '.sep', '.sol')
        #now we can add corresponding possible variables
        aCHM =[]
        aGW = ['rchrg_dp', 'gwqmn', 'gw_revap','revapmn','gw_delay','alpha_bf']
        aHRU =['ov_n']
        aMGT = ['cn2']
        aSDR = []
        aSEP =[]
        aSOL=['sol_awc','sol_k','sol_alb','sol_bd'] 

        aExtension = np.asarray(aExtension)
        nFile_type= len(aExtension)

        #the parameter is located in the different files
        aParameter_table = np.empty( (nFile_type)  , dtype = object )

        #hru level
        for iVariable in range(nParameter_hru):
            sParameter_hru = aParameter_hru_name[iVariable]

            if sParameter_hru in aCHM:
                pass
            else:
                if sParameter_hru in aGW:
                    if( aParameter_table[1] is None  ):
                        aParameter_table[1] = np.array(sParameter_hru)
                    else:
                        aParameter_table[1]=np.append(aParameter_table[1],sParameter_hru)  
                    pass
                else:
                    if sParameter_hru in aHRU:
                        pass
                    else:
                        if sParameter_hru in aMGT:
                            if( aParameter_table[3] is None  ):
                                aParameter_table[3] = np.array(sParameter_hru)
                            else:
                                aParameter_table[3]=np.append(aParameter_table[3],sParameter_hru)                          
                        else:
                            if sParameter_hru in aSDR:
                                pass
                            else: 
                                if sParameter_hru in aSEP:
                                    pass
                                else:
                                    
                                    pass

        #soil level
        for iVariable in range(nParameter_soil):
            sParameter_soil = aParameter_soil_name[iVariable]           
            if sParameter_soil in aSOL:
                if( aParameter_table[6] is None  ):
                    aParameter_table[6] = np.array(sParameter_soil)
                else:
                    aParameter_table[6]= np.append(aParameter_table[6],sParameter_soil)
            else:
                pass                            
                                    
                          

        aParameter_user = np.full( (nFile_type) , None , dtype = np.dtype(object) ) #list of parameter actually used in this file type
        aParameter_count = np.full( (nFile_type) , 0 , dtype = int ) #how many parameter in this file type
        aParameter_flag = np.full( (nFile_type) , 0 , dtype = int )  #whether there is parameter in this file type
        aParameter_index = np.full( (nFile_type) , -1 , dtype = np.dtype(object) ) #the index of each parameter in this file type
    
        for p in range(0, nParameter_hru):
            para = aParameter_hru_name[p]
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
        for p in range(0, nParameter_soil):
            para = aParameter_soil_name[p]
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
        sWorkspace_target_case = sWorkspace_output
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
                sWorkspace_target_case = sWorkspace_output

        iHru_index = 0 
        for iSubbasin in range(1, nsubbasin+1):
            #subbasin string
            sSubbasin = "{:05d}".format( iSubbasin )
            nhru_subbasin = aHru_configuration[ iSubbasin-1]
            #loop through all hru in this subbasin
            for iHru in range(1, nhru_subbasin+1):
                #hru string
                sHru = "{:04d}".format( iHru)
                #find the hry type 
                sHru_code = aHru_info[iHru_index]
                iIndex = np.where(aHru_combination == sHru_code)
                iHru_index = iHru_index + 1

                aParameter_hru = self.aHru_combination[iIndex[0][0]].aParameter_hru

                for iFile_type in range(0, nFile_type):
                    #check whether these is parameter chanage or not
                    sExtension = aExtension[iFile_type]
                    iFlag = aParameter_flag[iFile_type]
                    if( iFlag == 1):
                        if sExtension == '.sol':
                            #soil layer special treatment
                            sFilename = sSubbasin + sHru + sExtension
                            sFilename_hru = os.path.join(sWorkspace_source_case , sFilename )
                            #open the file to read
                            ifs=open(sFilename_hru, 'rb')   
                            sLine=(ifs.readline()).rstrip().decode("utf-8", 'ignore')

                            #open the new file to write out
                            sFilename_hru_out = os.path.join(sWorkspace_target_case , sFilename)
                            #do we need to remove linnk first, i guess it's better to do so
                            if os.path.exists(sFilename_hru_out):                
                                os.remove(sFilename_hru_out)

                            ofs=open(sFilename_hru_out, 'w') 
                            print(sFilename_hru_out)
                            #because of the python interface, pest will no longer interact with model files directly
                            #starting from here we will       
                            aValue_hru  = np.array(aParameter_hru)                      
                            
                            while sLine:                               
                                for i in range(0, aParameter_count[iFile_type]):                               
                                    if 'Soil Albedo (Moist)' in sLine:                                        
                                        dummy1 = np.array(aParameter_index[iFile_type])
                                        dummy2 = np.array(aParameter_user[iFile_type])
                                        dummy_index1 = np.where(dummy2 == 'sol_alb')
                                        dummy_index2 = dummy1[dummy_index1]
                                        sLine_new = '{0: <27}'.format(' Soil Albedo (Moist) ')
                                        if 'sol_alb' in dummy2:
                                            nSoil_layer = self.aHru_combination[iIndex[0][0]].nSoil_layer                                                
                                            dummy_index1 = np.where(dummy2 == 'sol_alb')                                            
                                            dummy_index2 = dummy1[dummy_index1][0]
                                            for j in range(nSoil_layer):
                                                aParameter_soil = self.aHru_combination[iIndex[0][0]].aSoil[j].aParameter_soil
                                                sLine_new = sLine_new +  "{:12.2f}".format( aParameter_soil[dummy_index2].dValue_current  ) 
                                            sLine_new = sLine_new + '\n'
                                            ofs.write(sLine_new)
                                            break
                                        else:
                                            pass
                                        
                                    else:
                                        if ' Ave. AW Incl. Rock' in sLine :                                      
                                            sLine_new = '{0: <27}'.format(' Ave. AW Incl. Rock: ')
                                            dummy1 = np.array(aParameter_index[iFile_type])
                                            dummy2 = np.array(aParameter_user[iFile_type])
                                            if 'sol_awc' in dummy2:
                                                nSoil_layer = self.aHru_combination[iIndex[0][0]].nSoil_layer                                                
                                                dummy_index1 = np.where(dummy2 == 'sol_awc')                                            
                                                dummy_index2 = dummy1[dummy_index1][0]
                                                for j in range(nSoil_layer):
                                                    aParameter_soil = self.aHru_combination[iIndex[0][0]].aSoil[j].aParameter_soil
                                                    sLine_new = sLine_new +  "{:12.2f}".format( aParameter_soil[dummy_index2].dValue_current  ) 
                                                sLine_new = sLine_new + '\n'
                                                ofs.write(sLine_new)
                                                break
                                            else:
                                                pass
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
                            pass
                        else:
                            sFilename = sSubbasin + sHru + sExtension
                            sFilename_hru = os.path.join(sWorkspace_source_case , sFilename )
                            #open the file to read
                            ifs=open(sFilename_hru, 'rb')   
                            sLine=(ifs.readline()).rstrip().decode("utf-8", 'ignore')

                            #open the new file to write out
                            sFilename_hru_out = os.path.join(sWorkspace_target_case , sFilename)
                            #do we need to remove linnk first, i guess it's better to do so
                            if os.path.exists(sFilename_hru_out):                
                                os.remove(sFilename_hru_out)

                            ofs=open(sFilename_hru_out, 'w') 
                            print(sFilename_hru_out)
                            #because of the python interface, pest will no longer interact with model files directly
                            #starting from here we will       
                            aValue  = np.array(aParameter_hru)                      
                            #aValue = dummy_data[:, iIndex[0]]
                            while sLine:
                                aParameter = aParameter_user[iFile_type]

                                for i in range(0, aParameter_count[iFile_type]):
                                    #sKey = aParameter[i]
                                    if 'cn2' in sLine.lower() : 
                                        dummy = 'cn2' + "{:02d}".format(iSubbasin) \
                                        + "{:02d}".format(iHru) 
                                        dummy1 = np.array(aParameter_index[iFile_type])
                                        dummy2 = np.array(aParameter_user[iFile_type])
                                        dummy_index1 = np.where(dummy2 == 'cn2')
                                        dummy_index2 = dummy1[dummy_index1][0]
                                        sLine_new = "{:16.2f}".format(  aValue[dummy_index2].dValue_current  )     + '    | pest parameter CN2 \n'
                                        ofs.write(sLine_new)
                                        break
                                    else:
                                        if ' something ' in sLine :
                                            
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
         
    def swaty_copy_executable_file(self):
        """    
        prepare executable file
        """    
        sWorkspace_bin = self.sWorkspace_bin 
        sFilename_swat = self.sFilename_swat   
        sWorkspace_output = self.sWorkspace_output
   
        sWorkspace_pest_model = sWorkspace_output
        #copy swat
        
        sFilename_swat_source = os.path.join(str(Path(sWorkspace_bin)) ,  sFilename_swat )
             
        sFilename_swat_new = os.path.join(str(Path(sWorkspace_output)) ,  'swat' )

        print(sFilename_swat_source)
        print(sFilename_swat_new)
        copy2(sFilename_swat_source, sFilename_swat_new)
        self.sFilename_swat_current = sFilename_swat_new


        os.chmod(sFilename_swat_new, stat.S_IRWXU )

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
    
    def swaty_prepare_simulation_bash_file(self):

        sWorkspace_output = self.sWorkspace_output

        sFilename_bash = os.path.join(sWorkspace_output,  'run_swat.sh' )
        
        ifs = open(sFilename_bash, 'w')       
        #end of example
        sLine = '#!/bin/bash' + '\n'
        ifs.write(sLine)    
        sLine = 'module purge' + '\n'
        ifs.write(sLine)    
        sLine = 'module load gcc/7.3.0' + '\n'
        ifs.write(sLine)
        sLine = 'cd ' + sWorkspace_output + '\n'
        ifs.write(sLine)
        sLine = './swat' + '\n'
        ifs.write(sLine)
        ifs.close()
        #change mod
        os.chmod(sFilename_bash, stat.S_IRWXU )
        print('Bash file is prepared.')
        return sFilename_bash
    
    def swaty_prepare_simulation_job_file(self):

        sWorkspace_output = self.sWorkspace_output
        sJob = self.sJob
        sFilename_job = os.path.join(sWorkspace_output,  'submit_swat.job' )
      
        ifs = open(sFilename_job, 'w')   

        #end of example
        sLine = '#!/bin/bash' + '\n'
        ifs.write(sLine)
        sLine = '#SBATCH -A m1800' + '\n'
        ifs.write(sLine)
        sLine = '#SBATCH -t 0:10:00' + '\n'
        ifs.write(sLine)
        sLine = '#SBATCH -q debug' + '\n'
        ifs.write(sLine)
        sLine = '#SBATCH -N 1' + '\n'
        ifs.write(sLine)
        sLine = '#SBATCH -n 2' + '\n'
        ifs.write(sLine)
        sLine = '#SBATCH -J ' + sJob + '' + '\n'
        ifs.write(sLine)
        sLine = '#SBATCH -C haswell' + '\n'
        ifs.write(sLine)
        sLine = '#SBATCH -L SCRATCH' + '\n'
        ifs.write(sLine)

        sLine = '#SBATCH -o out.out' + '\n'
        ifs.write(sLine)
        sLine = '#SBATCH -e err.err' + '\n'
        ifs.write(sLine)
        sLine = '#SBATCH --mail-type=ALL' + '\n'
        ifs.write(sLine)
        sLine = '#SBATCH --mail-user=chang.liao@pnnl.gov' + '\n'
        ifs.write(sLine)
        sLine = 'cd $SLURM_SUBMIT_DIR' + '\n'
        ifs.write(sLine)
        sLine = 'module purge' + '\n'
        ifs.write(sLine)    
        sLine = 'module load gcc/6.1.0' + '\n'
        ifs.write(sLine)
        sLine = 'cd ' + sWorkspace_output+ '\n'
        ifs.write(sLine)
        sLine = './swat' + '\n'
        ifs.write(sLine)
        ifs.close()
        os.chmod(sFilename_job, stat.S_IRWXU )

        #alaso need sbatch to submit it

        print('Job file is prepared.')
        return sFilename_job
    
    def swaty_prepare_observation_discharge_file(self):
        sModel = self.sModel
        sWorkspace_scratch = self.sWorkspace_scratch    
        sWorkspace_data = self.sWorkspace_data
        sFilename_observation_discharge = self.sFilename_observation_discharge
        iYear_start = self.iYear_start
        iYear_end  =self.iYear_end
        iMonth_start = self.iMonth_start
        iMonth_end  =self.iMonth_end
        iDay_start = self.iDay_start
        iDay_end  =self.iDay_end    
        sRegion = self.sRegion
        dummy1 = datetime.datetime(iYear_start, iMonth_start, iDay_start)
        
        lJulian_start = julian.to_jd(dummy1, fmt='jd')
        
   
        nstress = self.nstress

        sFilename_discharge = sWorkspace_data + slash + sModel + slash \
            + sRegion + slash + 'auxiliary' + slash + sFilename_observation_discharge
        aData_dummy = text_reader_string(sFilename_discharge, cDelimiter_in=',', iSkipline_in=1)
        print(sFilename_discharge)
        aData = np.array( aData_dummy )
        aMonth =  aData[:,0] 
        aDay =  aData[:,1] 
        aYear =  aData[:,2] 
        aDischarge = aData[:, 3] #unit is cms because it is convected in excel
        nobs = len(aDischarge)
    
        #save a txt file for other purpose
        sPath =  sWorkspace_data + slash + sModel + slash + sRegion + slash \
        + 'auxiliary' + slash + 'usgs' + slash + 'discharge' + slash
        Path(sPath).mkdir(parents=True, exist_ok=True)

        aDischarge_simulation_daily = np.full( (nstress), missing_value, dtype=float )

        for i in range(0, nobs):
            iYear = int(aYear[i])
            iMonth = int( aMonth[i])
            iDay = int(aDay[i])
            dDischarge = float(aDischarge[i])
            dummy2 = datetime.datetime(iYear, iMonth, iDay)
            #jd_dummy = gcal2jd(iYear, iMonth, iDay)    
            lJulian_end = julian.to_jd(dummy2, fmt='jd')    
            lIndex = lJulian_end - lJulian_start
            if lIndex >=0 and lIndex < nstress:

                aDischarge_simulation_daily[ int(lIndex)] = dDischarge

        aDischarge_simulation_monthly = convert_time_series_daily_to_monthly(aDischarge_simulation_daily,\
            iYear_start, iMonth_start, iDay_start, \
          iYear_end, iMonth_end, iDay_end , sType_in = 'sum'  )
        #ofs.write(aDischarge_observation)
        #ofs.close()
        sFilename_observation_discharge_out = sPath + slash + 'discharge_observation_daily.txt' 
        np.savetxt(sFilename_observation_discharge_out, aDischarge_simulation_daily, delimiter=',', fmt='%0.6f') 
        sFilename_observation_discharge_out = sPath + slash + 'discharge_observation_monthly.txt' 
        np.savetxt(sFilename_observation_discharge_out, aDischarge_simulation_monthly, delimiter=',', fmt='%0.6f') 
        print('finished')
    
    def swaty_extract_stream_discharge(self, sFilename_output_in=None):
        """
        extract discharge from swat model simulation
        """     
        sModel = self.sModel
        sRegion = self.sRegion
        sCase = self.sCase
        iYear_start = self.iYear_start    
        iYear_end  = self.iYear_end   
        nstress = self.nstress
        nsegment = self.nsegment
        sTime_step_calibration = self.sTime_step_calibration
        
      
        sPath_current = self.sWorkspace_output
        
        print('The current path is: ' + sPath_current)    
        sFilename = os.path.join( sPath_current ,  'output.rch')
        aData = text_reader_string(sFilename, iSkipline_in=9)
        aData_all = np.array( aData )
        nrow_dummy = len(aData_all)
        ncolumn_dummy = len(aData_all[0,:])

        aData_discharge = aData_all[:, 5].astype(float) 

        aIndex = np.arange(nsegment-1 , nstress * nsegment + 1, nsegment)

        aDischarge_simulation_daily = aData_discharge[aIndex]

        iYear_start_in = self.iYear_start
        iMonth_start_in = self.iMonth_start
        iDay_start_in = self.iDay_start

        iYear_end_in = self.iYear_end
        iMonth_end_in = self.iMonth_end
        iDay_end_in = self.iDay_end

        sFilename_out=''
        if sTime_step_calibration == 'daily':            
            sFilename_out = os.path.join(sPath_current , 'stream_discharge_daily.txt') 
            np.savetxt(sFilename_out, aDischarge_simulation_daily, delimiter=",")
        else: 
            if sTime_step_calibration == 'monthly':
                aDischarge_simulation_monthly = convert_time_series_daily_to_monthly(aDischarge_simulation_daily,\
                    iYear_start_in, iMonth_start_in, iDay_start_in, \
                    iYear_end_in, iMonth_end_in, iDay_end_in , sType_in = 'sum'  )
                
                sFilename_out = os.path.join(sPath_current , 'stream_discharge_monthly.txt')  
                np.savetxt(sFilename_out, aDischarge_simulation_monthly, delimiter=",")
            else:
                #annual 
                sFilename_out = os.path.join(sPath_current , 'stream_discharge_annual.txt') 
                pass


        sTime  = datetime.datetime.now().strftime("%m%d%Y%H%M%S")
        #save history
        sFilename_new = os.path.join(sPath_current , 'stream_discharge' + sTime_step_calibration + '.txt')
        copy2(sFilename_out, sFilename_new)

        #save for pest calibration
        if sFilename_output_in is not None:
            copy2(sFilename_out, sFilename_output_in)

        print('Finished extracting stream discharge: ' + sFilename_out)

    def swaty_tsplot_stream_discharge(self):
        iYear_start = self.iYear_start
        iYear_end = self.iYear_end
        nstress_month = self.nstress_month

        sWorkspace_simulation_case = self.sWorkspace_output


        sFilename1 = self.sFilename_observation_discharge 
        #'/global/u1/l/liao313/data/swat/arw/auxiliary/usgs/discharge/stream_discharge_monthly.txt'

        aData = text_reader_string(sFilename1)
        aDischarge_obs = np.array( aData ).astype(float)  
        aDischarge_obs = aDischarge_obs.flatten() * cms2cmd

        sFilename2 = os.path.join(self.sWorkspace_output , 'stream_discharge_monthly.txt' )

        aData = text_reader_string(sFilename2)
        aDischarge_simulation1 = np.array( aData ).astype(float)  
        aDischarge_simulation1 = aDischarge_simulation1.flatten() * cms2cmd

        sFilename3 =  '/global/u1/l/liao313/data/swat/arw/auxiliary/usgs/discharge/stream_discharge_monthly_opt.txt'

        aData = text_reader_string(sFilename3)
        aDischarge_simulation2 = np.array( aData ).astype(float)  
        aDischarge_simulation2 = aDischarge_simulation2.flatten() * cms2cmd

        #dummy1 = np.percentile(aDischarge_simulation, 99)
        #dummy2 = np.where( aDischarge_simulation > dummy1 )


        #plot simulation
        dates = list()
        for iYear in range(iYear_start, iYear_end+1):
            for iMonth in range(1,13):
                dSimulation = datetime.datetime(iYear, iMonth, 1)
                dates.append(dSimulation)
    


        sLabel_Y =r'Stream discharge ($m^{3} \, day^{-1}$)' 
        sLabel_legend = 'Simulated stream discharge'


        aDate= np.tile( dates , (3,1))
        aData = np.array([aDischarge_obs , aDischarge_simulation1,aDischarge_simulation2])

        aLabel_legend = ['Default','Initial','Calibrated']
        aColor_in = ['black', 'red', 'blue']

        sFilename_out = sWorkspace_simulation_case + slash + 'discharge_monthly_scatter1.png'

        scatter_plot_data(aDischarge_obs,aDischarge_simulation1,sFilename_out,\
            iFlag_scientific_notation_x_in=1,\
                          iFlag_scientific_notation_y_in=1,\
                              dMin_x_in = 0.0, \
                                  dMax_x_in = 1E7, \
                                       dMin_y_in = 0.0, \
                                  dMax_y_in = 1E7, \
         iSize_x_in = 8, \
                          iSize_y_in = 8,\
                              sLabel_legend_in = 'Initial',\
                                   sLabel_x_in = r'Observed discharge ($m^{3} \, day^{-1}$)',\
                          sLabel_y_in = r'Simulated discharge ($m^{3} \, day^{-1}$)' )

        sFilename_out = sWorkspace_simulation_case + slash + 'discharge_monthly_scatter2.png'
        scatter_plot_data(aDischarge_obs,aDischarge_simulation2,sFilename_out,\
             iFlag_scientific_notation_x_in=1,\
                          iFlag_scientific_notation_y_in=1,\
                               dMin_x_in = 0.0, \
                                  dMax_x_in = 1E7, \
                                       dMin_y_in = 0.0, \
                                  dMax_y_in = 1E7, \
             iSize_x_in = 8, \
                          iSize_y_in = 8,\
                              sLabel_legend_in = 'Calibrated',\
                                   sLabel_x_in =r'Observed discharge ($m^{3} \, day^{-1}$)',\
                          sLabel_y_in = r'Calibrated discharge ($m^{3} \, day^{-1}$)' )

        sFilename_out = sWorkspace_simulation_case + slash + 'discharge_monthly.png'
        plot_time_series_data(aDate, aData,\
             sFilename_out,\
             sTitle_in = '', \
                 sLabel_y_in= sLabel_Y,\
                     aColor_in =aColor_in,\
                  aLabel_legend_in = aLabel_legend, \
                iSize_x_in = 12,\
                     iSize_y_in = 5)




        print("finished")
    
    def export_config_to_json(self, sFilename_output):
        aSkip = [ 'aSubbasin' ,'aHru_combination' ]
        obj = self.__dict__.copy()
        for sKey in aSkip:
            obj.pop(sKey, None)
            pass
        

        with open(sFilename_output, 'w', encoding='utf-8') as f:
            json.dump(obj, f,sort_keys=True, \
                ensure_ascii=False, \
                indent=4, cls=CaseClassEncoder)
        return

    def tojson(self):
        aSkip = [ 'aSubbasin', 'aHru_combination'    ]  

        obj = self.__dict__.copy()
        for sKey in aSkip:
            obj.pop(sKey, None)

        sJson = json.dumps(obj,\
            sort_keys=True, \
                indent = 4, \
                    ensure_ascii=True, \
                        cls=CaseClassEncoder)
        return sJson