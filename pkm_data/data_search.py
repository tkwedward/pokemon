import pokemon

def search_pokemon(number, table):
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
    return pokemon.Pokemon(number, name, hp, atk, df, spAtk, spDf, spd, ability, type1, type2, mv1='撞擊', mv2='流星閃沖', mv3='月亮之力', mv4='制裁光礫', lv=100)
