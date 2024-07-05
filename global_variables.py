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

times_live_button_pussed = 0
my_old_url = ""
my_counter = 5
time_sleep_reload_page_after_too_many_requests = 20
time_sleep_between_each_link = 3
count_tries_to_connect = 1
total_corner_live = 'https://www.totalcorner.com/match/today'

vba_code="""
Sub start()
    If Cells(1, 14) = "Game_ID" Then
        Columns.EntireColumn(14).Delete
    End If
    If Cells(1, 16) = "table" Then
        Columns.EntireColumn(16).Delete
    End If
        If Cells(1, 13) = "ID_goals" Then
        Columns.EntireColumn(13).Delete
    End If
    
    f_column = Cells(1, Columns.Count).End(xlToLeft).Column + 1
    Range(Columns(f_column), Columns(f_column + 84)).ColumnWidth = 0.2
    Range(Columns(f_column + 85), Columns(f_column + 95)).ColumnWidth = 0.4
    
    
    Columns(f_column + 44).ColumnWidth = 0.1
    Columns(f_column + 84).ColumnWidth = 0.1
    Columns(f_column + 44).Interior.Color = RGB(0, 0, 0)
    Columns(f_column + 84).Interior.Color = RGB(0, 0, 0)
    
    my_row = 2
    temp_goal = ""
    total_goal = 0
    goal_end_85 = 0
    Do While True
        If Cells(my_row, 14) <> 0 Then
            'paint  the cell with goal color if home goal or away
            If Cells(my_row, f_column - 1) = "Home" Then
                Cells(my_row, f_column + Int(Cells(my_row, f_column - 2))).Interior.Color = RGB(0, 255, 0)
            Else
                Cells(my_row, f_column + Int(Cells(my_row, f_column - 2))).Interior.Color = RGB(255, 0, 255)
            End If
        
            If temp_goal = "" Then
                temp_goal = Str(Cells(my_row, f_column - 2))
            End If
            
            If Int(Cells(my_row, 2)) = Int(Cells(my_row + 1, 2)) Then
            
                'finds if ther is more than 1 goals on the same minute
                If Cells(my_row, f_column - 2) >= Cells(my_row + 1, f_column - 2) Then
                    Cells(my_row, f_column - 2) = Int(Cells(my_row, f_column - 2)) + 1
                Else
                    Cells(my_row, f_column - 2) = Cells(my_row + 1, f_column - 2)
                End If
                
                temp_goal = temp_goal + ", " + Str(Cells(my_row, f_column - 2))
                
                Cells(my_row, f_column - 1) = Cells(my_row + 1, f_column - 1)
                Rows(my_row + 1).EntireRow.Delete
                my_row = my_row - 1
            Else
                Cells(my_row, f_column - 2) = temp_goal
                If Int(Right(temp_goal, 2)) > 84 Then
                    Cells(my_row, f_column + 95) = 1
                End If
                temp_goal = ""
            End If
        End If
    
        my_row = my_row + 1
        If (Len(Cells(my_row, 1)) = 0) Then
            Exit Do
        End If
    Loop
    
    my_row = 2
    'color win lose draw
    Do While True
        If Cells(my_row, 6) > Cells(my_row, 7) Then
            Cells(my_row, 5).Interior.Color = RGB(229, 255, 204)
            Cells(my_row, 8).Interior.Color = RGB(255, 204, 204)
        ElseIf Cells(my_row, 6) < Cells(my_row, 7) Then
            Cells(my_row, 5).Interior.Color = RGB(255, 204, 204)
            Cells(my_row, 8).Interior.Color = RGB(229, 255, 204)
        Else
            Cells(my_row, 5).Interior.Color = RGB(255, 255, 204)
            Cells(my_row, 8).Interior.Color = RGB(255, 255, 204)
        End If
        
        my_row = my_row + 1
        If (Len(Cells(my_row, 1)) = 0) Then
            Exit Do
        End If
    Loop
End Sub


"""



def my_pages_to_collect_data(my_league_link):

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(my_league_link, headers=headers)
        response.raise_for_status()


        soup = BeautifulSoup(response.content, 'html.parser')
        soup_str = str(soup)
        pos_pager_start = soup_str.rfind('/page:')+6
        pos_pager_end = soup_str.find('"', pos_pager_start)

        # print(soup_str[pos_pager_start:pos_pager_end])
        return int(soup_str[pos_pager_start:pos_pager_end])+1


    except Exception as error:
        print(error.args)
        return 2




# the league list is getting from the text file "league list.txt" and the format is line 1 title/ line 2 link /line3 title etc.
def list_league():
    file_path = 'league list.txt'
    my_list = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for index, line in enumerate(file, start=1):
                if len(line) > 5:
                    my_list.append(line[:-1])

    return my_list


current_year = '2024'
temp_month='12'



