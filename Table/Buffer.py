#!/usr/bin/env python
# -*-coding:Latin-1 -*
""""
Module to read document and create Bytes files
"""

import sys

def reader(path):
    """Read the file in Bytes. Example of path: C:/Users/Datasystems/Documents/Documentation_DataSystemsDOC.pdf"""
    
    file = open(path, 'rb')
    data = file.read()
    file.close()
    return data