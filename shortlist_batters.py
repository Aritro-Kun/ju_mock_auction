import pandas as pd

df_batter = pd.read_csv('bat_stats.csv')

#Criteria 1, Average above 40
first_criterion_batters = []
for index, row in df_batter.iterrows():
    if row['BattingAverage']>40:
        first_criterion_batters.append(row['StrikerName'])
print(first_criterion_batters)

#Criteria 2, Matches above 100
second_criterion_batters = []
for i in first_criterion_batters:
    for index, row in df_batter.iterrows():
        if row['StrikerName']==i:
            if row['Matches']>100:
                second_criterion_batters.append(i)
            break
print(second_criterion_batters)