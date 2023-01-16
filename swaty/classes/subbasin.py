

import numpy as np

import json
from json import JSONEncoder
from swaty.classes.swatpara import swatpara
class SubbasinClassEncoder(JSONEncoder):
    """
    The subbasin class json encoder

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
  

class pysubbasin(object):
    """
    The subbasin class

    Args:
        object (_type_): _description_

    Returns:
        _type_: _description_
    """
    lIndex_subbasin=-1
    iFlag_subbasin=0
    nSoil_layer = 1
    nParameter_subbasin=0
    aParameter_subbasin=None
    aParameter_subbasin_name = None

    def  __init__(self, aConfig_in =None):

        if aConfig_in is not None:
            pass
        else:
            pass
            
        

        return
    
    def setup_parameter_by_dict(self, aPara_in= None):
        """
        Set up the subbasin class object parameter

        Args:
            aPara_in (dict, optional): The dictionary that stores parameters. Defaults to None.
        """
        if aPara_in is not None:
            self.nParameter_subbasin = len(aPara_in)
            self.aParameter_subbasin=list()
            self.aParameter_subbasin_name =list()
            for i in range(self.nParameter_subbasin):
                subbasin_dummy = aPara_in[i]
                pParameter_subbasin = swatpara(subbasin_dummy)
                self.aParameter_subbasin.append(pParameter_subbasin)
                sName = pParameter_subbasin.sName
                if sName not in self.aParameter_subbasin_name:
                    self.aParameter_subbasin_name.append(sName)
        else:
            pass

        return
    
    def setup_parameter_by_list(self, aPara_in= None):
        """
        Another function to set up the subbasin class object parameter

        Args:
            aPara_in (list, optional): The list that stores parameters. Defaults to None.
        """

        if aPara_in is not None:
            self.nParameter_subbasin = len(aPara_in)
            self.aParameter_subbasin=list()
            self.aParameter_subbasin_name =list()
            for i in range(self.nParameter_subbasin):
                pParameter_subbasin = aPara_in[i]                
                self.aParameter_subbasin.append(pParameter_subbasin)
                sName = pParameter_subbasin.sName
                if sName not in self.aParameter_subbasin_name:
                    self.aParameter_subbasin_name.append(sName)
        else:
            pass

        return


    def tojson(self):
        """
        Convert a subbasin object to a JSON object

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
                        cls=SubbasinClassEncoder)
        return sJson 