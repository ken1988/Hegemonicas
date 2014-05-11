
import random
import webapp2
import os
import world
from google.appengine.ext import db

class DB_Region(db.Model):
    regionID = db.StringProperty(multiline=False)
    nationID = db.StringProperty(multiline=False)
    region_name = db.StringProperty(multiline=False)
    region_pop = db.StringListProperty()
    region_product = db.StringListProperty()
    region_consume = db.StringListProperty()

class Region_Main():

    def get(self):
        region_data =DB_Region().get()
        print region_data

    def production(self):
        print "p"

    def consumption(self):
        print "test"


    def construction(self):
        print "something is build up"
