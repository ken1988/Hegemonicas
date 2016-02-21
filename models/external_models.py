'''
Created on 2013/01/22
------------------------------------------------------
ユーザ間の交流（外交）で使用するModelを管理
------------------------------------------------------
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


class Messages(db.Model):
    frmID = db.StringProperty(multiline=False)
    toID  = db.StringProperty(multiline=False)
    title = db.StringProperty(multiline=False)
    contents = db.TextProperty()
    SecClear = db.RatingProperty()
    postDate = db.TimeProperty()
    tags = db.StringListProperty()

class news(db.Model):
    nationID = db.StringProperty(multiline=False)
    contents = db.TextProperty()
    postDate = db.DateTimeProperty()
    location = db.StringListProperty()
    tags = db.StringListProperty()