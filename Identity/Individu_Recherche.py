#-*- coding: utf-8 -*-

import requests, os, json, glob


def Recherche_Order(ModelBase, Modelfield) :
		return ModelBase.objects.order_by(Modelfield)

def Recherche_Filter(ModelBase, Modelfield) :
		return ModelBase.objects.filter(**Modelfield)

def set_if_not_none(mapping, key, value):
    if value is not None :
        if len(value) != 0 :
            mapping[key] = value