#!/usr/bin/env python
# -*-coding:Latin-1 -*
""""
Module to manipulate documents in the GED
"""

import Gedurl
import zeep
import sys

#Declaration of the URL service 
EnterSearch =  Gedurl.GEDurl + '/services/EnterpriseSearch?wsdl'
#Declaration of the client SOAP via Zeep
client = zeep.Client(wsdl=EnterSearch)

_criterion= {
    "field": zeep.xsd.SkipValue,
    "composition": zeep.xsd.SkipValue,
    "operator": zeep.xsd.SkipValue,
    "stringValue": zeep.xsd.SkipValue,
    "dateValue": zeep.xsd.SkipValue,
    "intValue": zeep.xsd.SkipValue,
    "doubleValue": zeep.xsd.SkipValue,
    "extendedAttribue": zeep.xsd.SkipValue,
    "type": zeep.xsd.SkipValue   
}

def find_parameters(sid, title):

    rien = zeep.xsd.SkipValue    
    _criterion.update({'field': 'title', 'operator': "contains", 'stringValue': title,'type': 0, 'extendedAttribute': 0})

    return client.service.findByParameters(sid, rien, [_criterion], 1)