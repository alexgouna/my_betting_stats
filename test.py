import sqlite3
import tkinter as tk
from tkinter import ttk

conn = sqlite3.connect('database.db')
c = conn.cursor()

conn.commit()

# Function to populate the Treeview
def populate_treeview(tree):
    c.execute('SELECT * FROM table_team_games')
    rows = c.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)

# Function to handle double-click event
def on_double_click(event):
    item = tree.selection()[0]
    item_id = tree.item(item, "values")[0]
    print(f"Selected ID: {item_id}")

# Set up the main application window
root = tk.Tk()
root.title("Team Games")

# Create the Treeview
tree = ttk.Treeview(root, columns=("ID", "Game_ID", "League", "Time", "Home", "Goal_Home", "Goal_Away", "Away", "Corner", "Corner_half", "Dangerous_Attacks", "Shots"), show="headings")

# Define the headings
for col in tree["columns"]:
    tree.heading(col, text=col)

# Populate the Treeview with data
populate_treeview(tree)


tree.bind("<Double-1>", on_double_click)

tree.pack(expand=True, fill="both")


root.mainloop()
conn.close()
