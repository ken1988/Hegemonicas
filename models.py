# -*- coding: utf_8 -*-
<<<<<<< HEAD
=======
'''
Created on 2015/05/07

@author: ken
'''
>>>>>>> branch 'master' of git@github.com:ken1988/Hegemonicas.git
import random
from google.appengine.ext import db

class user(db.Model):
    name = db.StringProperty(multiline= False)
    password = db.StringProperty(multiline=False)
    mail = db.EmailProperty()
    nationID = db.StringProperty(multiline=False)
    SecClear = db.RatingProperty()

    def create(self,Cname,Cpassword,Cmail,CnationID):
        self.name = Cname
        self.password = Cpassword
        self.mail = Cmail
        self.nationID = CnationID
        self.SecClear = 1

class Nation(db.Model):
    ownerID = db.StringProperty(multiline=False)
    orgID = db.StringProperty(multiline=False)
    Nation_Name = db.StringProperty(multiline=False)
    basicData = db.StringListProperty()
    materialData = db.StringListProperty()
    policyData = db.StringListProperty()

    def initialize(self,uid,nation_name):
        self.ownerID = uid
        self.Nation_Name = nation_name

    def getNation(self):
        return

    def startRegion(self):
        return

class Region(db.Model):
    regionID = db.StringProperty(multiline=False)
    nationID = db.StringProperty(multiline=False)
    region_name = db.StringProperty(multiline=False)
    region_pop = db.StringListProperty()
    region_product = db.StringListProperty()
    region_consume = db.StringListProperty()

    def get(self):
        return

    def production(self):
        return

    def consumption(self):
        return


    def construction(self):
        return
