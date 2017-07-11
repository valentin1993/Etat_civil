#!/usr/bin/env python
# -*-coding:Latin-1 -*
""""
Module to manipulate documents in the GED
"""

import Gedurl
import zeep
import sys
import Buffer
import Logger
import Workflow
import time

#Declaration of the URL service 
Document =  Gedurl.GEDurl + '/services/Document?wsdl'
#Declaration of the client SOAP via Zeep
client = zeep.Client(wsdl=Document)

#Declaration of document properties (Dictionary)
_document = {
    "id": zeep.xsd.SkipValue,
    "fileSize": zeep.xsd.SkipValue,
    "status": zeep.xsd.SkipValue,
    "exportStatus": zeep.xsd.SkipValue,
    "title": zeep.xsd.SkipValue,
    "version": zeep.xsd.SkipValue,
    "exportVersion": zeep.xsd.SkipValue,
    "fileVersion": zeep.xsd.SkipValue,
    "date": zeep.xsd.SkipValue,
    "publisher": zeep.xsd.SkipValue,
    "publisherId": zeep.xsd.SkipValue,
    "creator": zeep.xsd.SkipValue,
    "creatorId": zeep.xsd.SkipValue,
    "type": zeep.xsd.SkipValue,
    "lockUserId": zeep.xsd.SkipValue,
    "creation": zeep.xsd.SkipValue,
    "fileName": zeep.xsd.SkipValue,
    "indexed": zeep.xsd.SkipValue,
    "signed": zeep.xsd.SkipValue,
    "stamped": zeep.xsd.SkipValue,
    "tags": zeep.xsd.SkipValue,
    "folderId": zeep.xsd.SkipValue,
    "templateId": zeep.xsd.SkipValue,
    "customId": zeep.xsd.SkipValue,
    "immutable": zeep.xsd.SkipValue,
    "digest": zeep.xsd.SkipValue,
    "exportName": zeep.xsd.SkipValue,
    "exportId": zeep.xsd.SkipValue,
    "docRef": zeep.xsd.SkipValue,
    "docRefType": zeep.xsd.SkipValue,
    "deleteUserId": zeep.xsd.SkipValue,
    "attributes": zeep.xsd.SkipValue,
    "language": "fr",
    "summary": zeep.xsd.SkipValue,
    "score": zeep.xsd.SkipValue,
    "icon": zeep.xsd.SkipValue,
    "path": zeep.xsd.SkipValue,
    "comment": zeep.xsd.SkipValue,
    "lastModified": zeep.xsd.SkipValue,
    "rating": zeep.xsd.SkipValue,
    "workflowStatus": zeep.xsd.SkipValue,
    "published": 1,
    "startPublishing": zeep.xsd.SkipValue,
    "stopPublishing": zeep.xsd.SkipValue,
    "pages": zeep.xsd.SkipValue,
    "nature": zeep.xsd.SkipValue,
    "formId": zeep.xsd.SkipValue
}


#Function to create a new document
def create(path, sid, **parameters):
    """Function to create a new document. Need the path of local document, the SID, the 'fileName' of document (with extension) and the 'folderId'.
        Others parameters are optionnal"""

    _document.update(parameters)
    doc = client.service.create(sid, _document, Buffer.reader(path))

    # Workflow.workflow(sid, [doc['id']])

    time.sleep(3)

    client.service.reindex(sid, doc['id'], None) 

    return doc


#Function to update a document
def upload(path, sid, fileid, filename):
    """Function to update an existing file. Need the path of the local document, the SID and the 'id' of the document. Others parameters are optionnal"""
    
    rien = zeep.xsd.SkipValue
    doc = client.service.upload(sid, fileid, rien, False, filename, "fr", Buffer.reader(path))

    # Workflow.workflow(sid, [fileid])

    #time.sleep(3)

    #client.service.reindex(sid, fileid, None) 
    
    return doc


#Function to list the documents of a specific folder
def list_doc(sid, folderid):
    """Function to have the list of documents for a specific folder. Need the id of the folder"""
    
    return client.service.listDocuments(sid, folderid, None)

#Function to delete the specific docuement
def delete(sid, fileid):
    """Function to delete the specific document. Need the id of the document"""
    
    client.service.delete(sid, fileid)