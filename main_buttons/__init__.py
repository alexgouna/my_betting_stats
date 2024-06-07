import Global_variables as my_var
from tkinter import messagebox
import sqlite3
import sql_my_commands


def save_links(my_frame):
    my_link_list = []

    conn = sqlite3.connect("my_database.db")
    c = conn.cursor()
    c.execute("DELETE FROM my_links ")
    conn.commit()
    conn.close()

    #geting the list of records
    for widget in my_frame.winfo_children():
        if widget.winfo_class() == 'Entry' and len(widget.get())>10:
            my_link_list.append(widget.get())
        widget.destroy()

    conn = sqlite3.connect("my_database.db")
    c = conn.cursor()
    for item in my_link_list:
        c.execute("INSERT INTO my_links (link_description) VALUES ('{0}')".format(item))
    conn.commit()
    conn.close()



def submit_button():

    my_answer=False
    # create new clear tables
    if my_var.my_checkbox_var==1:
        my_answer = messagebox.askokcancel(title="Προσοχή!!!", message="Η βάση δεδομένων θα μηδενιστεί και θα ξεκινήσει από την αρχή!!!")
    if my_answer:
        sql_my_commands.create_my_databases()


    # θα τερξει του σ πινακεσ δεδομενων
    my_data=[]
    # conn = sqlite3.connect("my_database.db")
    # c = conn.cursor()
    for page in range(my_var.first_page_to_search,my_var.last_page_to_search+1):
        for my_link in my_var.list_of_link_to_retreive_data():
            my_data.append(sql_my_commands.import_data_from_url(my_link+str(page)))

    #insert data to database table 'match'
    try:
        for data in my_data[0]:
            if not sql_my_commands.data_exist(data,'match'):

                sql = sql_my_commands.import_data_to_tables(data,'match')
                print(sql)
            print(data)
    except Exception:
        print(Exception,"2222222")


    # conn.commit()
    # conn.close()









def start_button():
    pass

def submit_start_button():
    submit_button()
    start_button()







