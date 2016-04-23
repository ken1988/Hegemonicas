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
    nationID = ndb.KeyProperty(repeated = True)

