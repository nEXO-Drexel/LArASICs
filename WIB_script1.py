# -*- coding: utf-8 -*-
"""
File Name: WIB_script1.py
Author: Brady Eckert
Email: beckert@bnl.gov/brady.eckert@drexel.edu
Description: 
!Modified from top_on.py (nEXO branch) in April 2024!
This code will communicate with the WIB and FEMB to run test pulses. The goal is for it to be simple to change ASIC settings from this file. It will reduce the number of inputs used in top_on.py; also will add comments
I'll make it turn the FEMB on and off using the basic code from top_on.py's if/elif statements for selecting modes
Jumper shorting across JMP2 on WIB sets WIB's IP to 192.168.121.1
Set laptop's LAN IP to 192.168.121.50 with subnet mask 255.255.255.0
Last modified: 2024 Jun 12
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
##  A GUI should be able to change the values for the relevant keys we want to modify
reg_settings_dict=dict(pls_cs=1,\
                    dac_sel=1,\
                    fpgadac_en=1,\
                    asicdac_en=0,\
                    fpgadac_v=0x08,\
                    pls_gap = 500,\
                    pls_dly = 10,\
                    mon_cs=0,\
                    data_cs = 0,\
                    sts=1, snc=1, sg0=0, sg1=1, st0=0, st1=0, smn=0, sdf=1,\
                    slk0 = 0, stb1 = 0, stb = 0, s16=0, slk1=0, sdc=0, swdac1=1, swdac2=0, dac=0x0 )

#####
from femb_qc import FEMB_QC
a=FEMB_QC()

### Setting some identifiers 
crateno=1         # WarmInterfaceElectronicsCrate number
PTBslotno=26       # PowerTimingBackplate number-> WIB SN
fembno_str="739"  # Each FEMB should have some identifier number on it
a.env="RT"        # test environment: e.g. RT for room temp, LN for liquid nitrogen, etc.
fembslotno=1      # which slot of the WIB the FEMB is plugged in to
a.CLS.femb_sws[fembslotno-1]=1

## a few more settings-- I haven't needed to modify any of these yet
a.CLS.WIB_ver = 0x120
FEMB_infos = a.FEMB_CHKOUT_Input(crateno, PTBslotno)
#print('FEMB_infos: ',FEMB_infos)
a.WIB_IPs = ["192.168.121.1"]
a.CLS.UDP.MultiPort = False
a.CLS.WIB_IPs = a.WIB_IPs
a.CLS.val = 200   #data amount to take #how many UDP HS package are collected per time


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

# First turn on like the mode 1 if statement from top_on.py
a.CLS.pwr_femb_ignore = False 
a.FEMB_CHKOUT(FEMB_infos, pwr_int_f = False, testcode = 0, ana_flg=True, reg_settings_dict=reg_settings_dict )

## Then turn it off like the mode 0 if statement from top_on.py
for wib_ip in a.WIB_IPs:
    a.CLS.FEMBs_CE_OFF_DIR(wib_ip)

print ("Data saved at :", a.userdir)
