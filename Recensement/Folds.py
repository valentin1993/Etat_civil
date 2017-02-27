#!/usr/bin/env python
# -*-coding:Latin-1 -*
""""
Module to manipulate folders in the GED
"""

import Gedurl
import zeep
import sys

#Declaration of the URL service 
Folder =  Gedurl.GEDurl + '/services/Folder?wsdl'
#Declaration of the client SOAP via Zeep
client = zeep.Client(wsdl=Folder)

#Declaration of folder properties (Dictionary)
_folder = {
    "id": zeep.xsd.SkipValue,
    "name": zeep.xsd.SkipValue,
    "parendId": zeep.xsd.SkipValue,
    "description": zeep.xsd.SkipValue,
    "lastModified": zeep.xsd.SkipValue,
    "type": zeep.xsd.SkipValue,
    "templateId": zeep.xsd.SkipValue,
    "templateLocked": zeep.xsd.SkipValue,
    "creation": zeep.xsd.SkipValue,
    "creator": zeep.xsd.SkipValue,
    "position": zeep.xsd.SkipValue,
    "hidden": 0,
    "foldRef": zeep.xsd.SkipValue,
    "attributes": zeep.xsd.SkipValue,
    "storage": zeep.xsd.SkipValue,
    "tags": zeep.xsd.SkipValue
}

#Function to create a new folder in specific folder/workspace
def create(sid, **parameters):
    """Function to create a new folder in specific folder/workspace. Need the SID, the 'name' of the folder and the 'parentId' of the folder.
        Others parameters are optionnal"""
    
    _folder.update(parameters)
    return client.service.create(sid, _folder)

#Function to delete a specific folder
def delete(sid, folderid):
    """Function to delete a specific folder. Need the SID and the id of the folder"""
    
    client.service.delete(sid, folderid)

#Function to list the workspace
def list_workspace(sid):
    """Function to have the list of the workspace. Need SID"""
    
    return client.service.listWorkspace(sid)

#Function to list the child folder
def list_folder(sid, folderid):
    """Function to have the list of folders for a specific folder/workspace. Need SID and the id of the folder"""
    
    return client.service.listChildren(sid, folderid)