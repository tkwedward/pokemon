import copy
import pandas as pd
import numpy as np
from random import randint
from pkm_data.path_utility import r_path
from pokemon import Pokemon, Move
from pkm_data.status import BURN, FROZEN, PARALYZE, POISON
from pkm_data.general_function import check_end

"""
data:
    move_table = csv file 轉換成 dataframe

function:
- search_move_table(name, move_table=move_table):
    目的︰從 move_table 整一個 move instance
- return_move_list(mv1, mv2, mv3, mv4)
    目的︰返回 pkm 的招數表
- cal_damage(attacker, defender, move):
    目的︰用來計算傷害, modifier 是天氣等等因素來計算
- attack_order
    目的︰check 精靈狀態和是否能夠出招
- choose_move:
    目的︰選擇攻擊招數和攻擊目標
"""

move_table = pd.read_csv(r_path('pkm_data/move_table/total_move.csv'))


def search_move_table(name, move_table=move_table):
    """
    目的︰從 move_table 整一個 move instance

    arg:
    name: 招式的名稱
    move_table: 招式表

    return:
    Move 的 instance
    """

    row = move_table[move_table['中文名']==name]
    # category = row['類型'].iloc[0] #這是變化、物理或特殊類形
    category = '變化' #這是變化、物理或特殊類形
    damage = row['威力'].iloc[0]
    accuracy = row['命中'].iloc[0]
    pp = row['PP/上限'].iloc[0]
    offset = row['先制'].iloc[0] #是否先制技
    m_type = row['type'].iloc[0]
    special =None # 有沒有特殊效果
    return Move(name, category=category, damage=damage, accuracy=accuracy, pp=pp, offset=offset, special=special, m_type=m_type)



def return_move_list(mv1, mv2, mv3, mv4):
    """
    目的︰返回 pkm 的招數表

    arg:
    mv1, mv2, mv3, mv4︰4種招式的名稱

    return︰
    4招招式的list

    主要透過 search_move_table 這個 function，在招式表中找尋四招招式
    """
    a = search_move_table(mv1)
    b = search_move_table(mv2)
    c = search_move_table(mv3)
    d = search_move_table(mv4)
    return (0, a, b, c, d)

def cal_damage(attacker, defender):
    """
    目的︰用來計算傷害, modifier 是天氣等等因素來計算

    args:
    attacker︰攻擊者
    defender: 防守者
    attacker.round_move: 攻擊者所出的 move instance

    return:
    damage_point︰扣了多少血
    """
    if float(attacker.round_move.damage) <0.1:
        print("{}使出了{}。".format(attacker.name, attacker.round_move.name))
        return 0
    else:
        targets = 1
        weather = 1
        badge = 1
        critical = 1
        random = 1
        STAB = 1.5 if attacker.round_move.m_type in attacker.type else 1   # 屬性加成
        Type = 1 # 相剋
        # print ("相生相剋"+str(damage_table[move.m_type].loc[defender.type[0]]))

        Burn = 1
        other = 1
        modifier = targets * weather * badge * critical * random * STAB * Type * Burn * other
        # print(int(move.damage))
        damage_point = round(((2.0 * attacker.lv /5+2.0) * float(attacker.round_move.damage) * attacker.atk/attacker.df /50.0 +2) * modifier)
        print("{}{}使出了{}, {}{}受了{}點傷害。".format(attacker.identity, attacker.name, attacker.round_move.name, defender.identity, defender.name, damage_point))
        return damage_point

def check_status_damage(pkm, *status_list):
    """
    用來 loop 各種 status 的傷害
    """
    for status in status_list:
        if isinstance(pkm.status, status):
            try:
                pkm.movable =  status.damage(pkm)
            except AttributeError:
                print(pkm.movable)

def check_status_effect(pkm, *status_list):
    """
    用來 loop 各種 status 的 effect
    """
    for status in status_list:
        if isinstance(pkm.status , status):
            try:
                pkm.movable =  status.battle_effect(pkm)
            except AttributeError:
                print(pkm.movable)

def attack_order(attack_pkm, defense_pkm):
    """
    目的︰check 精靈狀態和是否能夠出招
    input:
    - attack_pkm: 攻擊者
    - defense_pkm: 防守者

    attack_team: 攻擊者的 team object
    10 用 check_status_effect check 麻痺, 燒傷, 凍傷的效果
    30 chekc attack pokemon 是否 movable
    40 call cal_damage function，計算傷害

    """
    # 1. check attack pkm 是否有麻痺
    check_status_effect(attack_pkm, PARALYZE, FROZEN, BURN)

    if attack_pkm.movable==False:
        pass
    else:
        defense_pkm.hp -= cal_damage(attack_pkm, defense_pkm) # 防守者減血
    loop =check_end(defense_pkm) # check 是否死了

    return loop


def choose_move(pkm):
    """
    目的︰選擇攻擊招數和攻擊目標

    input:
    pkm: 想讓那一隻 pkm 出招
    pkm.mv_list: 這隻 pkm 的 attack list
    pkm2_mv_number: 出哪一招的number
    pkm2_mv: 出哪一招的
    target_list: 被攻擊的 pokemon list

    processing:
    10 print 出招數
    20 讓 user 選擇出哪一招
    30 整一個target_list
    35 在 target_list 選擇攻擊哪一隻精靈
    40 在pkm 上加上 attribute: round_move 和 target(list)

    """
    while(True):
        print('我方{} 請選擇招式︰1. {}, 2. {}, 3. {}, 4. {}'.format(str(pkm), *pkm.move_list[1:5]))
        pkm2_mv_number = int(input())
        if pkm2_mv_number in list(range(1,5)):
            pkm.round_move = pkm.move_list[pkm2_mv_number] # user 選中的pokemon招式
            break
        else:
            print('wrong input')

    # 選擇攻擊哪一隻 pkm
    # pkm 為要選擇目標的精靈
    # pkm_index 為現在這隻 pkm 在 active_pkm_list 中的index, 用途是找出它，並 delete
    while(True):
        # active_pkm_list = pkm.active_pkm_list
        # pkm_index = active_pkm_list.index(pkm)
        # active_pkm_list.pop(pkm_index)
        print(pkm.active_pkm_list)
        print('請選擇目標︰ '+ ', '.join(["{}. {}".format(index+1, str(item)) for index, item in enumerate(pkm.active_pkm_list)])) # 將 list 化為 str
        pkm2_target_number = int(input())

        try:
            if pkm2_target_number in list(range(0,4)):
                pkm2_target = pkm.active_pkm_list[pkm2_target_number-1] # user 選中的pokemon招式
                pkm.target = pkm2_target # user 選中的pokemon招式
                break
            else:
                print('wrong input')
        except:
            print('wrong input')
