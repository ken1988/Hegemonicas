# -*- coding: utf_8 -*-
'''
Created on 2016/5/4

@author: ken
'''
from models import common_models, internal_models
from models.internal_models import WorldMap
from models.common_models import World
from models.internal_models import Nation
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
        world = World.get_by_id(params['worldID'])
        worldmaps = WorldMap.query(WorldMap.world_id == params['worldID'])
        nation = Nation.get_by_id(params['nationID'])
        projects=[]

        for prjID in nation.Projectque:
            projects.append(internal_models.Project.get_by_id(prjID.id()))

        nation_stat = 0
        return_param ={"world_name":world.world_name,
                       "nation_name":nation.Nation_Name,
                       "view_point":10,
                       "nation_stat":nation_stat}
        return return_param


    def validation_initial(self,params):
        try:
            world = World.get_by_id(params['worldID'])
            nation = Nation.get_by_id(params['nationID'])
            user = params['user']
            ercd = 0

            if not nation.key in user.nationID:
                ercd = 5772779643207680
            elif not nation.key in world.nations:
                ercd = 5875668269137920

            return ercd

        except Exception:
            ercd = 5777752678465536
            return ercd

class Internal_GameProcess():
    '''
    classdocs
    '''
    def Game_Production(self):
        return

    def Game_Consumption(self):
        return