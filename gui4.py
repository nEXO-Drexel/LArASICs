"""
File Name: gui4.py
Author: Brady Eckert and Kamayani Richhariya
Email: be348@drexel.edu
Description: 
A class for the LArASIC gui.
Future Additions: modify CLS.val and number of times to make data
Usage: $ python3 gui4.py
Last modified: 2024 Sep 25
"""

import tkinter as tk
#from tkinter import ttk
import sys 
import os
import numpy as np
import pickle
import matplotlib 
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageTk, Image
from datetime import datetime

from femb_qc import FEMB_QC

class gui_class:

    def __init__(self,m):
        self.m = m
        m.title("LArASIC Control")
        m.geometry('1000x800')
        self.Title = tk.Label(m, text='LArASIC settings control').grid(row=0, column=3, columnspan=2)
        self.add_logo()

        ## Register settings--see documentation for explanation of each key
        self.reg_settings_dict = dict(pls_cs=1, dac_sel=1, fpgadac_en=0, asicdac_en=0,\
                        fpgadac_v=0x00, pls_gap = 500, pls_dly = 10, mon_cs=0, data_cs = 0,\
                        sts=1, snc=1, sg0=0, sg1=1, st0=0, st1=0, smn=0, sdf=1,\
                        slk0 = 0, stb1 = 0, stb = 0, s16=0, slk1=0, sdc=0, swdac1=0, swdac2=0, dac=0x0)

        ## other variables to set
        self.wibno='not set'
        self.fembno='not set'
        self.fembslotno = 1
        self.environment='RT'
        self.rundate = datetime.now().strftime('%Y_%m_%d')
        self.savedir = "/Users/be348/nexoStuff/LArASIC/code/data/newdir/"+self.rundate+"/"
        self.last_file = ""

        ## making the radio buttons and labels
        self.set_radio_buttons()
        self.Gain  = tk.Label(m, text='Gain (mV/fC)').grid(row=1, column=1)
        self.Gain1 = tk.Radiobutton(m, text="4.7", variable=self.Gain_radio, value=4.7).grid(row=2, column=1)
        self.Gain2 = tk.Radiobutton(m, text="7.8", variable=self.Gain_radio, value=7.8).grid(row=3, column=1)
        self.Gain3 = tk.Radiobutton(m, text="14" , variable=self.Gain_radio, value=14 ).grid(row=4, column=1)
        self.Gain4 = tk.Radiobutton(m, text="25" , variable=self.Gain_radio, value=25 ).grid(row=5, column=1)

        self.Baseline  = tk.Label(m, text='Channel baseline').grid(row=1, column=2)
        self.Baseline1 = tk.Radiobutton(m, text="200 mV - collection mode", variable=self.baseline_radio, value=1).grid(row=2, column=2)
        self.Baseline2 = tk.Radiobutton(m, text="900 mV - induction mode" , variable=self.baseline_radio, value=0).grid(row=3, column=2)

        self.UBuffer  = tk.Label(m, text='Unity Buffer').grid(row=1, column=3)
        self.UBuffer1 = tk.Radiobutton(m, text="0 - bypass buffer", variable=self.SBF_radio, value=0).grid(row=2, column=3)  
        self.UBuffer2 = tk.Radiobutton(m, text="1 - engage buffer", variable=self.SBF_radio, value=1).grid(row=3, column=3) 

        self.ST  = tk.Label(m, text='Shaping time (us)').grid(row=1, column=4)
        self.ST1 = tk.Radiobutton(m, text="0.5", variable=self.Shaping_radio, value=0.5).grid(row=2, column=4)
        self.ST2 = tk.Radiobutton(m, text="1.0", variable=self.Shaping_radio, value=1.0).grid(row=3, column=4)
        self.ST3 = tk.Radiobutton(m, text="2.0", variable=self.Shaping_radio, value=2.0).grid(row=4, column=4)
        self.ST4 = tk.Radiobutton(m, text="3.0", variable=self.Shaping_radio, value=3.0).grid(row=5, column=4)

        self.Input= tk.Label(m, text='Input').grid(row=1, column=5)
        self.FPGA = tk.Radiobutton(m, text="Test pulse: FPGA DAC", variable=self.Input_radio, value=1).grid(row=2, column=5)
        self.ASIC = tk.Radiobutton(m, text="Test pulse: ASIC DAC", variable=self.Input_radio, value=2).grid(row=3, column=5)
        self.EXT  = tk.Radiobutton(m, text="External source"     , variable=self.Input_radio, value=3).grid(row=4, column=5)

        self.FEMBSlot  = tk.Label(m, text='FEMB Slot #').grid(row=1, column=6)
        self.FEMBSlot1 = tk.Radiobutton(m, text="1", variable=self.fembslot_radio, value=1).grid(row=2, column=6)
        self.FEMBSlot2 = tk.Radiobutton(m, text="2", variable=self.fembslot_radio, value=2).grid(row=3, column=6)
        self.FEMBSlot3 = tk.Radiobutton(m, text="3", variable=self.fembslot_radio, value=3).grid(row=4, column=6)
        self.FEMBSlot4 = tk.Radiobutton(m, text="4", variable=self.fembslot_radio, value=4).grid(row=5, column=6)

        self.Apply    = tk.Button(m, text="Apply settings", command=self.applybutton).grid(row=8, column=2, sticky='E')
        self.TakeData = tk.Button(m, text="Take Data", command=self.takedatabutton).grid(row=8, column=3)
        self.Showplot = tk.Button(m, text="Show Plot",command=self.showplot).grid(row=8, column=4, sticky='W')

        ## entries
        self.WIBLabel = tk.Label(m, text="WIB #").grid(row=6, column=1, sticky='E')
        self.WIBEntry = tk.Entry(m, textvariable=self.wibno_radio).grid(row=6, column=2,sticky='W')

        self.FEMBLabel = tk.Label(m, text='FEMB #').grid(row=6, column=3, sticky='E')
        self.FEMBEntry = tk.Entry(m, textvariable=self.fembno_radio).grid(row=6, column=4,sticky='W')

        self.ENVLabel = tk.Label(m, text='Test Environment:').grid(row=6, column=5, sticky='E')
        self.ENVEntry = tk.Entry(m, textvariable=self.env_radio).grid(row=6, column=6,sticky='W')

        self.SaveDirLabel = tk.Label(m, text='Save Directory:').grid(row=7,column=1,sticky='E')
        self.SaveDirEntry = tk.Entry(m, textvariable=self.savedir_radio,justify='left',width=80).grid(row=7,column=2,columnspan=5,sticky='W')

    ## set up radio buttons all together
    def set_radio_buttons(self):
        self.Input_radio = tk.IntVar(value=3)
        self.Gain_radio = tk.DoubleVar(value=14)
        self.SBF_radio = tk.IntVar(value=1)
        self.Shaping_radio = tk.DoubleVar(value=1.0)
        self.baseline_radio = tk.IntVar(value=1)

        self.wibno_radio = tk.StringVar()
        self.fembno_radio = tk.StringVar()
        self.fembslot_radio = tk.IntVar()
        self.env_radio = tk.StringVar(value="RT")
        self.savedir_radio=tk.StringVar(value=self.savedir)

    ## adding nEXO logo, it works
    def add_logo(self):
        imagefilename = '/Users/be348/nexoStuff/LArASIC/code/nEXO/images/nEXO-logo.png'
        img = ImageTk.PhotoImage(Image.open(imagefilename).resize((300,100),Image.Resampling.LANCZOS))
        self.logo = tk.Label(self.m,image=img)
        self.logo.image = img
        self.logo.grid(row=0,column=1,columnspan=2,sticky='NE')

    ## functions for using the radio variables to modify the dictionary for options that change multiple bits
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
        self.wibno = self.wibno_radio.get()
        self.environment = self.env_radio.get()
        self.fembslotno = self.fembslot_radio.get()

    def takedatabutton(self):
        a=FEMB_QC()
        a.CLS.femb_sws[self.fembslotno-1]=1
        a.CLS.WIB_ver = 0x120
        FEMB_infos = a.FEMB_CHKOUT_Input()
        a.WIB_IPs = ["192.168.121.1"]
        a.CLS.UDP.MultiPort = False
        a.CLS.WIB_IPs = a.WIB_IPs
        a.CLS.val = 100

        a.userdir = self.savedir + "WIB_" + self.wibno + "/"
        a.databkdir = a.userdir 
        a.user_f = a.userdir + "tmp.csv"
        a.f_qcindex = a.databkdir + "tmp.csv"

        if (os.path.exists(a.userdir )): pass
        else:
            try:  os.makedirs(a.userdir )
            except OSError: print ("Error to create folder %s"%a.userdir ); sys.exit()
        if (os.path.exists(a.databkdir )): pass
        else:
            try: os.makedirs(a.databkdir )
            except OSError: print ("Error to create folder %s"%a.databkdir ); sys.exit()

        # power on and run with reg_settings_dict and produce the results pdf
        a.CLS.pwr_femb_ignore = False 
        a.FEMB_CHKOUT(FEMB_infos, pwr_int_f = False, testcode = 0, ana_flg=True, reg_settings_dict=self.reg_settings_dict)

        # power off the femb
        a.CLS.FEMBs_CE_OFF_DIR(a.WIB_IPs[0])

        self.last_file = a.last_file_saved
        print ("Data saved at: ", a.userdir)

    def showplot(self):
        ## showplot() will use the last file saved to display the waveforms, maybe it should be relabelled
        fig=Figure(figsize=(5,3),dpi=200)
        # retrieve the data from self.last_file (setting manually for now)
        #with open(self.last_file,'rb') as f:
        myfile = '/Users/be348/nexoStuff/LArASIC/code/data/newdir/2024_08_19//WIB_P6/FEMB_CHKOUT_RT_2024_08_19_12_55_14.bin'
        with open(myfile,'rb') as f:
            rawdata = pickle.load(f)
        waveforms=rawdata[self.fembslotno-1][1][2][4]

        plot1 = fig.add_subplot(111)
        plot1.set_title('Waveform plot')
        plot1.set_xlabel("Time ($\mu$s)")
        plot1.set_ylabel("ADC/bin")
        for chni in range(len(waveforms)):
            plot1.plot((0.5*np.arange(500)),waveforms[chni],color='C%d'%(chni%9))
        plot1.set_xbound(0,50)
        fig.tight_layout()

        mycanvas = FigureCanvasTkAgg(fig,master=self.m)
        mycanvas.get_tk_widget().grid(row=10,rowspan=2,column=1,columnspan=4)

if __name__ == "__main__":
    print('running gui')
    window=tk.Tk()
    gui_class(window)
    window.mainloop()
    print('done')

