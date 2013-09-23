'''
Created on 2013/01/22

@author: ken
'''
import random
import webapp2
import os
from google.appengine.ext import db

class BBSmessages(db.Model):
    orgID = db.StringProperty(multiline=False)
    frmID = db.StringProperty(multiline=False)
    parentsID = db.StringProperty(multiline=False)
    title = db.StringProperty(multiline=False)
    contents = db.TextProperty()
    SecClear = db.RatingProperty()
    postDate = db.TimeProperty()
    tags = db.StringListProperty()

class Loadforums():

    def get(self):
        bbsdata = BBSmessages().get()
        return bbsdata
