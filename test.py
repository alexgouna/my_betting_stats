import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import sqlite3

class CustomTreeview(ttk.Treeview):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.tag_configure('highlight_1', background='yellow')

    def set_cell_color(self, row_id, col, color):
        tags = self.item(row_id, 'tags')
        cell_tag = f'cell_{row_id}_{col}'
        self.tag_configure(cell_tag, background=color)
        current_tags = self.item(row_id, 'tags')
        if isinstance(current_tags, tuple):
            my_tag = current_tags[0]
        else:
            my_tag = current_tags
        if cell_tag not in my_tag:
            self.item(row_id, tags=my_tag + (cell_tag))

def my_table_games_tree_view(my_root):
    def apply_filters(*args):
        query = "SELECT * FROM table_team_games WHERE League LIKE '%" + filter_entry.get() + "%' OR Home LIKE '%" + filter_entry.get() + "%' OR Away LIKE '%" + filter_entry.get() + "%'"
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
                row_id = tree.insert("", "end", values=values)

                # Apply cell color for cells containing the number 1
                for col_idx, value in enumerate(values):
                    if str(value) == '1':
                        tree.set_cell_color(row_id, col_idx, 'yellow')

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

    # Create a frame for the filter entry
    filter_frame = tk.Frame(frame)
    filter_frame.pack(fill=tk.X)

    filter_label = tk.Label(filter_frame, text="Filter:")
    filter_label.pack(side=tk.LEFT, padx=5, pady=5)

    filter_entry = tk.Entry(filter_frame)
    filter_entry.pack(side=tk.LEFT, fill=tk.X, expand=1, padx=5, pady=5)
    filter_entry.bind("<KeyRelease>", apply_filters)

    # Create the Treeview widget
    tree = CustomTreeview(frame, columns=visible_cols, show='headings')
    for col in visible_cols:
        tree.heading(col, text=col, command=lambda _col=col: sort_treeview(_col, False))
        tree.column(col, width=100, anchor='center')

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    # Create a vertical scrollbar
    v_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscrollcommand=v_scrollbar.set)

    apply_filters()

# Example usage
root = tk.Tk()
my_table_games_tree_view(root)
root.mainloop()
