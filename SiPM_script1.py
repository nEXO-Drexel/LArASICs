# -*- coding: utf-8 -*-
"""
File Name: SiPM_script1.py
Author: Brady Eckert
Email: beckert@bnl.gov/brady.eckert@drexel.edu
Description: 
This script will be used for reading out signals from a 4x4 HPK SiPM array through a transition board. Branched off from WIB_script3.py. The goal of this will be to take data from a SiPM array with an 8P2S configuration (only 2 channels). Things that should be changeable include: gain, shaping times, a.CLS.val, number of times to take a set of data.
I was starting to try this with WIB_script2.py by taking un-russian-nesting-doll-ing the code to be able to call the actual data taking method multiple times.
Last modified: 2024 Aug 1
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

### REG SETTINGS, see documentation for explanation of each key, no test pulse gets rid of a lot of them
reg_settings_dict=dict(pls_cs=0,\
                    #dac_sel=0,\
                    #fpgadac_en=0,\
                    #asicdac_en=0,\
                    #fpgadac_v=0x00,\
                    #pls_gap = 500,\
                    #pls_dly = 10,\
                    mon_cs=1,\
                    data_cs = 0,\
                    sts=0, snc=1, sg0=0, sg1=1, st0=0, st1=0, smn=0, sdf=1,\
                    slk0 = 0, stb1 = 0, stb = 0, s16=0, slk1=0, sdc=0, swdac1=0, swdac2=0, dac=0x00 )

###
rundate = datetime.now().strftime('%Y_%m_%d')
savedir = "/Users/be348/nexoStuff/LArASIC/code/data/SiPMsReadout/"+rundate+"/" # ~ = /Users/be348=

#####
from femb_qc import FEMB_QC
a=FEMB_QC()

### Setting some identifiers 
#crateno=1         # WarmInterfaceElectronicsCrate number
#PTBslotno=1       # PowerTimingBackplate number
wibno_str="P6"
fembno_str="731"  # FEMB identifier number
a.env="RT"        # test environment
fembslotno=2 ;a.CLS.femb_sws[fembslotno-1]=1

## 
a.CLS.WIB_ver = 0x120 
FEMB_infos = a.FEMB_CHKOUT_Input()#crateno, PTBslotno)
a.WIB_IPs = ["192.168.121.1"]
a.CLS.UDP.MultiPort = False
a.CLS.WIB_IPs = a.WIB_IPs
a.CLS.val = 100    #UDP HS package collected


### Setting up directories for saving the data
a.userdir = savedir + "/WIB" + wibno_str + "_FEMB" +fembno_str + "/"
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

rs=reg_settings_dict
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
## Power off
'''for wib_ip in a.WIB_IPs:
    a.CLS.FEMBs_CE_OFF_DIR(wib_ip)'''
a.CLS.FEMBs_CE_OFF_DIR(a.WIB_IPs[0])

print ("Data saved at :", a.userdir)
