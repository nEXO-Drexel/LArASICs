"""
File Name: Gui2.py
Author: Kamayani Richhariya (and Brady Eckert)
Email: be348@drexel.edu
Description: 

Last modified: 2024 Aug 13
"""

import tkinter as tk
#from tkinter import *
#from tkinter.ttk import *
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

m = tk.Tk()
m.geometry("1100x300")
Title = tk.Label(m, text='LArASIC settings control')
Title.grid(row=0, column=3)

# radio button variables
Gain_radio = tk.DoubleVar()  
Channel_baseline_radio = tk.IntVar()  
SBF_radio = tk.IntVar()  
Shaping_time_radio = tk.IntVar()  
Input_radio = tk.IntVar()  

## functions for using the radio variables to modify the dictionary
def set_Gain(Gain_radio_dict):
    if   Gain_radio.get() == 4.7: return dict(Gain_radio_dict, sg0=0,sg1=0)
    elif Gain_radio.get() == 7.8: return dict(Gain_radio_dict, sg0=1,sg1=0)
    elif Gain_radio.get() ==  14: return dict(Gain_radio_dict, sg0=0,sg1=1)
    elif Gain_radio.get() ==  25: return dict(Gain_radio_dict, sg0=1,sg1=1)

def set_baseline(Channel_baseline_dict):
    if   Channel_baseline_radio.get() == 1: return dict(Channel_baseline_dict,snc = 1)
    elif Channel_baseline_radio.get() == 0: return dict(Channel_baseline_dict,snc = 0)

def set_SBF(SBF_dict):
    if   SBF_radio.get() == 1: return dict(SBF_dict,sdf= 0)
    elif SBF_radio.get() == 2: return dict(SBF_dict,sdf= 1)

def set_Shaping_time(Shaping_time_dict):
    if   Shaping_time_radio.get() == 1: return dict(Shaping_time_dict,st0=1,st1=0) 
    elif Shaping_time_radio.get() == 2: return dict(Shaping_time_dict,st0=0,st1=0)
    elif Shaping_time_radio.get() == 3: return dict(Shaping_time_dict,st0=1,st1=1)
    elif Shaping_time_radio.get() == 4: return dict(Shaping_time_dict,st0=0,st1=1)

def set_Input(Input_dict):
    if Input_radio.get() == 1:
        Input_dict['pls_cs'] = 1 
        Input_dict['dac_sel'] = 1
        Input_dict['fpgadac_en'] = 1
        Input_dict['fpgadac_v'] = 0x08
        Input_dict['asicdac_en'] = 0
        Input_dict['dac'] = 0
        Input_dict['sts'] = 1
        Input_dict['swdac1'] = 1
        Input_dict['swdac2'] = 0
    elif Input_radio.get() == 2:
        Input_dict['pls_cs'] = 1 
        Input_dict['dac_sel'] = 1
        Input_dict['asicdac_en'] = 1
        Input_dict['dac'] = 0x08
        Input_dict['fpgadac_en'] = 0
        Input_dict['fpgadac_v'] = 0
        Input_dict['sts'] = 1
        Input_dict['swdac1'] = 0
        Input_dict['swdac2'] = 1
    elif Input_radio.get() == 3:
        Input_dict['pls_cs'] = 1 
        Input_dict['dac_sel'] = 1
        Input_dict['sts'] = 0  
    return Input_dict


### Buttons
def selection_Gain_radio():
    print('Gain set to ',Gain_radio.get(),'mV/fC')
    #if Gain_radio.get() == 1: print("Gain set to 4.7 mV/fC")
    #elif Gain_radio.get()==2: print("Gain set to 7.8 mV/fC")
    #elif Gain_radio.get()==3: print("Gain set to 14 mV/fC")
    #elif Gain_radio.get()==4: print("Gain set to 25 mV/fC")

Gain = tk.Label(m, text='Gain (mV/fC)').grid(row=1, column=1)
R1 = tk.Radiobutton(m, text="4.7", variable=Gain_radio, value=4.7, command=selection_Gain_radio).grid(row=2, column=1)  
R2 = tk.Radiobutton(m, text="7.8", variable=Gain_radio, value=7.8, command=selection_Gain_radio).grid(row=3, column=1)  
R3 = tk.Radiobutton(m, text="14" , variable=Gain_radio, value=14 , command=selection_Gain_radio).grid(row=4, column=1)  
R4 = tk.Radiobutton(m, text="25" , variable=Gain_radio, value=25 , command=selection_Gain_radio).grid(row=5, column=1)

def selection_Channel_baseline():  
    if Channel_baseline_radio.get()  ==1: print('Channel baseline set to 200mV - collection mode')
    elif Channel_baseline_radio.get()==2: print('Channel baseline set to 900mV - induction mode')

Channel_baseline = tk.Label(m, text='Channel baseline').grid(row=1, column=2)
R5 = tk.Radiobutton(m, text="200 mV - collection mode", variable=Channel_baseline_radio, value=1, command=selection_Channel_baseline).grid(row=2, column=2)  
R6 = tk.Radiobutton(m, text="900 mV - induction mode" , variable=Channel_baseline_radio, value=0, command=selection_Channel_baseline).grid(row=3, column=2)  

def selection_SBF():
    if SBF_radio.get()==1: print('')
    elif SBF_radio.get()==2: print('')

SBF = tk.Label(m, text='SBF').grid(row=1, column=3)
R7 = tk.Radiobutton(m, text="0 - bypass buffer", variable=SBF_radio, value=1, command=selection_SBF).grid(row=2, column=3)  
R8 = tk.Radiobutton(m, text="1 - unity buffer", variable=SBF_radio, value=2, command=selection_SBF).grid(row=3, column=3) 

def selection_Shaping_time():
    if   Shaping_time_radio.get() == 1: print('Shaping time set to 0.5 us')
    elif Shaping_time_radio.get() == 2: print('Shaping time set to 1.0 us')
    elif Shaping_time_radio.get() == 3: print('Shaping time set to 2.0 us')
    elif Shaping_time_radio.get() == 4: print('Shaping time set to 3.0 us')

Shaping_time = tk.Label(m, text='Shaping_time (us)').grid(row=1, column=4)

R9  = tk.Radiobutton(m, text="0.5", variable=Shaping_time_radio, value=1, command=selection_Shaping_time).grid(row=2, column=4)  
R10 = tk.Radiobutton(m, text="1.0", variable=Shaping_time_radio, value=2, command=selection_Shaping_time).grid(row=3, column=4)  
R11 = tk.Radiobutton(m, text="2.0", variable=Shaping_time_radio, value=3, command=selection_Shaping_time).grid(row=4, column=4)  
R12 = tk.Radiobutton(m, text="3.0", variable=Shaping_time_radio, value=4, command=selection_Shaping_time).grid(row=5, column=4)

def selection_Input():  
   print("You selected the option " + str(Input_radio.get())) 

Input = tk.Label(m, text='Input')
Input.grid(row=1, column=5)

R13 = tk.Radiobutton(m, text="FPGA DAC", variable=Input_radio, value=1, command=selection_Input).grid(row=2, column=5)  
R14 = tk.Radiobutton(m, text="ASIC DAC", variable=Input_radio, value=2, command=selection_Input).grid(row=3, column=5)  
R15 = tk.Radiobutton(m, text="External source", variable=Input_radio, value=3, command=selection_Input).grid(row=4, column=5)  

def gobutton():
    print('you hit go')
    ### REG SETTINGS, see documentation for explanation of each key
    reg_settings_dict=dict(pls_cs=1, dac_sel=1,\
                    fpgadac_en=1, asicdac_en=0,\
                    fpgadac_v=0x08,\
                    pls_gap = 500,\
                    pls_dly = 10,\
                    mon_cs=0,\
                    data_cs = 0,\
                    sts=1, snc=1, sg0=0, sg1=1, st0=0, st1=0, smn=0, sdf=1,\
                    slk0 = 0, stb1 = 0, stb = 0, s16=0, slk1=0, sdc=0, swdac1=1, swdac2=0, dac=0x0 )
    print(reg_settings_dict)
    reg_settings_dict=set_Gain(reg_settings_dict)
    reg_settings_dict=set_baseline(reg_settings_dict)
    reg_settings_dict=set_SBF(reg_settings_dict)
    reg_settings_dict=set_Shaping_time(reg_settings_dict)
    reg_settings_dict=set_Input(reg_settings_dict)
    print(reg_settings_dict)



Go = tk.Button(m, text="GO!", command=gobutton )
Go.grid(row=6, column=3) 

m.mainloop()


#print(reg_settings_dict)