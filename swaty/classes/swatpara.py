from abc import ABCMeta
import numpy as np
import json
from json import JSONEncoder


class ParaClassEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        
        return JSONEncoder.default(self, obj)

class swatpara(object):
    sName=''
    iParameter_type=1 #1 watershed, 2 subbsain 3 hru
    iIndex=1
    iSoil_layer=1
    dValue_init=0.0
    dValue_current=0.5
    dValue_lower=-1
    dValue_upper=1
    def __init__(self, aConfig_in):

        if 'iParameter_type' in aConfig_in:
            self.iParameter_type = int(aConfig_in['iParameter_type'])
        
        if 'iIndex' in aConfig_in:
            self.iIndex = int(aConfig_in['iIndex'])
        else:
            self.iIndex = 1

        if 'iSoil_layer' in aConfig_in:
            self.iSoil_layer = int(aConfig_in['iSoil_layer'])
        else:
            self.iSoil_layer =1

        if 'sName' in aConfig_in:
            self.sName = aConfig_in['sName']

        if 'dValue_init' in aConfig_in:
            self.dValue_init = float(aConfig_in['dValue_init'])
        
        if 'dValue_current' in aConfig_in:
            self.dValue_current = float(aConfig_in['dValue_current'])
        else:
            self.dValue_current = self.dValue_init
        
        if 'dValue_lower' in aConfig_in:
            self.dValue_lower = float(aConfig_in['dValue_lower'])

        if 'dValue_upper' in aConfig_in:
            self.dValue_upper = float(aConfig_in['dValue_upper'])

        return
    def tojson(self):
        sJson = json.dumps(self.__dict__, \
                sort_keys=True, \
                indent = 4, \
                ensure_ascii=True, \
                cls=ParaClassEncoder)
        return sJson