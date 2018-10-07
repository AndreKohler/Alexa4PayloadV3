'''
Created on 23.06.2018

@author: akohler
'''
import os
import sys
import uuid
from datetime import datetime





from .action import alexa

DEFAULT_RANGE = (0, 100)
DEFAULT_RANGE_LOGIC = (True, False)

def what_percentage(value, range):
    _min, _max = range
    return ( (value - _min) / (_max - _min) ) * 100

def calc_percentage(percent, range):
    _min, _max = range
    return (_max - _min) * (percent / 100) + _min

def clamp_percentage(percent, range):
    _min, _max = range
    return min(_max, max(_min, percent))
    #pydevd.settrace("192.168.178.37", port=5678)

#======================================================
# Start - A.Kohler
#P3 - Directives
#======================================================


# Alexa PowerController

@alexa('TurnOn', 'TurnOn', 'powerState','Alexa.PowerController')
def TurnOn(self, directive):
    device_id = directive['endpoint']['endpointId']
    items = self.items(device_id)
    #pydevd.settrace("192.168.178.37", port=5678)
    for item in items:
        on, off = self.item_range(item, DEFAULT_RANGE_LOGIC)
        self.logger.info("Alexa: turnOn({}, {})".format(item.id(), on))
        if on != None:
            item( on )
            self.response_Value = 'ON'
    myValue = self.p3_respond(directive)
    return myValue

@alexa('TurnOff', 'TurnOff', 'powerState','Alexa.PowerController')
def TurnOff(self, directive):
    device_id = directive['endpoint']['endpointId']
    items = self.items(device_id)

    for item in items:
        on, off = self.item_range(item, DEFAULT_RANGE_LOGIC)
        self.logger.info("Alexa: turnOff({}, {})".format(item.id(), off))
        if off != None:
            item( off )
            self.response_Value = 'OFF'
    return self.p3_respond(directive)


# Alexa-Doorlock Controller

@alexa('Lock', 'Lock', 'LockConfirmation','Alexa.LockController')
def Lock(self, directive):
    device_id = directive['endpoint']['endpointId']
    items = self.items(device_id)

    for item in items:
        on, off = self.item_range(item, DEFAULT_RANGE_LOGIC)
        self.logger.info("Alexa: Lock({}, {})".format(item.id(), on))
        if on != None:
            item( on )
            self.response_Value = None
            self.response_Value = 'LOCKED'
    
    return self.p3_respond(directive)

@alexa('Unlock', 'Unlock', 'UnlockConfirmation','Alexa.LockController')
def Unlock(self, directive):
    device_id = directive['endpoint']['endpointId']
    items = self.items(device_id)

    for item in items:
        on, off = self.item_range(item, DEFAULT_RANGE_LOGIC)
        self.logger.info("Alexa: Unlock({}, {})".format(item.id(), off))
        if off != None:
            item( off )
            self.response_Value = None
            self.response_Value = 'UNLOCKED'
    
    return self.p3_respond(directive)


# Alexa-Brightness-Controller 

@alexa('AdjustBrightness', 'AdjustBrightness', 'brightness','Alexa.BrightnessController')
def AdjustBrightness(self, directive):
    #pydevd.settrace("192.168.178.37", port=5678)
    device_id = directive['endpoint']['endpointId']
    items = self.items(device_id)
    
    percentage_delta = float( directive['payload']['brightnessDelta'] )

    for item in items:
        item_range = self.item_range(item, DEFAULT_RANGE)
        item_now = item()
        percentage_now = what_percentage(item_now, item_range)
        percentage_new = clamp_percentage(percentage_now + percentage_delta, item_range)
        item_new = calc_percentage(percentage_new, item_range)
        self.logger.info("Alexa P3: AdjustBrightness({}, {:.1f})".format(item.id(), item_new))
        item( item_new )
        self.response_Value = None
        self.response_Value = int(percentage_new)
    
    return self.p3_respond(directive)

@alexa('SetBrightness', 'SetBrightness', 'brightness','Alexa.BrightnessController')
def SetBrightness(self, directive):
    #pydevd.settrace("192.168.178.37", port=5678)
    device_id = directive['endpoint']['endpointId']
    items = self.items(device_id)
    new_percentage = float( directive['payload']['brightness'] )

    for item in items:
        item_range = self.item_range(item, DEFAULT_RANGE)
        item_new = calc_percentage(new_percentage, item_range)
        self.logger.info("Alexa P3: SetBrightness({}, {:.1f})".format(item.id(), item_new))
        item( item_new )
        self.response_Value = None
        self.response_Value = int(new_percentage)

    return self.p3_respond(directive)



# Alexa-Percentage-Controller

@alexa('AdjustPercentage', 'AdjustPercentage', 'percentage','Alexa.PercentageController')
def AdjustPercentage(self, directive):
    #pydevd.settrace("192.168.178.37", port=5678)
    device_id = directive['endpoint']['endpointId']
    items = self.items(device_id)
    
    percentage_delta = float( directive['payload']['percentageDelta'] )

    for item in items:
        item_range = self.item_range(item, DEFAULT_RANGE)
        item_now = item()
        percentage_now = what_percentage(item_now, item_range)
        percentage_new = clamp_percentage(percentage_now + percentage_delta, item_range)
        item_new = calc_percentage(percentage_new, item_range)
        self.logger.info("Alexa P3: AdjustPercentage({}, {:.1f})".format(item.id(), item_new))
        item( item_new )
        self.response_Value = None
        self.response_Value = int(new_percentage)
    
    return self.p3_respond(directive)
    
@alexa('SetPercentage', 'SetPercentage', 'percentage','Alexa.PercentageController')
def SetPercentage(self, directive):
    #pydevd.settrace("192.168.178.37", port=5678)
    device_id = directive['endpoint']['endpointId']
    items = self.items(device_id)
    new_percentage = float( directive['payload']['percentage'] )

    for item in items:
        item_range = self.item_range(item, DEFAULT_RANGE)
        item_new = calc_percentage(new_percentage, item_range)
        self.logger.info("Alexa P3: SetPercentage({}, {:.1f})".format(item.id(), item_new))
        item( item_new )
        self.response_Value = None
        self.response_Value = int(new_percentage)
    
    return self.p3_respond(directive)


#======================================================
# Ende - A.Kohler
#======================================================
