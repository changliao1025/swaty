from abc import ABCMeta, abstractmethod
import datetime
from pyearth.system.define_global_variables import *


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

    aParameter=None
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

    nParameter_water=0
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
    def __init__(self, aParameter):
        self.sFilename_model_configuration    = aParameter[ 'sFilename_model_configuration']
        self.sWorkspace_home = aParameter[ 'sWorkspace_home']
        self.sWorkspace_data = aParameter[ 'sWorkspace_data']
       
        self.sWorkspace_scratch    = aParameter[ 'sWorkspace_scratch']
        sWorkspace_scratch = self.sWorkspace_scratch
        sWorkspace_data=self.sWorkspace_data
        self.sRegion               = aParameter[ 'sRegion']
        self.sModel                = aParameter[ 'sModel']
        self.sPython               = aParameter[ 'sPython']
        #self.sDate_start              = aParameter[ 'sDate_start']
        #self.sDate_end                = aParameter[ 'sDate_end']
        self.nsegment = int( aParameter[ 'nsegment'] )
        self.nsubbasin = int (aParameter[ 'nsubbasin'])

        self.sWorkspace_project= aParameter[ 'sWorkspace_project']
        self.sWorkspace_bin= aParameter[ 'sWorkspace_bin']

        self.sWorkspace_simulation = sWorkspace_scratch + slash + '04model' + slash \
            + self.sModel + slash + self.sRegion +  slash + 'simulation'
        sPath = self.sWorkspace_simulation
        Path(sPath).mkdir(parents=True, exist_ok=True)

        self.sWorkspace_calibration = sWorkspace_scratch + slash + '04model' + slash  \
            + self.sModel + slash + self.sRegion +  slash + 'calibration'
        sPath = self.sWorkspace_calibration
        Path(sPath).mkdir(parents=True, exist_ok=True)

        iCase_index = int(aParameter['iCase_index'])
        sCase_index = "{:03d}".format( iCase_index )
        sDate   = aParameter[ 'sDate']
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

        self.iFlag_calibration =  int(aParameter['iFlag_calibration']) 
        self.iFlag_simulation =  int(aParameter['iFlag_simulation']) 
        self.iFlag_watershed =  int(aParameter['iFlag_watershed']) 
        self.iFlag_subbasin =  int(aParameter['iFlag_subbasin']) 
        self.iFlag_hru =  int(aParameter['iFlag_hru']) 
        self.sFilename_observation_discharge = aParameter[ 'sFilename_observation_discharge']
        self.sFilename_swat = aParameter[ 'sFilename_swat']
        

        self.iYear_start  = int( aParameter['iYear_start'] )
        self.iYear_end    = int( aParameter['iYear_end']   )
        self.iMonth_start = int( aParameter['iMonth_start'])
        self.iMonth_end   = int( aParameter['iMonth_end']  ) 
        self.iDay_start   = int( aParameter['iDay_start']  )
        self.iDay_end     = int( aParameter['iDay_end']    )
        self.nstress      = int( aParameter['nstress']     )

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

        self.iFlag_mode   = int( aParameter['iFlag_mode']) 
        self.iFlag_replace= int( aParameter['iFlag_replace'] ) 

        #for replace and calibration
        self.aParameter_value =  aParameter['aParameter_value'] #this should be a variable sized array
        self.aParameter_value_lower =  aParameter['aParameter_value_lower'] #this should be a variable sized array
        self.aParameter_value_upper =  aParameter['aParameter_value_upper'] #this should be a variable sized array
        self.aParameter =  aParameter['aParameter']  #list

        if self.aParameter is not None:
            self.aParameter_watershed, self.aParameter_subbasin, self.aParameter_hru,\
                self.aParameter_value_watershed, self.aParameter_value_subbasin, self.aParameter_value_hru, \
                self.aParameter_value_lower_watershed, self.aParameter_value_lower_subbasin, self.aParameter_value_lower_hru, \
                  self.aParameter_value_upper_watershed, self.aParameter_value_upper_subbasin, self.aParameter_value_upper_hru \
               = swat_define_parameter(self.aParameter, self.aParameter_value, self.aParameter_value_lower, self.aParameter_value_upper)
        
            self.nParameter_watershed = self.aParameter_watershed.size
            self.nParameter_subbasin = self.aParameter_subbasin.size
            self.nParameter_hru = self.aParameter_hru.size
            pass

        self.sJob =  aParameter['sJob'] 

        self.sWorkspace_data_project = self.sWorkspace_data +  slash + self.sWorkspace_project

        self.sWorkspace_simulation_copy = self.sWorkspace_data  + aParameter['sWorkspace_simulation_copy']

                
        return
        