import pandas as pd
import numpy as np
from pkm_data.path_utility import r_path
from pokemon import Pokemon, Move


def search_move_table(name):
    row = move_table[move_table['中文名']==name]
    category = row['類型'].iloc[0] #這是變化、物理或特殊類形
    damage = row['威力'].iloc[0]
    accuracy = row['命中'].iloc[0]
    pp = row['PP/上限'].iloc[0]
    offset = row['先制'].iloc[0] #是否先制技
    m_type = row['type'].iloc[0]
    special =None # 有沒有特殊效果
    return Move(name, category=category, damage=damage, accuracy=accuracy, pp=pp, offset=offset, type=type, special=special, m_type=m_type)

def return_move_list(mv1, mv2, mv3, mv4):
    a = search_move_table(mv1)
    b = search_move_table(mv2)
    c = search_move_table(mv3)
    d = search_move_table(mv4)
    return (0, a, b, c, d)

# 用來計算傷害, modifier 是天氣等等因素來計算
def cal_damage(attacker, defender, move):
    if float(move.damage) <0.1:
        print("{}使出了{}。".format(attacker.name, move.name))
        return 0
    else:
        targets = 1
        weather = 1
        badge = 1
        critical = 1
        random = 1
        STAB = 1
        if move.m_type in attacker.type:
            STAB = 1.5 # 招式屬性加成
        Type = 1 # 相剋
        # print ("相生相剋"+str(damage_table[move.m_type].loc[defender.type[0]]))

        Burn = 1
        other = 1
        modifier = targets * weather * badge * critical * random * STAB * Type * Burn * other
        # print(int(move.damage))
        damage_point = round(((2.0 * attacker.lv /5+2.0) * float(move.damage) * attacker.atk/attacker.df /50.0 +2) * modifier)
        print("{}使出了{}, {}受了{}點傷害。".format(attacker.name, move.name,defender.name, damage_point))
        return damage_point

# check game 結束了嗎？
def check_end(pkm_hp):
    print(pkm_hp)
    if pkm_hp<=0.0:
        print('game finish')
        return False
    else:
        return True
