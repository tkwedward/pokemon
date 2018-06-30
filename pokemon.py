# strength 為六圍其中之一
# effort 為努力值
# individual 為個體值
# lv為 level
# special 為計 hp時用的
# char 是性格修正，不過性格現在還未整好
def six_value(strength, effort=0, individual=0, lv=5, special=None, char=1.0):
    if special == 'hp':
        return round(((strength*2.0 + individual + effort/4.0)*(lv/100.0)) + lv + 10.0)
    else:
        return round(((strength*2.0 + individual + effort/4.0)*(lv/100.0) + 5.0) * char)

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


[number='全國編號', name='中文名稱', atk='atk', df='df', hp='hp', spAtk='spAtk', spDf='spDf', spd='spd',   ability='特性1', type1='屬性1', type2='屬性2'
       '夢特1',  '屬性', '性別比例', '捕捉機率', '日文名稱', '特性1', '特性2', '總經驗值',],
      dtype='object')
class Pokemon(object):
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

    def __repr__(self):
        return "{}, hp為{}, 攻擊為{}, 防禦為{}, 特攻為{}, 特防為{}, 速度為{}, 種族值為{}。攻擊1為{}".format(self.name, self.hp, self.atk, self.df, self.spAtk, self.spDef, self.spd, self.strength)

    def __str__(self):
        return "{}, hp為{}, 攻擊為{}, 防禦為{}, 特攻為{}, 特防為{}, 速度為{}, 種族值為{}。攻擊1為{}".format(self.name, self.hp, self.atk, self.df, self.spAtk, self.spDef, self.spd, self.strength, self.mv1)

class Move(object):
    def __init__(self, name, damage=0, type=None, category=None, accuracy=1.0, pp=10, offset=None, special=None, m_type=None):
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
