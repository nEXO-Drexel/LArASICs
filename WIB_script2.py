# -*- coding: utf-8 -*-
"""
File Name: WIB_script2.py
Author: Brady Eckert
Email: beckert@bnl.gov/brady.eckert@drexel.edu
Description: 
This script will be for learning to get raw data from the FEMB/WIB. It will take the register settings to adjust the FE ASIC settings in reg_settings_dict, then turn on the FEMB, take data, and turn the FEMB off.
Last modified: 2024 May 22
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
reg_settings_dict=dict(pls_cs=1,\
                    dac_sel=1,\
                    fpgadac_en=0,\
                    asicdac_en=0,\
                    fpgadac_v=0x08,\
                    pls_gap = 500,\
                    pls_dly = 10,\
                    mon_cs=0,\
                    data_cs = 0,\
                    sts=1, snc=1, sg0=0, sg1=1, st0=0, st1=0, smn=0, sdf=1,\
                    slk0 = 0, stb1 = 0, stb = 0, s16=0, slk1=0, sdc=0, swdac1=1, swdac2=0, dac=0x08 )
rs=reg_settings_dict

#####
from femb_qc import FEMB_QC
a=FEMB_QC()

### Setting some identifiers 
#crateno=1  
#PTBslotno=1 
fembno_str="739"
a.env="RT" 
fembslotno=4 ;a.CLS.femb_sws[fembslotno-1]=1

a.CLS.WIB_ver = 0x120
FEMB_infos = a.FEMB_CHKOUT_Input(crateno=1, slotno=1)
a.WIB_IPs = ["192.168.121.1" ]
a.CLS.UDP.MultiPort = False
a.CLS.WIB_IPs = a.WIB_IPs

# UDP packet size
a.CLS.val = 200

### Setting up directory for saving the data 
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

#-----turn on and configure------
a.CLS.pwr_femb_ignore = False
#a.FEMB_CHKOUT(FEMB_infos, pwr_int_f=False, testcode=0, ana_flg=False, reg_settings_dict=reg_settings_dict)
#-FEMB_CHKOUT would do the following
pwr_qcs = []
a.CLS.pwr_int_f = False
#qc_data = a.FEMB_CHK_ACQ(testcode = 0, rs=reg_settings_dict)
#--FEMB_CHK_ACQ would do the following
#--sts_num and FM_only_f are set to the default values, f_save is set to False, but f_save isnt mentioned anywhere else so not relevant?
a.CLS.WIBs_SCAN()
a.CLS.FEMBs_SCAN()
a.CLS.WIBs_CFG_INIT()
cfglog = a.CLS.CE_CHK_CFG(pls_cs = rs['pls_cs'], \
                    dac_sel = rs['dac_sel'],\
                    fpgadac_en = rs['fpgadac_en'], \
                    asicdac_en = rs['asicdac_en'], \
                    fpgadac_v = rs['fpgadac_v'],\
                    pls_gap = rs['pls_gap'], \
                    pls_dly = rs['pls_dly'], \
                    mon_cs = rs['mon_cs'], \
                    data_cs = rs['data_cs'],\
                    sts=rs['sts'], snc=rs['snc'], sg0=rs['sg0'], sg1=rs['sg1'], st0=rs['st0'], st1=rs['st1'], smn=rs['smn'], sdf=rs['sdf'],\
                    slk0=rs['slk0'], stb1=rs['stb1'], stb=rs['stb'], s16=rs['s16'], slk1=rs['slk1'], sdc=rs['sdc'],swdac1=rs['swdac1'], swdac2=rs['swdac2'], dac=rs['dac'])

time.sleep(2)
print("FEMB configured")
a.CLS.savedir = a.databkdir
#--qc_data = self.CLS.TPC_UDPACQ(cfglog)
#--returns qc_data, but this script will take data later

#-skipping the ana_flg section in FEMB_CHKOUT 
a.raw_data=[]


#-----take data------
a.CLS.TPC_UDPACQ(cfglog)
time.sleep(2)
a.CLS.TPC_UDPACQ(cfglog)

print("Data saved at:", a.userdir)
print("------Done------")