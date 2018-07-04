import copy
from random import randint

def Probability(percentage):
    """
    arg:
        percent: percentage in %
    data:
        num: 代表著從 1 - 100 中抽中哪個數字
    return:
        probability in decimal
    """
    num = randint(1,100)
    if num <= percentage*100:
        return True
    else:
        return False

# check game 結束了嗎？
def check_end(pkm, team):
    """
    args
    pkm_hp︰pokemon 餘下多少血

    process:
    10 check hp 是否少於 0, 如果少於0, print 精靈倒下了，然後嘗試從隊伍中抽走這隻pokemon
    30 將這隻死了的 pkm 放進 death list 中

    40 如果 pkm list length = 0，那麼結束；否則就換精靈
    50 換精靈時，要將 這隻精靈的 movable 改成 False，否則就會換精靈後繼續出招

    return
    loop = False，break the loop
    """
    # 10 check hp 是否少於 0, 如果少於0, print 精靈倒下了，然後嘗試從隊伍中抽走這隻pokemon
    if pkm.hp<=0.0:
        print('{} hp = 0, {}倒下了'.format(pkm.name, pkm.name))
        # 30 將這隻死了的 pkm 放進 death list 中
        try:
            index = team['team_list'].index(pkm)
            print('隊伍編號{}'.format(index))
            print(team)
            team['death'].append(team['team_list'].pop(index))
            print(team)
        except ValueError:
            pass

        # 40 如果 list length = 0，那麼結束；否則就換精靈
        if len(team['team_list'])==0:
            return False
        else:
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

    processing:
    10 將team_list print 出來
    20 將精靈回復原本的能力值
    30 選擇出哪隻精靈
    40 return 出被選的精靈

    return:
    Next pokemon instance in the list
    """
    # 10 將team_list print 出來
    team_list = [ str(num)+'. '+str(pkm_name) for num, pkm_name in enumerate(team['team_list'])]
    team_list_string = ', '.join(team_list)

    # 20 將精靈回復原本的能力值
    pkm.atk = pkm.strength_list['atk']
    pkm.df = pkm.strength_list['df']
    pkm.spAtk = pkm.strength_list['spAtk']
    pkm.spDf = pkm.strength_list['spDf']
    pkm.spd = pkm.strength_list['spd']

    # 30 選擇出哪隻精靈
    if team['player']=='human':
        print('請選擇出哪一隻精靈？')
        print(team_list_string)
        pkm_next_number = int(input())
    else:
        pkm_next_number = randint(0,len(team['team_list'])-1)
        print('敵方派出了'+str(team['team_list'][pkm_next_number]))

    return team['team_list'][pkm_next_number]
