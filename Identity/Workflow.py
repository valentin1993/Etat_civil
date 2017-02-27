#!/usr/bin/env python
# -*-coding:Latin-1 -*
""""
Module to manipulate documents in the GED
"""

import Gedurl
import zeep
import sys

#Declaration of the URL service 
Workflow =  Gedurl.GEDurl + '/services/Workflow?wsdl'
#Declaration of the client SOAP via Zeep
client = zeep.Client(wsdl=Workflow)

def workflow(sid, docids):

    tag = zeep.xsd.SkipValue
    return client.service.startWorkflow(sid, "etat-civil", tag, docids)