# -*- coding: utf_8 -*-
'''
Created on 2016/5/4

@author: ken
'''
from models import common_models
from models import internal_models
from google.appengine.ext import ndb

class Internal_GameScreen():
    '''
    ゲーム画面表示に関するクラス
    '''
    def display_initial(self,params):
        '''
        初期画面を表示する
        '''
        return_param = {}
        erparam = self.validation_initial(params)

        if erparam == True:
            nation_stat = 0
            return_param ={"view_point":00,
                           "nation_stat":nation_stat,
                           "erparam":erparam}
        else:
            return_param = {"erparam":erparam}

        return return_param

    def validation_initial(self,params):
        try:
            world = common_models.World.get_by_id(params['worldID'])
            nation = internal_models.Nation.get_by_id(params['nationID'])
            user = params['user']
            ermsg = []

            if not nation.key in user.nationID:
                ermsg.append("所有していない国のIDが指定されました。")

            if not nation.key in world.nations:
                ermsg.append("ワールドに存在しない国のIDが指定されました")

            if len(ermsg) == 0:
                return True
            else:
                return ermsg

        except Exception:
            ermsg.append("例外エラーが発生しました")
            return ermsg

class Internal_GameProcess():
    '''
    classdocs
    '''
    def Game_Production(self):
        return

    def Game_Consumption(self):
        return