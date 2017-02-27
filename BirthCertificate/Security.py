#!/usr/bin/env python
# -*-coding:Latin-1 -*
""""
Module to modify the users and groups in the GED
"""

import Gedurl
import zeep
import sys

#Declaration of the URL service 
Security =  Gedurl.GEDurl + '/services/Security?wsdl'
#Declaration of the client SOAP via Zeep
client = zeep.Client(wsdl=Security)

#Declaration of the user parameters (Dictionary)
_user = {
    "id": zeep.xsd.SkipValue,
    "username": zeep.xsd.SkipValue,
    "password": zeep.xsd.SkipValue,
    "passwordmd4": zeep.xsd.SkipValue,
    "name": zeep.xsd.SkipValue,
    "firstName": zeep.xsd.SkipValue,
    "street": zeep.xsd.SkipValue,
    "postalCode": zeep.xsd.SkipValue,
    "city": zeep.xsd.SkipValue,
    "country": zeep.xsd.SkipValue,
    "state": zeep.xsd.SkipValue,
    "language": "fr",
    "email": zeep.xsd.SkipValue,
    "emailSignature": zeep.xsd.SkipValue,
    "email2": zeep.xsd.SkipValue,
    "emailSignature2": zeep.xsd.SkipValue,
    "telephone": zeep.xsd.SkipValue,
    "telephone2": zeep.xsd.SkipValue,
    "type": 0,
    "groupIds": zeep.xsd.SkipValue,
    "enabled": 1,
    "passwordChanged": zeep.xsd.SkipValue,
    "passwordExpires": zeep.xsd.SkipValue,
    "source": 0,
    "quota": -1,
    "quotaCount": zeep.xsd.SkipValue,
    "lastModified": zeep.xsd.SkipValue
}

#Decalration of the group parameters (Dictionary)
_group = {
    "id": zeep.xsd.SkipValue,
    "name": zeep.xsd.SkipValue,
    "description": zeep.xsd.SkipValue,
    "type": zeep.xsd.SkipValue,
    "inheritGroupId": zeep.xsd.SkipValue,
    "userIds": zeep.xsd.SkipValue,
    "lastModified": zeep.xsd.SkipValue
}


#Function to create/update a user
def user(sid, **parameters):
    """Function to create/update a user. To create, need the SID, the 'username', the 'password', the 'firstName', the 'name', the 'email' and the 'groupIds'.
        To update, need the SID and the 'id'. Others parameters are optionnal"""

    _user.update(parameters)
    return client.service.storeUser(sid, _user)


#Function to list the existing users
def list_user(sid):
    """Function to list the existing users. Need the SID"""    

    return client.service.listUsers(sid)


#Function to get specific user by it userid
def get_user(sid, userid):
    """Function to get specific user by it userid. Need the SID and the userid"""

    return client.service.getUser(sid, userid)


#Function to get specific user by it username
def get_user_name(sid, username):
    """Function to get specific user by it username. Need the SID and the username"""

    return client.service.getUserByUsername(sid, username)


#Function to delete user by it userid
def delete_user(sid, userid):
    """Function to delete user by it userid. Need the SIS and the userid"""

    client.service.deleteUser(sid, userid)


#Function to change the password of a specific user
def change_password(sid, userid, oldpass, newpass):
    """Function to change the password of a specific user. Need the SID, the userid, the old password and the new password"""
    
    result = client.service.changePassword(sid, userid, oldpass, newpass)

    if(result == 0):
        return "Mot de passe change"
    elif(result == 1):
        return "Mot de passe incorect"
    elif(result == 2):
        return "Le nouveau mot de passe ne correspond pas au critere"
    else:
        return "Erreur"


#Function to create/update a group
def group(sid, **parameters):
    """Function to create/update a group. To create, need the SID and the 'name'.
        To update, need the SID and the 'id'. Others parameters are optionnal"""

    _group.update(parameters)
    return client.service.storeGroup(sid, _group)


#Function to list the existing group
def list_group(sid):
    """Function to list the existing group. Need the SID"""

    return client.service.listGroups(sid)


#Function to delete a specific group
def delete_group(sid, groupid):
    """Function to delete a specific group. Need the SID and the groupid"""

    client.service.deleteGroup(sid, groupid)