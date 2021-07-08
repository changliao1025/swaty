from abc import ABCMeta, abstractmethod
import datetime
from pyearth.system.define_global_variables import *
pDate = datetime.datetime.today()
sDate_default = "{:04d}".format(pDate.year) + "{:02d}".format(pDate.month) + "{:02d}".format(pDate.day)

class pyswat(object):
    __metaclass__ = ABCMeta
    iCase_index=0
    iSiteID=0
    iFlag_calibration=0
    iFlag_mode=0
    iYear_start=0
    iYear_end=0
    iMonth_start=0
    iMonth_end=0
    iDay_start=0
    iDay_end=0
    nstress=0
    nsegment =0
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
        self.nbasin = int (aParameter[ 'nbasin'])

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
        self.sFilename_observation_discharge = aParameter[ 'sFilename_observation_discharge']
        self.sFilename_swat = aParameter[ 'sFilename_swat']
        

        self.iYear_start  = int( aParameter['iYear_start'] )
        self.iYear_end    = int( aParameter['iYear_end']   )
        self.iMonth_start = int( aParameter['iMonth_start'])
        self.iMonth_end   = int( aParameter['iMonth_end']  ) 
        self.iDay_start   = int( aParameter['iDay_start']  )
        self.iDay_end     = int( aParameter['iDay_end']    )
        self.nstress      = int( aParameter['nstress']     )
        self.iFlag_mode   = int( aParameter['iFlag_mode']) 
        self.iFlag_replace= int( aParameter['iFlag_replace'] ) 
        #for replace and calibration
        self.aValue =  aParameter['aValue']
        self.aVariable =  aParameter['aVariable'] 

        self.sJob =  aParameter['sJob'] 

        self.sWorkspace_data_project = self.sWorkspace_data +  slash + self.sWorkspace_project

        self.sWorkspace_simulation_copy = self.sWorkspace_data  + aParameter['sWorkspace_simulation_copy']

                
        return
        