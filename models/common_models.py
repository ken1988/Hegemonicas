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

class World(ndb.Model):
    world_name = ndb.StringProperty()
    wcreator = ndb.StringProperty()
    year = ndb.IntegerProperty()
    month = ndb.IntegerProperty()
    turn = ndb.IntegerProperty()
    Max_nation = ndb.IntegerProperty()
    Max_turn = ndb.IntegerProperty()
    available = ndb.BooleanProperty()
    Numnations = ndb.IntegerProperty()
    nations = ndb.KeyProperty(repeated = True)

    def creation(self,wname,wcreator,wMax_nat,wMax_turn):
        #新規作成
        self.world_name = wname
        self.wcreator = wcreator
        self.Max_nation = wMax_nat
        self.Max_turn = wMax_turn
        self.available = True
        self.Numnations = 0

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