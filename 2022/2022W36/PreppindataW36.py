import pandas as pd
import re

emp = pd.read_csv(r"C:\Data\PreppinData\employee_data.csv")

eptime = pd.read_excel(xlsx, 'episode_details')[['Episode', 'runtime_in_secs']]
dialogue = pd.read_excel(xlsx, 'dialogue').drop_duplicates().merge(eptime, on='Episode') 

dialogue = dialogue.sort_values(['Episode', 'time_in_secs'], ascending=True)

dialogue['next_time'] = dialogue.groupby('Episode')['time_in_secs'].shift(-1)
dialogue['Duration'] = dialogue.apply(lambda x: (x['runtime_in_secs'] if pd.isna(x['next_time']) 
                                                 else x['next_time'])-x['time_in_secs'], axis=1) 
dialogue = dialogue.rename(columns={'time_in_secs':'start_time'})
dialogue = dialogue[dialogue['section']=='Gameplay'].reset_index(drop=True)

dialogue = pd.concat([dialogue.drop(['name', 'runtime_in_secs', 'next_time'], axis=1), 
                      pd.DataFrame([map(str.strip, x) for x in dialogue['name'].str.split(',').values.tolist()])],
    			  axis=1, sort=False)

dialogue = dialogue.melt(id_vars=[c for c in dialogue.columns if not re.match('\d',str(c))],
                         value_name='name', var_name='ToDrop')\
    .drop('ToDrop', axis=1).dropna(subset=['name']).reset_index(drop=True)
    
dialogue = dialogue.drop_duplicates()[['Episode', 'name', 'start_time', 'Duration', 'youtube_timestamp', 'dialogue', 'section']]  
