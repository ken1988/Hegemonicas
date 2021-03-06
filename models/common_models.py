# -*- coding: utf_8 -*-
'''
Created on 2016/01/03
------------------------------------------------------
プログラム全体を通して共通で使用するModelを管理
------------------------------------------------------
@author: ken
'''
from google.appengine.ext import ndb

class user(ndb.Model):
    name = ndb.StringProperty()
    password = ndb.StringProperty()
    mail = ndb.StringProperty()
    worldID = ndb.KeyProperty(repeated = True)
    nationID = ndb.KeyProperty(repeated = True)
    category = ndb.StringProperty()
    rank = ndb.IntegerProperty()
    rank_point = ndb.IntegerProperty()
    achivement = ndb.KeyProperty(repeated = True)

    def join_to_world(self, world_id,nation_id):
        self.worldID.append(world_id)
        self.nationID.append(nation_id)
        self.put()
        return

class World(ndb.Model):
    world_name = ndb.StringProperty()
    wcreator = ndb.StringProperty()
    year = ndb.IntegerProperty()
    month = ndb.IntegerProperty()
    turn = ndb.IntegerProperty()
    Max_nation = ndb.IntegerProperty()
    Max_turn = ndb.IntegerProperty()
    Max_height = ndb.IntegerProperty()
    Max_width  = ndb.IntegerProperty()
    available = ndb.BooleanProperty()
    Numnations = ndb.IntegerProperty()
    nations = ndb.KeyProperty(repeated = True)
    update_hex = ndb.KeyProperty(repeated = True)#マップ更新時に対象とするhexのキー値
    world_imgs = ndb.BlobProperty(repeated = True)

    def creation(self,wname,wcreator,wMax_nat,wMax_turn,world_size):
        #新規作成
        self.world_name = wname
        self.wcreator = wcreator
        self.Max_nation = wMax_nat
        self.Max_turn = wMax_turn
        self.available = True
        self.Numnations = 0

        if world_size == "tiny":
            self.Max_height = 20
            self.Max_width = 12
        elif world_size == "small":
            self.Max_height = 40
            self.Max_width = 24
        elif world_size == "standard":
            self.Max_height = 80
            self.Max_width = 52
        elif world_size == "large":
            self.Max_height = 128
            self.Max_width = 80
        else:
            self.Max_height = 80
            self.Max_width = 52

        #日付の初期設定
        self.year = 1
        self.turn = 1
        self.month = 1

        self.put()
        return

    def join(self, nation_id):
        self.nations.append(nation_id)
        self.Numnations = self.Numnations + 1
        if self.Numnations + 1 == self.Max_nation:
            self.update_avst()

        self.put()
        return

    def update_avst(self):
        self.available = False
        return

class err_code(ndb.Model):
    category = ndb.StringProperty()
    disp_text = ndb.TextProperty()