import numpy as np
import json
from json import JSONEncoder
from swaty.classes.swatpara import swatpara

class SoilClassEncoder(JSONEncoder):
    """
    The JSON encoder for the soil class

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
  

class pysoil(object):
    """
    The soil class

    Args:
        object (_type_): _description_

    Returns:
        _type_: _description_
    """
   
    lIndex_hru=-1
    lIndex_soil_layer=-1
    iFlag_soil=0
    
    sSoil_type=''
    nParameter_soil=0
    aParameter_soil=None
    aParameter_soil_name = None

    def  __init__(self, aConfig_in=None):

        if aConfig_in is not None:
            pass
        else:
            pass
        
        return
    
    def setup_parameter_by_dict(self, aPara_in= None):
        """
        Set up the soil class object parameter

        Args:
            aPara_in (dict, optional): The dictionary that stores parameters. Defaults to None.
        """
        if aPara_in is not None:
            self.nParameter_soil = len(aPara_in)
            self.aParameter_soil=list()
            self.aParameter_soil_name =list()
            for i in range(self.nParameter_soil):
                soil_dummy = aPara_in[i]
                pParameter_soil = swatpara(soil_dummy)
                self.aParameter_soil.append(pParameter_soil)
                sName = pParameter_soil.sName
                if sName not in self.aParameter_soil_name:
                    self.aParameter_soil_name.append(sName)
        else:
            pass

        return
    def setup_parameter_by_list(self, aPara_in= None):
        """
        Another function to set up the soil class object parameter

        Args:
            aPara_in (list, optional): The list that stores parameters. Defaults to None.
        """
        if aPara_in is not None:
            self.nParameter_soil = len(aPara_in)
            self.aParameter_soil=list()
            self.aParameter_soil_name =list()
            for i in range(self.nParameter_soil):
                pParameter_soil = aPara_in[i]
                #pParameter_soil = swatpara(soil_dummy)
                self.aParameter_soil.append(pParameter_soil)
                sName = pParameter_soil.sName
                if sName not in self.aParameter_soil_name:
                    self.aParameter_soil_name.append(sName)
        else:
            pass

        return
    def tojson(self):
        """
        Convert the object to a JSON object

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
                        cls=SoilClassEncoder)
        return sJson 