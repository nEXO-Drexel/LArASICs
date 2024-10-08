# -*- coding: utf-8 -*-
"""
File Name: WIB_daq_cycle.py
Author: Brady Eckert
Email: be348@drexel.edu
Description: 
This script will be used for testing WIBs and FEMBs for the single-WIB stands
Last modified: 2024 Oct 4
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
from cls_config import CLS_CONFIG
from raw_convertor import RAW_CONV

### REG SETTINGS, see documentation for explanation of each key
reg_settings_dict=dict(pls_cs=1,\
                    dac_sel=1,\
                    fpgadac_en=0,\
                    asicdac_en=1,\
                    fpgadac_v=0x00,\
                    pls_gap = 500,\
                    pls_dly = 10,\
                    mon_cs=0,\
                    data_cs = 0,\
                    sts=1, snc=1, sg0=0, sg1=1, st0=0, st1=0, smn=0, sdf=1,\
                    slk0 = 0, stb1 = 0, stb = 0, s16=0, slk1=0, sdc=0, swdac1=0, swdac2=1, dac=0x08 )

###
rundate = datetime.now().strftime('%Y_%m_%d')
savedir = "./data/"+rundate+"/" 

#####
from femb_qc import FEMB_QC
a=FEMB_QC()

### Setting some identifiers 
wibno_str="P6"    # WIB ID number
fembno_str="731"  # FEMB ID number
a.env="RT"        # test environment
fembslotno=2      # FEMB slot number
a.CLS.femb_sws[fembslotno-1]=1

## 
a.CLS.WIB_ver = 0x120 
FEMB_infos = a.FEMB_CHKOUT_Input()

a.WIB_IPs = ["192.168.121.1"]
a.CLS.UDP.MultiPort = False
a.CLS.WIB_IPs = a.WIB_IPs
a.CLS.val = 100    #UDP HS package collected


### Setting up directories for saving the data
a.userdir = savedir + "/WIB_" + wibno_str + "_FEMB_" + fembno_str + "/"
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

# Power on, run test code 0 with the settings from reg_settings_dict
a.CLS.pwr_femb_ignore = False 
a.FEMB_CHKOUT(FEMB_infos, ana_flg=True, reg_settings_dict=reg_settings_dict )

## Power off
a.CLS.FEMBs_CE_OFF_DIR(a.WIB_IPs[0])

print ("Data saved at :", a.userdir)
