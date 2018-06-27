
# coding: utf-8

# In[ ]:


import sqlite3
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

path = "C:/Users/yappa/OneDrive/Udacity/DataAnalyst/Project-3/"
database = path + 'database.sqlite'


# In[300]:


with sqlite3.connect(database) as connection:
    tables = pd.read_sql("""SELECT * FROM sqlite_master WHERE type = 'table';""", connection)
    countries = pd.read_sql_query("SELECT * from Country", connection)
    matches = pd.read_sql_query("SELECT * from Match", connection)
    leagues = pd.read_sql_query("SELECT * from League", connection)
    teams = pd.read_sql_query("SELECT * from Team", connection)
    players = pd.read_sql_query("SELECT * from Player", connection)
    pattributes = pd.read_sql_query("SELECT * from Player_Attributes", connection)
    sequence = pd.read_sql_query("SELECT * from sqlite_sequence", connection)
    tattributes = pd.read_sql_query("SELECT * from Team_Attributes", connection)
    


# In[301]:


#Filtering match data from the top 5 leagues
selected_countries = ['France', 'Italy', 'Spain', 'Germany', 'England']
countries = countries[countries.name.isin(selected_countries)]
leagues = countries.merge(leagues, on = 'id')
matches = matches[matches.league_id.isin(leagues.id)]


# In[302]:


#Assigning team names to match data
matches = matches.merge(teams, left_on = 'home_team_api_id', right_on = 'team_api_id')
matches = matches.merge(teams, left_on = 'away_team_api_id', right_on = 'team_api_id')
matches = matches.merge(leagues, left_on = 'country_id', right_on = 'id')


# In[303]:


#Aggregating league data for goals scored across the seasons
matches = matches[['name_y', 'season', 'team_long_name_x', 'home_team_goal', 'team_long_name_y', 'away_team_goal']]
matches = matches.groupby(['season', 'name_y'])['home_team_goal', 'away_team_goal'].sum().reset_index()
matches['total_goals'] = matches ['home_team_goal'] + matches['away_team_goal']
leaguelist = set(matches['name_y'])


# In[304]:


#Examining number of goals scored broken down by individual league
epl = matches[matches.name_y == 'England Premier League']
ligue1 = matches[matches.name_y == 'France Ligue 1']
bundesliga = matches[matches.name_y == 'Germany 1. Bundesliga']
seriea = matches[matches.name_y == 'Italy Serie A']
bbva = matches[matches.name_y == 'Spain LIGA BBVA']
print(ligue1)


# In[305]:


#Resizing graph to fit x - axis labels, plotting from 5 dataframes for visual comparison 
plt.figure(figsize=(20,10))
plt.plot(epl['season'], epl['total_goals'], label = 'EPL')
plt.plot(ligue1['season'], ligue1['total_goals'], label = 'Ligue 1')
plt.plot(bundesliga['season'], bundesliga['total_goals'], label = 'Bundesliga')
plt.plot(seriea['season'], seriea['total_goals'], label = 'Serie A')
plt.plot(bbva['season'], bbva['total_goals'], label = 'BBVA')
plt.legend()


# In[306]:


eplgoals = epl['total_goals']
ligue1goals = ligue1['total_goals']
bundesligagoals = bundesliga['total_goals']
serieagoals = seriea['total_goals']
bbvagoals = bbva['total_goals']


# In[309]:


f, p = stats.f_oneway(eplgoals, ligue1goals, bundesligagoals, serieagoals, bbvagoals)


# In[310]:


print ('One-way ANOVA')
print ('=============')
 
print ('F value:', f)
print ('P value:', p, '\n')


# In[337]:


pvalues = []
leaguepairs = []
league1 = [eplgoals, ligue1goals, bundesligagoals, serieagoals, bbvagoals]
name1 = ['EPL', 'Ligue 1', 'Bundesliga', 'Serie A', 'BBVA']
league2 = [eplgoals, ligue1goals, bundesligagoals, serieagoals, bbvagoals]
name2 = ['EPL', 'Ligue 1', 'Bundesliga', 'Serie A', 'BBVA']
for value1 in league1:
    for value2 in league2:
        t, p = stats.ttest_ind(value1, value2)
        pvalues.append(p)

for lname1 in name1:
    for lname2 in name2:
        leaguepairs.append((lname1, lname2))

    
results = pd.DataFrame({'League Pair': leaguepairs, 'P-Values': pvalues})


# In[335]:


results = results[results['P-Values'] != 1]


# In[336]:


print(results)

