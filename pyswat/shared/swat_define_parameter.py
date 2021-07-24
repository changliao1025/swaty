import numpy as np

def swat_define_parameter(aParameter_in, aValue_in, aValue_lower_in, aValue_upper_in):
    

    aParameter_watershed_all = np.array(['SFTMP','SMTMP','AI0'])
    aParameter_subbasin_all = np.array(['CH_K2','CH_N2'])
    aParameter_hru_all = np.array(['CN2'])

    aParameter_watershed = list()
    aParameter_subbasin     = list()
    aParameter_hru       = list()
    aParameter_value_watershed = list()
    aParameter_value_lower_watershed = list()
    aParameter_value_upper_watershed = list()

    aParameter_value_subbasin     = list()
    aParameter_value_lower_subbasin = list()
    aParameter_value_upper_subbasin = list()
    aParameter_value_hru       = list()
    aParameter_value_lower_hru  = list()
    aParameter_value_upper_hru  = list()

    aParameter_in= np.array(aParameter_in)
    nParameter  = aParameter_in.size
    

    for i in range(nParameter):
        sParameter  = aParameter_in[i]
        aValue = aValue_in[i]
        aValue_lower = aValue_lower_in[i]
        aValue_upper = aValue_upper_in[i]
        if sParameter in aParameter_watershed_all:
            aParameter_watershed.append(sParameter)
            aParameter_value_watershed.append(aValue)
            aParameter_value_lower_watershed.append(aValue_lower)
            aParameter_value_upper_watershed.append(aValue_upper)
        else: 
            if sParameter in aParameter_subbasin_all:
                aParameter_subbasin.append(sParameter)
                aParameter_value_subbasin.append(aValue)
                aParameter_value_lower_subbasin.append(aValue_lower)
                aParameter_value_upper_subbasin.append(aValue_upper)
            else:
                if sParameter in aParameter_hru_all:
                    aParameter_hru.append(sParameter)
                    aParameter_value_hru.append(aValue)
                    aParameter_value_lower_hru.append(aValue_lower)
                    aParameter_value_upper_hru.append(aValue_upper)

        pass

    aParameter_watershed = np.array(aParameter_watershed)
    aParameter_subbasin = np.array(aParameter_subbasin)
    aParameter_hru = np.array(aParameter_hru)

    aParameter_value_watershed = np.array(aParameter_value_watershed)
    aParameter_value_subbasin =     np.array(aParameter_value_subbasin)
    aParameter_value_hru =       np.array(aParameter_value_hru)

    aParameter_value_lower_watershed = np.array(aParameter_value_lower_watershed)
    aParameter_value_lower_subbasin =     np.array(aParameter_value_lower_subbasin)
    aParameter_value_lower_hru =       np.array(aParameter_value_lower_hru)

    aParameter_value_upper_watershed = np.array(aParameter_value_upper_watershed)
    aParameter_value_upper_subbasin =     np.array(aParameter_value_upper_subbasin)
    aParameter_value_upper_hru =       np.array(aParameter_value_upper_hru)

    
    return aParameter_watershed, aParameter_subbasin, aParameter_hru,\
        aParameter_value_watershed,aParameter_value_subbasin,aParameter_value_hru,\
            aParameter_value_lower_watershed, aParameter_value_lower_subbasin,  aParameter_value_lower_hru,\
            aParameter_value_upper_watershed, aParameter_value_upper_subbasin, aParameter_value_upper_hru
