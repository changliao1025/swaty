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
class pywatershed(object):
    __metaclass__ = ABCMeta
    lIndex=-1
    iFlag_watershed=0
    nSoil_layer = 1
    nParameter_watershed=0
    aParameter_watershed=None
    aParameter_watershed_name = None

    def  __init__(self,aConfig_in):

        self.nParameter_watershed = len(aConfig_in)
        self.aParameter_watershed=list()
        for i in range(self.nParameter_watershed):
            watershed_dummy = aConfig_in[i]
            pParameter_watershed = swatpara(watershed_dummy)
            self.aParameter_watershed.append(pParameter_watershed)
        return