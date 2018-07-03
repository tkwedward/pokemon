import pandas as pd
import numpy as np
from random import randint
from pkm_data.path_utility import r_path
from pokemon import Pokemon, Move


def search_move_table(name, move_table):
    """
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

def return_move_list(mv1, mv2, mv3, mv4, move_table):
    """
    arg:
    mv1, mv2, mv3, mv4︰4種招式的名稱
    move_table︰招式表

    return︰
    4招招式的list

    主要透過 search_move_table 這個 function，在招式表中找尋四招招式
    """
    a = search_move_table(mv1, move_table)
    b = search_move_table(mv2, move_table)
    c = search_move_table(mv3, move_table)
    d = search_move_table(mv4, move_table)
    return (0, a, b, c, d)

# 用來計算傷害, modifier 是天氣等等因素來計算
def cal_damage(attacker, defender, move):
    """
    args:
    attacker︰攻擊者
    defender: 防守者
    move: 攻擊者所出的 move instance

    return:
    damage_point︰扣了多少血
    """
    if float(move.damage) <0.1:
        print("{}使出了{}。".format(attacker.name, move.name))
        return 0
    else:
        targets = 1
        weather = 1
        badge = 1
        critical = 1
        random = 1
        STAB = 1.5 if move.m_type in attacker.type else 1   # 屬性加成
        Type = 1 # 相剋
        # print ("相生相剋"+str(damage_table[move.m_type].loc[defender.type[0]]))

        Burn = 1
        other = 1
        modifier = targets * weather * badge * critical * random * STAB * Type * Burn * other
        # print(int(move.damage))
        damage_point = round(((2.0 * attacker.lv /5+2.0) * float(move.damage) * attacker.atk/attacker.df /50.0 +2) * modifier)
        print("{}使出了{}, {}受了{}點傷害。".format(attacker.name, move.name,defender.name, damage_point))
        return damage_point

def attack_order(attack_team, defense_team, attack_move):
    """
    """
    if attack_team['active'].movable==False:
        pass
    else:
        defense_team['active'].hp -= cal_damage(attack_team['active'], defense_team['active'], attack_move) # 防守者減血
    loop =check_end(defense_team['active'], defense_team) # check 是否死了

    return loop


# check game 結束了嗎？
def check_end(pkm, team):
    """
    args
    pkm_hp︰pokemon 餘下多少血

    return
    loop = False，break the loop
    """
    if pkm.hp<=0.0:
        print('{}倒下了'.format(pkm.name))
        # 從隊伍中移除死了的精靈
        position = team['team_list'].index(pkm)
        team['death'].append(team['team_list'].pop(position))
        print(team)


        if len(team['team_list'])==0:
            # 如果沒有精靈了，就 end loop
            return False
        else:
            # 如果還有，那麼就選下一隻出場的 pokemon
            team['active'] = change_pokemon(team)
            team['active'].movable =False
            return True
    else:
        return True

def change_pokemon(team):
    """
    data:
    team_list: a list of pokemon
    team_list_string: the label to user about which pokemons are left in the team
    pkm_next_number: the input of the user, which tell the program that the one they want to choose.

    return:
    Next pokemon instance in the list
    """
    team_list = [ str(num)+'. '+str(pkm_name) for num, pkm_name in enumerate(team['team_list'])]
    team_list_string = ', '.join(team_list)

    if team['player']=='human':
        print('請選擇出哪一隻精靈？')
        print(team_list_string)
        pkm_next_number = int(input())
    else:
        pkm_next_number = randint(0,len(team['team_list'])-1)
        print('敵方派出了'+str(team['team_list'][pkm_next_number]))

    return team['team_list'][pkm_next_number]
