'''
Created on 2013/10/12

@author: ken-subPC
'''
import random
import webapp2
import os
from models import internal_models
from google.appengine.ext import db

class OverviewResp():
    '''
    classdocs
    '''
    def get(self):
        internal_models.Nation.get_by_key_name("test2", None)
        return
