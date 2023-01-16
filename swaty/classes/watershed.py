import numpy as np
import json
from json import JSONEncoder
from swaty.classes.swatpara import swatpara

class WatershedClassEncoder(JSONEncoder):
    """
    The watershed class json encoder

    Args:
        JSONEncoder (_type_): _description_
    """
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
        
class pywatershed(object):
    """
    The watershed class

    Args:
        object (_type_): _description_

    Returns:
        _type_: _description_
    """

    lIndex_watershed=-1
    iFlag_watershed=0
    nSoil_layer = 1
    nParameter_watershed=0
    aParameter_watershed=None
    aParameter_watershed_name = None

    def  __init__(self, aConfig_in=None):
        if aConfig_in is not None:
            pass
        else:
            pass
        return
    
    def setup_parameter_by_dict(self, aPara_in):
        """
        Set up the watershed class object parameter

        Args:
            aPara_in (dict, optional): The dictionary that stores parameters. Defaults to None.
        """
        if aPara_in is not None:
            self.nParameter_watershed = len(aPara_in)
            self.aParameter_watershed=list()
            self.aParameter_watershed_name=list()
            for i in range(self.nParameter_watershed):
                watershed_dummy = aPara_in[i]
                pParameter_watershed = swatpara(watershed_dummy)
                self.aParameter_watershed.append(pParameter_watershed)
                self.aParameter_watershed_name.append(pParameter_watershed.sName)
        else:
            pass
        return

    def tojson(self):
        """
        Convert a watershed object to a JSON object

        Returns:
            _type_: _description_
        """


        aSkip = []      

        obj = self.__dict__.copy()
        for sKey in aSkip:
            obj.pop(sKey, None)
        sJson = json.dumps(obj,\
            sort_keys=True, \
                indent = 4, \
                    ensure_ascii=True, \
                        cls=WatershedClassEncoder)
        return sJson    