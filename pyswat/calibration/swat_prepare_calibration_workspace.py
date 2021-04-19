import sys
import os

def swat_prepare_calibration_workspace(sFilename_configuration_in, sModel):
    """
    this function is used to create a new calibration workspace.
    iID
    sFilename_configuration_in
    """

    
    
    

    sWorkspace_calibration_relative = config['sWorkspace_calibration']

    
    sWorkspace_calibration = sWorkspace_scratch + slash + sWorkspace_calibration_relative

    sWorkspace_pest_model = sWorkspace_calibration + slash + sModel
    if not os.path.exists(sWorkspace_pest_model):
        os.makedirs(sWorkspace_pest_model)
    else:      
        print("The simulation folder already exist")

    print('The calibration workspace is prepared successfully!')