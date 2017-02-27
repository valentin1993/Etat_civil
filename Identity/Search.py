#!/usr/bin/env python
# -*-coding:Latin-1 -*
""""
Module to search folders/documents in the GED
"""

import Gedurl
import zeep
import sys

#Declaration of the URL service 
Search =  Gedurl.GEDurl + '/services/Search?wsdl'
#Declaration of the client SOAP via Zeep
client = zeep.Client(wsdl=Search)

#Declaration of Search Options (Dictionary)
_search_title = {
    "caseSensitive": 1,
    "maxHits": zeep.xsd.SkipValue,
    "type": zeep.xsd.SkipValue,
    "expression": zeep.xsd.SkipValue,
    "name": zeep.xsd.SkipValue,
    "description": zeep.xsd.SkipValue,
    "topOperator": zeep.xsd.SkipValue,
    "retrieveAliases": zeep.xsd.SkipValue,
    "filterIds": zeep.xsd.SkipValue,
    "folderId": zeep.xsd.SkipValue,
    "searchInSubPath": zeep.xsd.SkipValue,
    "expressionLanguage": zeep.xsd.SkipValue,
    "sizeMin": zeep.xsd.SkipValue,
    "sizeMax": zeep.xsd.SkipValue,
    "format": zeep.xsd.SkipValue,
    "fields": ["title"],
    "language": "fr",
    "dateForm": zeep.xsd.SkipValue,
    "dateTo": zeep.xsd.SkipValue,
    "creationForm": zeep.xsd.SkipValue,
    "creationTo": zeep.xsd.SkipValue,
    "template": zeep.xsd.SkipValue
}

#Function to search a document by expression and in specific folder (if necessary)
def find(sid, **parameters):
    """Function to search a document by expression. Need the SID, the 'expression'. Others parameters are optionnal"""
    
    _search_title.update(parameters)
    return client.service.find(sid, _search_title)

#Function to search a folder by its name
def find_folder(sid, foldername):
    """Function to search a folder by its name. Need the SID and the name of the folder"""
    
    return client.service.findFolders(sid, foldername)

#Function to search a file by its name
def find_doc(sid, filename):
    """Function to search a file by its name. Need the SID and the name of the file"""
    
    return client.service.findByFilename(sid, filename)