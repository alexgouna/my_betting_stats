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

import sql_connections
import get_my_data_from_total_cormer



def duplicate(my_table):
    # for i in range(len(my_table)-1):
    #     for j in range(i+1,len(my_table)):
    #         if
    i=0
    while i<len(my_table)-1:
        j=i+1
        while j<len(my_table):
            if my_table[i][0]==my_table[j][0]:
                my_table.remove(my_table[j])
            else:
                j=j+1
    print("remove duplicates")
    return my_table




def retrieve_my_data(self):
    my_data=[]
    my_table=[]
    if len(self.entry_search.get())>10:
        my_data.append(get_my_data_from_total_cormer.get_my_team_first_page_link(self.entry_search.get()))
    else:
        print(my_var.list_league())
        for my_link in my_var.list_league():
            print(my_link)
            for link in sql_connections.get_my_team_first_page_link(my_link):
                for i in range(1,my_var.my_pages_to_collect_data):
                    my_data.append(get_my_data_from_total_cormer.get_my_team_first_page_link(link+str(i)))


    for page in my_data:
        for row in page:
            my_table.append(row)

    my_table = duplicate(my_table)


            # print(my_data)
            # print('----------------------------')
            # for dato in my_data:
            #     print(dato)
    sql_connections.insert_data_of_the_games(my_table)
def create_database(self):
    sql_connections.drop_create_table()


class DesignMainWindow:

    def __init__(self, root):

        self.root = root
        # create all the frames
        self.frame_top = Frame(self.root, height=50)
        self.frame_buttom = Frame(self.root, height=500)

        self.entry_search = Entry(self.frame_top, width=60)
        self.my_button = Button(self.frame_top,text="press here",command=lambda: retrieve_my_data(self))
        self.my_button_create_database_and_tables = Button(self.frame_top, text="create database and tables", command=lambda: create_database(self))




        self.frame_top.pack(side=TOP, expand=False, fill=BOTH)
        self.frame_buttom.pack(side=BOTTOM, expand=True, fill=BOTH)
        self.entry_search.pack(pady=5)
        self.my_button.pack(pady=5)
        self.my_button_create_database_and_tables.pack(pady=5)







class Start:
    def __init__(self):
        self.root = Tk()
        self.root.title("Main!!!")
        self.root.geometry("800x400")

        self.main_window = DesignMainWindow(self.root)

        mainloop()


if __name__ == "__main__":
    Start()
