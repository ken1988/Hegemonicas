# -*- coding: utf_8 -*-
import random
import webapp2
import os
import csv
import teleforum
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp

class MapChip(db.Model):
    locationX = db.IntegerProperty()
    locationY = db.IntegerProperty()
    terra = db.StringProperty(multiline=False)
    architect = db.StringProperty(multiline=False)
    pop = db.IntegerProperty()
    indpop1 = db.IntegerProperty()
    indpop2 = db.IntegerProperty()
    indpop3 = db.IntegerProperty()
    poptype = db.StringProperty(multiline=False)
    resistPoint = db.IntegerProperty()
    navigate = db.StringProperty(multiline=False)
    national = db.StringProperty(multiline=False)

class user(db.Model):
    name = db.StringProperty(multiline= False)
    password = db.StringProperty(multiline=False)
    mail = db.EmailProperty()
    nationID = db.StringProperty(multiline=False)
    SecClear = db.RatingProperty()

class news(db.Model):
    nationID = db.StringProperty(multiline=False)
    contents = db.TextProperty()
    postDate = db.DateTimeProperty()
    location = db.StringListProperty()
    tags = db.StringListProperty()

class Messages(db.Model):
    frmID = db.StringProperty(multiline=False)
    toID  = db.StringProperty(multiline=False)
    title = db.StringProperty(multiline=False)
    contents = db.TextProperty()
    SecClear = db.RatingProperty()
    postDate = db.TimeProperty()
    tags = db.StringListProperty()

class nationData(db.Model):
    ownerID = db.StringProperty(multiline=False)
    orgID = db.StringProperty(multiline=False)
    basicData = db.StringListProperty()
    materialData = db.StringListProperty()
    policyData = db.StringListProperty()

class MakeMap(webapp2.RequestHandler):

    def get(self):

        terrain = ["Sea","Plain","Mountain"]
        architect = ['Town','Farm','None','None','None','None','None','None']
        reader=csv.reader(open('test-map.csv'))

        locy = 0
        for row in reader:
            locx = 0

            for column in row:
                column = int(column)
                newName = "X" + str(locx) +":Y" + str(locy)
                newMap = MapChip(key_name = newName)
                newMap.locationX = locx
                newMap.locationY = locy
                newMap.terra = terrain[column]

                if newMap.terra == "Plain":
                    arc = random.choice(architect)
                    newMap.architect = arc
                    if arc == "Town":
                        newMap.pop = 100
                newMap.put()

                template_values = {
                                   'locationX': newMap.locationX,
                                   'locationY': newMap.locationY,
                                   'terra'    : newMap.terra,
                                   'architect': newMap.architect,
                                   'pop'      : newMap.pop,
                                   }

                path = os.path.join(os.path.dirname(__file__), './templates/MapMaker.html')
                self.response.out.write(template.render(path, template_values))
                locx = locx + 1

            locy = reader.line_num

class UpdateMap(webapp2.RequestHandler):

    def get(self):

        MapChip.all()
        self.redirect('/')


class MainteUser(webapp.RequestHandler):

    def get(self):
        userdata =user().all.fetch(20)

        template_values = {
                       'name': userdata.name,
                       'mail': userdata.mail,
                        'nationID': userdata.nationID,
                       'SecClear'    : userdata.SecClear,
                       }

        path = os.path.join(os.path.dirname(__file__), './templates/profile.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        template_values = {'name':'test'}

        path = os.path.join(os.path.dirname(__file__), './templates/profile.html')
        self.response.out.write(template.render(path, template_values))

class register(webapp.RequestHandler):

    def get(self):
        #get => 登録画面への初回アクセス。特に何も処理しない。
        template_values = {
                           'phase': 1
                           }
        path = os.path.join(os.path.dirname(__file__), './templates/register.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        #post => 登録画面へのデータ送信。入力チェックと確認画面の表示、DBへの登録。
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), './templates/register.html')
        self.response.out.write(template.render(path, template_values))

class ManageSession(webapp2.RequestHandler):

    def get(self):
        # who want to logout the system uses get method.

        path = os.path.join(os.path.dirname(__file__), './templates/index.html')
        self.redirect('/MakeMap')

    def post(self):
        # who want to login the system uses get method.
        pr_user = user().get_by_key_name("name", None)

        self.redirect('/game_screen')

class GameScreen(webapp2.RequestHandler):

    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), './templates/game_screen.html')
        self.response.out.write(template.render(path, template_values))


class MailScreen(webapp2.RequestHandler):

    def get(self):
        # who want to logout the system uses get method.

        path = os.path.join(os.path.dirname(__file__), './templates/index.html')
        self.redirect('/MakeMap')

    def post(self):
        # who want to login the system uses get method.
        user().get_by_key_name("name", None)

        self.redirect('/game_screen')

class PolicyScreen(webapp2.RequestHandler):

    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), './templates/policy_screen.html')
        self.response.out.write(template.render(path, template_values))

class DiplomacyScreen(webapp2.RequestHandler):

    def get(self):
        teleforum.Loadforums
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), './templates/diplomacy_screen.html')
        self.response.out.write(template.render(path, template_values))

class SettingsScreen(webapp2.RequestHandler):

    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), './templates/setting_screen.html')
        self.response.out.write(template.render(path, template_values))

class MainPage(webapp2.RequestHandler):

    def get(self):
        Worldmap = MapChip.all().order('locationX').fetch(20, 0)
        template_values = {
                           'world' : Worldmap,
                       }

        path = os.path.join(os.path.dirname(__file__), './templates/index.html')
        self.response.out.write(template.render(path, template_values))

app = webapp2.WSGIApplication([('/',MainPage),
                                ('/MakeMap', MakeMap),
                                ('/MainteUser', MainteUser),
                                ('/register', register),
                                ('/login', ManageSession),
                                ('/logout', ManageSession),
                                ('/game_screen', GameScreen),
                                ('/mail', MailScreen),
                                ('/game_diplomacy', DiplomacyScreen),
                                ('/game_policy', PolicyScreen),
                                ('/settings', SettingsScreen)],
                                     debug=True)