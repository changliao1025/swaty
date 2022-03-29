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
from swaty.classes.swatpara import swatpara
class pysubbasin(object):
    __metaclass__ = ABCMeta
    lIndex=-1
    iFlag_subbasin=0
    nSoil_layer = 1
    nParameter_subbasin=0
    aParameter_subbasin=None
    aParameter_subbasin_name = None

    def  __init__(self,aConfig_in):
        self.nParameter_subbasin = len(aConfig_in)
        self.aParameter_subbasin=list()
        self.aParameter_subbasin_name =list()
        for i in range(self.nParameter_subbasin):
            subbasin_dummy = aConfig_in[i]
            pParameter_subbasin = swatpara(subbasin_dummy)
            self.aParameter_subbasin.append(pParameter_subbasin)
            sName = pParameter_subbasin.sName
            if sName not in self.aParameter_subbasin_name:
                self.aParameter_subbasin_name.append(sName)

        return