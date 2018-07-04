import pandas as pd
import numpy as np
from random import randint
from pkm_data.path_utility import r_path
from pkm_data.general_function import Probability, check_end
from pokemon import Pokemon, Move

"""
增加己方能力類︰





- 引火	もらいび	Flash Fire	受到火屬性的招式攻擊時，吸收火焰，讓自己使出的火屬性招式變強。
- 威嚇	いかく	Intimidate	出場時威嚇對手，使其退縮，從而降低對手的攻擊。


class ABILILTY_CHANGE(name, explain)
    name = 能力名稱
    explain = 能力解說
    (pkm, attack_by, 沙隱, +1/2, Agility ,condition=SANDSTROM)

    (pkm, 加速, +1/2, spd, condition=None)
    (pkm, 複眼, +1/8, accurarcy , condition=)


    (pkm, water type, 儲水, +1/8, hp , condition=)
    (pkm, electric type, 蓄電, +1/8, hp , condition=)

    method(pkm, pkm2, change, value, condition=None):
    arg
        - pkm: 攻擊的精靈(可以是自己，亦可以是對方)
        - pkm2: 防守的精靈(可以是自己，亦可以是對方)
        - change: 改變的能力
        - value: 改變的數值, +/- double

    return:
        能力或 hp 的改變
"""

"""
粗糙皮膚	さめはだ	Rough Skin	受到攻擊時，用粗糙的皮膚弄傷接觸到自己的對手。

"""

"""
令對方陷入異常狀能類
名︰靜電、毒針、火焰身體
- 孢子	ほうし	Effect Spore	透過攻擊有時會使接觸到自己的對手，陷入中毒、麻痺或睡眠狀態。
- 同步	シンクロ	Synchronize	將自己的中毒、麻痺或灼傷狀態傳染給對手。
方案1︰

class STATUS_CHANGE(name, explain)
    name = 能力名稱
    explain = 能力解說

    method(pkm, attack_by, status, probability):
    arg
        - pkm: 防守的精靈(可以是自己，亦可以是對方)
        - attack_by: 攻擊的精靈(可以是自己，亦可以是對方)
        - status: 被改變的能力

    processing:
    10 計算Probability
    20 如果中奬，就會令 pkm.attack_by.status = status
    30 如果沒有中奬，那麼就沒有事

"""

"""
不會陷入異常狀能類
- 柔軟	じゅうなん	Limber	因為身體柔軟，不會陷入麻痺狀態。
- 遲鈍	どんかん	Oblivious	感覺遲鈍，不會陷入著迷和被挑釁狀態。
- 不眠	ふみん	Insomnia	因為擁有不會睡覺的體質，所以不會陷入睡眠狀態。
- 我行我素	マイペース	Own Tempo	因為我行我素，不會陷入混亂狀態。
"""

"""
改變天氣
降雨	あめふらし	Drizzle	出場時，會將天氣變為下雨。
無關天氣	ノーてんき	Cloud Nine	任何天氣的影響都會消失。
免疫	めんえき	Immunity	因為體內擁有免疫能力，不會陷入中毒狀態。
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
