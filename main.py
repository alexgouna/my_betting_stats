import threading
from tkinter import *
from tkinter import ttk, messagebox
import global_variables as my_var
import pandas as pd
import sqlite3
import requests
from bs4 import BeautifulSoup
from io import StringIO
from time import sleep
from urllib.request import Request, urlopen
import Show_data
import os
import sql_connections
import get_my_data_from_total_cormer
import openpyxl
import xlwings as xw
import os
import datetime

def duplicate_or_already_exist_in_sql(my_table):
    i = 0
    while i < len(my_table) - 1:
        j = i + 1
        while j < len(my_table):
            if my_table[i][0] == my_table[j][0]:
                # print(my_table[i][0], "    ", my_table[j][0])
                my_table.remove(my_table[j])
            else:
                j = j + 1
        i = i + 1
    print("remove duplicates")

    my_table = sql_connections.find_if_exist(my_table)


    # print(my_table)

    return my_table


def retrieve_my_data(self):
    my_data = []
    my_table = []
    if len(self.entry_search.get()) > 10:
        my_data.append(get_my_data_from_total_cormer.get_my_team_first_page_link(self.entry_search.get()))
    else:
        # print(my_var.list_league())
        for my_link in my_var.list_league():
            # print(my_link)
            for link in sql_connections.get_my_team_first_page_link(my_link):
                for i in range(1, my_var.my_pages_to_collect_data):
                    my_data.append(get_my_data_from_total_cormer.get_my_team_first_page_link(link + str(i)))

    for page in my_data:
        # print(page)
        if page is not None:
            for row in page:
                my_table.append(row)
    my_table = duplicate_or_already_exist_in_sql(my_table)

    sql_connections.insert_data_of_the_games(my_table)


def create_database(self):
    answer = messagebox.askyesno('Warning!!!','You will delete all Data!!!\nDo you want to continue?', icon='warning')
    # print(answer)
    if answer:
        sql_connections.drop_create_table()


def date_today(my_date):
    if int(datetime.date.today().year) == int(my_date[:4]):
        if int(datetime.date.today().month) == int(my_date[5:7]):
            if int(datetime.date.today().day) == int(my_date[8:10]):
                return True
    return False

def remove_empty(my_table):
    for line in my_table:
        # print(line)
        if line[4]== '0 - 0' and line[6]== '0 - 0' and line[7]== '0-0' and not date_today(line[2]):
            my_table.remove(line)
            remove_empty(my_table)
    return my_table


def live_page(self):
    my_var.times_live_button_pussed += 1
    # print("live page data")
    my_data = []
    my_table = []
    my_link = my_var.total_corner_live
    counter = 0
    temp_counter_for_test = 0
    for link in sql_connections.get_my_team_first_page_link(my_link):
        temp_counter_for_test += 1
        # print('2222222',link)
        total_pages = my_var.my_pages_to_collect_data(link)
        if my_var.times_live_button_pussed < 2:
            for i in range(1, total_pages):
                my_var.current_year = '2024'
                my_var.temp_month = '12'
                my_data.append(get_my_data_from_total_cormer.get_my_team_first_page_link(link + str(i)))
        else:
            # αν πατήσω κουμπί των live περισσότερες από μία φορές.
            if counter < 30:
                for i in range(1, total_pages):
                    my_var.current_year = '2024'
                    my_var.temp_month = '12'
                    my_data.append(get_my_data_from_total_cormer.get_my_team_first_page_link(link + str(i)))
            counter += 1
        #     ------------------------------TEST------------------TEST------------------TEST------------------TEST------------------TEST----------
        if temp_counter_for_test == 5:
            break
        #     ------------------------------TEST------------------TEST------------------TEST------------------TEST------------------TEST----------
        # print(my_data)
    for page in my_data:
        # print(page)
        if page is not None:
            for row in page:
                my_table.append(row)

    # find if exist already in sql and delete
    my_table = duplicate_or_already_exist_in_sql(my_table)


    # find if the game haven't started yet.
    my_table = remove_empty(my_table)


    sql_connections.insert_data_of_the_games(my_table)


def show_detailed_data():
    Show_data.show_detailed_data()

def create_excell_all_data():
    my_team = sql_connections.get_all_teams_data()
    file_path = os.path.join(os.path.expanduser("~"), "Desktop", "totalcorner_all_data.xlsx")

    wb = xw.Book()
    wb.api.VBProject.VBComponents.Add(1).CodeModule.AddFromString(my_var.vba_code)



    try:
        my_table = pd.DataFrame(my_team)

        # Add an identifier column to distinguish the tables
        my_table['Table'] = 'Table1'

        my_table.columns = ['ID', 'Game_ID', 'League', 'Date', 'Home', 'Goal_Home', 'Goal_Away', 'Away', 'Corner',
                          'Half_corner', 'Attacks',
                          'Shots', 'ID_goals', 'Game_ID', 'Minutes', 'Home_Away', 'table']

        my_table.to_excel(file_path, index=False, engine='openpyxl')
    except Exception as error:
        print(error.args)


class DesignMainWindow:

    def __init__(self, root):
        self.root = root
        # create all the frames
        self.frame_top = Frame(self.root, height=50)
        self.frame_buttom = Frame(self.root, height=500)

        self.entry_search = Entry(self.frame_top, width=60)
        self.my_button = Button(self.frame_top, text="press here to get data from leagues from the text",
                                command=lambda: retrieve_my_data(self))
        self.my_button_live_page_data = Button(self.frame_top, text="get data from live page",
                                               command=lambda: live_page(self), padx=30, pady=30)
        self.my_button_create_database_and_tables = Button(self.frame_top, text="create database and tables",
                                                           command=lambda: create_database(self))
        self.my_button_show_data_details = Button(self.frame_top, text="Show detailed data",
                                                  command=show_detailed_data, padx=30, pady=30)
        self.my_button_create_excell_all_data = Button(self.frame_top, text="Create excell all data",
                                                  command=create_excell_all_data, padx=30, pady=30)


        self.frame_top.pack(side=TOP, expand=False, fill=BOTH)
        self.frame_buttom.pack(side=BOTTOM, expand=True, fill=BOTH)
        self.entry_search.pack(pady=5)
        self.my_button.pack(pady=5)
        self.my_button_live_page_data.pack(pady=5)
        self.my_button_create_database_and_tables.pack(pady=5)
        self.my_button_show_data_details.pack(pady=5)
        self.my_button_create_excell_all_data.pack(pady=5)

        # Bind the Escape key to a function that does nothing
        self.root.bind('<Escape>', self.do_nothing)

    def do_nothing(self, event):
        print("escape")


class Start:
    def __init__(self):
        self.root = Tk()
        self.root.title("Main!!!")
        self.root.geometry("800x400")

        self.main_window = DesignMainWindow(self.root)

        mainloop()


if __name__ == "__main__":
    Start()
