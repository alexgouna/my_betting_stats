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



def get_my_team_first_page_link(my_league_link):
    print("aaaaaaaaaaaaaaaa")
    print(my_league_link)
    print("aaaaaaaaaaaaaaaa")
    try:
        print("55555555555555")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        print("6666666666666666666")
        response = requests.get(my_league_link, headers=headers)
        print("ccccccccccccc")
        print(my_league_link)
        response.raise_for_status()
        print("hhhhhhhhhh")
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        print("bbbbbbbbbbbb")
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
    except Exception:
        print(Exception)
        print("yurgyu4hu45yu456yf3yf34y")




