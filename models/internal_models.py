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
class Terrain(ndb.Model):
    terrain_name = ndb.StringProperty()
    Fland = ndb.BooleanProperty()

class Architect(ndb.Model):
    architect_name = ndb.StringProperty()

class Unit(ndb.Model):
    owner = ndb.StringProperty()

class Population(ndb.Model):
    #年齢は年少、生産、高齢の3分類

    young_men = ndb.IntegerProperty()
    young_women = ndb.IntegerProperty()
    work_men = ndb.IntegerProperty()
    work_women = ndb.IntegerProperty()
    retired_men = ndb.IntegerProperty()
    retired_women = ndb.IntegerProperty()
    unemployed = ndb.IntegerProperty()
    unwork_women = ndb.IntegerProperty() #出産中などで働かない女性数

    def sum_pop(self):
        total_pop = self.young_men + self.young_women + self.work_men + self.work_women + self.retired_men + self.retired_women
        return total_pop

class Nation(ndb.Model):
    ownerID = ndb.KeyProperty()
    worldID = ndb.KeyProperty()
    orgID = ndb.KeyProperty()
    region = ndb.KeyProperty(repeated = True)
    Capital_name = ndb.StringProperty()
    SecClear =ndb.IntegerProperty()
    Nation_Name = ndb.StringProperty()
    Projectque = ndb.KeyProperty(repeated = True)
    basicData = ndb.StringProperty(repeated = True)
    materialData = ndb.StringProperty(repeated = True)
    policyData = ndb.StringProperty(repeated = True)

    def creation(self,uid,world_id,nation_name):
        self.ownerID = uid
        self.worldID = world_id
        self.Nation_Name = nation_name
        self.put()
        return self.key

    def initialization(self,region_key,region_name):
        self.region.append(region_key)
        self.Capital_name = region_name
        self.put()
        return

    def getNation(self):
        return

    def startRegion(self):
        return

class Project(ndb.Model):
    project_name = ndb.StringProperty()
    target_region = ndb.StringProperty()
    target_X = ndb.IntegerProperty()
    target_Y = ndb.IntegerProperty()
    input = ndb.StringProperty(repeated = True)
    output = ndb.StringProperty()
    est_Trun  = ndb.IntegerProperty()

class Region(ndb.Model):
    nationID = ndb.KeyProperty()
    region_name = ndb.StringProperty()
    region_maps = ndb.KeyProperty(repeated = True) #World Mapを突っ込む
    region_pop = ndb.StructuredProperty(Population, repeated = True) #上流、中流、下流×都市、農村の6分類を作成
    region_product = ndb.IntegerProperty(repeated = True)
    region_consume = ndb.IntegerProperty(repeated = True)

    def creation(self,nationID,name,location):
        self.nationID = nationID
        self.region_name = name
        self.region_location = location
        self.put()
        return self.key

    def get(self):
        return

    def production(self):
        return

    def consumption(self):
        return


    def construction(self):
        return

class WorldMap(ndb.Model):
    world_id = ndb.KeyProperty() #所属するworld
    locationX = ndb.IntegerProperty() #X座標
    locationY = ndb.IntegerProperty() #Y座標
    ruler = ndb.KeyProperty() #現在の支配者
    terra = ndb.StructuredProperty(Terrain)     #基礎地形
    architect = ndb.StructuredProperty(Architect)  #建築物
    localname = ndb.StringProperty() #固有名称
    resistPoint = ndb.IntegerProperty() #攻撃に対する抵抗値
    national = ndb.JsonProperty(repeated = True)#住民の国籍（国Key+比率のデータをJSONでシリアライズ）

    def disp_map(self,position,world):

        return

    def make_map(self):

        return
