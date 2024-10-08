"""
File Name: gui3.py
Author: Brady Eckert and Kamayani Richhariya
Email: be348@drexel.edu
Description: 
A class for the LArASIC gui. This allows sets up radio buttons for LArASIC settings and test pulses. Also has entry widgets for some input strings. The apply settings button sets reg_settings_dict to the selected options and retrieves text entries. The take data button is a filler. The show plot button shows a basic plot in the window.
To Do in gui4.py: incorporate the data taking functions from WIB_script3 or SiPM_script1
Usage: $ python3 gui3.py
Last modified: 2024 Aug 15
"""

import tkinter as tk

import numpy as np
import matplotlib 
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class gui_class:

    def __init__(self,m):
        self.m = m
        m.geometry('1000x600')
        self.Title = tk.Label(m, text='LArASIC settings control').grid(row=0, column=3,columnspan=2)

        ## Register settings--see documentation for explanation of each key
        self.reg_settings_dict=dict(pls_cs=1, dac_sel=1, fpgadac_en=0, asicdac_en=0,\
                        fpgadac_v=0x00, pls_gap = 500, pls_dly = 10, mon_cs=0, data_cs = 0,\
                        sts=1, snc=1, sg0=0, sg1=1, st0=0, st1=0, smn=0, sdf=1,\
                        slk0 = 0, stb1 = 0, stb = 0, s16=0, slk1=0, sdc=0, swdac1=0, swdac2=0, dac=0x0)

        ## other variables to set
        self.wibno='not set'
        self.fembno='not set'
        self.fembslotno=1
        self.environment='RT'
        self.rundate=datetime.now().strftime('%Y_%m_%d')
        self.savedir = "/Users/be348/nexoStuff/LArASIC/code/data/newdir/"+self.rundate+"/"


        ## radio button variables
        self.Input_radio = tk.IntVar(value=3)
        self.Gain_radio = tk.DoubleVar(value=14)
        self.SBF_radio = tk.IntVar(value=1)
        self.Shaping_radio = tk.DoubleVar(value=1.0)
        self.baseline_radio = tk.IntVar(value=1)

        self.wibno_radio = tk.StringVar()
        self.fembno_radio = tk.StringVar()
        self.fembslot_radio = tk.IntVar()
        self.env_radio = tk.StringVar()

        ## making the buttons and labels
        self.L1 = tk.Label(m, text='Gain (mV/fC)').grid(row=1, column=1)
        self.R1 = tk.Radiobutton(m, text="4.7", variable=self.Gain_radio, value=4.7).grid(row=2, column=1)
        self.R2 = tk.Radiobutton(m, text="7.8", variable=self.Gain_radio, value=7.8).grid(row=3, column=1)
        self.R3 = tk.Radiobutton(m, text="14" , variable=self.Gain_radio, value=14 ).grid(row=4, column=1)
        self.R4 = tk.Radiobutton(m, text="25" , variable=self.Gain_radio, value=25 ).grid(row=5, column=1)

        self.L2 = tk.Label(m, text='Channel baseline').grid(row=1, column=2)
        self.R5 = tk.Radiobutton(m, text="200 mV - collection mode", variable=self.baseline_radio, value=1).grid(row=2, column=2)
        self.R6 = tk.Radiobutton(m, text="900 mV - induction mode" , variable=self.baseline_radio, value=0).grid(row=3, column=2)

        self.L3 = tk.Label(m, text='Unity Buffer').grid(row=1, column=3)
        self.R7 = tk.Radiobutton(m, text="0 - bypass buffer", variable=self.SBF_radio, value=0).grid(row=2, column=3)  
        self.R8 = tk.Radiobutton(m, text="1 - engage buffer", variable=self.SBF_radio, value=1).grid(row=3, column=3) 

        self.L4  = tk.Label(m, text='Shaping_time (us)').grid(row=1, column=4)
        self.R9  = tk.Radiobutton(m, text="0.5", variable=self.Shaping_radio, value=0.5).grid(row=2, column=4)
        self.R10 = tk.Radiobutton(m, text="1.0", variable=self.Shaping_radio, value=1.0).grid(row=3, column=4)
        self.R11 = tk.Radiobutton(m, text="2.0", variable=self.Shaping_radio, value=2.0).grid(row=4, column=4)
        self.R12 = tk.Radiobutton(m, text="3.0", variable=self.Shaping_radio, value=3.0).grid(row=5, column=4)

        self.L5  = tk.Label(m, text='Input').grid(row=1, column=5)
        self.R13 = tk.Radiobutton(m, text="Test pulse: FPGA DAC", variable=self.Input_radio, value=1).grid(row=2, column=5)
        self.R14 = tk.Radiobutton(m, text="Test pulse: ASIC DAC", variable=self.Input_radio, value=2).grid(row=3, column=5)
        self.R15 = tk.Radiobutton(m, text="External source"     , variable=self.Input_radio, value=3).grid(row=4, column=5)

        self.L6  = tk.Label(m, text='FEMB Slot #').grid(row=1, column=6)
        self.R16 = tk.Radiobutton(m, text="1", variable=self.fembslot_radio, value=1).grid(row=2, column=6)
        self.R17 = tk.Radiobutton(m, text="2", variable=self.fembslot_radio, value=2).grid(row=3, column=6)
        self.R18 = tk.Radiobutton(m, text="3", variable=self.fembslot_radio, value=3).grid(row=4, column=6)
        self.R19 = tk.Radiobutton(m, text="4", variable=self.fembslot_radio, value=4).grid(row=5, column=6)

        self.Apply = tk.Button(m, text="Apply settings", command=self.applybutton).grid(row=8, column=2, sticky='E')
        self.Go    = tk.Button(m, text="Take Data", command=self.takedatabutton).grid(row=8, column=3)
        self.Showplot = tk.Button(m, text="Show Plot",command=self.showplot).grid(row=8, column=4, sticky='W')

        ## entries
        self.L7 = tk.Label(m, text="WIB #").grid(row=6, column=1, sticky='E')
        self.E1 = tk.Entry(m, textvariable=self.wibno_radio).grid(row=6, column=2,sticky='W')

        self.L8 = tk.Label(m, text='FEMB #').grid(row=6, column=3, sticky='E')
        self.E2 = tk.Entry(m, textvariable=self.fembno_radio).grid(row=6, column=4,sticky='W')

        self.L9 = tk.Label(m, text='Environment').grid(row=6, column=5, sticky='E')
        self.E3 = tk.Entry(m, textvariable=self.env_radio).grid(row=6, column=6,sticky='W')

    ## functions for using the radio variables to modify the dictionary
    def set_Gain(self,Gain_radio_dict):
        if   self.Gain_radio.get() == 4.7: return dict(Gain_radio_dict, sg0=0,sg1=0)
        elif self.Gain_radio.get() == 7.8: return dict(Gain_radio_dict, sg0=1,sg1=0)
        elif self.Gain_radio.get() ==  14: return dict(Gain_radio_dict, sg0=0,sg1=1)
        elif self.Gain_radio.get() ==  25: return dict(Gain_radio_dict, sg0=1,sg1=1)

    def set_Shaping_time(self,Shaping_time_dict):
        if   self.Shaping_radio.get() == 0.5: return dict(Shaping_time_dict, st0=1, st1=0)
        elif self.Shaping_radio.get() == 1.0: return dict(Shaping_time_dict, st0=0, st1=0)
        elif self.Shaping_radio.get() == 2.0: return dict(Shaping_time_dict, st0=1, st1=1)
        elif self.Shaping_radio.get() == 3.0: return dict(Shaping_time_dict, st0=0, st1=1)

    def set_Input(self,Input_dict):
        if   self.Input_radio.get() == 1: return dict(Input_dict, fpgadac_en=1, fpgadac_v=0x08, sts=1, swdac1=1)
        elif self.Input_radio.get() == 2: return dict(Input_dict, asicdac_en=1, dac=0x08, sts=1, swdac2=1)
        elif self.Input_radio.get() == 3: return dict(Input_dict, sts=0) 

    ## Button functions
    def applybutton(self):
        print('Applying settings to register dictionary')
        self.reg_settings_dict = self.set_Gain(self.reg_settings_dict)
        self.reg_settings_dict = self.set_Shaping_time(self.reg_settings_dict)
        self.reg_settings_dict = self.set_Input(self.reg_settings_dict)
        self.reg_settings_dict = dict(self.reg_settings_dict, sdf=self.SBF_radio.get(), snc=self.baseline_radio.get())
        self.wibno=self.wibno_radio.get()
        self.environment.get()

    def takedatabutton(self):
        print(self.reg_settings_dict)
        print(self.wibno)
        print(self.environment)

    def showplot(self):
        fig=Figure(figsize=(6,3),dpi=100)
        y=[i**2 for i in range(-10,11,1)]
        plot1 = fig.add_subplot(111)
        plot1.plot(y)
        mycanvas = FigureCanvasTkAgg(fig,master=self.m)
        mycanvas.get_tk_widget().grid(row=10,rowspan=3,column=1,columnspan=5)

if __name__ == "__main__":
    print('running gui')
    window=tk.Tk()
    gui_class(window)
    window.mainloop()
    print('done')

