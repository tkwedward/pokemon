
def six_value(strength, effort=0, individual=0, lv=5, special=None, char=1.0):
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
    if special == 'hp':
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
    def __init__(self, number, name, hp, atk, df, spAtk, spDef, spd,   ability=None, character=None, individual=0, effort=0, lv=5, exp=0 , type1=None, type2=None, state=None, sex='M', mv1=None, mv2=None, mv3=None, mv4=None):
        self.number = number
        self.name = name
        self.hp = six_value(hp, lv=lv, special='hp')
        self.atk =six_value(atk, lv=lv)
        self.df =six_value(df, lv=lv)
        self.spAtk =six_value(spAtk, lv=lv)
        self.spDef =six_value(spDef, lv=lv)
        self.spd =six_value(spd, lv=lv)
        self.sex = sex
        self.strength = hp + atk + df + spAtk + spDef + spd
        self.mv1 = mv1
        self.mv2 = mv2
        self.mv3 = mv3
        self.mv4 = mv4
        self.lv = lv
        self.type = (type1, type2)
        self.movable = True # 可以戰鬥嗎？

    def __repr__(self):
        # return "{}".format(self.name)
        return "{}".format(self.name)

    def __str__(self):
        return "{}".format(self.name)
        # return "{}, hp為{}, 攻擊為{}, 防禦為{}, 特攻為{}, 特防為{}, 速度為{}, 種族值為{}。".format(self.name, self.hp, self.atk, self.df, self.spAtk, self.spDef, self.spd, self.strength)

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
