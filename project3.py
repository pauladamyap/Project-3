import numpy as np
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

path = "C:/Users/yappa/OneDrive/Udacity/DataAnalyst/Project-3/"
database = path + 'database.sqlite'

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

players.head(5)
sequence.head(5)
