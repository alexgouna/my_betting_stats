import sqlite3
from tkinter import *
import Global_variables as my_var
from main_buttons import submit_button as submit_button
from main_buttons import save_links as save_links
from main_buttons import start_button as start_button
from main_buttons import submit_start_button as submit_start_button



def design_main_window(root):

    def cansel_button():
        root.destroy()

    def save_links_temp(my_frame):
        #GETING THE LIST OF LINKS TO SEARCH AND REARRANGE THE ENTRIES
        save_links(my_frame)
        label_center_left_title(my_frame)



    #top label
    def label_top_title(frame_top):
        my_label = Label(frame_top, text="Παράμετροι για μεταφορά δεδομένων", font=(25))
        my_label.pack(fill=BOTH, padx=20, pady=20)


    def label_center_left_title(my_frame):
        my_link_list = my_var.list_of_link_to_retreive_data()

        my_label = Label(my_frame,text="Λίστα με links για αναζήτηση δεδομένων",font=(15))
        my_label.pack(fill=BOTH,pady=10)
        for link in range(len(my_link_list)+3):
            link_entry = Entry(my_frame)
            link_entry.pack(fill=BOTH,padx=20)
            try:
                link_entry.insert(0,my_link_list[link])
            except:pass
        my_button = Button(my_frame,text="Save",command=lambda:save_links_temp(my_frame),padx=10)
        my_button.pack(pady=15)

    #center right
    def label_center_right_title(my_frame):
        my_label = Label(my_frame, text="Πόσες σελίδες θα ελέγξω", font=(15))
        my_label.pack(fill=BOTH,pady=10)

    def label_center_right_start_page(my_frame):
        my_label = Label(my_frame,text="Πρώτη Σελίδα:",anchor='e')
        my_label2 = Label(my_frame, text="Τελευταία Σελίδα:",anchor='e')
        my_label.pack(side=TOP,fill=BOTH)
        my_label2.pack(side=TOP,fill=BOTH)

    #center right right
    def entry_center_right_start_page(my_frame):
        my_entry_start_page=Entry(my_frame)
        my_entry_end_page=Entry(my_frame)
        my_entry_start_page.pack(side=TOP,fill=BOTH,anchor="w",padx=10)
        my_entry_end_page.pack(side=TOP,fill=BOTH,anchor="w",padx=10)

    # center right bottom
    def entry_center_right_bottom_checkbox(my_frame):
        def first_use():
            my_var.my_checkbox_var = my_checkbox_var_temp.get()

        my_checkbox_var_temp = IntVar()
        my_checkbox = Checkbutton(my_frame, text='Επέλεξε αν είναι η πρώτη χρήση',variable=my_checkbox_var_temp,  onvalue=1, offvalue=0, command=first_use)
        my_checkbox.pack()

    def bottom_buttons(my_frame,root):
        my_new_frame = Frame(my_frame)
        my_new_frame.pack(side=RIGHT, padx=50)

        #bottom buttons
        button_submit = Button(my_new_frame, text="Submit", command=submit_button, padx=10, pady=10,font=20)
        button_start_program = Button(my_new_frame, text="Start program", command=start_button, padx=10, pady=10,font=20)
        button_cansel = Button(my_new_frame, text="Cansel", command=cansel_button, padx=10, pady=10,font=20)
        button_submit_start_program = Button(my_new_frame, text="Submit and Start program", command=submit_start_button,
                                             padx=10, pady=10,font=20)
        button_submit.grid(row=0, column=0, pady=10, sticky='e')
        button_start_program.grid(row=0, column=1, pady=10, sticky='e')
        button_cansel.grid(row=0, column=2, pady=10, sticky='e')
        button_submit_start_program.grid(row=1, column=0, columnspan=3, sticky='we')


    #Create main frames
    frame_top = Frame(root,height =100)
    frame_center = Frame(root,height =500)

    #Pack the main frames
    frame_top.pack(side=TOP, fill=BOTH, expand=False)
    frame_center.pack(side=TOP, fill=BOTH, expand=True)


    #Create center left and right frames inside the center frame
    frame_center_left = Frame(frame_center,width=400)
    frame_center_right = Frame(frame_center,width=200)

    #Pack center left and right frames
    frame_center_left.pack(side=LEFT, fill=BOTH, expand=True)
    frame_center_right.pack(side=RIGHT, fill=BOTH, expand=True)
    label_top_title(frame_top)
    label_center_left_title(frame_center_left)
    label_center_right_title(frame_center_right)


    # center right left and right frame
    frame_center_right_top = Frame(frame_center_right)
    frame_center_right_bottom = Frame(frame_center_right)
    frame_center_right_top.pack(side=TOP, fill=BOTH, expand=True)
    frame_center_right_bottom.pack(side=BOTTOM, fill=BOTH, expand=True)


    frame_center_right_top_left = Frame(frame_center_right_top)
    frame_center_right_top_right = Frame(frame_center_right_top)
    frame_center_right_top_left.pack(side=LEFT, fill=BOTH,pady=10)
    frame_center_right_top_right.pack(side=RIGHT, fill=BOTH, expand=True,pady=10)


    # center right LEFT
    label_center_right_start_page(frame_center_right_top_left)
    entry_center_right_start_page(frame_center_right_top_right)
    entry_center_right_bottom_checkbox(frame_center_right_bottom)

    bottom_buttons(frame_center_right_bottom,root)



def start():

    root = Tk()
    root.title("Main!!!")
    root.geometry("800x400")

    design_main_window(root)


    mainloop()

start()
