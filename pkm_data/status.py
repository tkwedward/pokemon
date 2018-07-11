import pandas as pd
import numpy as np
from random import randint
from pkm_data.general_function import Probability, check_end
from pkm_data.path_utility import r_path
from pokemon import Pokemon, Move

class FEAR(object):
    name = "畏懼"
    def effect(pkm):
        pkm.target.movable =
        print("{}{}畏懼，無法使出招式。".format(pkm.identity, pkm.name))

class BURN(object):
    """
    class BURN
    problem: 要在pokemon中加入一個full hp的計量

    data:
    pkm︰受了燒傷的pokemon

    attribute:
    name = 中文名稱
    effect = 效果解說

    method:
    strength_effect(pkm = 燒傷了的 pokemon)
        令 pkm 的 atk 下降了 50%
        return None

    damage(pkm = 燒傷了的 pokemon)
        計算被燒傷了的 damage，並出燒傷了要扣血的 message
        return None
    """
    name="燒傷"

    def strength_effect(pkm):
        return pkm.strength_list['atk'] * 0.50

    def damage(pkm):
        burn_damage = int(pkm.fullHP*1/16.0)
        pkm.hp -= burn_damage
        print("{}因為被燒傷，扣了{}血".format(pkm.name, burn_damage))

class FROZEN(object):
    """
    class FROZEN
    - inherent from: object
    attribute:
    name = 中文名稱
    effect = 效果解說

    method:
    - battle_effect(pkm = 凍傷了的 pokemon)
        令 pkm 無法移動

    - heal(pkm = 凍傷了的 pokemon)
        pkm 的 object 變回 None

    """
    name="凍傷"

    def battle_effect(pkm):
        print('{}被冰凍了，無法移動'.format(pkm.identity + pkm.name))
        return False

    def heal(pkm):
        result = Probability(0.20)
        if result:
            pkm.status = None
            print('{}解除了冰凍'.format(pkm.identity + pkm.name))
        else:
            return None

class PARALYZE(object):
    """
    class PARALYZE
    - inherent from: object
    attribute:
    name = 中文名稱
    effect = 效果解說

    method:
    - strength_effect(pkm = 麻痺了的 pokemon)
        arg:
            pkm = 麻痺了的 pokemon
        effect:
            令 pkm 速度下陷 50%
        return:
            None
    - battle_effect(pkm= 麻痺了的 pokemon)
        arg:
            pkm = 麻痺了的 pokemon
        effect:
            25% 機會會無法行動
        return:
            None
    """
    name="麻痺"

    def battle_effect(pkm):
        result = Probability(0.25)
        if result:
            print('{}因為麻痺，無法出招'.format(pkm.identity + pkm.name))
            return False
        else:
            return None

    def strength_effect(pkm):
        pkm.speed = None

class POISON(object):
    """
    class POISON
    - inherent from: object
    attribute:
    name = 中文名稱
    effect = 效果解說

    method:
    - damge(pkm= 中毒的 pokemon)
        arg:
            pkm = 麻痺了的 pokemon
        effect:
            回合结束时损失最大ＨＰ的1⁄8
        return:
            None
    """
    name="中毒"

    def __inti__(self):
        pass

    def damage(pkm):
        damage =int(pkm.strength_list['hp']*1/8.0)
        pkm.hp -=damage
        print("{}因中毒而失去{}點hp".format(pkm.identity + pkm.name, damage))

class BADLY_POISON(object):
    """
    class POISON
    - inherent from: BADLY_POISON
    attribute:
    name = 中文名稱
    effect = 效果解說

    method:
    - damge(pkm= 中毒的 pokemon)
        arg:
            pkm = 麻痺了的 pokemon
        effect:
            回合结束时损失最大ＨＰ的1⁄8
        return:
            None
    """
    name="猛毒"

    def __inti__(self):
        pass

    def damage(pkm):
        pkm.counter += 1
        damage =int(pkm.strength_list['hp']*pkm.counter/16.0)
        pkm.hp -=damage

        print("{}因猛毒而失去{}點hp".format(pkm.identity + pkm.name, damage))
        check_end(pkm)
