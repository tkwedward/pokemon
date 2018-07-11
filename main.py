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
from pkm_data.pkm_battle import attack_order, return_move_list, choose_move, check_status_damage
from pkm_data.general_function import Probability, check_end, loop_active_list, loop_list_function, loop_pokemon

# 用來整完整的 path
from pkm_data.path_utility import r_path
from pkm_data.ability import CHANGE_WEATHER

from pkm_data.status import BURN, FROZEN, PARALYZE, POISON, BADLY_POISON
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
BATTLE_TYPE = 1

#team1: 隊伍一的精靈, team1_dead: 隊伍死了的精靈
#team2: 隊伍一的精靈, team2_dead: 隊伍死了的精靈
team1 = {
         # 'team_list': [search_pokemon(150), search_pokemon(150), search_pokemon(150), search_pokemon(150), search_pokemon(150), search_pokemon(150)],

         'team_list': [search_pokemon(number=randint(1, 802)) for x in range(1,7)],
         'death':[],
         'player': 'computer'
         }

team2 =  {
         'team_list': [search_pokemon(number=randint(1, 802)) for x in range(1,7)],
         'death':[],
         'player': 'human'
         }



team1['active'] = [ team1['team_list'][x] for x in range(0, BATTLE_TYPE) ]
team2['active'] = [ team2['team_list'][x] for x in range(0, BATTLE_TYPE) ]
# one on one

print('隊伍1中有'+' ,'.join([str(pkm) for pkm in team1['team_list']]))
print('隊伍2中有'+' ,'.join([str(pkm) for pkm in team2['team_list']]))

# pkm_status_report
"""
將 Attribute 加入去 pokemon 之中
"""
# 將 pokemon 的 hp數值放進 pkm1_hp 的variable 當中，戰鬥時的傷害是利用這個數字作計算
# pkm1_mv_list 是利用 招式 的名字，透過 return_move_list 來返回 pkm 4招的資料
pkm1_mv_list = return_move_list(team1['active'][0].mv1, team1['active'][0].mv2, team1['active'][0].mv3, team1['active'][0].mv4)

pkm2_mv_list = return_move_list(team2['active'][0].mv1, team2['active'][0].mv2, team2['active'][0].mv3, team2['active'][0].mv4)

event_dict = {
            'event_list':[],
            'ability_list':[],
            'weather': None,

        } # 事件觸發計算器

# 用來在 pokemon 之中加入 status (異常狀態) 和 round_move(招數) = None，一開始沒有任何 異常狀態 和一開始沒有選擇 招數
loop_active_list(team1['team_list'],
                ('status', None),
                ('round_move', None),
                ('target', None),
                ('identity', '敵方'),
                ('team', team1),
                ('opponent_team', team2),
                ('event', event_dict)
                )
loop_active_list(team2['team_list'],
                ('status', None),
                ('round_move', None),
                ('target', None),
                ('identity', '我方'),
                ('team', team2),
                ('opponent_team', team1),
                ('event', event_dict)
                )

# 這裏 print 出 招式表
loop_active_list(team1['team_list'],
                ('move_list', pkm1_mv_list),
                print_out=False # print out move_list
                )
loop_active_list(team2['team_list'],
                ('move_list', pkm1_mv_list),
                print_out=False # print out move_list
                )
print('\n隊伍1')
for x in team1['team_list']:
    print(x.pkm_status_report())

print('\n隊伍2')
for x in team2['team_list']:
    print(x.pkm_status_report())



loop = True


"""
戰鬥前的效果
"""

team2['active'][0].status = BADLY_POISON()
team1['active'][0].status = BURN()



# 測試求雨的行，某隻精靈發動了求雨

CHANGE_WEATHER('求雨').effect(team2['active'][0])
print(team2['active'][0].event)

# for 雙打的, 用 exception 是因為單打時會出現錯誤
try:
    team1['active'][1].status = FROZEN()
    team2['active'][1].status = POISON()
except:
    pass

ROUND = 1

while(loop):

    """
    # Stage 0 開始戰鬥
    attack_order_list = 按 active pkm 速度而排列的 list

    - 每一 round +1
    - print 出下雨等狀態
    - 將 pkm 的 movable 變為 True
    - 出一個 active_pkm_list
    """

    def STAGE_ZERO_ABILITY():
        pass

    print('ROUND '+str(ROUND))
    event_dict['weather'].effect()
    print(event_dict['weather'].count)
    ROUND+=1
    print('\n# Stage 0 開始戰鬥')


    # for event in event_count:
    #     event.count-=1
    #     if event.count==0:
    #         print(str(event)+"完結了")
    #     else:
    #         print("正在"+str(event))



    # 整一個 active_pkm_list, 並先比較pkm 的speed
    active_pkm_list = team1['active'] + team2['active']
    attack_order_list = sorted(active_pkm_list, key=lambda x: x.hp, reverse=False)
    print(attack_order_list)

    loop_pokemon(attack_order_list)

    # 將team1['movable'] reset 為 True, 加入active_pkm_list
    loop_active_list(team1['team_list'],
                    ('movable', True),
                    ('active_pkm_list', active_pkm_list)
                    )
    loop_active_list(team2['team_list'],
                    ('movable', True),
                    ('active_pkm_list', active_pkm_list)
                    )

    #戰鬥中顯示雙方有多少 hp 餘下
    for x in range(0,len(team1['active'])):
        print('敵方{} {}有{} hp.'.format(x, team1['active'][x].name, team1['active'][x].hp))
    for x in range(0,len(team2['active'])):
        print('我方{} {}有{} hp.'.format(x, team2['active'][x].name, team2['active'][x].hp))



    """
    Stage 1: player 選擇attack, change pkm, use tool or escape?

    """
    print('\n# Stage 1: 選擇攻擊、轉精靈、使用道具或逃跑')
    # 玩家輸入資料
    while(True):
        print('請選擇招式︰1. 攻擊, 2. 替換精靈, 3. 使用道具, 4. 逃走')
        player_choice = int(input())
        if player_choice==1:
            break
        else:
            print('wrong input')

    """
    Stage 2: 選擇出甚麼招數, 並向哪一隻 pkm 攻擊
    pkm1_mv_list = pokemon 的 move list
    pkm1_mv_number = 選擇一個 random number
    pkm1_mv = 在 pkm1_mv_list 中找其中一招

    3. 在 pkm 之中加入一個叫 target 的 attribute
    """
    print('\n# Stage 2︰選擇攻擊招數和攻擊對像')
    # 電腦選招
    for index, pkm in enumerate(team1['active']):
        # pkm.opponent_team['active'] = 敵方的list
        target_list = pkm.opponent_team['active']

        # pkm_index = target_list.index(pkm)
        # target_list.pop(pkm_index)

        pkm_mv_number = randint(1, 4)
        pkm_target_number = randint(0, len(target_list)-1)

        pkm.round_move = pkm1_mv_list[pkm_mv_number]
        pkm.target = target_list[pkm_target_number]


    # 玩家選招
    pkm2_mv_number = None
    pkm2_mv = None
    loop_list_function(team2['active'], choose_move)

    # choose_move(team2['active'][0], pkm2_mv_list, active_pkm_list)



    """
    Stage 3. 計算傷害
    pkm.target = 這隻 pokemon 的目標
    pkm.round_move = 這 round pokemon 使用的招數。

    active_pkm_list = 一個list 將所有 active 的 pkm 放在一起
    attack_order_list = 一個list 將所有 pkm 的 speed 排序
    1. 先整一個 attack order list
    2. 按著 attack list 來決定攻擊誰
    3. loop 在 attack_order_list 的每一隻 pkm，如果 loop 是 True 的，就進行用 attack_order 來
    """
    print('\n# Stage 3︰計算傷害')
    # 計算傷害，然後看game 完結了沒有
    # pkm2_mv 招式的 object instance



    for pkm in attack_order_list:
        if loop==True:
            loop = attack_order(pkm, pkm.target)


    """
    Stage 4. 準備結束
    10 Check 中毒效果
    20 Check 猛毒效果
    30 Check 能否解凍
    40 Check 沙暴損害

    """
    print('\n# Stage 4')
    # 10 Check 中毒效果



    # loop 每一隻 active 了的 pkm
    for pkm in active_pkm_list:
        check_status_damage(pkm, POISON, BADLY_POISON, FROZEN)


    print('----------------------------------')
