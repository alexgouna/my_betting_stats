import tkinter as tk

def create_table(root, rows, columns):
    for i in range(rows):
        for j in range(columns):
            entry = tk.Entry(root, width=10)
            entry.grid(row=i, column=j)
            entry.insert(tk.END, f'R{i}C{j}')

root = tk.Tk()
root.title("Table View Example")

rows, columns = 5, 5
create_table(root, rows, columns)

root.mainloop()
