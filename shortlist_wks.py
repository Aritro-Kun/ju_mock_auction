import pandas as pd
from fuzzywuzzy import fuzz, process

df_wk = pd.read_csv('wk_stats.csv')
df_bat = pd.read_csv('bat_stats.csv')
df_players = pd.read_csv('players_list.csv')

details_of_suggested_players = []
types=[]
for index, row in df_players.iterrows():
    if row['Type'] not in types:
        types.append(row['Type'])

preferred_wks = []

for index, row in df_wk.iterrows():
    if row['innings']>50 and float(row['dismissals_per_innings'])>0.8:
        catches_per_inning = float(row['catches'])/float(row['innings'])
        stumpings_per_inning = float(row['stumpings'])/float(row['innings'])

        preferred_wks.append([row['player'], row['matches'], row['innings'], row['dismissals'], row['catches'], row['stumpings'], row['dismissals_per_innings'], catches_per_inning, stumpings_per_inning])

#Choosing two exceptional, cases, where we are keeping in mind, recent stats.
for index, row in df_wk.iterrows():
    if row['player']=='PD Salt (DC/KKR)' or row['player']=='Rahmanullah Gurbaz (KKR)':
        catches_per_inning = float(row['catches'])/float(row['innings'])
        stumpings_per_inning = float(row['stumpings'])/float(row['innings'])

        preferred_wks.append([row['player'], row['matches'], row['innings'], row['dismissals'], row['catches'], row['stumpings'], row['dismissals_per_innings'], catches_per_inning, stumpings_per_inning])

#Shortlisted, around 8 wicket keepers. 
#Further screening around to 2 keepers, keeping in mind two options, What?
#Our main criterion for selecting a wk is: The WK is a batter, with an average of over 30 and a strike rate of over 135. 

batter_names = df_bat['StrikerName'].tolist()
batter_keeper_names = []

for i in preferred_wks:
    filtered_names = [name for name in batter_names if name[0]==i[0][0]]
    closest_match, score = process.extractOne(i[0], filtered_names, scorer=fuzz.token_sort_ratio)
    batter_keeper_names.append(closest_match)
    

print(batter_keeper_names)

final_suggested_list = []

for i in batter_keeper_names:
    for index, row in df_bat.iterrows():
        if row['StrikerName']==i:
            if row['BattingAverage']>30 and row['StrikeRate']>135:
                final_suggested_list.append(i)

for i in final_suggested_list:
    matching_names = [name[0] for name in preferred_wks if name[0][0]==i[0]]
    closest_match,score = process.extractOne(i, matching_names, scorer=fuzz.token_sort_ratio)
    for j in range (0, len(preferred_wks)):
        if closest_match == preferred_wks[j][0]:
            details_of_suggested_players.append(preferred_wks[j])


shortlisted_prize = df_players['Name'].tolist()

for i in range(len(details_of_suggested_players)):
    shortlisted_prize_name = [name for name in shortlisted_prize if name[0] == details_of_suggested_players[i][0][0]]
    closest_match, score = process.extractOne(details_of_suggested_players[i][0], shortlisted_prize_name, scorer=fuzz.token_sort_ratio)
    for index, row in df_players.iterrows():
        if row['Name'] == closest_match:
            details_of_suggested_players[i].append(row['Price'])
            break

all_batsmen = df_bat['StrikerName'].to_list()
for i in range(len(details_of_suggested_players)):
    priority_batsmen = [name for name in all_batsmen if name[0]==details_of_suggested_players[i][0][0]]
    closest_match, score = process.extractOne(details_of_suggested_players[i][0], priority_batsmen, scorer=fuzz.token_sort_ratio)
    for index, row in df_bat.iterrows():
        if row['StrikerName']==closest_match:
            details_of_suggested_players[i].append(row['Matches'])
            details_of_suggested_players[i].append(row['Innings'])
            details_of_suggested_players[i].append(row['Balls'])
            details_of_suggested_players[i].append(row['TotalRuns'])
            details_of_suggested_players[i].append(row['BattingAverage'])
            details_of_suggested_players[i].append(row['StrikeRate'])

print(details_of_suggested_players)