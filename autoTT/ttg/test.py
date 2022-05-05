# import tkinter as tk
# from tkinter import ttk, END
#
# root = tk.Tk()
# root.title("Tab Widget")
# tabControl = ttk.Notebook(root)
#
# tab1 = ttk.Frame(tabControl)
# tab2 = ttk.Frame(tabControl)
#
# tabControl.add(tab1, text='Tab 1')
# tabControl.add(tab2, text='Tab 2')
# tabControl.pack(expand=1, fill="both")
# #
# ttk.Label(tab1,
#           text="Welcome to \
# GeeksForGeeks").grid(column=0,
#                      row=0,
#                      padx=30,
#                      pady=30)
# ttk.Label(tab2,
#           text="Lets dive into the\
# world of computers").grid(column=0,
#                           row=0,
#                           padx=30,
#                           pady=30)
#
# root.mainloop()
from tkinter import *
from tkinter import ttk


class Table:

    def __init__(self, root):

        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(root, width=20, fg='black',bg='red',
                               font=('Arial', 16, 'bold'))

                self.e.grid(row=i, column=j)
                self.e.insert(END, lst[i][j])

            # take the data


lst = [(1, 'Raj', 'Mumbai', 19),
       (2, 'Aaryan', 'Pune', 18),
       (3, 'Vaishnavi', 'Mumbai', 20),
       (4, 'Rachna', 'Mumbai', 21),
       (5, 'Shubham', 'Delhi', 21)]

# find total number of rows and
# columns in list
total_rows = len(lst)
total_columns = len(lst[0])

# create root window
root = Tk()
root.title("Tab Widget")
tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Tab 1')
tabControl.add(tab2, text='Tab 2')
tabControl.pack(expand=1, fill="both")

t = Table(tab1)
root.mainloop()