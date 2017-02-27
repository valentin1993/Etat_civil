#!/usr/bin/env python
# -*-coding:Latin-1 -*
""""
Module to login and logout users to the GED
"""

import Gedurl
import zeep
import sys

#Declaration of the URL service 
Auth =  Gedurl.GEDurl + '/services/Auth?wsdl'
#Declaration of the client SOAP via Zeep
client = zeep.Client(wsdl=Auth)

#Connect the user and return the SID (string)
def login(username="", password=""):
    """Function to connect user to the GED with his username and password, return the user's SID (string)"""
    
    return client.service.login(username, password)

#Disconnect the user via SID
def logout(sid=""):
    """Function to disconnect user to the GED with his SID""" 
    
    client.service.logout(sid)