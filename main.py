# -*- coding: utf_8 -*-
import random
import webapp2
import os
import csv
import uuid
import datetime
from models import internal_models
from models import common_models
from models import external_models
from middle_process import gamescreen
import Cookie
import hashlib
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from __builtin__ import True

class Common_Handler(webapp2.RequestHandler):
    def display(self,tTitle,tURL,templates,flogin):
    #tTitle: ページタイトル
    #tURL: 使用するテンプレートURL
    #templates: コンテンツ内Item
    #flogin: ログインフォーム表示フラグ

        template_values = {"Ptitle": tTitle,
                           "flogin": flogin}
        template_values.update(templates)
        path = os.path.join(os.path.dirname(__file__), './templates/', tURL)
        self.response.out.write(template.render(path, template_values))

    def makeHash(self,source):
        h = hashlib.md5()
        h.update(source)
        return_key = h.hexdigest()
        return return_key

    def get_user(self,uid):
        #ログイン確認＆ユーザデータ取得
        if uid == "":
            return False
        else:
            user = common_models.user().get_by_id(uid)
            return user

    def validate(self):

        return

    def disp_err(self,errcd):
        #エラーメッセージ出力
        err = common_models.err_code.get_by_id(errcd)
        return err.disp_text

class Signin(Common_Handler):
    def get(self):
        self.signin_out()
        return

    def post(self):
        self.signin_out()
        return

    def signin_out(self):

        if self.request.get("mode") == 'logout':
            #logoutモードの場合cookieを破棄する
            self.response.delete_cookie('clid')
            self.response.delete_cookie('hash')

        elif self.request.get("mode") == 'login':
            #loginモードの場合cookieを生成する
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
                    return

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
    def post(self):
        res = self.get_user(self.request.cookies.get('hash', ''))
        if res == False:
            self.redirect("./")
        else:
            user = res

        if self.request.get("mode") == "valid":
            ercd = self.validate(user)
            return ercd

        sys_message = ""
        if self.request.get("msg"):
            sys_message = self.disp_err(self.request.get("msg"))


            if self.request.get("nation").isdigit() and self.request.get("world").isdigit():
                params = {"nationID":int(self.request.get("nation")),
                          "worldID":int(self.request.get("world")),
                          "sys_message":sys_message,
                          "user":user,
                          }
                newScreen = gamescreen.Internal_GameScreen()
                res_param = newScreen.display_initial(params)
            else:
                res_param["erparam"] = "5825485334380544"

            if res_param["erparam"] == True:
                templates = {}
                self.display('ゲーム画面','game_screen.html',templates,0)
        return

    def validate(self,user):

        if self.request.get("nation").isdigit() and self.request.get("world").isdigit():
            params = {"nationID":int(self.request.get("nation")),
                      "worldID":int(self.request.get("world")),
                      "user":user,
                      }
            newScreen = gamescreen.Internal_GameScreen()
            ercd = newScreen.validation_initial(params)
        else:
            ercd = "5825485334380544"

        return ercd

class UserScreen(Common_Handler):
#ユーザメイン画面
#ログイン後、いったんユーザメイン画面に入り各ワールドへ遷移する

    def get(self):
        res = self.get_user(self.request.cookies.get('hash', ''))
        if res == False:
            self.redirect("./")
            return
        else:
            user = res

        sys_message = ""
        if self.request.get("msg"):
            sys_message = self.disp_err(int(self.request.get("msg")))

        Joined_world = user.worldID
        Joined_nation = user.nationID
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
                     "user": user,
                     "worlds_a":worlds_a,
                     "joined_list":joined_list,
                     "sys_message":sys_message
                     }

        self.display('ユーザ画面','user_screen.html',templates,0)
        return

    def post(self):
        return

class User_Regi(Common_Handler):

    def get(self):
        #get => 登録画面への初回アクセス。特に何も処理しない。
        template_values = {}
        self.display('ユーザ登録画面','user_registration.html',template_values,0)

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
        res = self.get_user(self.request.cookies.get('hash', ''))
        if res == False:
            self.redirect("./")
            return

        #get => 登録画面への初回アクセス。
        tWorld = common_models.World().get_by_id(int(self.request.get("world_key")))
        template_values = {"world_name": tWorld.world_name,
                           "world_key": self.request.get("world_key")}
        self.display('ワールド参加画面','nation_registration.html',template_values,0)
        return

    def post(self):
        capital_location = []

        uid = self.request.cookies.get('hash', '')
        nation_name = self.request.get("nation_name")
        capital_name = self.request.get("capital_name")
        capital_location.append(int(self.request.get("locationX")))
        capital_location.append(int(self.request.get("locationY")))

        owner = common_models.user().get_by_id(uid)
        tworld = common_models.World().get_by_id(int(self.request.get("world_key")))

        new_nation = internal_models.Nation()
        new_key = new_nation.creation(owner.key, tworld.key, nation_name)

        first_region = internal_models.Region()
        reg_key = first_region.creation(new_key, capital_name, capital_location)

        new_nation.initialization(reg_key,capital_name)
        owner.join_to_world(tworld.key,new_key)
        tworld.join(new_key)
        self.redirect('/user_screen')
        return

class NewWorld(Common_Handler):

    def get(self):
        res = self.get_user(self.request.cookies.get('hash', ''))
        if res == False:
            self.redirect("./")
            return

        #get => 登録画面への初回アクセス。
        template_values = {"creator": self.request.get("creator")}
        self.display('ワールド作成画面','world_creation.html',template_values,0)
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

class SystemConsol(Common_Handler):

    def get(self):
        res = self.get_user(self.request.cookies.get('hash', ''))
        if res == False:
            self.redirect("./")
            return
        else:
            user = res

        all_errcd = common_models.err_code.query()
        templates = {"all_ercd":all_errcd}
        self.display('システム管理画面','administration_screen.html',templates,0)
        return

    def post(self):
        res = self.get_user(self.request.cookies.get('hash', ''))
        if res == False:
            self.redirect("./")
        else:
            user = res

        new_cd = common_models.err_code()
        new_cd.category = self.request.get("err_cat")
        new_cd.disp_text = self.request.get("err_txt")
        ercd = new_cd.put()

        templates = {"new_code":ercd}
        self.display('システム管理画面','administration_screen.html',templates,0)
        return

class MainPage(Common_Handler):

    def get(self):

        sys_message = ""
        if self.request.get("msg"):
            sys_message = self.disp_err(self.request.get("msg"))

        templates = {"sys_message":sys_message}
        self.display('メインページ','index.html',templates,1)

app = webapp2.WSGIApplication([('/',MainPage),
                                ('/sign-in', Signin),
                                ('/new_user', User_Regi),
                                ('/game_screen', GameScreen),
                                ('/join_world', JoinWorld),
                                ('/user_screen', UserScreen),
                                ('/new_world', NewWorld),
                                ('/maintenance', SystemConsol),
                                ],debug=True)