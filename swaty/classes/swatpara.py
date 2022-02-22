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
    iParameter_type=1
    dValue_init=0.0
    dValue_lower=-1
    dValue__upper=1
    def __init__(self, aConfig_in):

        if 'iParameter_type' in aConfig_in:
            self.iParameter_type = int(aConfig_in['iParameter_type'])
        if 'sName' in aConfig_in:
            self.sName = aConfig_in['sName']

        if 'dValue_init' in aConfig_in:
            self.dValue_init = float(aConfig_in['dValue_init'])
        
        if 'dValue_lower' in aConfig_in:
            self.dValue_lower = float(aConfig_in['dValue_lower'])

        if 'dValue__upper' in aConfig_in:
            self.dValue__upper = float(aConfig_in['dValue__upper'])

        return
    def tojson(self):
        sJson = json.dumps(self.__dict__, \
                sort_keys=True, \
                indent = 4, \
                ensure_ascii=True, \
                cls=ParaClassEncoder)
        return sJson