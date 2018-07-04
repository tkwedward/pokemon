import sys
sys.path.append('/Users/mac/Desktop/projects/pokemon')
print(sys.path)
import pandas as pd
from random import randint
print(__file__)
# 製造 Pokemon 和 Move 的 instance, 找出哪一隻 pkm
from pokemon import Pokemon, Move, search_pokemon
# 用它的招式搜查和 計算傷害點數
# 用了 battle.cal_damage 和 return_move_list
from pkm_data.pkm_battle import attack_order, return_move_list
from pkm_data.general_function import Probability, check_end

# 用來整完整的 path
from pkm_data.path_utility import r_path


from pkm_data.status import BURN, FROZEN, PARALYZE, POISON, BADLY_POISON, Event
from pkm_data.weather import RAIN, HEAVY_RAIN, SUNNY, HARSH_SUNLIGHT, HAIL, SANDSTORM, STRONG_WIND




"""
ability_table︰是引入pokemon 特性的 csv table
pokemon_table︰是引入802隻 pokemon 資料的 csv table
move_table︰引入所有招式的table
damage_table︰屬性相剋表
"""
ability_table = pd.read_csv(r_path('pkm_data/ability/ability.csv'))


damage_table = pd.read_csv(r_path('pkm_data/damage_table.csv'))
damage_table.index = ['普', '格', '飛', '毒', '地', '岩', '蟲', '鬼', '鋼', '火', '水','草', '電', '超', '冰', '龍', '惡', '妖']

"""
Data:
- weather (string): 天氣,

- team(dictionary): 隊伍的 dictionary, 裏面有active, team_list 和 death三個list, 還有 player 是電腦還是人類

- player_choice(integer): 在該會合中，player 在四種選擇中選出一個, valid value:0-3
- pkm1_mv_list: team1 出場精靈的招數表
- pkm2_mv_list: team2 出場精靈的招數表

- event_count: 一個list, 記住會發生甚麼事情
"""

"""
戰鬥準備︰選擇精靈，找招數
"""
#team1: 隊伍一的精靈, team1_dead: 隊伍死了的精靈
#team2: 隊伍一的精靈, team2_dead: 隊伍死了的精靈
team1 = {'active':None,
         'team_list': [search_pokemon(150), search_pokemon(150), search_pokemon(150), search_pokemon(150), search_pokemon(150), search_pokemon(150)],
         # 'team_list': [search_pokemon(number=randint(1, 802), table=pokemon_table) for x in range(1,7)],
         'death':[],
         'player': 'computer'
         }

team2 =  {'active':None,
         'team_list': [search_pokemon(number=randint(1, 802)) for x in range(1,7)],
         'death':[],
         'player': 'human'
         }

# one on one
team1 = {'active':None,
         'team_list': [search_pokemon(150), ],
         # 'team_list': [search_pokemon(number=randint(1, 802), table=pokemon_table) for x in range(1,7)],
         'death':[],
         'player': 'computer'
         }

team2 =  {'active':None,
         'team_list': [search_pokemon(248)],
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
pkm1_mv_list = return_move_list(team1['active'].mv1, team1['active'].mv2, team1['active'].mv3, team1['active'].mv4)


pkm2_mv_list = return_move_list(team2['active'].mv1, team2['active'].mv2, team2['active'].mv3, team2['active'].mv4)

loop = True


"""
戰鬥前的效果
"""
event_count = [Event('下雨', '天氣', 5)] # 事件觸發計算器
team2['active'].status = BADLY_POISON()
team1['active'].status = FROZEN()
WEATHER = SANDSTORM()

while(loop):
    """
    # Stage 0 開始戰鬥
    """
    print('# Stage 0 開始戰鬥')
    for event in event_count:
        event.count-=1
        if event.count==0:
            print(str(event)+"完結了")
        else:
            print("正在"+str(event))
    # pkm1 是敵方，這裏是抽取一個 random 數字作為招式 選擇
    team1['active'].movable = True
    team2['active'].movable = True
    #戰鬥中顯示雙方有多少 hp 餘下
    print('敵方{}有{} hp.'.format(team1['active'].name, team1['active'].hp))
    print('{}有{} hp.'.format(team2['active'].name, team2['active'].hp))

    """
    Stage 1: player 選擇attack, change pkm, use tool or escape?

    """
    print('# Stage 1')
    # 玩家輸入資料
    while(True):
        print('請選擇招式︰1. 攻擊, 2. 替換精靈, 3. 使用道具, 4. 逃走')
        player_choice = int(input())
        if player_choice==1:
            break
        else:
            print('wrong input')

    """
    Stage 2: 選擇出甚麼招數
    """
    print('# Stage 2')
    # 電臘選招
    pkm1_mv_number = randint(1, 4)
    pkm1_mv = pkm1_mv_list[pkm1_mv_number]
    pkm2_mv = None


    # 玩家選招
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

    """
    Stage 3. 計算傷害
    """
    print('# Stage 3')
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

    """
    Stage 4. 準備結束
    10 Check 中毒效果
    20 Check 猛毒效果
    30 Check 能否解凍
    40 Check 沙暴損害

    """
    print('# Stage 4')
    # 10 Check 中毒效果
    if isinstance(team1['active'].status, POISON):
        POISON.damage(team1['active'], team1)
    if isinstance(team2['active'].status, POISON):
        POISON.damage(team2['active'], team2)

    # 20 Check 猛毒效果
    if isinstance(team1['active'].status, BADLY_POISON):
        BADLY_POISON.damage(team1['active'], team1)
    if isinstance(team2['active'].status, BADLY_POISON):
        BADLY_POISON.damage(team2['active'], team2)

    # 30 Check 能否解凍
    if isinstance(team1['active'].status, FROZEN):
        FROZEN.heal(team1['active'])
    if isinstance(team2['active'].status, FROZEN):
        FROZEN.heal(team2['active'])

    # 40 Check 沙暴損害
    if isinstance(WEATHER, SANDSTORM):
        WEATHER.damage(pkm=team1['active'], team=team1)
    if isinstance(WEATHER, SANDSTORM):
        WEATHER.damage(pkm=team2['active'], team=team2)

    print('----------------------------------')
