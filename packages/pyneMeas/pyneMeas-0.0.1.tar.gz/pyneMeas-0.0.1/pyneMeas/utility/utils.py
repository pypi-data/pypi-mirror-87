# -*- coding: utf-8 -*-
"""
VERSION 4.0
@author: Jakob Seidl
jakob.seidl@nanoelectronics.physics.unsw.edu.au
"""

import tkinter as tk
from tkinter.filedialog import asksaveasfilename, askdirectory

import json
import numpy as np
import matplotlib


def array(start,target,stepsize,upDown = False):
    
    sign = 1 if (target>start) else -1
    sweepArray = np.arange(start,target+sign*stepsize,sign*stepsize)
    if upDown:
        sweepArrayBack = np.arange(target,start+-sign*stepsize,-sign*stepsize)
        sweepArray = np.concatenate((sweepArray,sweepArrayBack))
    return sweepArray

def targetArray(targetList,stepsize):
    arrayList = []
    for index, item in enumerate(targetList):

        if index == 0:
             pass
        elif index == 1:
            arrayList.append(array(targetList[index - 1], targetList[index], stepsize))
        elif (index > 1):
            arrayList.append(array(targetList[index-1],targetList[index],stepsize)[1:]) #in order to avoid doublicating numbers
    return np.concatenate((arrayList))

def fileDialog(initAd = "/"):
    root = tk.Tk()
    #root.lift()
    root.attributes('-topmost','true')   
    root.withdraw()
    fullPath = asksaveasfilename(initialdir = initAd)
    a = ''.join(fullPath).rfind("/")
    basePath = fullPath[0:a+1]
    fileName = fullPath[a+1:]
    return [basePath,fileName]


def sendEmail(targetAddress, measurementName):
    """
    Sends and email from our group's shared account. Users that are not in our group will find these credentials empty. They need to be populated before the email can be sent.

    """
    import smtplib
    sent_from = 'Christopher.PyNE@nanoelectronics.physics.unsw.edu.au'
    password = 'p00dles18'
    subject = 'Measurement finished'
    body = 'Eureka, your measurement >>>' + measurementName + '<<< has just finished!'
    email_text = """\  
    From: %s  
    To: %s  
    Subject: %s

    %s
    """ % (sent_from, targetAddress, subject, body)
    mail = smtplib.SMTP('smtp.gmail.com:587')  # or 587
    mail.ehlo()
    mail.starttls()
    mail.login(sent_from, password)
    mail.sendmail(sent_from, targetAddress, email_text)
    print('Email sent to: ' + targetAddress)
    mail.close()