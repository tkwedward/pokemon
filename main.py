import sys
sys.path.append('/Users/mac/Desktop/projects/pokemon')
import pandas as pd
from random import randint

# 製造 Pokemon 和 Move 的 instance
from pokemon import Pokemon, Move

# 用它的招式搜查和 計算傷害點數
# 用了 battle.cal_damage 和 return_move_list
from pkm_data.battle import attack_order, return_move_list

# 找出哪一隻 pkm
from pkm_data.data_search import search_pokemon

# 用來整完整的 path
from pkm_data.path_utility import r_path




"""
ability_table︰是引入pokemon 特性的 csv table
pokemon_table︰是引入802隻 pokemon 資料的 csv table
move_table︰引入所有招式的table
damage_table︰屬性相剋表
"""
ability_table = pd.read_csv(r_path('pkm_data/ability/ability.csv'))
pokemon_table = pd.read_csv(r_path('pkm_data/pokedex/all_pkm.csv'))
move_table = pd.read_csv(r_path('pkm_data/move_table/total_move.csv'))
damage_table = pd.read_csv(r_path('pkm_data/damage_table.csv'))
damage_table.index = ['普', '格', '飛', '毒', '地', '岩', '蟲', '鬼', '鋼', '火', '水','草', '電', '超', '冰', '龍', '惡', '妖']

"""
team1: 隊伍一的精靈, team1_dead: 隊伍死了的精靈
team2: 隊伍一的精靈, team2_dead: 隊伍死了的精靈
"""

team1 = {'active':None,
         'team_list': [search_pokemon(number=randint(1, 802), table=pokemon_table) for x in range(1,7)],
         'death':[],
         'player': 'computer'
         }


team2 =  {'active':None,
         'team_list': [search_pokemon(number=randint(1, 802), table=pokemon_table) for x in range(1,7)],
         'death':[],
         'player': 'human'
         }
print('隊伍1中有')
print(team1)
print('隊伍2中有')
print(team2)
team1['active'] = team1['team_list'][0]
team2['active'] = team2['team_list'][0]




# 將 pokemon 的 hp數值放進 pkm1_hp 的variable 當中，戰鬥時的傷害是利用這個數字作計算
# pkm1_mv_list 是利用 招式 的名字，透過 return_move_list 來返回 pkm 4招的資料

pkm1_mv_list = return_move_list(team1['active'].mv1, team1['active'].mv2, team1['active'].mv3, team1['active'].mv4, move_table)


pkm2_mv_list = return_move_list(team2['active'].mv1, team2['active'].mv2, team2['active'].mv3, team2['active'].mv4, move_table)
loop = True

# 開始戰鬥
while(loop):
    # pkm1 是敵方，這裏是抽取一個 random 數字作為招式 選擇
    team1['active'].movable = True
    team2['active'].movable = True

    pkm1_mv_number = randint(1, 4)
    pkm1_mv = pkm1_mv_list[pkm1_mv_number]
    pkm2_mv = None

    #戰鬥中顯示雙方有多少 hp 餘下
    print('敵方{}有{} hp.'.format(team1['active'].name, team1['active'].hp))
    print('{}有{} hp.'.format(team2['active'].name, team2['active'].hp))

    # pkm2_mv_number 是 1-4，由玩家輸入
    # pkm2_mv 是選擇用哪一種招式
    pkm2_mv_number = None
    pkm2_mv = None

    # 玩家輸入資料
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
    if team1['active'].spd>team2['active'].spd:
        """
        attack_order(攻擊者, 防守者)
        """
        loop = attack_order(team1, team2, pkm1_mv)
        if (loop):
            loop=attack_order(team2, team1, pkm2_mv)
    else:
        # 攻擊者，防守者，攻擊者招數
        loop=attack_order(team2, team1, pkm2_mv)
        # 查看戰鬥結束了沒有
        if (loop):
            loop = attack_order(team1, team2, pkm1_mv)
