# Overview
SWATy is a Python package to support the Soil & Water Assessment Tool (SWAT) model simulation and calibration.

Currently, it does not build a SWAT model from scratch. Instead, it relies on an existing SWAT model that is often created by the ArcSWAT tool (https://swat.tamu.edu/software/arcswat/).

Once provided the existing SWAT model along with several outputs from the ArcSWAT tool, modelers can use SWATy to custmize the SWAT for different purposes/applications:

* Run an existing SWAT model simulation in different platforms.

* Modify the inputs and parameters for new simulations.

* Analyze and visualize model output.

* Calibrate model parameter through the PyPEST package (https://pypi.org/project/pypest/).

# Installation
Currently, SWATy is only available through the PyPI. It would be available on the Conda platform soon.

SWATy depends on several Python packages, it is recommended to install these packages through Conda before installing SWATy in the correct order.

To avoid package conflict, it is also recommended to install SWATy in a new Conda environment using the following steps:

1. conda create --name swaty python=3.8

2. conda activate swaty

3. conda install -c conda-forge numpy

4. conda install -c conda-forge matplotlib

5. conda install -c conda-forge pyearth

6. pip install swaty

# Usage

The notebook.py (https://github.com/changliao1025/swaty/blob/master/tests/example/notebook.py) and swat.ipynb files provide some quick start points to run the example either within a Python environment or a Jupter Notebook.

Below is some details of running the example using a pure Python environment.

SWATy uses the Object-oriented programming (OOP) approach to manage a SWAT model case, which is fully defined by the swatcase class (https://github.com/changliao1025/swaty/blob/master/swaty/classes/pycase.py)

To initialize a swatcase object, SWATy used a JSON file as configuration file which contains all the required information. 
Currently, the exmaple provides two options to either generate a JSON file on-the-fly or read an existing JSON file. Such a template JSON file is provided here: https://github.com/changliao1025/swaty/blob/master/tests/configurations/template.json

Below are some key content description in the template JSON file:
* aParameter_hru: a swatpara object which contains all HRU level parameters

* aParameter_basin: a swatpara object which contains all sub-basin level parameters

* aParameter_water: a swatpara object which contains all watershed level parameters
    For example, {
            "dValue_init": 1.0,
            "dValue_lower": -5.0,
            "dValue_upper": 5.0,
            "iParameter_type": 1,
            "sName": "SMTMP"
        }
    describes the parameter name "SMTMP" and its upper/lower bound.

* iCase_index: the uquine ID (combined with sDate) to idenitfy a simulation 

* iFlag_calibration: flag to turn on the calibration mode

* iFlag_standalone: flag to indicate whether this is a standalone or a embeded (during PEST calibration) simulation

* iFlag_hru/iFlag_subbasin/iFlag_watershed: flag for parameter replacement

* sFilename_HRULandUseSoilsReport: the filename of the HRULandUseSoilsReport, which is generated by ArcSWAT

* sFilename_LandUseSoilsReport: the filename of the LandUseSoilsReport, which is generated by ArcSWAT

* sFilename_swat: the executable binary file of SWAT, it can be for either Windows or Linux. The Linux version of SWAT can be either downloaded from the official webiste or be compiled from the source code. See https://github.com/changliao1025/swat_hpc for more details.

* sWorkspace_input: the input folder path, which will be used to store all the input files

* sWorkspace_output: the output folder path, which will be used to store all the output files

* sWorkspace_simulation_copy: the path to the ArcSWAT generated SWAT input files. If a tar file is provided, it will be extracted to the output path.

A swatcase object is often initialized by either 

```
oSwat = swaty_generate_template_configuration_file(sFilename_configuration_in, sWorkspace_input,sWorkspace_output, sPath_bin, iFlag_standalone_in=1, iCase_index_in=3, sDate_in='20220308')
```

or

```
oSwat = swaty_read_model_configuration_file(sFilename_configuration_in, iFlag_standalone_in=1,iCase_index_in=2,sDate_in='20220308', sWorkspace_input_in=sWorkspace_input, sWorkspace_output_in=sWorkspace_output)
```

After that, modelers can carry a SWAT simulation in the following steps:

## The setup function
1. Untar/copy the existing SWAT files into the simulation folder, output files are excluded.

2. Generate the look-up table of HRU using the ArcSWAT reports.

3. Replace the SWAT parameters for HRU, sub-basin, and watershed levels, if their corresponding flags are turned on.

4. Copy the binary SWAT file to the simulation folder, update file permission.

5. Generate both the bash and slurm job files, which can be used to run the SWAT simulation.
```
oSwat.setup()

    def setup(self):
        """
        Set up a SWAT case
        """
        self.copy_TxtInOut_files()
        self.swaty_prepare_watershed_configuration()      
        if (self.iFlag_replace_parameter == 1):
            self.swaty_prepare_watershed_parameter_file()
            self.swaty_write_watershed_input_file()    
            self.swaty_prepare_subbasin_parameter_file()
            self.swaty_write_subbasin_input_file()      
            self.swaty_prepare_hru_parameter_file()
            self.swaty_write_hru_input_file()        
        else:
            pass

        self.swaty_copy_executable_file()
        sFilename_bash = self.swaty_prepare_simulation_bash_file()
        sFilename_job = self.swaty_prepare_simulation_job_file() 
        return
```

## The run function
The run function can run the SWAT simulation as a subprocess or submit the slurm job file.
```
oSwat.run()
```

## The analyze function
After the simulation is finished, this function can
1. extract river discharge and convert it other formats

```
oSwat.analyze()
```

## The evaluate function
The evaluate function can be used to compare simulated variables with observations.
```
oSwat.evaluate()
```

Through the SWATy package, the whole SWAT simulation process can be automated. For example, modelers can launch multiple SWAT simulations with different parameters to conduct a simple sensitivity test. 

Besides, SWATy can be linked to the PyPEST package to conduct model calibration using the PEST software.
      
# Acknowledgement

This research was supported by several funding sources:

* The U.S. Department of Energy (DOE), Office of Science (SC) Biological and Environmental Research (BER) program, as part of BER's Environmental System Science (ESS) program. 

* A Laboratory Directed Research and Development (LDRD) Program.

This contribution originates from an effort of hydrology-based design of geomorphic evapotranspiration covers for reclamation of mine land at Pacific Northwest National Laboratory (PNNL).


# Contact
Please contact Chang Liao (changliao.climate@gmail.com) if you have any questions.


