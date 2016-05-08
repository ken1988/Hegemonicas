# -*- coding: utf_8 -*-
'''
Created on 2013/01/22
------------------------------------------------------
ユーザ間の交流（外交）で使用するModelを管理
------------------------------------------------------
@author: ken
'''
import datetime
import time
import random
import webapp2
import os
from google.appengine.ext import ndb

class Base_message(ndb.Model):
    fromID = ndb.KeyProperty() #発信者のID。
    toID  = ndb.KeyProperty(repeated = True) #相手のID。複数指定可。
    title = ndb.StringProperty()
    contents = ndb.TextProperty()
    postDate = ndb.DateTimeProperty(auto_now_add = True)
    tags = ndb.StringProperty(repeated = True)
    broadcast = ndb.BooleanProperty()

    def Send_message(self,msg_pack):
        self.Valid_message(msg_pack)
        self.fromID = msg_pack['userID']
        self.toID   = msg_pack['tuserID']
        self.title  = msg_pack['title']
        self.contents = msg_pack['contents']
        self.tags = msg_pack['tags']
        self.put()
        return

    def Receive_message(self):
        return

    def Trash_message(self):
        return

    def Valid_message(self,data_pack):
        return

class Sect_message(Base_message):
    SecClear = ndb.IntegerProperty()

class world_news(Base_message):
    author = ndb.StringProperty()
    location = ndb.IntegerProperty(repeated = True)

    def Send_message(self, msg_pack):
        self.broadcast = True
        self.location = msg_pack['location']
        Base_message.Send_message(self,msg_pack)
        return