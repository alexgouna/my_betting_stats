import Global_variables as my_var
from tkinter import messagebox
from tkinter import *
import sql_my_commands
import sqlite3


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
        print(item)
    conn.commit()
    conn.close()
    print(my_link_list)


def submit_button():
    my_answer=True
    if my_var.my_checkbox_var==1:
        my_answer = messagebox.askokcancel(title="Προσοχή!!!", message="Η βάση δεδομένων θα μηδενιστεί και θα ξεκινήσει από την αρχή!!!")
    if my_answer:
        sql_my_commands.create_my_databases()

    # θα τερξει του σ πινακεσ δεδομενων







def start_button():
    pass

def submit_start_button():
    submit_button()
    start_button()







