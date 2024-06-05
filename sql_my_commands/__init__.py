import sqlite3
import sql_my_commands.create_tables


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

