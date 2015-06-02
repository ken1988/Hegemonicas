# -*- coding: utf_8 -*-
import random
import webapp2
import os
import csv
import uuid
import teleforum
import gamescreen
import datetime
import models
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from webapp2_extras import sessions
from webapp2_extras import auth

class BaseSessionRequestHandler(webapp2.RequestHandler):
    def dispatch(self):
        #このリクエストに対するセッションストアを作る
        self.session_store = sessions.get_store(request=self.request)
        try:
            #ディスパッチャーの起動
            webapp2.RequestHandler.dispatch(self)
        finally:
            #セッションを保存
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        backend = self.session_store.config.get('default_backend','securecookie')
        return self.session_store.get_session(backend=backend)

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

class MakeMap(webapp2.RequestHandler):
    def get(self):
        self.redirect('/')

class UpdateMap(webapp2.RequestHandler):

    def get(self):

        MapChip.all()
        self.redirect('/')


class MainteUser(webapp.RequestHandler):

    def get(self):
        userdata =models.user().all.fetch(20)

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

class register(webapp2.RequestHandler):

    def get(self):
        #get => 登録画面への初回アクセス。特に何も処理しない。
        template_values = {
                           'phase': 1
                           }
        path = os.path.join(os.path.dirname(__file__), './templates/register.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        #post => 登録画面へのデータ送信。入力チェックと確認画面の表示、DBへの登録。
        uid = self.request.get("uid")
        iname = self.request.get("name")
        ipassword = self.request.get("password")
        imail = self.request.get("e-mail")
        inationID = self.request.get("uid")
        nation_name = self.request.get("Nation_name")

        #-----------------------------------------------------
        newUser = models.user(key_name = uid)
        newUser.create(iname, ipassword, imail, inationID)
        newUser.put()
        #-----------------------------------------------------
        newNation = models.Nation()
        newNation.initialize(uid, nation_name)
        newNation.put()
        #-----------------------------------------------------
        self.redirect('/game_screen')

class ManageSession(webapp2.RequestHandler):

    def get(self):
        # who want to logout the system uses get method.
        self.redirect('/')

    def post(self):
        # who want to login the system uses get method.
        Uname = self.request.get("name")
        Pword = self.request.get("password")
        pr_user = models.user().get_by_key_name(Uname, None)

        if Pword == pr_user.password:
            self.session['user'] = pr_user
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write('test:%d'%models.user)
            #self.('/game_screen')
        else:
            self.redirect('/')

class putcookie(webapp2.RequestHandler):
    def get(self):

        now_date = datetime.datetime.now()
        expires = now_date
        expires = expires + datetime.timedelta(seconds=+30)

        expires = expires.strftime('%a, %d-%b-%Y %H:%M:%S GMT')

        client_id = self.request.cookies.get('name', '')
        if client_id == '':
            client_id = str(uuid.uuid4())
            self.response.write('set new<br />')

            myCookie = 'name=%s; expires=%s;' % (client_id, expires)
            self.response.headers.add_header('Set-Cookie', myCookie )

            self.response.write(myCookie)
        else:
            self.response.write('exist<br />')


class getcookie(webapp2.RequestHandler):
    def get(self):

        client_id = self.request.cookies.get('name', '')
        self.response.write(client_id)

class GameScreen(webapp2.RequestHandler):

    def get(self):

        gamescreen.OverviewResp
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), './templates/game_screen.html')
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
                                ('/settings', SettingsScreen)
                                ],debug=True,
                                    config={'webapp2_extras.sessions':
                                            {'secret_key':'my_seacret_key',     #秘密キー必須
                                            'cookie_name':'TestSessio2n',      #セッションクッキー名
                                            'session_max_age':360,             #セッション生存時間 (sec)
                                            'cookie_arg':
                                            {'max_age':None,
                                             'domain':None,
                                             'path':'/',
                                             'secure':None,
                                             'httponly':None},
                                             'default_backend':'securecookie',  #保存先の指定
                                             },})