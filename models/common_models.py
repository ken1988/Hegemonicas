'''
Created on 2016/01/03
------------------------------------------------------
プログラム全体を通して共通で使用するModelを管理
------------------------------------------------------
@author: ken
'''
from google.appengine.ext import ndb

class user(ndb.Model):
    name = ndb.StringProperty(multiline= False)
    password = ndb.StringProperty(multiline=False)
    mail = ndb.StringProperty(multiline=False)
    nationID = ndb.StringProperty(multiline=False)
    SecClear = ndb.IntegerProperty()

    def create(self,Cname,Cpassword,Cmail,CnationID):
        self.name = Cname
        self.password = Cpassword
        self.mail = Cmail
        self.nationID = CnationID
        self.SecClear = 1

class Terrain(ndb.model):
    return

class Architect(ndb.model):
    return

class Unit(ndb.model):