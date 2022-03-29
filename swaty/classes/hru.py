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

class HruClassEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.float32):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        
         
        if isinstance(obj, swatpara):
            return json.loads(obj.tojson()) 
       
        if isinstance(obj, list):
            pass  
        return JSONEncoder.default(self, obj)
  

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
        self.aParameter_hru_name=list()
        for i in range(self.nParameter_hru):
            hru_dummy = aConfig_in[i]
            pParameter_hru = swatpara(hru_dummy)
            self.aParameter_hru.append(pParameter_hru)

            sName = pParameter_hru.sName
            if sName not in self.aParameter_hru_name:
                self.aParameter_hru_name.append(sName)
        return
    
    def tojson(self):
        aSkip = []      

        obj = self.__dict__.copy()
        for sKey in aSkip:
            obj.pop(sKey, None)
        sJson = json.dumps(obj,\
            sort_keys=True, \
                indent = 4, \
                    ensure_ascii=True, \
                        cls=HruClassEncoder)
        return sJson 