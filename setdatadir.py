# -*- coding: utf-8 -*-
"""
File Name: setdatadir.py
Author: GSS/beckert
Mail: gao.hillhill@gmail.com/be348@drexel.edu
Description: Use to set the directory to save the data = savedir
This doesnt seem very necessaty since it could be set in 3 lines in a script
Created Time: 3/20/2019 4:50:34 PM GSS/gao.hillhill@gmail.com
Last modified: 2024 Jul 12
"""
from datetime import datetime
rundate = datetime.now().strftime('%Y_%m_%d')
savedir = "/Users/be348/nexoStuff/LArASIC/code/data/SingleWIBStands/"+rundate+"/P26/"

