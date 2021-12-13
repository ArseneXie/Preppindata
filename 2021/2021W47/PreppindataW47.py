import pandas as pd

xlsx = pd.ExcelFile(r"C:\Data\PreppinData\top_female_poker_players_and_events.xlsx")

player = pd.read_excel(xlsx,'top_100')[['name', 'all_time_money_usd', 'player_id']]
event = pd.read_excel(xlsx,'top_100_poker_events')
event = event.fillna({'prize_usd':0}) 

final = pd.merge(player, event, on='player_id')
final['win_count'] = final['player_place'].apply(lambda x: 1 if x=='1st' else 0)
final = final.groupby(['name'], as_index=False).agg(
    max_event_date = ('event_date', 'max'),
    min_event_date = ('event_date', 'min'),
    win_count = ('win_count', 'sum'),
    number_of_events = ('event_name', 'count'),
    total_prize_money = ('all_time_money_usd', 'max'),
    event_country = ('event_country', 'nunique'),
    biggest_win = ('prize_usd', 'max')
    )
final['career_length'] = (final['max_event_date'] - final['min_event_date']).dt.days/365
final['percent_won'] = final['win_count']/final['number_of_events'] 

final = final[['name', 'number_of_events', 'total_prize_money', 'event_country',
               'biggest_win', 'career_length', 'percent_won']]
final = final.melt(id_vars='name', value_name='raw_value', var_name='metric')
final['scaled_value'] = final.groupby(['metric'])['raw_value'].rank(method='average',ascending=True)
final = final.sort_values(['name','metric'])
