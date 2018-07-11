import pandas as pd
from pkm_data.path_utility import r_path

pokemon_table = pd.read_csv(r_path('pkm_data/pokedex/all_pkm.csv'))

def search_pokemon(number, table=pokemon_table):
    row = table[table['全國編號']==number]
    name = row['中文名稱'].iloc[0]
    hp = int(row['hp'].iloc[0])
    atk = int(row['atk'].iloc[0])
    df = int(row['df'].iloc[0])
    spAtk = int(row['spAtk'].iloc[0])
    spDf = int(row['spDf'].iloc[0])
    spd = int(row['spd'].iloc[0])
    ability = row['特性1'].iloc[0]
    type1 = row['屬性1'].iloc[0]
    type2 = row['屬性2'].iloc[0]
    return Pokemon(number, name, hp, atk, df, spAtk, spDf, spd, ability, type1, type2, mv1='撞擊', mv2='流星閃沖', mv3='月亮之力', mv4='制裁光礫', lv=100)


def six_value(strength=None, effort=0, individual=0, lv=5, category=None, char=1.0):
    """
    arg:
    strength 為六圍其中之一，hp, atk, def, ...
    # effort 為努力值
    # individual 為個體值
    # lv為 level
    # special 為計 hp時用的
    # char 是性格修正，不過性格現在還未整好

    return:
    # 由種族值計算出來的 具體數值
    """
    if category == 'hp':
        return round(((strength*2.0 + individual + effort/4.0)*(lv/100.0)) + lv + 10.0)
    else:
        return round(((strength*2.0 + individual + effort/4.0)*(lv/100.0) + 5.0) * char)


class Pokemon(object):
    """ # Pokemon(object):
    number︰pokemon 的編號
    name: 名字
    sex:性別
    mv1, mv2, mv3, mv4: 四招︰
    hp, atk, df, spAtk, spDef, spd: 六圍
    individual: 個體值
    effort︰努力值
    ability: 特性
    character:性格
    lv: 等級
    exp: 經驗值
    type1:屬性1
    type2:屬性2
    state:狀態
    """
    def __init__(self, number, name, hp, atk, df, spAtk, spDef, spd, ability=None, character=None, individual=0, effort=0, lv=5, exp=0 , type1=None, type2=None, status=None, sex='M', mv1=None, mv2=None, mv3=None, mv4=None):
        self.number = number
        self.name = name
        self.hp = six_value(hp, lv=lv, category='hp')
        self.atk =six_value(atk, lv=lv)
        self.df =six_value(df, lv=lv)
        self.spAtk =six_value(spAtk, lv=lv)
        self.spDef =six_value(spDef, lv=lv)
        self.spd =six_value(spd, lv=lv)
        self.strength_list = {'hp':self.hp, 'atk':self.atk, 'df':self.df, 'spAtk': self.spAtk, 'spDef': self.spDef, 'spd':self.spd}
        self.sex = sex
        self.total_strength = hp + atk + df + spAtk + spDef + spd
        self.mv1 = mv1
        self.mv2 = mv2
        self.mv3 = mv3
        self.mv4 = mv4
        self.lv = lv
        self.type = (type1, type2)
        self.ability = ability


        # 戰鬥用
        self.counter = 0
        self.team = None # 這隻精靈的隊伍
        self.opponent_team = None # 敵方精靈的隊伍
        self.identity = None # 我方或是敵方
        self.event = None # 戰鬥時的 event_dict

        self.status = None # 進入戰鬥時有沒有異常狀態
        self.movable = True # 可以戰鬥嗎？
        self.move_list = None # 招數表
        self.active_pkm_list = None # 所有active 的pkm
        self.round_move = None # 這round 用甚麼招數
        self.target = None # 這 round 的目標是誰
        self.attacked_by = None # 被誰攻擊了
        self.attacked_move = None # 被甚麼 攻擊招數攻擊到

        self.ability_parameter_1 = None # ability 的 parameter, 可能是 rain, 或是上升能力的 parameter
        self.ability_parameter_2 = None # ability 的 parameter, 可能是 rain, 或是上升能力的 parameter

    def __repr__(self):
        # return "{}".format(self.name)
        return "{}".format(self.name)

    def __str__(self):
        return "{}".format(self.name)

    def pkm_status_report(self):
        return "{}, hp為{}, 攻擊為{}, 防禦為{}, 特攻為{}, 特防為{}, 速度為{}。".format(self.name, self.hp, self.atk, self.df, self.spAtk, self.spDef, self.spd)

class Move(object):
    """
    name︰pokemon名稱
    damage: 招式的傷害值
    category: 招式是物理、特殊、還是變化
    accuracy: 招式命中率
    pp: 招式的 power point
    offset: 是否先制
    special: 有沒有特殊效果
    m_type: 招式的屬性
    """
    def __init__(self, name, damage=0, category=None, accuracy=1.0, pp=10, offset=None, special=None, m_type=None):
        self.name = name
        self.category = category #這是變化、物理或特殊類形
        self.damage = damage
        self.accuracy = accuracy
        self.pp = pp
        self.offset = offset #是否先制技
        self.special = special # 有沒有特殊效果
        self.m_type = m_type # move type, 即是招式屬性

    def __repr__(self):
        return self.name
    def __str__(self):
        return self.name
    def detail(self):
        return "招式名字:{}, 招式威力:{}".format(self.name, self.damage)
