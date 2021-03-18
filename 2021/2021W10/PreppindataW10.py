import pandas as pd

xlsx = pd.ExcelFile("F:/Data/Pokemon Input.xlsx")

pokemon = pd.read_excel(xlsx,sheet_name='Pokemon')
pokemon = pokemon[~pokemon['Name'].str.match('^Mega\s')]
pokemon = pokemon[pokemon['#'].str.strip().astype('float64')<=386]
pokemon = pokemon.drop('Type', axis=1).drop_duplicates()

evolution = pd.read_excel(xlsx,sheet_name='Evolution').drop_duplicates()
evolution = evolution[evolution['Evolving to'].isin(pokemon['Name'])]

evo_rule = evolution[['Evolving from', 'Evolving to']].set_index('Evolving to').T.to_dict('records')[0]
def get_group(who):
    return get_group(evo_rule[who]) if who in evo_rule else who 

evolution = evolution.rename(columns={'Evolving from':'Name'})
evolution['Evolving from'] = evolution['Name'].apply(lambda x: evo_rule.get(x, None) )

final = pd.merge(pokemon,evolution, how='left', on='Name')
final['Evolving from'] = final['Name'].apply(lambda x: evo_rule.get(x, None))
final['Evolution Group'] = final.apply(lambda x: get_group(x['Evolving from'] if x['Evolving from'] else x['Name']), axis=1)

final = final[['Evolution Group', '#', 'Name', 'Total', 'HP', 'Attack', 'Defense', 'Special Attack', 
               'Special Defense', 'Speed', 'Evolving from', 'Evolving to', 'Level', 'Condition', 'Evolution Type']]