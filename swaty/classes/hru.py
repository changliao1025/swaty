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


class pyhru(object):
    __metaclass__ = ABCMeta

    lIndex=-1
    iFlag_hru=0
    nSoil_layer = 1
    nParameter_hru=0
    aParameter_hru=None
    aParameter_hru_name = None
    

    def  __init__(self,aConfig_in):
        self.nParameter_hru = len(aConfig_in)
        self.aParameter_hru=list()
        for i in range(self.nParameter_hru):
            hru_dummy = aConfig_in[i]
            pParameter_hru = swatpara(hru_dummy)
            self.aParameter_hru.append(pParameter_hru)

            sName = pParameter_hru.sName
            if sName not in self.aParameter_hru_name:
                self.aParameter_hru_name.append(sName)
        return