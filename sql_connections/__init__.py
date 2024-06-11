import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import sqlite3
import requests
from bs4 import BeautifulSoup
from io import StringIO
from time import sleep
from urllib.request import Request, urlopen
import global_variables as my_var




def drop_create_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS table_team_games")
    c.execute("DROP TABLE IF EXISTS table_goals")
    c.execute("""CREATE TABLE table_team_games (
                    ID INTEGER UNIQUE,
                    Game_ID INTEGER,
                    League TEXT,
                    Time TEXT,
                    Home TEXT,
                    Goal_Home INTEGER,
                    Goal_Away INTEGER,
                    Away TEXT,
                    Corner TEXT,
                    Corner_half TEXT,
                    Dangerous_Attacks TEXT,
                    Shots TEXT,
    	            PRIMARY KEY("ID" AUTOINCREMENT))
                    """)
    c.execute("""CREATE TABLE table_goals (
                    ID INTEGER UNIQUE,
                    Game_ID INTEGER,
                    goal_minute INTEGER,
                    Home_Away_scored TEXT,
    	            PRIMARY KEY("ID" AUTOINCREMENT))
                    """)
    conn.commit()
    conn.close()
def goal(my_goal,home_away):
    if home_away =='Home':
        return int(my_goal[:my_goal.find('-')])
    else:
        return int(my_goal[my_goal.find('-')+2:])

def insert_data_of_the_games(my_table):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    for game in my_table:
        sql = f"""INSERT INTO table_team_games 
                    (Game_ID, League, Time, Home, Goal_Home, Goal_Away, 
                    Away, Corner, Corner_half, Dangerous_Attacks, Shots)
                    VALUES ({int(game[0])},'{game[1]}','{game[2]}','{game[3]}',{goal(game[4],'Home')},{goal(game[4],'Away')},
                    '{game[5]}','{game[6]}','{game[7]}','{game[8]}','{game[9]}')
               """
        print(sql)
        c.execute(sql)
    conn.commit()
    conn.close()


def get_my_team_first_page_link(my_league_link):
    print(my_league_link)
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(my_league_link, headers=headers)
        print(my_league_link)
        response.raise_for_status()
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        team_links = soup.find_all('a', href=True)
        team_info = []
        for link in team_links:
            href = link['href']
            if '/team/view/' in href:
                team_first_page_link = 'https://www.totalcorner.com/team/view/' + href.split('/team/view/')[1] + '/page:'
                # team_name = link.text.strip()
                team_info.append(team_first_page_link)
        # # Print team numbers and names
        # for team_number, team_name in team_info:
        #     print(f"Team number: {team_number}, Team name: {team_name}")
        return team_info
    except Exception as error:
        print(error)




