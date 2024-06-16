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
                    Game_ID TEXT,
                    League TEXT,
                    Time TEXT,
                    Home TEXT,
                    Goal_Home TEXT,
                    Goal_Away TEXT,
                    Away TEXT,
                    Corner TEXT,
                    Corner_half TEXT,
                    Dangerous_Attacks TEXT,
                    Shots TEXT,
    	            PRIMARY KEY("ID" AUTOINCREMENT))
                    """)
    c.execute("""CREATE TABLE table_goals (
                    ID INTEGER UNIQUE,
                    Game_ID TEXT,
                    goal_minute TEXT,
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




def find_if_exist(my_table):

    # replace first 30 games

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    sql = f"""SELECT Game_ID from table_team_games"""
    sql_table_game_id = c.execute(sql).fetchall()

    i=0
    while i<len(my_table):
        for j in range(0,len(sql_table_game_id)):
            if int(my_table[i][0])==int(sql_table_game_id[j][0]):
                if i<30:
                    # remove game to be replaced
                    sql = f"""DELETE FROM table_team_games WHERE Game_ID = '{int(sql_table_game_id[j][0])}'"""
                    c.execute(sql)
                    # REMOVE GOALES OF THE GAME
                    sql = f"""DELETE FROM table_goals WHERE Game_ID = '{int(sql_table_game_id[j][0])}'"""
                    c.execute(sql)

                else:
                    my_table.remove(my_table[i])
                    i=i-1
                break
        i=i+1
    conn.commit()
    conn.close()
    return my_table


def team_name(my_name):
    if my_name.find("'") > 0 :
        my_name = my_name[:my_name.find("'")]+my_name[my_name.find("'")+1:]
    return my_name

def insert_data_of_the_games(my_table):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    for game in my_table:
        sql = f"""INSERT INTO table_team_games 
                    (Game_ID, League, Time, Home, Goal_Home, Goal_Away, 
                    Away, Corner, Corner_half, Dangerous_Attacks, Shots)
                    VALUES ('{game[0]}','{game[1]}','{game[2]}','{team_name(game[3])}','{goal(game[4],'Home')}','{goal(game[4],'Away')}',
                    '{team_name(game[5])}','{game[6]}','{game[7]}','{game[8]}','{game[9]}')
               """
        # print(sql)
        c.execute(sql)
        for my_goal in game[10]:
            if my_goal != None:
                sql = f"""INSERT INTO table_goals 
                            (Game_ID, goal_minute, Home_Away_scored)
                            VALUES ('{game[0]}','{my_goal[1]}','{my_goal[0]}')
                       """
                # print(sql)
                c.execute(sql)

    conn.commit()
    conn.close()


def get_my_team_first_page_link(my_link):
    # print('666666666666666',my_link)

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(my_link, headers=headers)
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

        # print('545555555555555555555555555',team_info)
        return team_info
    except Exception as error:
        print(error)




