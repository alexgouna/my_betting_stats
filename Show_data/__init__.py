from tkinter import *
from tkinter import ttk
import sqlite3
import Show_data.goal_stats_for_teams




class DesignDetailWindow:

    def __init__(self, root_detail):
        def populate_treeview(tree):
            c.execute('SELECT * FROM table_team_games')
            rows = c.fetchall()
            for row in rows:
                tree.insert("", "end", values=row)

        # Function to handle double-click event
        def on_double_click(event):
            item = self.tree.selection()[0]
            my_game = self.tree.item(item, "values")
            goal_stats_for_teams.start(my_game[4],my_game[7],)
            print(f"Selected ID: {my_game}")


        self.root_detail = root_detail
        # create all the frames
        self.tree = ttk.Treeview(self.root_detail, columns=("ID", "Game_ID", "League", "Time", "Home", "Goal_Home", "Goal_Away", "Away", "Corner", "Corner_half", "Dangerous_Attacks", "Shots"), show="headings")
        # Define the headings
        columns = [
            ("ID", 50),
            ("Game_ID", 80),
            ("League", 100),
            ("Time", 80),
            ("Home", 100),
            ("Goal_Home", 80),
            ("Goal_Away", 80),
            ("Away", 100),
            ("Corner", 80),
            ("Corner_half", 100),
            ("Dangerous_Attacks", 130),
            ("Shots", 80)
        ]

        for col, width in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        populate_treeview(self.tree)
        self.tree.bind("<Double-1>", on_double_click)
        self.tree.pack(expand=True, fill="both")






class show_detailed_data:

    def __init__(self):
        # create the new window
        self.root_detail = Tk()
        self.root_detail.title("Details !!!")
        self.root_detail.geometry("800x400")
        print("sadfgs")
        self.detail_window = DesignDetailWindow(self.root_detail)

        mainloop()












