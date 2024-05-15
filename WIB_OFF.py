# -*- coding: utf-8 -*-
"""
File Name: WIB_OFF.py
Author: Brady Eckert
Email: beckert@bnl.gov/brady.eckert@drexel.edu
Description: 

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

####
from femb_qc import FEMB_QC
a=FEMB_QC()

### Setting some identifiers 
crateno=1 
PTBslotno=1 
fembno_str="739"
a.env="RT"  
fembslotno=4 
a.CLS.femb_sws[fembslotno-1]=1

a.CLS.WIB_ver = 0x120
FEMB_infos = a.FEMB_CHKOUT_Input(crateno, PTBslotno)
a.WIB_IPs = ["192.168.121.1" ]
a.CLS.UDP.MultiPort = False
a.CLS.WIB_IPs = a.WIB_IPs
a.CLS.val = 200   

for wib_ip in a.WIB_IPs:
    a.CLS.FEMBs_CE_OFF_DIR(wib_ip)
