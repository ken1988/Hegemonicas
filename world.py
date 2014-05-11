'''
Created on 2014/04/14

@author: ken
'''
import random
from google.appengine.ext import db

class DB_World(db.Model):
    WorldID = db.StringProperty(multiline=False)
    WorldTime = db.DateTimeProperty
    WorldTurn = db.StringProperty(multiline=False)

class World():

    def world_get(self):
        world = DB_World.all()
