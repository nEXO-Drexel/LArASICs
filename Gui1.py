"""
File Name: Gui1.py
Author: Kamayani Richhariya (and Brady Eckert)
Email: be348@drexel.edu
Description: 
!Copied from Kamayani Richhariya's GUI_LArASIC.ipynb!
This code will ask for user input to change settings on LArASICs aboard the FEMB. 
Some other future additions: inputs for how much data to take (control a.CLS.val and number of cycles to run a.FEMB_CHKOUT), other identifiers like WIB or FEMB number, FEMB slot number, have GO! close GUI and continue to trigger DAQ for some amount of data to take, some cool name/acronym for this, Drexel nEXO and BNL logo
wibno_str= "P22" #string
fembno_str="731"  # FEMB identifier number string
a.env="RT"        # test environment string
fembslotno=1    # int
The print at the end for re_settings_dict currently isnt showing values being changed, so selecting different values and hitting GO! doesnt change the respective values
Remove global monitor option, that can just be set to off
Last modified: 2024 Jul 12
"""

import tkinter
from tkinter import *
from tkinter.ttk import *
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
m = tkinter.Tk()
m.geometry("1100x300")
Title = tkinter.Label(m, text='LArASIC settings control')
Title.grid(row=0, column=3)

### REG SETTINGS, see documentation for explanation of each key
## The GUI will be able to change the values for these keys that control test pulses and DAQ
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


def setting_Gain(Gain_radio_dict):
    if Gain_radio == 1:
        Gain_radio_dict['sg0'] = 0
        Gain_radio_dict['sg1'] = 0
        #reg_settings_dict['sg0']=0
    elif Gain_radio == 2:
        Gain_radio_dict['sg0'] = 1
        Gain_radio_dict['sg1'] = 0
    elif Gain_radio == 3:
        Gain_radio_dict['sg0'] = 0
        Gain_radio_dict['sg1'] = 1
    elif Gain_radio == 4:
        Gain_radio_dict['sg0'] = 1
        Gain_radio_dict['sg1'] = 1

def setting_Channel_baseline(Channel_baseline__dict):
    if Channel_baseline_radio == 1:
        Channel_baseline__dict['snc'] = 1
    elif Channel_baseline_radio == 2:
        Channel_baseline__dict['snc'] = 0

def setting_SBF(SBF_dict):
    if SBF_radio == 1:
        SBF_dict['sdf'] = 0
    elif SBF_radio == 2:
        SBF_dict['sdf'] = 1

def setting_Shaping_time(Shaping_time_dict):
    if Shaping_time_radio == 1:
        Shaping_time_dict['st0'] = 1
        Shaping_time_dict['st1'] = 0
    elif Shaping_time_radio == 2:
        Shaping_time_dict['st0'] = 0
        Shaping_time_dict['st1'] = 0
    elif Shaping_time_radio == 3:
        Shaping_time_dict['st0'] = 1
        Shaping_time_dict['st1'] = 1
    elif Shaping_time_radio == 4:
        Shaping_time_dict['st0'] = 0
        Shaping_time_dict['st1'] = 1
        
def setting_Input(Input_dict):
    if Input_radio == 1:
        Input_dict['pls_cs'] = 1 
        Input_dict['dac_sel'] = 1
        Input_dict['fpgadac_en'] = 1
        Input_dict['fpgadac_v'] = 0x08
        Input_dict['asicdac_en'] = 0
        Input_dict['dac'] = 0
        Input_dict['sts'] = 1
        Input_dict['swdac1'] = 1
        Input_dict['swdac2'] = 0
    elif Input_radio == 2:
        Input_dict['pls_cs'] = 1 
        Input_dict['dac_sel'] = 1
        Input_dict['asicdac_en'] = 1
        Input_dict['dac'] = 0x08
        Input_dict['fpgadac_en'] = 0
        Input_dict['fpgadac_v'] = 0
        Input_dict['sts'] = 1
        Input_dict['swdac1'] = 0
        Input_dict['swdac2'] = 1
    elif Input_radio == 3:
        Input_dict['pls_cs'] = 1 
        Input_dict['dac_sel'] = 1
        Input_dict['sts'] = 0        

def setting_SMN(SMN_dict):
    if SMN_radio == 1:
        SMN_dict['smn'] = 0
    elif SMN_radio ==2:
        SMN_dict['smn'] = 1

def selection_Gain_radio():  
   print("You selected the option " + str(Gain_radio.get())) 

Gain = tkinter.Label(m, text='Gain (mV/fC)')
Gain.grid(row=1, column=1)

Gain_radio = tkinter.IntVar()  
R1 = tkinter.Radiobutton(m, text="4.7", variable=Gain_radio, value=1,  
                  command=selection_Gain_radio)  
R1.grid(row=2, column=1)  
  
R2 = tkinter.Radiobutton(m, text="7.8", variable=Gain_radio, value=2,  
                  command=selection_Gain_radio)  
R2.grid(row=3, column=1)  
  
R3 = tkinter.Radiobutton(m, text="14", variable=Gain_radio, value=3,  
                  command=selection_Gain_radio)  
R3.grid(row=4, column=1)  

R4 = tkinter.Radiobutton(m, text="25", variable=Gain_radio, value=4,  
                  command=selection_Gain_radio)  
R4.grid(row=5, column=1)

def selection_Channel_baseline():  
   print("You selected the option " + str(Channel_baseline_radio.get())) 

Channel_baseline = tkinter.Label(m, text='Channel baseline')
Channel_baseline.grid(row=1, column=2)

Channel_baseline_radio = tkinter.IntVar()  
R5 = tkinter.Radiobutton(m, text="200 mV - collection mode", variable=Channel_baseline_radio, value=1,  
                  command=selection_Channel_baseline)  
R5.grid(row=2, column=2)  
  
R6 = tkinter.Radiobutton(m, text="900 mV - induction mode", variable=Channel_baseline_radio, value=2,  
                  command=selection_Channel_baseline)  
R6.grid(row=3, column=2)  

def selection_SBF():  
   print("You selected the option " + str(SBF_radio.get())) 

SBF = tkinter.Label(m, text='SBF')
SBF.grid(row=1, column=3)

SBF_radio = tkinter.IntVar()  
R7 = tkinter.Radiobutton(m, text="0 - bypass buffer", variable=SBF_radio, value=1,  
                  command=selection_SBF)  
R7.grid(row=2, column=3)  
  
R8 = tkinter.Radiobutton(m, text="1 - unity buffer", variable=SBF_radio, value=2,  
                  command=selection_SBF)  
R8.grid(row=3, column=3) 

def selection_Shaping_time():  
   print("You selected the option " + str(Shaping_time_radio.get())) 

Shaping_time = tkinter.Label(m, text='Shaping_time (us)')
Shaping_time.grid(row=1, column=4)

Shaping_time_radio = tkinter.IntVar()  
R9 = tkinter.Radiobutton(m, text="0.5", variable=Shaping_time_radio, value=1,  
                  command=selection_Shaping_time)  
R9.grid(row=2, column=4)  
  
R10 = tkinter.Radiobutton(m, text="1.0", variable=Shaping_time_radio, value=2,  
                  command=selection_Shaping_time)  
R10.grid(row=3, column=4)  
  
R11 = tkinter.Radiobutton(m, text="2.0", variable=Shaping_time_radio, value=3,  
                  command=selection_Shaping_time)  
R11.grid(row=4, column=4)  

R12 = tkinter.Radiobutton(m, text="3.0", variable=Shaping_time_radio, value=4,  
                  command=selection_Shaping_time)  
R12.grid(row=5, column=4)

def selection_Input():  
   print("You selected the option " + str(Input_radio.get())) 

Input = tkinter.Label(m, text='Input')
Input.grid(row=1, column=5)

Input_radio = tkinter.IntVar()  
R13 = tkinter.Radiobutton(m, text="FPGA DAC", variable=Input_radio, value=1,  
                  command=selection_Input)  
R13.grid(row=2, column=5)  
  
R14 = tkinter.Radiobutton(m, text="ASIC DAC", variable=Input_radio, value=2,  
                  command=selection_Input)  
R14.grid(row=3, column=5)  
  
R15 = tkinter.Radiobutton(m, text="External source", variable=Input_radio, value=3,  
                  command=selection_Input)  
R15.grid(row=4, column=5)  

def selection_SMN():  
   print("You selected the option " + str(SMN_radio.get()))

SMN = tkinter.Label(m, text='SMN')
SMN.grid(row=1, column=6)

SMN_radio = tkinter.IntVar()  
R16 = tkinter.Radiobutton(m, text="0 - disconnect channel from monitoring output", variable=SMN_radio, value=1,  
                  command=selection_SMN)  
R16.grid(row=2, column=6)  
  
R17 = tkinter.Radiobutton(m, text="1 - connect channel to global monitoring output", variable=SMN_radio, value=2,  
                  command=selection_SMN)  
R17.grid(row=3, column=6) 

Go = tkinter.Button(m, text="GO!", command=lambda: [setting_Gain(reg_settings_dict), 
                                                    setting_Channel_baseline(reg_settings_dict),
                                                    setting_SBF(reg_settings_dict),
                                                    setting_Shaping_time(reg_settings_dict),
                                                    setting_Input(reg_settings_dict),
                                                    setting_SMN(reg_settings_dict)] )
Go.grid(row=6, column=3) 

m.mainloop()


print(reg_settings_dict)