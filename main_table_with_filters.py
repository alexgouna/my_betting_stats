import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import sqlite3
import requests
from bs4 import BeautifulSoup
from io import StringIO
from time import sleep
from urllib.request import Request, urlopen




def my_table_games_tree_view(my_root):
    def apply_filters(*args):


        query = "SELECT * FROM table_team_games"


        params = []

        try:
            conn = sqlite3.connect('my_database.db')
            df = pd.read_sql_query(query, conn, params=params)
            conn.close()

            # Clear previous data in treeview
            for i in tree.get_children():
                tree.delete(i)

            # Insert new data into treeview, excluding hidden columns
            for i, row in df.iterrows():
                values = [row[col] for col in visible_cols]
                tree.insert("", "end", values=values)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply filters: {e}")



    def sort_treeview(col, reverse):
        data_list = [(tree.set(k, col), k) for k in tree.get_children('')]
        data_list.sort(reverse=reverse)

        for index, (val, k) in enumerate(data_list):
            tree.move(k, '', index)

        tree.heading(col, command=lambda: sort_treeview(col, not reverse))


    # Fetch column names for treeview and populate the dropdown
    conn = sqlite3.connect('my_database.db')
    my_table = pd.read_sql_query("SELECT * FROM table_team_games LIMIT 1", conn)
    conn.close()

    global visible_cols
    cols = my_table.columns.tolist()
    visible_cols = [col for i, col in enumerate(cols) ]


    tree = ttk.Treeview(my_root, columns=visible_cols, show='headings')
    for col in visible_cols:
        tree.heading(col, text=col, command=lambda _col=col: sort_treeview(_col, False))
        tree.column(col, width=100, anchor='center')

    tree.pack(pady=20, fill=tk.BOTH, expand=True)

    apply_filters()


