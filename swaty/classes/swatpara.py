
import numpy as np
import json
from json import JSONEncoder


class ParaClassEncoder(JSONEncoder):
    """
    The general parameter JSON encoder

    Args:
        JSONEncoder (_type_): _description_
    """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        
        return JSONEncoder.default(self, obj)

class swatpara(object):
    """
    The parameter class

    Args:
        object (_type_): _description_

    Returns:
        _type_: _description_
    """
    sName=''
    iParameter_type=1 #1 watershed, 2 subbsain 3 hru 4 soil layer
    #iIndex=1
    lIndex_subbasin=-1
    lIndex_hru=-1
    lIndex_soil_layer=-1
    
    iFlag_pseudo = 0
    dValue_init=0.0
    dValue_current=0.5
    dValue_lower=-1
    dValue_upper=1
    def __init__(self, aConfig_in):
        """
        Initialize a parameter object through a dictionary

        Args:
            aConfig_in (dict): The dictionary that stores parameters
        """

        if 'iParameter_type' in aConfig_in:
            self.iParameter_type = int(aConfig_in['iParameter_type'])
        
        if 'iFlag_pseudo' in aConfig_in:
            self.iFlag_pseudo = int(aConfig_in['iFlag_pseudo'])
        
        if 'lIndex_subbasin' in aConfig_in:
            self.lIndex_subbasin = int(aConfig_in['lIndex_subbasin'])
        else:
            self.lIndex_subbasin = 1
        
        if 'lIndex_hru' in aConfig_in:
            self.lIndex_hru = int(aConfig_in['lIndex_hru'])
        else:
            self.lIndex_hru = -1

        if 'lIndex_soil_layer' in aConfig_in:
            self.lIndex_soil_layer = int(aConfig_in['lIndex_soil_layer'])
        else:
            self.lIndex_soil_layer =-1

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
        """
        Convert a parameter object to a JSON object

        Returns:
            _type_: _description_
        """
        sJson = json.dumps(self.__dict__, \
                sort_keys=True, \
                indent = 4, \
                ensure_ascii=True, \
                cls=ParaClassEncoder)
        return sJson