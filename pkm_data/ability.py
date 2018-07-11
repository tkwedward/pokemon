import pandas as pd
import numpy as np
from random import randint
from pkm_data.path_utility import r_path
from pkm_data.general_function import Probability, check_end
from pkm_data.weather import RAIN, HEAVY_RAIN, SUNNY, HARSH_SUNLIGHT
from pkm_data.status import FEAR
from pokemon import Pokemon, Move


ability_map = [('降雨', CHANGE_WEATHER)]



class ABILITY(object):
    """
    name = 能力
    """
    def __init__(self, name, explanation=None):
        self.name = name
        self.explanation = explanation

class CHANGE_WEATHER(ABILITY):
    """
    改變天氣
    降雨	あめふらし	Drizzle	出場時，會將天氣變為下雨。
    無關天氣	ノーてんき	Cloud Nine	任何天氣的影響都會消失。
    stage 0 = 在回合開始時就發動
    """
    stage = 0
    def __init__(self,name):
        self.name = name

    def effect(self, pkm):
        pkm.event['weather'] = HEAVY_RAIN()


class STATS_CHANGE(ABILITY):
    # - 威嚇	いかく	Intimidate	出場時威嚇對手，使其退縮，從而降低對手的攻擊。
    """
    改變能力的效果
    stage 0 = 回合開始時發動
    沙隱, 引火
    (pkm, 加速, +1/2, spd, condition=None)
    (pkm, 複眼, +1/8, accurarcy , condition=)
    (pkm, water type, 儲水, +1/8, hp , condition=)
    (pkm, electric type, 蓄電, +1/8, hp , condition=)
    """
    stage = 0

    def effect(target, stats, modifier, condition=None):
        stats_value = getattr(target, stats)
        setattr(target, stats, stats_value * modifier)

class SPECIAL_CONDITION(ABILITY):
    """
    令對手陷入異常狀態
    名︰靜電、毒針、火焰身體、孢子、同步
    stage 3 = 計算傷害回合發動效果
    effect(pkm):
    arg
        - pkm: 防守的精靈(可以是自己，亦可以是對方)
        - pkm.attacked_by: 向己方發動攻擊的精靈
        - pkm.attacked_by.status: 對方的狀態

    processing:
    10 計算Probability
    20 如果中奬，就會令 pkm.attack_by.status = status
    30 如果沒有中奬，那麼就沒有事
    """
    stage = 3
    def effect(pkm, status):
        pass

class REDUCE_HP(ABILITY):
    """
    減低對方 HP 類 (粗糙皮膚)
    - 利用 self.attacked_by, self.attacked_move 來做定位
    - 在每次 attack 完後的 phase 就會生效
    """
    stage = 'after_attack'
    def effect(pkm):
        pkm.attack_by.hp -= pkm.attack_by * 1/16.0


"""
不會陷入異常狀能類
- 柔軟	じゅうなん	Limber	因為身體柔軟，不會陷入麻痺狀態。
- 遲鈍	どんかん	Oblivious	感覺遲鈍，不會陷入著迷和被挑釁狀態。
- 不眠	ふみん	Insomnia	因為擁有不會睡覺的體質，所以不會陷入睡眠狀態。
- 我行我素	マイペース	Own Tempo	因為我行我素，不會陷入混亂狀態。
- 免疫	めんえき	Immunity	因為體內擁有免疫能力，不會陷入中毒狀態。
"""



"""
- 免受傷害類型
飄浮	ふゆう	Levitate	從地面浮起，從而不會受到地面屬性招式的攻擊。

"""



"""
被堅硬的甲殼守護著，不會被對手的攻擊擊中要害。
受到對手的招式攻擊時不會被一擊打倒。一擊必殺的招式也沒有效果。
透過把周圍都弄濕，使誰都無法使用自爆等爆炸類的招式。
名︰使對手畏縮

變色	へんしょく	Color Change	自己的屬性會變為從對手所受招式的屬性。
鱗粉	りんぷん	Shield Dust	被鱗粉守護著，不會受到招式的追加效果影響。
- 吸盤	きゅうばん	Suction Cups	用吸盤將自己牢牢吸附在地面上，讓替換寶可夢的招式和道具失效。
- 踩影	かげふみ	Shadow Tag	踩住對手的影子使其無法逃走或替換。
- 神奇守護	ふしぎなまもり	Wonder Guard	不可思議的力量，只有效果絕佳的招式才會擊中自己。
"""

class Stench(object):
    name = "惡臭"
    explain = "以招式給予對手傷害時，有10%的機率使對手出現「畏懼」反應。※ 冒險效果： 排在隊伍最前面時，遭遇野生的Pokemon減為0.5倍。於戰爭金字塔內減為0.75倍。"

    def effect(pkm):
        if Probability(10):
            pkm.one_turn_effect = FEAR()

class Speed_Boost(object):
    name = "加速"
    effect = "every_turn"
    counter = 1

    def effect(pkm):
        if counter<=6:
            pkm.spd = (1+counter*0.5) * pkm.strength_list['spd']
            counter+=1

class Drizzle(object):
    name = "降雨"
    def effect(pkm):
        pkm.event['weather'] = WEATHER()

class Battle_Armor(object):
    name = "戰鬥盔甲"
    explain = "被堅硬的甲殼守護著，不會被對手的攻擊擊中要害"
    def effect(pkm):
        pass

class Sturdy(object):
    name = "結實"
    explain = "受到對手的招式攻擊時不會被一擊打倒。一擊必殺的招式也沒有效果。"
    def effect(pkm):
        pass

class Sturdy(object):
    name = "濕氣"
    explain = "透過把周圍都弄濕，使誰都無法使用自爆等爆炸類的招式。"
    def effect(pkm):
        pass
