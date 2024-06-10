import tkinter as tk
import os
from tkinter import ttk, messagebox
import pandas as pd
import sqlite3
import requests
from bs4 import BeautifulSoup
from io import StringIO
from time import sleep
from urllib.request import Request, urlopen



my_pages_to_collect_data = 1
count_tries_to_connect = 1

# the league list is getting from the text file "league list.txt" and the format is line 1 title/ line 2 link /line3 title etc.
def list_league():
    file_path = 'league list.txt'
    my_list=[]
    list_league_names=[]
    list_league_links=[]

    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for index, line in enumerate(file, start=1):
                if not len(line)<2:
                    if index%2!=0:
                        list_league_names.append(line[:-1])
                    else:
                        list_league_links.append(line[:-1])

    my_list.append(list_league_names)
    my_list.append(list_league_links)
    return my_list


def get_my_team_first_page_link(my_league_link):
    print(my_league_link)
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(my_league_link, headers=headers)
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
    except Exception:
        print(Exception)