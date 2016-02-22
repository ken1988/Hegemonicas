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
class World(ndb.Model):
    world_name = ndb.StringProperty()

    def creation(self):
        return

class Nation(ndb.Model):
    ownerID = ndb.StringProperty()
    orgID = ndb.StringProperty()
    Nation_Name = ndb.StringProperty()
    basicData = ndb.StringProperty(repeated = True)
    materialData = ndb.StringProperty(repeated = True)
    policyData = ndb.StringProperty(repeated = True)

    def initialize(self,uid,nation_name):
        self.ownerID = uid
        self.Nation_Name = nation_name

    def getNation(self):
        return

    def startRegion(self):
        return

class Region(ndb.Model):
    regionID = ndb.StringProperty()
    nationID = ndb.StringProperty()
    region_name = ndb.StringProperty()
    region_pop = ndb.StringProperty(repeated = True)
    region_product = ndb.StringProperty(repeated = True)
    region_consume = ndb.StringProperty(repeated = True)

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
    terra = ndb.StringProperty()
    architect = ndb.StringProperty()
    pop = ndb.IntegerProperty()
    indpop1 = ndb.IntegerProperty()
    indpop2 = ndb.IntegerProperty()
    indpop3 = ndb.IntegerProperty()
    poptype = ndb.StringProperty()
    resistPoint = ndb.IntegerProperty()
    navigate = ndb.StringProperty()
    national = ndb.StringProperty()

