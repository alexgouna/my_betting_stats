import sqlite3
import sql_my_commands.create_tables
from urllib.request import Request, urlopen
from datetime import datetime
import time
import pandas as pd




def create_my_databases():
    #create tables
    conn = sqlite3.connect("my_database.db")
    c = conn.cursor()

    #drop all tables
    c.execute("SELECT name FROM sqlite_schema WHERE type='table'")
    tables = c.fetchall()
    for table, in tables:
        try:
            sql = ("DROP TABLE {0};".format(table))
            c.execute(sql)
        except Exception:
            print(Exception)

    #recreate all tables
    #find all functions to gets the tables
    functions = [func for func in dir(sql_my_commands.create_tables) if callable(getattr(sql_my_commands.create_tables, func))]
    for func in functions:
        # Call the function without any arguments
        sql = getattr(sql_my_commands.create_tables, func)()

        try:
            c.execute(sql)
        except:
            print("problem on running table \n",sql)

    conn.commit()
    conn.close()


#return a table with the data from a link
def import_data_from_url(my_link):
    # get the data from site
    my_list = []
    try:
        url = my_link
        request = Request(url)
        request.add_header('user-agent',
                           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')
        page = urlopen(request)
        html_content = page.read()
        my_data = pd.read_html(html_content)
        for records in my_data[0].values.tolist():
            my_list.append(records)
    except Exception as error:
        print(error)
    return my_list



def my_table_headers(my_table):
    if my_table=="match":
        return "match_team1", "match_team2", "match_team1_goal", "match_team2_goal", "match_team1_corner", "match_team2_corner", "match_team1_shots", "match_team2_shots", "match_league", "match_league_year"
    else:
        return "asdfafdasfdsafdasfdas"



def my_column_list(my_data,my_table):
    def goal_corner_shots(player, my_data):
        pos = my_data.find("-")
        if player == 1:
            return my_data[:pos - 1]
        else:
            return my_data[pos + 2:]
    # fix data to collect
    if my_table=="match":
        match_team1 = my_data[2]
        match_team2 = my_data[4]
        match_team1_goal = int(goal_corner_shots(1, my_data[3]))
        match_team2_goal = int(goal_corner_shots(2, my_data[3]))
        match_team1_corner = int(goal_corner_shots(1, my_data[7]))
        match_team2_corner = int(goal_corner_shots(2, my_data[7]))
        match_team1_shots = int(goal_corner_shots(1, my_data[13]))
        match_team2_shots = int(goal_corner_shots(1, my_data[13]))
        match_league = "Esoccer Battle - 8 mins play"
        match_league_year = 2024
        return match_team1,match_team2,match_team1_goal,match_team2_goal,match_team1_corner,match_team2_corner,match_team1_shots,match_team2_shots,match_league,match_league_year



#import data to my tables
def import_data_to_tables(my_data,my_table):
    conn = sqlite3.connect("my_database.db")
    c = conn.cursor()
    try:
        sql = "INSERT INTO {0} {1} VALUES {2}".format(my_table,my_table_headers(my_table),my_column_list(my_data,my_table))
        print(sql)
        print("==================")
        c.execute(sql)
    except:pass

    conn.commit()
    conn.close()





def data_exist(my_data,my_table):
    print("00000000000")
    def my_sql(my_data,my_table):
        sql = "SELECT COUNT(*) FROM {0} WHERE ".format(my_table)
        for i in range(len(my_column_list(my_data, my_table))):
            if type(my_column_list(my_data, my_table)[i])== str:
                sql = sql + my_table_headers(my_table)[i] + "='" + str(my_column_list(my_data, my_table)[i]) + "' AND "
            else:
                sql = sql + my_table_headers(my_table)[i] + "=" + str(my_column_list(my_data, my_table)[i]) + " AND "
        print(sql[:-4])
        return sql[:-4]

    conn = sqlite3.connect("my_database.db")
    c = conn.cursor()
    test=0
    print(my_sql(my_data, my_table), "----------------------------")
    try:
        print(my_sql(my_data,my_table),"8888888888888888888")
        c.execute(my_sql(my_data,my_table))
        test = c.fetchall()
    except Exception:
        print("7777777777777777777777")
    conn.commit()
    conn.close()
    print("test = ",test)
    if test >0 :
        return True
    else:
        return False













