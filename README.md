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



# Acknowledgement

This research was supported by several funding sources:

* The U.S. Department of Energy (DOE), Office of Science (SC) Biological and Environmental Research (BER) program, as part of BER's Environmental System Science (ESS) program. 

* A Laboratory Directed Research and Development (LDRD) Program.
This contribution originates from a effort of hydrology-based design of geomorphic evapotranspiration covers for reclamation of mine land at Pacific Northwest National Laboratory (PNNL).




# Contact
Please contact Chang Liao (changliao.climate@gmail.com) if you have any questions.


