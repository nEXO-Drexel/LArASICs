# Ahoy!
Here's some information about the code in this directory. This code is branched from https://github.com/sgaobnl/CE_LD.git at the nEXO branch in April 2024; I took the necessary code used for communicating with the SBND FEMB and ProtoDUNE WIB and based WIB_script1.py on top_on.py.


# Here are some directions to get you started with this code
## Set the path to save data
Edit setdatadir.py to assign the directory, the rundate is simply for descriptive documentation.
```
savedir = "/path/to/where/you/want/to/save/the/data/"+rundate="/"
```
## Use WIB_script1 for operation
WIB_script1 contains reg_settings_dict, which will allow easy modifications to the ASIC and test pulse settings, and some other identifiers for the femb number, femb slot number, testing environment, etc. It then runs through a process similar to top_on.py by turning on the femb, sending test pulses, checking for errors, and turning off the femb. It will output 2 binary files and one pdf of test results.
```
python3 WIB_script1.py
```

## WIB_script2
I used this one to try to figure out how to take data more directly. Didn't finish that yet

## WIB_script3 
I used this one for testing the single-WIB stands. It was easy to change the WIB and FEMB number to quickly check for connections. Also worked with the WIB's with firmware version 0x119. 

# Using the GUI
Use the script gui4.py for now. I will rename it something better later. To see the development and changes, see the other gui scripts in rough/ . 
## Gui4.py
```
python3 Gui4.py
```
