'''
Created on 2013/10/12

@author: ken-subPC
'''
import random
import webapp2
import os
from google.appengine.ext import db

class nationData(db.Model):
    ownerID = db.StringProperty(multiline=False)
    orgID = db.StringProperty(multiline=False)
    Nation_Name = db.StringProperty(multiline=False)
    basicData = db.StringListProperty()
    materialData = db.StringListProperty()
    policyData = db.StringListProperty()

class OverviewResp():
    '''
    classdocs
    '''

    def get(self):
        nationData.get()
        return

class MakeNewNation():

    def register(self):
        newNation = nationData()
        newNation.ownerID = self.request.get("uid")
        newNation.Nation_Name = self.request.get("Nation_name")
        newNation.put()
        return

