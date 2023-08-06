"""
This module reads, supplies and updates the current 'measurement ID', a running number on each setup.
A two letter identifier of each setup, e.g., AT for Attocube, Pr for probe station, He for Heliox  etc. is also saved in this file.
Both are read in the sweep function sweepAndSave() each time a measurement is done.
"""
# This has to be set every time pyNe is installed on a new system. It denotes the path where the unique number is saved.
import platform
import os
# preFix = {'Darwin':'', # THis just gives the right prefix for MAc ('Darwin' and Windows)
#           'Windows':'../'}

relPath = os.path.realpath(__file__)[:-15]
IDpath =  relPath + 'GlobalMeasIDBinary'



# >>>>>>>>>>>>>>>>>>>>>>> Name of the current measurement setup. Used as a prefix for each measurement <<<<<<<<<<<<<<<<<<<<

currentSetup = "At"

# >>>>>>>>>>>>>>>>>>>>>>> Name of the current measurement setup. Used as a prefix for each measurement <<<<<<<<<<<<<<<<<<<<

def readCurrentID():
        IDTXT =open(IDpath,"r")
        ID = int(IDTXT.read())
        IDTXT.close()
        return(ID) 
    
def increaseID():
        ID = readCurrentID()
        IDTXT =open(IDpath,"w")
        IDTXT.write(str(ID+1))
        IDTXT.close()
def readCurrentSetup():
    return currentSetup
        
def init():
    """Creates a new ID file at the path specified in variable 'Idpath'. Should only be called if the ID file was deleted etc. """
    IDTXT =open(IDpath,"w")
    IDTXT.write(str(0))
    IDTXT.close()
    
