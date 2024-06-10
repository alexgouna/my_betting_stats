import threading
from tkinter import *
from tkinter import ttk
import global_variables as my_var
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import sqlite3
import requests
from bs4 import BeautifulSoup
from io import StringIO
from time import sleep
from urllib.request import Request, urlopen

import main_table_with_filters
import sql_connections



def display_main_screen_positions(self):
    self.frame_top.pack(side=TOP, expand=False, fill=BOTH)
    self.frame_buttom.pack(side=BOTTOM, expand=True, fill=BOTH)

    self.frame_top_left.pack(side=LEFT, expand=True, fill=BOTH)
    self.frame_top_right.pack(side=RIGHT, expand=True, fill=BOTH)

    self.entry_search.pack(pady=25)
    self.league_selection.pack(pady=25)


class DesignMainWindow:

    def __init__(self, root):
        self.options = my_var.list_league()
        self.selected_option = StringVar()

        self.root = root
        # create all the frames
        self.frame_top = Frame(self.root, height=50)
        self.frame_buttom = Frame(self.root, height=500)
        self.frame_top_left = Frame(self.frame_top)
        self.frame_top_right = Frame(self.frame_top)

        self.entry_search = Entry(self.frame_top_left, width=30)

        self.league_selection = ttk.Combobox(self.frame_top_right, textvariable=self.selected_option, width=50)
        self.league_selection['values'] = self.options[0]
        self.league_selection.current(0)
        self.league_selection.bind("<<ComboboxSelected>>", self.on_select)

        display_main_screen_positions(self)

    def on_select(self, event):
        sql_connections.drop_create_table()
        for i in range(len(self.options[0])):
            if self.options[0][i] == self.league_selection.get():
                try:
                    my_team_first_page_links = (my_var.get_my_team_first_page_link(self.options[1][i]))
                    for link in my_team_first_page_links:
                        for page in range(my_var.my_pages_to_collect_data):
                            sql_connections.game_data(link+str(page))
                        sleep(1)
                except Exception as error:
                    print(error)
        main_table_with_filters.my_table_games_tree_view(self.frame_buttom)

class Start:
    def __init__(self):
        self.root = Tk()
        self.root.title("Main!!!")
        self.root.geometry("800x400")

        self.main_window = DesignMainWindow(self.root)

        mainloop()


if __name__ == "__main__":
    Start()
