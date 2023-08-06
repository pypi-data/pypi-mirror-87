# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 11:26:29 2020

@author: danaukes
"""

class GenericData(object):
    def __init__(self, **kwargs):
        self.keys = kwargs.keys()
        for key,value in kwargs.items():
            setattr(self,key,value)
    def to_dict(self):
        output = {}
        for key in self.keys:
            output[key] = getattr(self,key)
        return output
