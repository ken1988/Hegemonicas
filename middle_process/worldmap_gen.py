'''
Created on 2016/06/19

@author: ken
'''
from models import common_models
from models import internal_models
from google.appengine.ext import ndb

class Generate_Worldmap():
    def generate(self, world):

        x = 0
        y = 0
        while y < world.Max_height:
            x = 0
            y = y + 1
            while x < world.Max_width:
                x = x + 1
                created_hex = internal_models.WorldMap()
                created_hex.world_id = world.key
                created_hex.locationX = x
                created_hex.locationY = y
                created_hex.put()

        return
