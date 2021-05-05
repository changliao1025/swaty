from abc import ABCMeta, abstractmethod
from pyearth.system.define_global_variables import *
class pyswat(object):
    __metaclass__ = ABCMeta
    iCase_index=0
    iSiteID=0
    iFlag_calibration=0
    sWorkspace_data=''
    sWorkspace_scratch=''
    sFilename_model_configuration=''
    sWorkspace_project=''
    sWorkspace_simulation=''
    sWorkspace_simulation_case=''
    sWorkspace_calibration=''
    sWorkspace_calibration_case=''
    sRegion=''
    sModel=''
    sCase=''
    sDate=''
    sSiteID=''
    sDate_start =''
    sDate_end=''
    def __init__(self, aParameter):
        self.sFilename_model_configuration    = aParameter[ 'sFilename_model_configuration']

        self.sWorkspace_data = aParameter[ 'sWorkspace_data']
       
        self.sWorkspace_scratch    = aParameter[ 'sWorkspace_scratch']
        sWorkspace_scratch = self.sWorkspace_scratch
        sWorkspace_data=self.sWorkspace_data
        self.sRegion               = aParameter[ 'sRegion']
        self.sModel                = aParameter[ 'sModel']
        #self.sDate_start              = aParameter[ 'sDate_start']
        #self.sDate_end                = aParameter[ 'sDate_end']

        self.sWorkspace_simulation = sWorkspace_scratch + slash + '04model' + slash \
            + self.sModel + slash + self.sRegion +  slash + 'simulation'
        sPath = self.sWorkspace_simulation
        Path(sPath).mkdir(parents=True, exist_ok=True)

        self.sWorkspace_calibration = sWorkspace_scratch + slash + '04model' + slash  \
            + self.sModel + slash + self.sRegion +  slash + 'calibration'
        sPath = self.sWorkspace_calibration
        Path(sPath).mkdir(parents=True, exist_ok=True)


        sCase_index = "{:03d}".format( int(aParameter['iCase_index']) )
        sDate   = aParameter[ 'sDate']
        if sDate is not None:
            self.sDate= sDate
        else:
            self.sDate = sDate_default
            
        sCase = self.sModel + self.sDate + sCase_index
        self.sCase = sCase
        

        self.sWorkspace_simulation_case = self.sWorkspace_simulation + slash + sCase
        sPath = self.sWorkspace_simulation_case
        Path(sPath).mkdir(parents=True, exist_ok=True)

        self.sWorkspace_calibration_case = self.sWorkspace_calibration + slash + sCase
        sPath = self.sWorkspace_calibration_case
        Path(sPath).mkdir(parents=True, exist_ok=True)

        #self.iFlag_calibration =  int(aParameter['iFlag_calibration']) 

                
        return
        