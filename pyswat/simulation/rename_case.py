import datetime,os
import numpy as np
pDate = datetime.datetime.today()
sDate_default = "{:04d}".format(pDate.year) + "{:02d}".format(pDate.month) + "{:02d}".format(pDate.day)

aCN2 = np.arange(10) * 10 + 5
aAWC = np.arange(10) / 10.0 + 0.05
sModel='swat'
#start loop
ncase = len(aCN2)

sWorkspace_dummy = '/pic/scratch/liao313/04model/swat/tinpan/simulation'
for i in range(ncase):
    #call the create case function
    
    sCN2 = "{:03d}".format(i)
    sIndex =sCN2
    
    
    sCase = 'CN2_' + sCN2

    sOld_name = sWorkspace_dummy + '/' + sCase
    sNew_name = sWorkspace_dummy + '/' + sModel + sDate_default + sIndex
    print(sOld_name, sNew_name)
    os.rename(sOld_name, sNew_name)

ncase = len(aAWC)
for i in range(ncase):
    #call the create case function
    
    sAWC = "{:03d}".format(i)
    sIndex ="{:03d}".format(i+10)
    
    sCase = 'AWC_' + sAWC
    sOld_name = sWorkspace_dummy + '/' + sCase
    sNew_name = sWorkspace_dummy + '/' + sModel + sDate_default + sIndex
    print(sOld_name, sNew_name)
    os.rename(sOld_name, sNew_name)

    