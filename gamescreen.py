'''
Created on 2013/10/12

@author: ken-subPC
'''
import random
import webapp2
import os
import nation
from google.appengine.ext import db

class OverviewResp():
    '''
    classdocs
    '''
    def get(self):
        nation.DB_Nation.get_by_key_name("test2", None)
        return
