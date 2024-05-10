# Ahoy!
Here's some information about the code in this directory. This code is branched from https://github.com/sgaobnl/CE_LD.git at the nEXO branch in April 2024; I took the necessary code used for communicating with the SBND FEMB and ProtoDUNE WIB and based WIB_script1.py on top_on.py.


# Here are some directions to get started with this code
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

