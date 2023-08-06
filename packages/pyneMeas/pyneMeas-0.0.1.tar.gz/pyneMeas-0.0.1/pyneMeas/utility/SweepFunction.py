"""
VERSION 4.0
@author: Jakob Seidl
jakob.seidl@nanoelectronics.physics.unsw.edu.au
"""
from collections import Iterable
import json
from pyneMeas.utility import GlobalMeasID as ID
import pyneMeas.Instruments.Instrument as Instrument
import numpy as np
import scipy.io as sio
import time
import os
import pandas as pd
from itertools import product
import matplotlib as mpl
import matplotlib.pyplot as plt
import warnings


# Specify plotting options:
#Plot style presets: e.g, 'fivethirtyeight' or 'ggplot'. More examples -> https://matplotlib.org/3.3.3/gallery/style_sheets/style_sheets_reference.html
plt.style.use('seaborn')
mpl.rcParams['axes.linewidth'] = 1.0    #  boxplot linewidth
mpl.rcParams.update({'font.size': 11})  #  fontsize
########################################



mpl.use('TkAgg') #This should be the default on windows I think, but on my mac it isnt
 #used to suppress the annoying matplotlib warning about singular axes
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib") #used to suppress the annoying matplotlib warning about singular axes.


# For each input point:
# 1. Sets the instruments to the input point by calling the inputSetters with the point
# 2. Calls each outputReaders to get the output point
# 3. Calls outputReceiver with the point
# After all input points have been processed, outputFinisher is called
# 

def sweepAndSave(
                 inputDict,
                 extraInstruments = [],
                 saveEnable = True,
                 delay = 0.0,
                 plotParams = None,
                 plotString  = ['og','ob'], #linePlot: symbol (-; -- or o,s,^,>   plus a colour: 'r' red, 'g' green etc.
                 comments = "No comments provided by user",
                 saveCounter = 10,
                 breakCondition = None,
                 outputReceiver = None):

    """sweepAndSave is the main function of this module and THE sweepfunction. It is the only function that the user actually calls himlself
    - all other functions provided here all called 'under the hood by sweepAndsave'. It can be subdivided into three parts:
    (1): Initialize: Check if user input is valid, create data and log files on disk and set up the plot object. All this is done ONCE ONLY.
    (2): sweep() function which calls receiver() within: LOOP Section: This is the actual sweep,
    i.e., iterative process carried out over every single datapoint in the inputArray. This is: (I) set setter Instr to inputArray point, then Query all meas instruments,
    (II) append data to files and plots and (III) every N-th iteration (default =10), force the file to be written on disk.
    (3): Wrap-up: Write the final instrument parameters and data to file, save the plot as .png, close all file connections (good practice!)"""
    def unpackInputDict(inputDict):
        keyList = ['basePath','fileName','inputHeaders','sweepArray',
                   'inputSetters','outputHeaders','outputReaders']
        return [inputDict[key] for key in keyList]

    basePath,fileName,inputHeaders,inputPoints, inputSetters,outputHeaders, outputReaders = unpackInputDict(inputDict)
    ######################################################################## Part(1) ########################################################################
    #########################################################################################################################################################
    #Turn input array into itertools.product if it isnt already. Since our sweepArray is usually a 1D array anyway, this is usually not necessary and is more of a relic than a feature:
    if (type(inputPoints) == product):
        pass
    elif (type(inputPoints) == list or type(inputPoints) == np.ndarray):
        inputPoints = product(inputPoints)
    else:
        pass

    #Check if the plotting parameters ('plotParams') exist in in- and outputHeaders:
    checkPlotHeaders(inputHeaders,outputHeaders,plotParams)

    if(saveEnable):
        ID.increaseID()
        fileName = str(ID.readCurrentSetup()) + str(ID.readCurrentID()) + "_" + fileName
        startTime = time.time() # Start time

        # TODO: this is slightly different for Adams version 3.1, let's see if it still works.
        # Make a copy of the initial configuration of the instruments
        instruments = set(filter(
            lambda i: issubclass(type(i), Instrument.Instrument),
            inputSetters + outputReaders + extraInstruments
        ))

        config = {}
        for instrument in instruments: #This goes through the list of all instruments and queries all options that have a associated 'get()' method. E.g., 'sourceMode' for the Keithely2401
            config["{}-{}-{}".format(instrument.get('name'),type(instrument).__name__,len(config)+1)] = instrument.getOptions()#The ['key'] for each instrument is its 'name' and its type.


        #  write the initial config to the LOG file:
        print(os.path.realpath(__file__))
        log = open(basePath+fileName +"_LOG"+ ".tsv", "w")
        log.write("Measurement Log file for measurement >>> "+ str(ID.readCurrentSetup()) + str(ID.readCurrentID())+" <<< \n")
        log.write("Starting time and date: "+time.asctime(time.localtime(time.time()))+"\n")
        log.write("\n")
        log.write("Set/sweeped variables/instruments:\n")
        log.write("Variable\tInst name\tInst type\n")
        log.write("-----------------------------------\n")
        for header,name, Insttype in zip(inputHeaders, [setter.name for setter in inputSetters], [setter.type for setter in inputSetters]):
            log.write(f"{header}\t{name}\t{Insttype}\n")

        log.write("\n")
        log.write("Measuring variables/instruments:\n")
        log.write("Variable\tInst name\tInst type\n")
        log.write("-----------------------------------\n")
        for header,name, Insttype in zip(outputHeaders, [getter.name for getter in outputReaders], [getter.type for getter in outputReaders]):
            log.write(f"{header}\t{name}\t{Insttype}\n")


        log.write("\n")
        log.write("User comments: "+str(comments) +"\n")
        log.write("-----------------------------------\n")
        log.write("Delay = "+str(delay)+"s \n")
        log.write("Initial instrument configuration\n")
        log.write("-----------------------------------\n")
        log.write(json.dumps(config, indent = 4, sort_keys = True)) #Writes all initial instrument paramters in intented Json format
        log.write("\n-----------------------------------\n")
        log.close()


        #Write data headers to plain text file :
        tsv = open(basePath + fileName + ".tsv", "w")
        tsv.write("\t".join(flatten(inputHeaders))+ "\t")
        tsv.write("\t".join(flatten(outputHeaders)) + "\n")

        # Prepare a dict for the data too. This dict will be used to write data to a .mat file which can be conveniently read by Matlab or Python
        pointsDict = {}
        for header in flatten((flatten(inputHeaders), flatten(outputHeaders))):
            pointsDict[header] = []


        ##############          Prepare Plotting: ###############

        measurementName = str(ID.readCurrentSetup()) + str(ID.readCurrentID()) # returns e.g. At104
        inputHeaders = flatten(inputHeaders);outputHeaders = flatten(outputHeaders); #Make sure we have simple lists, not lists within lists etc..

        allHeaders = inputHeaders + outputHeaders
        Xvalues1 = [];Yvalues1 = [];Xvalues2 = [];Yvalues2 = [] #Generate empty lists of X and Y Data. This is used later in the plotting routine.

        ############## Initialize the plot. Actual plotting happens within receiver() within save() ###############
        if plotParams != None and len(plotParams) == 2:  # If the user specifies one pair of plot parameters:
            allHeaders = inputHeaders + outputHeaders
            Xindex1 =  allHeaders.index(plotParams[0])
            Yindex1  = allHeaders.index(plotParams[1])

            mainFig = plt.figure(figsize=(8,8))
            ax1 = mainFig.add_subplot(111)
            line1, = ax1.plot(0,0,plotString[0])
            plt.ylabel(str(allHeaders[Yindex1]))
            plt.xlabel(str(allHeaders[Xindex1]))
            plt.title(measurementName)
            plt.show()

        if plotParams != None and len(plotParams) == 4:  # If the user specifies two pairs of plot parameters:
            Xindex1,Yindex1,Xindex2,Yindex2 = (allHeaders.index(plotParams[i])
                                               for i in range(4))

            mainFig = plt.figure(figsize=(10,8))

            ax1 = mainFig.add_subplot(211)
            plt.ylabel(str(allHeaders[Yindex1]))
            plt.xlabel(str(allHeaders[Xindex1]))
            line1, = ax1.plot(0,0,plotString[0])
            plt.title(measurementName)

            ax2 = mainFig.add_subplot(212)
            plt.ylabel(str(allHeaders[Yindex2]))
            plt.xlabel(str(allHeaders[Xindex2]))
            line2, = ax2.plot(0,0, plotString[1] if (len(plotString) == 2) else plotString[0]) # if user provides only one plotstring use first.
            plt.show()
        ############### END initialize plot ###############################




        ######################################################################## Part(2) --The loop-- ########################################################################
        #########################################################################################################################################################


        ########  The receiver() function is a sub-section of the save() function and is called for EACH point in the sweepArray.
        #It does two things: 1) Append the set of measured values (e.g. results from you SRS830 and K2401) to your measurement text file (.tsv)
            #and append it to your python dictionary of results (used for export as .mat file in the end). 2) It updates the current plot with the new data.

        ##############  Definition of receiver() ###############################
        def receiver(inputPoint, outputPoint,counter):

            checkPointMatchesHeaders(inputPoint, inputHeaders)
            checkPointMatchesHeaders(outputPoint, outputHeaders)

            for value, header in zip(flatten(inputPoint), flatten(inputHeaders)):
                pointsDict[header].append(value)
            for value, header in zip(flatten(outputPoint), flatten(outputHeaders)):
                pointsDict[header].append(value)

            tsv.write("\t".join(map(str, flatten(inputPoint))) + "\t") #takes the input points, 'flattens' the list (aka gets rid of unecessary lists in lists) turns them into strings and writes them separated by a tab \t in the tsv file.
            tsv.write("\t".join(map(str, flatten(outputPoint))) + "\n")

            #these force saving commands should probably only be executed every tenth iteration or so to speed things up.
            if counter%saveCounter == 0:
                tsv.flush()   #These two commands force the tsv file and .mat file to be saved to disk. Otherwise the file will be lost when killing the program
                os.fsync(tsv.fileno())
                sio.savemat(basePath +fileName + '.mat', pointsDict)
            #Do the actual Plotting:
            if plotParams != None and len(plotParams) ==2: # If the user specified ONE PAIR of variables he wants plotted, update those.
                points = flatten(inputPoint)+flatten(outputPoint)
                Xvalues1.append(points[Xindex1])
                Yvalues1.append(points[Yindex1])
                line1.set_ydata(Yvalues1)
                line1.set_xdata(Xvalues1)

                mainFig.canvas.draw()
                mainFig.canvas.flush_events()
#                if counter%3 ==0:
                try: #Introduced this since sometimes 'NaNs' or other chunk data may impede setting the axis limits properly
                    ax1.set_xlim(min(Xvalues1),max(Xvalues1))
                    ax1.set_ylim(min(Yvalues1),max(Yvalues1))
                except:
                    pass

            if plotParams != None and len(plotParams) ==4: # If the user specified TWO PAIRS of variables he wants plotted, update those.
                points = flatten(inputPoint)+flatten(outputPoint)

                # append the current values to the pre-existing lists of X, and Y-values
                for val, index in zip([Xvalues1,Yvalues1,Xvalues2,Yvalues2],
                                               [Xindex1,Yindex1,Xindex2,Yindex2]):
                    val.append(points[index])

                # Update the plot object with the updated x,y val lists
                line1.set_ydata(Yvalues1);line1.set_xdata(Xvalues1)
                line2.set_ydata(Yvalues2);line2.set_xdata(Xvalues2)

                # Set the x,y limits with regards to the new x,y data
                try: #Introduced this since sometimes 'NaNs' or other bad data may impede setting the axis limits properly
                    ax1.set_xlim(min(Xvalues1),max(Xvalues1));
                    ax1.set_ylim(min(Yvalues1),max(Yvalues1))
                    ax2.set_xlim(min(Xvalues2),max(Xvalues2));
                    ax2.set_ylim(min(Yvalues2),max(Yvalues2))

                except:
                    pass
                mainFig.canvas.draw() #Those two commands force the plot to actually update
                mainFig.canvas.flush_events()
                ############## END Definition of receiver() ###############################

            #if outputReceiver: #we dont really use that ever, ignore. This is a potential future interface if the user wants to do more with his data for each iteration
            #    outputReceiver(inputPoint, outputPoint)
            ##############  END Definition of receiver() ###############################   

        #sweep() does the actual sweep and calls receiver() defined just above! sweep() is defined just below, outside of the sweepAndSave() definition
        sweep(inputPoints, inputSetters, outputReaders, receiver,delay,breakCondition)






        ######################################################################## Part(3) ########################################################################
        #########################################################################################################################################################
        ###### Wrapping up the measurement: close the data.tsv file, write the final settings of all instruments in .log file,
        #save a final version of the data to .mat format and save the figure created as .png

        tsv.flush()  # These three commands force the tsv file and .mat file to be saved to disk. Otherwise the file will be lost when killing the program
        os.fsync(tsv.fileno())
        tsv.close()
        sio.savemat(basePath +fileName + '.mat', pointsDict)

        log = open(basePath +fileName +"_LOG"+ ".tsv", "a")
        log.write("Ending time and date: "+time.asctime(time.localtime(time.time()))+"\n")
        log.write("Time elapsed: "+str(time.time()-startTime)+" seconds." +"\n")
        log.write("Final instrument configuration: \n")
        log.write("-----------------------------------\n")
        log.write(json.dumps(config, indent = 4, sort_keys = True)) #Writes all the instrument parameters in indeted json format
        log.write("\n-----------------------------------\n")
        log.close()
        if plotParams != None:
            plt.savefig(basePath +fileName+'.png') #Save Plot as .png as additional feature (only if plotting parameters were specified

    elif(not saveEnable): #This elif branch is basically never executed and can be ignored. We just assume that the user wants to sav and plot his data anyway.
        sweepNoSave(inputPoints, inputSetters, outputReaders,delay,breakCondition) #This does the actual sweep (without saving)!


    return pd.DataFrame.from_dict(pointsDict)


######################################################################## END of sweepAndSave() ########################################################################
#######################################################################################################################################################################








##################################################################
def sweep(inputPoints, inputSetters, outputReaders, receiver,delay,breakCondition):
    """sweep() defines the 'actual sweep',i.e.,, we define what is done for each 'inputPoint' of the array we want to sweep over. """
    prevPoint = None
    counter = 0
#    running = True
#    if breakCondition ==None:
#        breakCondition = [outputReaders[0],-float("inf"),float("inf")]
#    print breakCondition

    # Actual loop over all points in inputArray:
    for inputPoint in inputPoints:
#            while(running): #If we wanted something like a break condition, this would be the place to put them. Not yet implemented, though.
                if len(inputPoint) != len(inputSetters):#Usually len(inputPoint) is 1 since it's a single point in a 1D array. One instrument, one value.
                    raise ValueError("Length of input point does not match length of input setters")

                #We define the 'previous' state of the sweep so we are able to
                if prevPoint == None: #For the first point of each sweep, this is the case. The setter.goTo(target) then slowly goes to the first value. This is mainly to catch user errors.
                    prevPoint = [None] * len(inputPoint) #Usually len(inputPoint) is 1 since it's a single point in a 1D array.
                    for value,setter in zip(inputPoint,inputSetters):
                        setter.goTo(value)
                #A Set source instrument
                for value, prevValue, setter in zip(inputPoint, prevPoint, inputSetters):
                    # Avoid setting a value if it is already set to it
                    if value != prevValue: #only change outputs if they are in fact different to the previous once. Saves time.
                        if callable(setter):# In principle one could directly pass a (lambda) function instead of a real instrument. Then this block is carried out.
                            setter(value)
                        else: # This is carried out when a real Instrument is passed to the SweepAndSave function, so nearly always.
                            setter.set(type(setter).defaultOutput, value)

                prevPoint = inputPoint
                #### B Reading out all instruments defined as 'outputReaders'
                time.sleep(delay) #This is the delay specified by the user, typicall 0.2s
                outputPoint = []
                for reader in outputReaders:
                    if callable(reader): # In principle one could directly pass a (lambda) function instead of a real instrument. Then this block is carried out.
                        tempRes = reader()
#                        print(tempRes)
                        outputPoint.append(tempRes)
#                        print(running)
                    else: #However, usually we provide a 'real' instrument object and the appropriate instrument.get('readVariable') is called.
                        tempRes = reader.get(type(reader).defaultInput)
                        outputPoint.append(tempRes)

                # Block below calls the receiver. In the sweepAndSave function, we define a receiver which we then hand over to the save() function called there.
                # So in normal use, this is used to plot and write the data to file. However, in principle you could pass ANY function to it and you could do other stuff with your data.
                receiver(inputPoint, outputPoint,counter)
                counter = counter+1


# sweepNoSave is not really used ever
def sweepNoSave(inputPoints, inputSetters, outputReaders,delay,breakCondition): #Since by default the 'saveEnable' option is True, this funciton is barely ever called.
    prevPoint = None
    for inputPoint in inputPoints:
        if len(inputPoint) != len(inputSetters):
            raise ValueError("Length of input point does not match length of input setters")

        #We define the 'previous' state of the sweep so we are able to only change outputs if they are in fact different to the previous once. Saves time.
        if prevPoint == None: #For the first point of each sweep, this is the case.
            prevPoint = [None] * len(inputPoint) #Usually len(inputPoint) is 1 since it's a single point in a 1D array.

        for value, prevValue, setter in zip(inputPoint, prevPoint, inputSetters):
            # Avoid setting a value if it is already set to it
            if value != prevValue:
                if callable(setter):
                    setter(value)
                else:
                    setter.set(type(setter).defaultOutput, value)
        prevPoint = inputPoint

        time.sleep(delay)
        outputPoint = []
        for reader in outputReaders:
            if callable(reader):
                outputPoint.append(reader())
            else:
                outputPoint.append(reader.get(type(reader).defaultInput))

#################################### From here on unimportant and helper functions ################
###################################################################################################

#Helper functions from here on:

# Checks if val is iterable, but not a string
def isIterable(val):
    return isinstance(val, Iterable) and not isinstance(val, str)

# Flattens a list: [[1, 2, 3], 4, [5], [6, 7]] => [1, 2, 3, 4, 5, 6, 7]
def flatten(iterable):
    flattenedList = []
    for e1 in iterable:
        if isIterable(e1):
            for e2 in e1:
                flattenedList.append(e2)
        else:
            flattenedList.append(e1)
    return flattenedList

def checkPointMatchesHeaders(point, headers): # I added heaps of flatten() in here in order to prevent weird errors where there shouldnt be any.
    if len(flatten(point)) != len(flatten(headers)):
        raise ValueError("Point {} does not have same length as header {}".format(flatten(point), flatten(headers)))

    for value, header in zip(flatten(point), flatten(headers)):
        if isIterable(header) and isIterable(value):
            if len(flatten(header)) != len(flatten(value)):
                raise ValueError("Point {} does not have same length as header {}".format(flatten(point), flatten(headers)))
        elif not isIterable(header) and not isIterable(value):
            pass
        else:
            raise ValueError("Point {} does not have same length as header {}".format(flatten(point), flatten(headers)))

def checkPlotHeaders(inputHeaders,outputHeaders,plotParams):
    if plotParams == None:
        return
    if (len(plotParams) ==2 and plotParams[0] in (flatten(inputHeaders)+flatten(outputHeaders)) and plotParams[1] in (flatten(inputHeaders)+flatten(outputHeaders))):
        return 1
    elif (len(plotParams) ==4 and plotParams[0] in (flatten(inputHeaders)+flatten(outputHeaders)) and plotParams[1] in (flatten(inputHeaders)+flatten(outputHeaders)) and plotParams[2] in (flatten(inputHeaders)+flatten(outputHeaders)) and plotParams[3] in (flatten(inputHeaders)+flatten(outputHeaders))):
        return 2
    else:
        raise ValueError("{} does either not have the right format (either two or 4 parameters) or one of the given values is not found in input or output Headers".format(plotParams))


