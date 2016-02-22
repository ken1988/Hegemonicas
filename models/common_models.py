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
    nationID = ndb.StringProperty()
    SecClear = ndb.IntegerProperty()

    def create(self,Cname,Cpassword,Cmail,CnationID):
        self.name = Cname
        self.password = Cpassword
        self.mail = Cmail
        self.nationID = CnationID
        self.SecClear = 1

class Terrain(ndb.Model):
    terrain = ndb.StringProperty()
    temperture = ndb.IntegerProperty()

class Architect(ndb.Model):
    owner = ndb.StringProperty()

class Unit(ndb.Model):
    owner = ndb.StringProperty()