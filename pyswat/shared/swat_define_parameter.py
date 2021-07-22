import numpy as np

def swat_define_parameter(aParameter_in, aValue_in):
    

    aParameter_watershed_all = np.array(['SFTMP','SMTMP','AI0'])
    aParameter_subbasin_all = np.array(['CH_K2','CH_N2'])
    aParameter_hru_all = np.array(['cn2'])

    aParameter_watershed = list()
    aParameter_subbasin     = list()
    aParameter_hru       = list()
    aValue_watershed = list()
    aValue_subbasin     = list()
    aValue_hru       = list()

    nParameter  = aParameter_in.size
    for i in range(nParameter):
        sParameter  = aParameter_in[i]
        aValue = aValue_in[i]
        if sParameter in aParameter_watershed_all:
            aParameter_watershed.append(sParameter)
            aValue_watershed.append(aValue)
        else: 
            if sParameter in aParameter_subbasin_all:
                aParameter_subbasin.append(sParameter)
                aValue_subbasin.append(aValue)
            else:
                if sParameter in aParameter_hru_all:
                    aParameter_hru.append(sParameter)
                    aValue_hru.append(aValue)

        pass

    aParameter_watershed = np.array(aParameter_watershed)
    aParameter_subbasin = np.array(aParameter_subbasin)
    aParameter_hru = np.array(aParameter_hru)

    aValue_watershed = np.array(aValue_watershed)
    aValue_subbasin =     np.array(aValue_subbasin)
    aValue_hru =       np.array(aValue_hru)

    
    return aParameter_watershed, aParameter_subbasin, aParameter_hru,aValue_watershed,aValue_subbasin,aValue_hru