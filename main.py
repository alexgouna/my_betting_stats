import threading
from tkinter import *
import Global_variables as my_var
from main_buttons import submit_button as submit_button
from main_buttons import save_links as save_links
from main_buttons import start_button as start_button
from main_buttons import submit_start_button as submit_start_button


# top label
def label_top_title(frame):
    my_label = Label(frame, text="Παράμετροι για μεταφορά δεδομένων", font=(25))
    my_label.pack(fill=BOTH, padx=20, pady=20)


def label_center_left_title(frame):
    my_link_list = my_var.list_of_link_to_retreive_data()

    my_label = Label(frame, text="Λίστα με links για αναζήτηση δεδομένων", font=(15))
    my_label.pack(fill=BOTH, pady=10)
    for link in range(len(my_link_list) + 3):
        link_entry = Entry(frame)
        link_entry.pack(fill=BOTH, padx=20)
        try:
            link_entry.insert(0, my_link_list[link])
        except:
            pass
    my_button = Button(frame, text="Save", command=lambda: save_links_temp(frame), padx=10)
    my_button.pack(pady=15)


def save_links_temp(frame):
    # GET THE LIST OF LINKS TO SEARCH AND REARRANGE THE ENTRIES
    save_links(frame)
    label_center_left_title(frame)


# center right
def label_center_right_title(frame):
    my_label = Label(frame, text="Πόσες σελίδες θα ελέγξω", font=(15))
    my_label.pack(fill=BOTH, pady=10)


def label_center_right_start_page(frame):
    my_label = Label(frame, text="Πρώτη Σελίδα:", anchor='e')
    my_label2 = Label(frame, text="Τελευταία Σελίδα:", anchor='e')
    my_label.pack(side=TOP, fill=BOTH)
    my_label2.pack(side=TOP, fill=BOTH)


# center right bottom
def entry_center_right_bottom_checkbox(frame):
    def first_use():
        my_var.my_checkbox_var = my_checkbox_var_temp.get()

    my_checkbox_var_temp = IntVar()
    my_checkbox = Checkbutton(frame, text='Επέλεξε αν είναι η πρώτη χρήση', variable=my_checkbox_var_temp,
                              onvalue=1, offvalue=0, command=first_use)
    my_checkbox.pack()


def bottom_buttons(frame, parent):
    my_new_frame = Frame(frame)
    my_new_frame.pack(side=RIGHT, padx=50)

    # bottom buttons
    button_submit = Button(my_new_frame, text="Submit", command=lambda: my_thread(parent), padx=10, pady=10, font=20)
    button_start_program = Button(my_new_frame, text="Start program", command=start_button, padx=10, pady=10, font=20)
    button_cansel = Button(my_new_frame, text="Cansel", command=lambda: cansel_button(parent), padx=10, pady=10, font=20)
    button_submit_start_program = Button(my_new_frame, text="Submit and Start program", command=submit_start_button,
                                         padx=10, pady=10, font=20)
    button_submit.grid(row=0, column=0, pady=10, sticky='e')
    button_start_program.grid(row=0, column=1, pady=10, sticky='e')
    button_cansel.grid(row=0, column=2, pady=10, sticky='e')
    button_submit_start_program.grid(row=1, column=0, columnspan=3, sticky='we')


def my_thread(parent):
    save_links_temp(parent.frame_center_left)
    try:
        my_var.first_page_to_search = int(parent.my_entry_start_page.get())
        my_var.last_page_to_search = int(parent.my_entry_end_page.get())
    except:
        my_var.first_page_to_search = 1
        my_var.last_page_to_search = 2

    threading.Thread(target=submit_button).start()


def cansel_button(parent):
    parent.root.destroy()


class DesignMainWindow:

    def __init__(self, root):
        self.root = root
        # create all the frames
        # Create main frames
        self.frame_top = Frame(self.root, height=100)
        self.frame_center = Frame(self.root, height=500)
        # Create center left and right frames inside the center frame
        self.frame_center_left = Frame(self.frame_center, width=400)
        self.frame_center_right = Frame(self.frame_center, width=200)
        # center right left and right frame
        self.frame_center_right_top = Frame(self.frame_center_right)
        self.frame_center_right_bottom = Frame(self.frame_center_right)
        self.frame_center_right_top_left = Frame(self.frame_center_right_top)
        self.frame_center_right_top_right = Frame(self.frame_center_right_top)

        self.my_entry_start_page = Entry(self.frame_center_right_top_right)
        self.my_entry_end_page = Entry(self.frame_center_right_top_right)

        # pack all the frames
        # Pack the main frames
        self.frame_top.pack(side=TOP, fill=BOTH, expand=False)
        self.frame_center.pack(side=TOP, fill=BOTH, expand=True)
        # Pack center left and right frames
        self.frame_center_left.pack(side=LEFT, fill=BOTH, expand=True)
        self.frame_center_right.pack(side=RIGHT, fill=BOTH, expand=True)

        label_top_title(self.frame_top)
        label_center_left_title(self.frame_center_left)
        label_center_right_title(self.frame_center_right)

        # center right left and right frame
        self.frame_center_right_top.pack(side=TOP, fill=BOTH, expand=True)
        self.frame_center_right_bottom.pack(side=BOTTOM, fill=BOTH, expand=True)
        self.frame_center_right_top_left.pack(side=LEFT, fill=BOTH, pady=10)
        self.frame_center_right_top_right.pack(side=RIGHT, fill=BOTH, expand=True, pady=10)

        # center right LEFT
        label_center_right_start_page(self.frame_center_right_top_left)

        self.my_entry_start_page.pack(side=TOP, fill=BOTH, anchor="w", padx=10)
        self.my_entry_end_page.pack(side=TOP, fill=BOTH, anchor="w", padx=10)

        entry_center_right_bottom_checkbox(self.frame_center_right_bottom)

        bottom_buttons(self.frame_center_right_bottom, self)


class Start:
    def __init__(self):
        self.root = Tk()
        self.root.title("Main!!!")
        self.root.geometry("800x400")

        self.main_window = DesignMainWindow(self.root)

        mainloop()


if __name__ == "__main__":
    Start()
