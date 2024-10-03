"""
File Name: Gui2.py
Author: Brady Eckert and Kamayani Richhariya
Email: be348@drexel.edu
Description: 

Last modified: 2024 Aug 14
"""

import tkinter as tk
#from tkinter import *
#from tkinter.ttk import *
import numpy as np
import matplotlib 
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
m.geometry("750x500")
Title = tk.Label(m, text='LArASIC settings control').grid(row=0, column=3)

# radio button variables
Gain_radio = tk.DoubleVar()
Shaping_time_radio = tk.DoubleVar()
Channel_baseline_radio = tk.IntVar(value=1)
SBF_radio = tk.IntVar(value=1)
Input_radio = tk.IntVar()

## functions for using the radio variables to modify the dictionary
def set_Gain(Gain_radio_dict):
    if   Gain_radio.get() == 4.7: return dict(Gain_radio_dict, sg0=0,sg1=0)
    elif Gain_radio.get() == 7.8: return dict(Gain_radio_dict, sg0=1,sg1=0)
    elif Gain_radio.get() ==  14: return dict(Gain_radio_dict, sg0=0,sg1=1)
    elif Gain_radio.get() ==  25: return dict(Gain_radio_dict, sg0=1,sg1=1)

def set_Shaping_time(Shaping_time_dict):
    if   Shaping_time_radio.get() == 0.5: return dict(Shaping_time_dict,st0=1,st1=0)
    elif Shaping_time_radio.get() == 1.0: return dict(Shaping_time_dict,st0=0,st1=0)
    elif Shaping_time_radio.get() == 2.0: return dict(Shaping_time_dict,st0=1,st1=1)
    elif Shaping_time_radio.get() == 3.0: return dict(Shaping_time_dict,st0=0,st1=1)

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

Gain = tk.Label(m, text='Gain (mV/fC)').grid(row=1, column=1)
R1 = tk.Radiobutton(m, text="4.7", variable=Gain_radio, value=4.7, command=selection_Gain_radio).grid(row=2, column=1)
R2 = tk.Radiobutton(m, text="7.8", variable=Gain_radio, value=7.8, command=selection_Gain_radio).grid(row=3, column=1)
R3 = tk.Radiobutton(m, text="14" , variable=Gain_radio, value=14 , command=selection_Gain_radio).grid(row=4, column=1)
R4 = tk.Radiobutton(m, text="25" , variable=Gain_radio, value=25 , command=selection_Gain_radio).grid(row=5, column=1)

def selection_Channel_baseline():  
    if   Channel_baseline_radio.get()==1: print('Channel baseline set to 200mV - collection mode')
    elif Channel_baseline_radio.get()==0: print('Channel baseline set to 900mV - induction mode')

Channel_baseline = tk.Label(m, text='Channel baseline').grid(row=1, column=2)
R5 = tk.Radiobutton(m, text="200 mV - collection mode", variable=Channel_baseline_radio, value=1, command=selection_Channel_baseline).grid(row=2, column=2)
R6 = tk.Radiobutton(m, text="900 mV - induction mode" , variable=Channel_baseline_radio, value=0, command=selection_Channel_baseline).grid(row=3, column=2)

def selection_SBF():
    if   SBF_radio.get()==0: print('Bypassing unity buffer')
    elif SBF_radio.get()==1: print('Unity buffer engaged')

SBF = tk.Label(m, text='SBF').grid(row=1, column=3)
R7 = tk.Radiobutton(m, text="0 - bypass buffer", variable=SBF_radio, value=0, command=selection_SBF).grid(row=2, column=3)  
R8 = tk.Radiobutton(m, text="1 - unity buffer" , variable=SBF_radio, value=1, command=selection_SBF).grid(row=3, column=3) 

def selection_Shaping_time():
    print('Shaping time set to ',Shaping_time_radio.get(),'us')

Shaping_time = tk.Label(m, text='Shaping_time (us)').grid(row=1, column=4)
R9  = tk.Radiobutton(m, text="0.5", variable=Shaping_time_radio, value=0.5, command=selection_Shaping_time).grid(row=2, column=4)
R10 = tk.Radiobutton(m, text="1.0", variable=Shaping_time_radio, value=1.0, command=selection_Shaping_time).grid(row=3, column=4)
R11 = tk.Radiobutton(m, text="2.0", variable=Shaping_time_radio, value=2.0, command=selection_Shaping_time).grid(row=4, column=4)
R12 = tk.Radiobutton(m, text="3.0", variable=Shaping_time_radio, value=3.0, command=selection_Shaping_time).grid(row=5, column=4)

def selection_Input():
    if   Input_radio.get()==1: print('Test pulse from the FPGA DAC selected')
    elif Input_radio.get()==2: print('Test pulse from the ASIC DAC selected')
    elif Input_radio.get()==3: print('FEMB set to receive data from external source')

Input = tk.Label(m, text='Input').grid(row=1, column=5)
R13 = tk.Radiobutton(m, text="Test pulse: FPGA DAC", variable=Input_radio, value=1, command=selection_Input).grid(row=2, column=5)
R14 = tk.Radiobutton(m, text="Test pulse: ASIC DAC", variable=Input_radio, value=2, command=selection_Input).grid(row=3, column=5)
R15 = tk.Radiobutton(m, text="External source"     , variable=Input_radio, value=3, command=selection_Input).grid(row=4, column=5)

def applybutton():
    print('Applying settings to register dictionary')
    ### REG SETTINGS, see documentation for explanation of each key
    reg_settings_dict=dict(pls_cs=1, dac_sel=1, fpgadac_en=1, asicdac_en=0,\
                    fpgadac_v=0x00, pls_gap = 500, pls_dly = 10,\
                    mon_cs=0,\
                    data_cs = 0,\
                    sts=1, snc=1, sg0=0, sg1=1, st0=0, st1=0, smn=0, sdf=1,\
                    slk0 = 0, stb1 = 0, stb = 0, s16=0, slk1=0, sdc=0, swdac1=1, swdac2=0, dac=0x0 )
    reg_settings_dict=set_Gain(reg_settings_dict)
    reg_settings_dict=set_Shaping_time(reg_settings_dict)
    reg_settings_dict=set_Input(reg_settings_dict)
    reg_settings_dict = dict(reg_settings_dict, sdf=SBF_radio.get(), snc= Channel_baseline_radio.get())
    #print(reg_settings_dict)

Apply = tk.Button(m, text="Apply settings", command=applybutton).grid(row=6, column=2) 

def gobutton():
    print('you hit go')
    print(reg_settings_dict)

Go = tk.Button(m, text="Take Data", command=gobutton).grid(row=6, column=3)

def showplot():
    print('hit showplot')
    fig=Figure(figsize=(3,3),dpi=100)
    y=[i**2 for i in range(-10,11,1)]
    plot1 = fig.add_subplot(111)
    plot1.plot(y)
    mycanvas = FigureCanvasTkAgg(fig,master=m)
    mycanvas.get_tk_widget().grid(row=8,rowspan=3,column=2,columnspan=3)

Showplot = tk.Button(m, text="Show Plot",command=showplot).grid(row=6,column=4)

m.mainloop()

print('mainloop over')
#print(reg_settings_dict)