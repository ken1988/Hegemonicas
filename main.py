# -*- coding: utf_8 -*-
import random
import webapp2
import os
import csv
import uuid
import gamescreen
import datetime
from models import internal_models
from models import common_models

import Cookie
import hashlib
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from __builtin__ import True

class Common_Handler(webapp2.RequestHandler):
    def display(self,tTitle,tURL,templates):
    #tTitle: ページタイトル
    #tURL: 使用するテンプレートURL
    #templates: コンテンツ内Item

        template_values = {"Ptitle": tTitle}
        path = os.path.join(os.path.dirname(__file__), './templates/common_header.html')
        header_html = template.render(path,template_values)
        path = os.path.join(os.path.dirname(__file__), './templates/common_footer.html')
        footer_html = template.render(path,template_values)

        templates['Common_Header'] = header_html
        templates['Common_Footer'] = footer_html
        path = os.path.join(os.path.dirname(__file__), './templates/'+tURL)
        self.response.out.write(template.render(path, templates))

    def makeHash(self,source):
        h = hashlib.md5()
        h.update(source)
        return_key = h.hexdigest()
        return return_key

class Signin(Common_Handler):
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
            #ユーザーキー、パスワードハッシュ生成
            user_key = self.makeHash(self.request.get("userID"))
            passwd = self.makeHash(self.request.get('password'))

            pr_user = common_models.user().get_by_id(user_key)
            if pr_user:
                if pr_user.password == passwd:

                    client_id = str(uuid.uuid4())
                    max_age = 60*120
                    pr_list = {'clid':client_id,'hash':user_key}
                    self.put_cookie(pr_list,max_age)
                self.redirect('/user_screen')
            else:
                self.redirect('/')

        return

    def put_cookie(self,param_list,max_age):
        for key,value in param_list.iteritems():

            keys = key.encode('utf_8')
            values = value.encode('utf_8')
            myCookie = Cookie.SimpleCookie(os.environ.get('HTTP_COOKIE', ''))
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
        Joined_world = user_data.worldID
        Joined_nation = user_data.nationID
        Available_world = common_models.World().query(common_models.World.available == True).fetch(keys_only=True)

        worlds_a = []
        worlds_b = []
        nations_data = []
        for world_key in Available_world:
            if not world_key in Joined_world:
                worlds_a.append(common_models.World().get_by_id(world_key.id()))

        for world_key in Joined_world:
            worlds_b.append(common_models.World().get_by_id(world_key.id()))

        for nation_key in Joined_nation:
            nations_data.append(internal_models.Nation.get_by_id(nation_key.id()))

        joined_list = zip(worlds_b,nations_data)
        templates = {
                     "user": user_data,
                     "worlds_a":worlds_a,
                     "joined_list":joined_list
                     }

        self.display('ユーザ画面','user_screen.html',templates)

    def post(self):
        return

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

        #パスワード,メールアドレスハッシュ生成
        password = self.makeHash(passstr)
        user_key = self.makeHash(uid)

        #ユーザオブジェクト登録
        new_user = common_models.user(id = user_key)
        new_user.mail = uid
        new_user.name = iname
        new_user.password = password
        new_user.put()

        self.redirect('/user_screen')

class JoinWorld(Common_Handler):

    def get(self):
        #get => 登録画面への初回アクセス。
        tWorld = common_models.World().get_by_id(int(self.request.get("world_key")))
        template_values = {"world_name": tWorld.world_name,
                           "world_key": self.request.get("world_key")}
        self.display('ワールド作成画面','nation_registration.html',template_values)
        return

    def post(self):
        uid = self.request.cookies.get('hash', '')
        nation_name = self.request.get("nation_name")
        owner = common_models.user().get_by_id(uid)
        tworld = common_models.World().get_by_id(int(self.request.get("world_key")))

        new_nation = internal_models.Nation()
        new_key = new_nation.creation(owner.key, tworld.key, nation_name)

        owner.join_to_world(tworld.key,new_key)
        tworld.join(new_key)
        self.redirect('/user_screen')
        return

class NewWorld(Common_Handler):

    def get(self):
        #get => 登録画面への初回アクセス。
        template_values = {"creator": self.request.get("creator")}
        self.display('ワールド作成画面','world_creation.html',template_values)
        return

    def post(self):
        wname = self.request.get("wname")
        wcreator = self.request.get("creator")
        wMax_nat = int(self.request.get("Max_nation"))
        wMax_turn = int(self.request.get("Max_turn"))
        new_world = common_models.World()
        new_world.creation(wname, wcreator, wMax_nat, wMax_turn)

        self.redirect('/user_screen')
        return

class MainPage(Common_Handler):

    def get(self):
        templates = {}
        self.display('メインページ','index.html',templates)

app = webapp2.WSGIApplication([('/',MainPage),
                                ('/sign-in', Signin),
                                ('/new_user', User_Regi),
                                ('/game_screen', GameScreen),
                                ('/join_world', JoinWorld),
                                ('/user_screen', UserScreen),
                                ('/new_world', NewWorld),
                                ],debug=True)