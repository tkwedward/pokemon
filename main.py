import sys
sys.path.append('/Users/mac/Desktop/projects/pokemon')
from random import randint
from pokemon import Pokemon, Move
import pkm_data.battle as battle
import pandas as pd
from pkm_data.path_utility import r_path

ability_table = pd.read_csv(r_path('/Users/mac/Desktop/projects/pokemon/ability/ability.csv'))
pokemon_table = pd.read_csv(r_path('pkm_data/pokedex/all_pkm.csv'))
move_table = pd.read_csv(r_path('pkm_data/move_table/total_move.csv'))
damage_table = pd.read_csv(r_path('pkm_data/damage_table.csv'))
damage_table.index = ['普', '格', '飛', '毒', '地', '岩', '蟲', '鬼', '鋼', '火', '水','草', '電', '超', '冰', '龍', '惡', '妖']


# 製造雙方的pokemon
pkm1 = Pokemon(155, '火球鼠', 'M', mv1='撞擊', mv2='瞪眼', mv3='煙幕', mv4='火花',  hp=39, atk=52, df=43, spAtk=60, spDef=50, spd=65, lv=25, type1='火')
pkm2 = Pokemon(152, '菊草葉', 'M', mv1='撞擊', mv2='叫聲', mv3='飛葉快刀', mv4='反射壁',  hp=39, atk=52, df=43, spAtk=60, spDef=50, spd=65, lv=25, type1='草')

#
pkm1_hp = pkm1.hp
pkm1_mv_list = battle.return_move_list(pkm1.mv1, pkm1.mv2, pkm1.mv3, pkm1.mv4)

pkm2_hp = pkm2.hp
pkm2_mv_list = battle.return_move_list(pkm2.mv1, pkm2.mv2, pkm2.mv3, pkm2.mv4)
print(pkm1_hp, pkm1_mv_list)
print(pkm2_hp, pkm2_mv_list)
loop = True

# 開始戰鬥
while(loop):
    pkm1_mv_number = randint(1, 4)
    pkm1_mv = pkm1_mv_list[pkm1_mv_number]
    pkm2_mv = None

    print('{}有{} hp.'.format(pkm1.name, pkm1_hp))
    print('{}有{} hp.'.format(pkm2.name, pkm2_hp))

    pkm2_mv_number = None
    pkm2_mv = None
    while(True):
        print('請選擇招式︰1. {}, 2. {}, 3. {}, 4. {}'.format(*pkm2_mv_list[1:5]))
        pkm2_mv_number = int(input())
        if pkm2_mv_number in list(range(1,5)):
            pkm2_mv = pkm2_mv_list[pkm2_mv_number] # user 選中的pokemon招式
            break
        else:
            print('wrong input')

    # 計算傷害，然後看game 完結了沒有
    # pkm2_mv 招式的 object instance
    if pkm1.spd>pkm2.spd:
        pkm1_hp -= battle.cal_damage(pkm1, pkm2, pkm1_mv)
        loop=battle.check_end(pkm1_hp)

        if (loop):
            pkm2_hp -= battle.cal_damage(pkm2, pkm1, pkm2_mv)
            loop=battle.check_end(pkm2_hp)

    else:
        # 攻擊者，防守者，攻擊者招數
        print(pkm2_mv.detail())
        pkm2_hp -= battle.cal_damage(pkm1, pkm2, pkm1_mv)
        loop=battle.check_end(pkm2_hp)
        #
        if (loop):
            pkm1_hp -= battle.cal_damage(pkm2, pkm1, pkm2_mv)
            loop=battle.check_end(pkm1_hp)
