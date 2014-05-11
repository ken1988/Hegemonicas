import random
from google.appengine.ext import db
import region


class DB_Nation(db.Model):
    ownerID = db.StringProperty(multiline=False)
    orgID = db.StringProperty(multiline=False)
    Nation_Name = db.StringProperty(multiline=False)
    basicData = db.StringListProperty()
    materialData = db.StringListProperty()
    policyData = db.StringListProperty()

class Nation_Main():

    def register(self,uid,nation_name):

        RegNation = DB_Nation()
        RegNation.ownerID = uid
        RegNation.Nation_Name = nation_name
        RegNation.put()

    def getNation(self):
        return

    def startRegion(self):
        return
