


def search_pokemon(table=pokemon_table, number):
    row = all_pokemon_df_2[all_pokemon_df_2['全國編號']==number]

    hp = int(row['hp'][0])
    atk = int(row['atk'][0])
    df = int(row['df'][0])
    spAtk = int(row['spAtk'][0])
    spDf = int(row['spDf'][0])
    spd = int(row['spd'][0])
    ability = row['特性1'][0]
    type1 = row['屬性1'][0]
    type2 = row['屬性2'][0]
    return (hp, atk, df, spAtk, spDf, spd, abililty, type1, type2)
