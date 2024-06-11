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

my_old_url=""
my_counter=5
my_pages_to_collect_data = 2
count_tries_to_connect = 1

# the league list is getting from the text file "league list.txt" and the format is line 1 title/ line 2 link /line3 title etc.
def list_league():
    file_path = 'league list.txt'
    my_list=[]


    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for index, line in enumerate(file, start=1):
                if len(line)>5:
                    my_list.append(line[:-1])

    return my_list

