# -*- coding: utf_8 -*-
import random
import webapp2
import os
import csv
import uuid
from models import external_models
import gamescreen
import datetime
from models import internal_models
from models import common_models
import Cookie
import hashlib
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from webapp2_extras import sessions
from webapp2_extras import auth

class Signin(webapp2.RequestHandler):
    def get(self):
        if self.request.get("mode") == 'logout':
            #cookieを破棄する
            self.response.delete_cookie('clid')
            self.response.delete_cookie('hash')
            self.redirect('/')
        return

    def post(self):
        if self.request.get("mode") == 'login':

            #Postがあった場合の処理
            uid = self.request.get("userID")
            password = self.request.get('password')

            #ユーザーキー生成
            h = hashlib.md5()
            h.update(uid)
            user_key = h.hexdigest()

            #パスワードハッシュ値生成
            m = hashlib.md5()
            m.update(password)
            passwd = m.hexdigest()

            pr_user = common_models.user().get_by_id(user_key)
            if pr_user:
                if pr_user.password == passwd:

                    client_id = str(uuid.uuid4())
                    disp_name = pr_user.country_name
                    max_age = 60*120
                    pr_list = {'clid':client_id,'hash':user_key,'disp_name':disp_name}
                    self.put_cookie(pr_list,max_age)

            self.redirect('/')
        return

    def put_cookie(self,param_list,max_age):
        for key,value in param_list.iteritems():
            keys = key.encode('utf_8')
            values = value.encode('utf_8')
            myCookie = Cookie.SimpleCookie(os.environ.get( 'HTTP_COOKIE', '' ))
            myCookie[keys] = values
            myCookie[keys]["path"] = "/"
            myCookie[keys]["max-age"] = max_age
            self.response.headers.add_header('Set-Cookie', myCookie.output(header=""))
        return

class Signout(webapp.RequestHandler):
    def get(self):
        return

    def post(self):
        return

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
        newUser = common_models.user(key_name = uid)
        newUser.create(iname, ipassword, imail, inationID)
        newUser.put()
        #-----------------------------------------------------
        newNation = internal_models.Nation()
        newNation.initialize(uid, nation_name)
        newNation.put()
        #-----------------------------------------------------
        self.redirect('/game_screen')

class GameScreen(webapp2.RequestHandler):
#ゲームメイン画面
    def get(self):

        gamescreen.OverviewResp
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), './templates/game_screen.html')
        self.response.out.write(template.render(path, template_values))


class SettingsScreen(webapp2.RequestHandler):
#ユーザ設定用の画面
    def get(self):
        userdata =common_models.user().all.fetch(20)

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

class MainPage(webapp2.RequestHandler):

    def get(self):

        template_values = {}

        path = os.path.join(os.path.dirname(__file__), './templates/index.html')
        self.response.out.write(template.render(path, template_values))


app = webapp2.WSGIApplication([('/',MainPage),
                                ('/sign-in', Signin),
                                ('/sign-out', Signout),
                                ('/new_user', register),
                                ('/game_screen', GameScreen),
                                ('/user_setting', SettingsScreen)
                                ],debug=True)