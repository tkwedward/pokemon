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
def check_end(pkm):
    """
    args
    pkm_hp︰pokemon 餘下多少血
    active_index: 在active_index list 中 pkm 的位置

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
        try:
            print('{} hp = 0, {}倒下了'.format(pkm.name, pkm.name))
            pkm.movable = False
            index = pkm.team['team_list'].index(pkm)
            pkm.team['team_list'].pop(index)
            # 30 將這隻死了的 pkm 放進 death list 中
            pkm.team['death'].append(pkm)

            # 40 如果 list length = 0，那麼結束；否則就換精靈
            if len(pkm.team['team_list'])==0:
                return False
            else:
                # 取得原本active 的位置，轉成另一隻精靈
                active_index = pkm.team['active'].index(pkm)
                pkm.team['active'][active_index] = change_pokemon(pkm)
                print(pkm.team)
                pkm.team['active'][active_index].movable =False
                return True
        except ValueError:
            print('沒有index')
    else:
        return True


def change_pokemon(pkm):
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
    team_list = [ str(num)+'. '+str(pkm_name) for num, pkm_name in enumerate(pkm.team['team_list'])]
    team_list_string = ', '.join(team_list)

    # 20 將精靈回復原本的能力值
    pkm.atk = pkm.strength_list['atk']
    pkm.df = pkm.strength_list['df']
    pkm.spAtk = pkm.strength_list['spAtk']
    pkm.spDef = pkm.strength_list['spDef']
    pkm.spd = pkm.strength_list['spd']

    # 30 選擇出哪隻精靈
    if len(pkm.team['team_list'])>0:
        if pkm.team['player']=='human':

            print('請選擇出哪一隻精靈？')
            print(team_list_string)
            pkm_next_number = int(input())

        else:
            pkm_next_number = randint(0,len(pkm.team['team_list'])-1)
            print(pkm_next_number, pkm.team['team_list'])
            print('敵方派出了'+str(pkm.team['team_list'][pkm_next_number]))
    else:
        print(pkm.identity+'輸了')
        loop=False
        return False

    return pkm.team['team_list'][pkm_next_number]

def loop_pokemon(team_list):
    for pkm in team_list:
        print(pkm.ability)

def loop_active_list(team_list, *attribute_pair, print_out=False):
    """
    目的:
        用來在 pokemon 身上加入一些 attribute，例如在 pkm 中加入 (status, 麻痺)
    input:
        team_list = 要 loop 的pokemon list
        attribute_pair = 一個 tuple: (attribute: value)
    processing:
    """
    for pkm in team_list:
        for pair in attribute_pair:
            setattr(pkm, pair[0], pair[1])
            if print_out:
                print("{}的{}是{}".format(pkm, pair[0], getattr(pkm, pair[0])))

def loop_list_function(team, *functions):
    """
    目的: 用來apply function to 一個 list 中每一個 element，例如想每一隻 pkm 都中毒
    - team 為 team['active']
    - 在 pkm_battle 中的 choose_move
    """
    for member in team:
        for function in functions:
            function(member)
