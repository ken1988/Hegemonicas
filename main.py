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

class Common_Handler(webapp2.RequestHandler):
    def display(self,tTitle,tURL,templates):
    #tTitle: ページタイトル
    #tURL: 使用するテンプレートURL
    #templates: コンテンツ内Item

        template_values = {"Ptitle": tTitle}
        path = os.path.join(os.path.dirname(__file__), './templates/common_header.html')
        header_html = template.render(path,template_values)

        templates['Common_Header'] = header_html
        path = os.path.join(os.path.dirname(__file__), './templates/'+tURL)
        self.response.out.write(template.render(path, templates))

class Signin(webapp2.RequestHandler):
#ログアウト時はsign-inへgetモードでアクセスする

    def get(self):
        if self.request.get("mode") == 'logout':
            #cookieを破棄する
            self.response.delete_cookie('clid')
            self.response.delete_cookie('hash')
            self.redirect('/')
        return

    def post(self):
#ログイン時はsign-inへpostモードでアクセスする

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
                    disp_name = pr_user.name
                    max_age = 60*120
                    pr_list = {'clid':client_id,'hash':user_key,'disp_name':disp_name}
                    self.put_cookie(pr_list,max_age)

            self.redirect('/user_screen')
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

class GameScreen(Common_Handler):
#ゲームメイン画面
    def get(self):
        gamescreen.OverviewResp

        templates = {}
        self.display('ゲーム画面','game_screen.html',templates)

class UserScreen(Common_Handler):
#ユーザメイン画面
#ログイン後、いったんユーザメイン画面に入り各ワールドへ遷移する

    def get(self):
        uid = self.request.cookies.get('hash', '')
        user_data = common_models.user.get_by_id(uid)
        templates = {"user": user_data}
        self.display('ユーザ画面','user_screen.html',templates)

    def post(self):
        return

class SettingsScreen(Common_Handler):
#ユーザ設定用の画面
    def get(self):
        userdata =common_models.user().all.fetch(20)

        templates = {
                       'name': userdata.name,
                       'mail': userdata.mail,
                    }

        self.display('ユーザ設定画面','profile.html',templates)

    def post(self):
        template_values = {'name':'test'}

        path = os.path.join(os.path.dirname(__file__), './templates/profile.html')
        self.response.out.write(template.render(path, template_values))

class User_Regi(Common_Handler):

    def get(self):
        #get => 登録画面への初回アクセス。特に何も処理しない。
        template_values = {}
        self.display('ユーザ登録画面','user_registration.html',template_values)

    def post(self):
        #post => 登録画面へのデータ送信。入力チェックと確認画面の表示、DBへの登録。
        uid = self.request.get("uid")
        iname = self.request.get("name")
        passstr = self.request.get("password")

        #パスワードハッシュ値生成
        m = hashlib.md5()
        m.update(passstr)
        password = m.hexdigest()

        #メールアドレスハッシュ値生成
        h = hashlib.md5()
        h.update(uid)
        user_key = h.hexdigest()

        #ユーザオブジェクト登録
        new_user = common_models.user(id = user_key)
        new_user.mail = uid
        new_user.name = iname
        new_user.password = password
        new_user.put()

        self.redirect('/user_screen')

class MainPage(Common_Handler):

    def get(self):
        templates = {}
        self.display('メインページ','index.html',templates)

app = webapp2.WSGIApplication([('/',MainPage),
                                ('/sign-in', Signin),
                                ('/new_user', User_Regi),
                                ('/game_screen', GameScreen),
                                ('/user_screen', UserScreen),
                                ('/user_setting', SettingsScreen)
                                ],debug=True)