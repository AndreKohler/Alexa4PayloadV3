'''
Created on 29.12.2018

@author: akohler
'''
import os
import sys
from argparse import Namespace
import logging
from datetime import datetime,timedelta
from .device import AlexaDevices, AlexaDevice
import json



def CreateStreamSettings(myItemConf):
    myRetVal = []
    for k,v in myItemConf.camera_setting.items():
        myRetVal.append(v)
    return myRetVal

def CreateStreamPayLoad(myItemConf):
    now = datetime.now()
    offset = timedelta(seconds=180)
    now = now + offset
    now = now.isoformat()
    expirationDate = now[0:22]+'Z'
    cameraStream = []
    cameraUri = []
 
    imageuri = myItemConf.camera_imageUri
    if myItemConf.alexa_auth_cred != '':
            imageuri = imageuri.replace("//","//"+myItemConf.alexa_auth_cred+"@")

    for k,v in myItemConf.camera_uri.items():
        cameraUri.append(v)
    
    i=0
    for k,v in myItemConf.camera_setting.items():
        if myItemConf.alexa_auth_cred != '':
            uri = v['protocols'][0].lower()+"://"+myItemConf.alexa_auth_cred+'@'+cameraUri[i]
        else:
            uri = v['protocols'][0].lower()+"://"+cameraUri[i]
        # Find highest resolution
        streamResolution = {}
        highestRes = 0
        for res in v['resolutions']:
            test = res['width']
            if res['width'] > highestRes:
                streamResolution = res
                highestRes = res['width']
            
        
        myStream= {
                     "uri":uri,
                     "expirationTime":  expirationDate,
                     "idleTimeoutSeconds": 30,
                     "protocol": v['protocols'][0].upper(),
                     "resolution":streamResolution,
                     "authorizationType": v['authorizationTypes'][0].upper(),
                     "videoCodec": v['videoCodecs'][0].upper(),
                     "audioCodec": v['audioCodecs'][0].upper()
                  }
        cameraStream.append(myStream)
        i +=1
    response = {"cameraStreams": cameraStream}
    response.update({ "imageUri":imageuri})
    return response

def DumpStreamInfo(directive):
    myFile = open("streamdump.txt","a+")
    myString=json.dumps(directive)
    
    
    myFile.write(myString+"\r\n")
    myFile.write("=====================\r\n")
    myFile.close()
    
