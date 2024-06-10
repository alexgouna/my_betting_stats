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
    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS table_team_games")
    c.execute("""CREATE TABLE table_team_games (
                ID INTEGER UNIQUE,
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
    conn.commit()
    conn.close()


def fix_team_name(team_name,team):
    try:
        for i in range(2):
            if team =="Home":
                if int(team_name[:1]):
                    team_name = team_name[2:]
            elif team =="Away":
                if int(team_name[-1:]):
                    team_name = team_name[:-2]
    except:
        pass
    return team_name


def fix_game_corner(my_corner,full_half_game):
    if my_corner.find("(")>0:
        if full_half_game=="Full":
            return my_corner[:my_corner.find("(")-1]
        elif full_half_game=="Half":
            return my_corner[my_corner.find("(")+1:-1]





def game_data(page_link):
    def my_goal(goal,team):
        if team=="Home":
            return int(goal[:(goal.find("-"))])
        else:
            return int(goal[(goal.find("-"))+2:])


    print(page_link)

    conn = sqlite3.connect('my_database.db')
    c = conn.cursor()
    try:
        request = Request(page_link)
        request.add_header('user-agent',
                           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')
        page = urlopen(request)
        html_content = page.read()
        my_data = pd.read_html(html_content)
        for records in my_data[0].values.tolist():
            if str(records[0])!='nan' and len(records[4])>4:
                c.execute("""INSERT INTO table_team_games (League, Time, Home , Goal_Home , Goal_Away , Away , Corner , Corner_half , Dangerous_Attacks , Shots)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                               (records[0],records[1],fix_team_name(records[3],"Home"),my_goal(str(records[4]),"Home"),my_goal(str(records[4]),"Away"),
                                fix_team_name(records[5],"Away"), fix_game_corner(records[7],"Full"),fix_game_corner(records[7],"Half"),records[12][:-3],records[13][:-3]))

    except Exception as error:
        print(error)
        sleep(2)
        if my_var.count_tries_to_connect<5:
            my_var.count_tries_to_connect = my_var.count_tries_to_connect + 1
            game_data(page_link)



    conn.commit()
    conn.close()