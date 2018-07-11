# strength 為六圍其中之一
# effort 為努力值
# individual 為個體值
# lv為 level
# special 為計 hp時用的
# char 是性格修正，不過性格現在還未整好
def six_value(strength, effort=0, individual=0, lv=5, special=None, char=1.0):
    if special == 'hp':
        return round(((strength*2 + individual + effort/4)*(lv/100)) + lv + 10)
    else:
        return round(((strength*2 + individual + effort/4)*(lv/100) + 5) * char)

class Pokemon(object):
    def __init__(self, number, name, sex, mv1, mv2, mv3, mv4, hp, atk, df, spAtk, spDef, spd, individual=0, effort=0,  ability=None, character=None, lv=5, exp=0, status=None):
        self.name = name
        self.hp = six_value(hp, special='hp')
        self.atk =six_value(atk)
        self.df =six_value(df)
        self.spAtk =six_value(spAtk)
        self.spDef =six_value(spDef)
        self.spd =six_value(spd)
        self.sex = sex
        self.strength = hp + atk + df + spAtk + spDef + spd
        self.mv1 = move(mv1)
        self.mv2 = move(mv2)
        self.mv3 = move(mv3)
        self.mv4 = move(mv3)
        self.status = status
        self.target = None

    def __repr__(self):
        return "{}, hp為{}, 攻擊為{}, 防禦為{}, 特攻為{}, 特防為{}, 速度為{}, 種族值為{}。".format(self.name, self.hp, self.atk, self.df, self.spAtk, self.spDef, self.spd, self.strength)

class move(object):
    def __init__(self, name, damage=0, atk_type=-1.0, accuracy=1.0):
        self.name = name
        self.damage = damage*atk_type
        self.accuracy = accuracy

    def __repr__(self):
        return self.name
