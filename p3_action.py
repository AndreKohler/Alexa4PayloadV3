'''
Created on 23.06.2018

@author: akohler
'''
import os
import sys
import uuid
from datetime import datetime
from hpmudext import get_device_id






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

DEFAULT_TEMP_RANGE = (16, 26)

def clamp_temp(temp, range):
    _min, _max = range
    return min(_max, max(_min, temp))


#======================================================
# Start - A.Kohler
# P3 - Directives
#======================================================
# Alexa ThermostatController

@alexa('SetThermostatMode', 'SetThermostatMode', 'thermostatMode','Alexa.ThermostatController',['SetTargetTemperature'])
def SetThermostatMode(self, directive):
    # define Mode-Lists
    device_id = directive['endpoint']['endpointId']
    items = self.items(device_id)
    
    AlexaItem = self.devices.get(device_id)
    myModes = AlexaItem.thermo_config
    myValueList = self.GenerateThermoList(myModes,1)
    myModeList = self.GenerateThermoList(myModes,2)
    
    # End of Modes-List
    
    
    new_Mode = directive['payload']['thermostatMode']['value'] 
    
    
    
    item_new = myModeList[new_Mode]
    for item in items:
        self.logger.info("Alexa: SetThermostatMode({}, {})".format(item.id(), item_new))
        item( item_new )
    
    #new_temp = items[0]() if items else 0
    
    self.response_Value = new_Mode
    myValue = self.p3_respond(directive)
    return myValue

@alexa('AdjustTargetTemperature', 'AdjustTargetTemperature', 'targetSetpoint','Alexa.ThermostatController',['SetThermostatMode'])
def AdjustTargetTemperature(self, directive):
    device_id = directive['endpoint']['endpointId']
    items = self.items(device_id)

    delta_temp = float( directive['payload']['targetSetpointDelta']['value'] )
    previous_temp = items[0]() if items else 0

    for item in items:
        item_range = self.item_range(item, DEFAULT_TEMP_RANGE)
        item_new = clamp_temp(previous_temp + delta_temp, item_range)
        self.logger.info("Alexa: AdjustTargetTemperature({}, {:.1f})".format(item.id(), item_new))
        item( item_new )

    new_temp = items[0]() if items else 0
    
    self.response_Value = None
    self.response_Value = {
                           "value": new_temp,
                           "scale": "CELSIUS"
                          }
    myValue = self.p3_respond(directive)
    return myValue
  
@alexa('SetTargetTemperature', 'SetTargetTemperature', 'targetSetpoint','Alexa.ThermostatController',['SetThermostatMode'])
def SetTargetTemperature(self, directive):
    device_id = directive['endpoint']['endpointId']
    items = self.items(device_id)

    target_temp = float( directive['payload']['targetSetpoint']['value'] )
    previous_temp = items[0]() if items else 0

    for item in items:
        item_range = self.item_range(item, DEFAULT_TEMP_RANGE)
        item_new = clamp_temp(target_temp, item_range)
        self.logger.info("Alexa: SetTargetTemperature({}, {:.1f})".format(item.id(), item_new))
        item( item_new )

    new_temp = items[0]() if items else 0
    
    self.response_Value = None
    self.response_Value = {
                           "value": new_temp,
                           "scale": "CELSIUS"
                          }
    myValue = self.p3_respond(directive)
    return myValue
  


# Alexa PowerController

@alexa('TurnOn', 'TurnOn', 'powerState','Alexa.PowerController',[])
def TurnOn(self, directive):
    device_id = directive['endpoint']['endpointId']
    items = self.items(device_id)

    for item in items:
        on, off = self.item_range(item, DEFAULT_RANGE_LOGIC)
        self.logger.info("Alexa: turnOn({}, {})".format(item.id(), on))
        if on != None:
            item( on )
            self.response_Value = 'ON'
    myValue = self.p3_respond(directive)
    return myValue

@alexa('TurnOff', 'TurnOff', 'powerState','Alexa.PowerController',[])
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

@alexa('Lock', 'Lock', 'LockConfirmation','Alexa.LockController',[])
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

@alexa('Unlock', 'Unlock', 'UnlockConfirmation','Alexa.LockController',[])
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

@alexa('AdjustBrightness', 'AdjustBrightness', 'brightness','Alexa.BrightnessController',[])
def AdjustBrightness(self, directive):
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

@alexa('SetBrightness', 'SetBrightness', 'brightness','Alexa.BrightnessController',[])
def SetBrightness(self, directive):
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

@alexa('AdjustPercentage', 'AdjustPercentage', 'percentage','Alexa.PercentageController',[])
def AdjustPercentage(self, directive):
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
    
@alexa('SetPercentage', 'SetPercentage', 'percentage','Alexa.PercentageController',[])
def SetPercentage(self, directive):
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

# Scene Controller

@alexa('Activate', 'Activate', 'ActivationStarted','Alexa.SceneController',[])
def Activate(self, directive):
    device_id = directive['endpoint']['endpointId']
    items = self.items(device_id)
    new_percentage = float( directive['payload']['percentage'] )

    for item in items:
        on, off = self.item_range(item, DEFAULT_RANGE_LOGIC)
        item_new = on                           # Should be the No. of the Scene
        self.logger.info("Alexa P3: Activate Scene ({}, {})".format(item.id(), item_new))
        item( item_new )
        self.response_Value = None
        self.response_Value = item_new
    
    return self.p3_respond(directive)


#======================================================
# No directives only Responses for Reportstate
#======================================================
@alexa('ReportTemperatur', 'ReportTemperatur', 'temperature','Alexa.TemperatureSensor',[])
def ReportTemperatur(self, directive):
    print ("")
#======================================================
# Ende - A.Kohler
#======================================================

