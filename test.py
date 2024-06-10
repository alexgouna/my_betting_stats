import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import sqlite3
import requests
from bs4 import BeautifulSoup
from io import StringIO
from time import sleep
from urllib.request import Request, urlopen

# Function to fetch and save data from URL
def fetch_and_save_data(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the table
        table = pd.read_html(StringIO(response.text))[0]
        print (table)
        print('------------------')
        print(list(table))
        print('---------23452345242354---------')
        # Extract team numbers and names
        team_links = soup.find_all('a', href=True)
        team_info = []
        for link in team_links:
            href = link['href']
            if '/team/view/' in href:
                team_number = href.split('/team/view/')[1]
                team_name = link.text.strip()
                team_info.append((team_number, team_name))

        # Print team numbers and names
        for team_number, team_name in team_info:
            print(f"Team number: {team_number}, Team name: {team_name}")

        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()

        # Drop old tables if exist
        cursor.execute("DROP TABLE IF EXISTS table_league")
        cursor.execute("DROP TABLE IF EXISTS table_teams")
        cursor.execute("DROP TABLE IF EXISTS table_team_games")

        # Create new table for league
        table.to_sql('table_league', conn, if_exists='replace', index=False)

        # Create new table for teams
        cursor.execute("CREATE TABLE table_teams (team_number TEXT, team_name TEXT)")
        cursor.executemany("INSERT INTO table_teams (team_number, team_name) VALUES (?, ?)", team_info)

        # Create new table for team games
        cursor.execute("CREATE TABLE table_team_games (team_number TEXT, game_data TEXT)")

        # Fetch and save team game data
        for team_number, team_name in team_info:
            for page in range(1, 21):
                team_url = f"https://www.totalcorner.com/team/view/{team_number}/page:{page}"
                try:
                    request = Request(team_url)
                    request.add_header('user-agent',
                                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')
                    page = urlopen(request)
                    html_content = page.read()
                    my_data = pd.read_html(html_content)
                    for records in my_data[0].values.tolist():
                        cursor.execute("INSERT INTO table_team_games (team_number, game_data) VALUES (?, ?)", (team_number, str(records)))

                except Exception as e:
                    print(f"Failed to fetch data for {team_number} on page {page}: {e}")
                sleep(1)

        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")

# Function to show the table with filters and sorting
def show_table_with_filters():
    def apply_filters(*args):
        filter_query = filter_var.get()
        filter_all_columns = filter_all_var.get()
        selected_column = column_var.get()

        query = "SELECT * FROM table_league"

        if filter_query:
            if filter_all_columns:
                conditions = [f'"{col}" LIKE ?' for col in visible_cols]
                query += " WHERE " + " OR ".join(conditions)
                params = [f"%{filter_query}%"] * len(visible_cols)
            else:
                query += f' WHERE "{selected_column}" LIKE ?'
                params = [f"%{filter_query}%"]
        else:
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

    def toggle_filter_mode():
        if filter_all_var.get():
            column_dropdown.config(state="disabled")
        else:
            column_dropdown.config(state="normal")
        apply_filters()

    def sort_treeview(col, reverse):
        data_list = [(tree.set(k, col), k) for k in tree.get_children('')]
        data_list.sort(reverse=reverse)

        for index, (val, k) in enumerate(data_list):
            tree.move(k, '', index)

        tree.heading(col, command=lambda: sort_treeview(col, not reverse))

    details_window = tk.Toplevel()
    details_window.title("Table Details")

    filter_var = tk.StringVar()
    filter_var.trace_add("write", apply_filters)

    filter_all_var = tk.BooleanVar(value=True)
    filter_all_var.trace_add("write", lambda *args: toggle_filter_mode())

    tk.Label(details_window, text="Filter:").pack(pady=5)
    tk.Entry(details_window, textvariable=filter_var).pack(pady=5)

    tk.Checkbutton(details_window, text="Filter all columns", variable=filter_all_var).pack(pady=5)

    column_var = tk.StringVar()
    column_dropdown = ttk.Combobox(details_window, textvariable=column_var)
    column_dropdown.pack(pady=5)

    # Fetch column names for treeview and populate the dropdown
    conn = sqlite3.connect('my_database.db')
    df = pd.read_sql_query("SELECT * FROM table_league LIMIT 1", conn)
    conn.close()

    global visible_cols
    cols = df.columns.tolist()
    visible_cols = [col for i, col in enumerate(cols) if i not in [1, -1]]  # Hide the second and last columns

    column_dropdown['values'] = visible_cols
    column_dropdown.current(0)
    tree = ttk.Treeview(details_window, columns=visible_cols, show='headings')
    for col in visible_cols:
        tree.heading(col, text=col, command=lambda _col=col: sort_treeview(_col, False))
        tree.column(col, width=100, anchor='center')

    tree.pack(pady=20, fill=tk.BOTH, expand=True)

    # Load initial data without any filters
    apply_filters()

# Main window
def main():
    root = tk.Tk()
    root.title("URL to Database")

    tk.Label(root, text="Enter URL:").pack(pady=5)
    url_var = tk.StringVar()
    tk.Entry(root, textvariable=url_var).pack(pady=5)
    tk.Button(root, text="Save to Database", command=lambda: fetch_and_save_data(url_var.get())).pack(pady=5)
    tk.Button(root, text="Show Table with Filters", command=show_table_with_filters).pack(pady=5)


    root.mainloop()

if __name__ == "__main__":
    main()
