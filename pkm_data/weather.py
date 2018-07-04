import pandas as pd
import numpy as np
from random import randint
from pkm_data.path_utility import r_path
from pkm_data.general_function import Probability, check_end
from pokemon import Pokemon, Move
"""
RAIN, 大雨
HEAVY_RAIN
SUNNY
HARSH_SUNLIGHT
HAIL
SANDSTORM
STRONG_WIND
"""
class WEATHER(object):
    """
    count: 還餘下多少回合

    method:
    - count_down
        每個回合 count -= 1
    """
    count = 5

    def __init__(self):
        pass

    def __str__(self):
        return self.name

    def count_down(self):
        self.count -= 1



class RAIN(WEATHER):
    """
    name: 名字
    count: 持續多少回合
    """
    name = '大雨'

    def __str__(self):
        return self.name

class HEAVY_RAIN(WEATHER):
    """
    class inherent = WEATHER

    attribute:
    name = 中文名稱
    effect = 效果解說
    """
    name="暴雨"

class SUNNY(WEATHER):
    """
    class inherent = WEATHER

    attribute:
    name = 中文名稱
    effect = 效果解說
    """
    name="晴天"


class HARSH_SUNLIGHT(WEATHER):
    """
    class inherent = WEATHER
    attribute:
    name = 中文名稱
    effect = 效果解說
    """
    name="大晴天"
    def __str__(self):
        return self.name


class HAIL(WEATHER):
    """
    class inherent = WEATHER
    attribute:
    name = 中文名稱
    effect = 效果解說
    """
    name="冰雹"
    def __str__(self):
        return self.name

class SANDSTORM(object):
    """
    class inherent = WEATHER
    attribute:
    name = 中文名稱
    effect = 效果解說
    """

    def __init__(self):
        self.name = "沙暴"

    def __str__(self):
        return self.name

    def damage(self, pkm, team):
        damage =int(pkm.strength_list['hp']/16.0)
        pkm.hp -=damage

        print("{}因{}而失去{}點hp".format(pkm.name, self.name, damage))
        check_end(pkm, team)


class STRONG_WIND(object):
    """
    class inherent = WEATHER
    attribute:
    name = 中文名稱
    effect = 效果解說
    """
    def __str__(self):
        return self.name
