import pandas as pd

xlsx = pd.ExcelFile(r"C:\Data\PreppinData\input_pkmn_stats_and_evolutions.xlsx")
factors = ['hp', 'attack', 'defense', 'special_attack', 'special_defense', 'speed']

stats = pd.read_excel(xlsx,'pkmn_stats').drop(['height', 'weight', 'evolves_from'], axis=1) 
stats = stats.melt(id_vars=[c for c in stats.columns if c not in factors], value_name='factor_value', var_name='combat_factors')

evol = pd.read_excel(xlsx,'pkmn_evolutions').dropna(subset=['Stage_2']).reset_index().rename(columns={'index': 'key'})

final = pd.merge(evol, stats.rename(columns={'name':'Stage_1'}), on='Stage_1').rename(columns={'factor_value':'intial_combat_power'})
final = pd.merge(final, stats[['name', 'combat_factors', 'factor_value']].rename(columns={'name':'Stage_2'}), 
                 on=['Stage_2','combat_factors']).rename(columns={'factor_value':'stage2_combat_power'})
final = pd.merge(final, stats[['name', 'combat_factors', 'factor_value']].rename(columns={'name':'Stage_3'}), 
                 on=['Stage_3','combat_factors'], how='left').rename(columns={'factor_value':'stage3_combat_power'})

final = final.groupby('key').agg({'Stage_1':'max', 'Stage_2':'max', 'Stage_3':'max', 'pokedex_number':'max', 'gen_introduced':'max',
                                  'intial_combat_power':'sum', 'stage2_combat_power':'sum', 'stage3_combat_power':'sum'})
final['final_combat_power'] = final.apply(lambda x: x['stage2_combat_power'] if pd.isna(x['Stage_3']) else int(x['stage3_combat_power']), axis=1)
final['combat_power_increase'] = (final['final_combat_power']-final['intial_combat_power'])/final['intial_combat_power']
final = final[['Stage_1', 'Stage_2', 'Stage_3', 'pokedex_number', 'gen_introduced', 
               'intial_combat_power', 'final_combat_power', 'combat_power_increase']].sort_values('combat_power_increase')
