import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import sqlite3

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
    visible_cols = [col for i, col in enumerate(cols)]

    # Create a frame to contain the Treeview and the scrollbar
    frame = tk.Frame(my_root)
    frame.pack(fill=tk.BOTH, expand=1)

    # Create the Treeview widget
    tree = ttk.Treeview(frame, columns=visible_cols, show='headings')
    for col in visible_cols:
        tree.heading(col, text=col, command=lambda _col=col: sort_treeview(_col, False))
        tree.column(col, width=100, anchor='center')

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    # Create a vertical scrollbar
    v_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscrollcommand=v_scrollbar.set)

    apply_filters()



