# -*- coding: utf_8 -*-
'''
Created on 2015/05/07
------------------------------------------------------
国、地域の処理（内政）で使用するModelを管理
------------------------------------------------------
@author: ken
'''
import random
from google.appengine.ext import ndb
from google.appengine.ext import db
class World(ndb.model):
    world_name = ndb.StringProperty(multiline=False)

    def creation(self):
        return

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


class WorldMap(ndb.Model):
    locationX = ndb.IntegerProperty()
    locationY = ndb.IntegerProperty()
    terra = db.StringProperty(multiline=False)
    architect = db.StringProperty(multiline=False)
    pop = db.IntegerProperty()
    indpop1 = db.IntegerProperty()
    indpop2 = db.IntegerProperty()
    indpop3 = db.IntegerProperty()
    poptype = db.StringProperty(multiline=False)
    resistPoint = db.IntegerProperty()
    navigate = db.StringProperty(multiline=False)
    national = db.StringProperty(multiline=False)
    return

