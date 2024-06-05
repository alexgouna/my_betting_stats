from tkinter import *
import sqlite3
def list_of_link_to_retreive_data():
    conn = sqlite3.connect("my_database.db")
    c = conn.cursor()
    my_data = []
    try:
        c.execute("SELECT * FROM my_links")
        my_data =c.fetchall()
    except:
        pass

    conn.commit()
    conn.close()

    my_data_export=[]
    for i in my_data:
        my_data_export.append(i[1])
    return my_data_export



first_page_to_search=1
last_page_to_search=1
my_checkbox_var =  0


