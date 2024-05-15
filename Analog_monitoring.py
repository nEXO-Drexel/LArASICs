# -*- coding: utf-8 -*-
"""
File Name: Analog_monitoring.py
Author: Brady Eckert
Email: beckert@bnl.gov/brady.eckert@drexel.edu
Description: This code will be similar to WIB_script1.py in the set-up and register setting. Shanshan (sgao@bnl.gov) updated top_on.py in the nEXO branch of CE_LD with mode 5 on May 10, 2024; cls_config was also updated to add CLS_CONFIG.CE_MON_CFG which lets you choose a channel to monitor.

Last modified: 2024 May 15
"""

import numpy as np
import sys 
import os
import string
import time
import struct
import codecs
import pickle
from datetime import datetime
from shutil import copyfile
from setdatadir import savedir #change this in setdatadir.py
from cls_config import CLS_CONFIG
from raw_convertor import RAW_CONV

### REG SETTINGS, see documentation for explanation of each key
# the new top_on uses some values-> a.CLS.CE_MON_CFG(pls_cs=0, dac_sel=0, mon_cs=1, sts=0, sg0=0, sg1=0, st0 =1, st1=1, snc=0, monchn=monchnno), I dont think this should send a test pulse so I'll disable the settings
reg_settings_dict=dict(pls_cs=0,\
                    dac_sel=0,\
                    fpgadac_en=0,\
                    asicdac_en=0,\
                    fpgadac_v=0,\
                    pls_gap = 0,\
                    pls_dly = 0,\
                    mon_cs=1,\
                    data_cs = 0,\
                    sts=0, snc=1, sg0=1, sg1=1, st0=1, st1=1, smn=0, sdf=1,\
                    slk0 = 0, stb1 = 0, stb = 0, s16=0, slk1=0, sdc=0, swdac1=0, swdac2=0, dac=0x00)
# select a channel (between 0-127) to monitor- this will be passed to CLS.CE_MON_CFG 
monchnno = int(40)

#####
from femb_qc import FEMB_QC
a=FEMB_QC()

### Setting some identifiers 
crateno=1  
PTBslotno=1  
fembno_str="739" 
a.env="RT" 
fembslotno=4 ; a.CLS.femb_sws[fembslotno-1]=1

## a few more settings-- I haven't needed to modify any of these yet
a.CLS.WIB_ver = 0x120
FEMB_infos = a.FEMB_CHKOUT_Input(crateno, PTBslotno)
a.WIB_IPs = ["192.168.121.1" ]
a.CLS.UDP.MultiPort = False
a.CLS.WIB_IPs = a.WIB_IPs
a.CLS.val = 200   #number of UDP HS packages collected per time

### Setting up some directories for saving the data using identifiers previously set
a.userdir = savedir + "/FEMB_" + fembno_str + "_" + a.env + "/"
a.databkdir = a.userdir 
a.user_f = a.userdir + "tmp.csv"
a.f_qcindex = a.databkdir + "tmp.csv"

if (os.path.exists(a.userdir )):
    pass
else:
    try:
        os.makedirs(a.userdir )
    except OSError:
        print ("Error to create folder %s"%a.userdir )
        sys.exit()
if (os.path.exists(a.databkdir )):
    pass
else:
    try:
        os.makedirs(a.databkdir )
    except OSError:
        print ("Error to create folder %s"%a.databkdir )
        sys.exit()

# Here-- turn on analog monitoring like the mode 5 if statement from top_on.py
#a.CLS.CE_MON_CFG(pls_cs=0, dac_sel=0, mon_cs=1, sts=0, sg0=0, sg1=0, st0 =1, st1=1, snc=0, monchn=monchnno)
rs = reg_settings_dict
a.CLS.CE_MON_CFG(pls_cs = rs['pls_cs'], \
                dac_sel = rs['dac_sel'],\
                fpgadac_en = rs['fpgadac_en'], \
                asicdac_en = rs['asicdac_en'], \
                fpgadac_v = rs['fpgadac_v'],\
                pls_gap = rs['pls_gap'], \
                pls_dly = rs['pls_dly'], \
                mon_cs = rs['mon_cs'], \
                data_cs = rs['data_cs'],\
                sts=rs['sts'], snc=rs['snc'], sg0=rs['sg0'], sg1=rs['sg1'], st0=rs['st0'], st1=rs['st1'], smn=rs['smn'], sdf=rs['sdf'],\
                slk0=rs['slk0'], stb1=rs['stb1'], stb=rs['stb'], s16=rs['s16'], slk1=rs['slk1'], sdc=rs['sdc'],swdac1=rs['swdac1'], swdac2=rs['swdac2'], dac=rs['dac'], \
                monchn = monchnno)

print ("Data saved at :", a.userdir)
print("WIB and FEMB are on, run WIB_OFF.py to turn the FEMB off")
