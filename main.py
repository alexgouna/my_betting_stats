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
import get_my_data_from_total_cormer


def on_click_button(self):
    my_data=[]
    print(my_var.list_league())
    for my_link in my_var.list_league():
        print(my_link)
        for link in sql_connections.get_my_team_first_page_link(my_link):
            for i in range(1,my_var.my_pages_to_collect_data):
                my_data.append(get_my_data_from_total_cormer.get_my_team_first_page_link(link+str(i)))
        # print(my_data)

        print('----------------------------')
        # for dato in my_data:
        #     print(dato)




class DesignMainWindow:

    def __init__(self, root):

        self.root = root
        # create all the frames
        self.frame_top = Frame(self.root, height=50)
        self.frame_buttom = Frame(self.root, height=500)

        self.entry_search = Entry(self.frame_top, width=60)
        self.my_button = Button(self.frame_top,text="press here",command=lambda: on_click_button(self))



        self.frame_top.pack(side=TOP, expand=False, fill=BOTH)
        self.frame_buttom.pack(side=BOTTOM, expand=True, fill=BOTH)
        self.entry_search.pack(pady=5)
        self.my_button.pack(pady=5)







class Start:
    def __init__(self):
        self.root = Tk()
        self.root.title("Main!!!")
        self.root.geometry("800x400")

        self.main_window = DesignMainWindow(self.root)

        mainloop()


if __name__ == "__main__":
    Start()
