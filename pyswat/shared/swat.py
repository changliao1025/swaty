from abc import ABCMeta, abstractmethod
import datetime
from pyearth.system.define_global_variables import *
from pyearth.toolbox.reader.text_reader_string import text_reader_string

from pyswat.shared.swat_define_parameter import swat_define_parameter
pDate = datetime.datetime.today()
sDate_default = "{:04d}".format(pDate.year) + "{:02d}".format(pDate.month) + "{:02d}".format(pDate.day)

class pyswat(object):
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

        self.sWorkspace_simulation = sWorkspace_scratch + slash + '04model' + slash \
            + self.sModel + slash + self.sRegion +  slash + 'simulation'
        sPath = self.sWorkspace_simulation
        Path(sPath).mkdir(parents=True, exist_ok=True)

        self.sWorkspace_calibration = sWorkspace_scratch + slash + '04model' + slash  \
            + self.sModel + slash + self.sRegion +  slash + 'calibration'
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
        

        self.sWorkspace_simulation_case = self.sWorkspace_simulation + slash + sCase
        sPath = self.sWorkspace_simulation_case
        Path(sPath).mkdir(parents=True, exist_ok=True)

        self.sWorkspace_calibration_case = self.sWorkspace_calibration + slash + sCase
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
        
        self.sWorkspace_data_project = self.sWorkspace_data +  slash + self.sWorkspace_project
        #read hru type
        if 'nhru' in aConfig_in:
            nhru = int( aConfig_in['nhru']) 
            if nhru > 1:
                self.nhru = nhru
            else:
                self.nhru=9
        
        

        self.nstress_month = iMonth_count

        self.iFlag_mode   = int( aConfig_in['iFlag_mode']) 
        self.iFlag_replace= int( aConfig_in['iFlag_replace'] ) 

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
               = swat_define_parameter(self.aParameter, self.aParameter_value, self.aParameter_value_lower, self.aParameter_value_upper)
        
            self.nParameter_watershed = self.aParameter_watershed.size
            self.nParameter_subbasin = self.aParameter_subbasin.size
            self.nParameter_hru = self.aParameter_hru.size

            self.nParameter = self.nParameter_watershed \
                + self.nParameter_subbasin * self.nsubbasin \
                    + self.nParameter_hru  *  self.nhru
            pass

        self.sJob =  aConfig_in['sJob'] 

        

        #self.sWorkspace_simulation_copy = self.sWorkspace_data  + aConfig_in['sWorkspace_simulation_copy']
        self.sWorkspace_simulation_copy = self.sWorkspace_calibration + slash + 'TxtInOut'
                
        return
        