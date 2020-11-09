import tkinter as tk
from tkinter import ttk
from code_computation import *

FRAME_BGs = ['red', 'orange', 'yellow']

def button_compute():
    """Creation of window for the generation of fiscal code"""

    global first_name, last_name, sex, day, month, year, city
    window_compute = tk.Tk()
    window_compute.title('Calcolo Codice Fiscale')

    frame1 = tk.Frame(master=window_compute, width=300, height=100, bg=FRAME_BGs[0])
    frame1.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

    #First Name
    tk.Label(frame1, text="Nome", bg=FRAME_BGs[0]).grid(row=0, padx=10, pady=10)
    first_name = tk.Entry(frame1)
    first_name.insert(tk.END, 'Mario')
    first_name.grid(row=0, column=1, padx=10, pady=10)
    #Last Name
    tk.Label(frame1, text="Cognome", bg=FRAME_BGs[0]).grid(row=1, padx=10, pady=10)
    last_name = tk.Entry(frame1)
    last_name.insert(tk.END, 'Rossi')
    last_name.grid(row=1, column=1, padx=10, pady=10)
    #Sex
    sex = tk.IntVar(window_compute)
    sex.set(1)
    tk.Label(frame1, text="sesso", bg=FRAME_BGs[0]).grid(row=2)
    male = tk.Radiobutton(frame1, text = SEX_STRINGS[1], variable = sex, value = 1, bg=FRAME_BGs[0])
    male.grid(row=2, column=1, padx=10, pady=5)
    female = tk.Radiobutton(frame1, text = SEX_STRINGS[2], variable = sex, value = 2, bg=FRAME_BGs[0])
    female.grid(row=2, column=2, padx=10, pady=5)

    frame2 = tk.Frame(master=window_compute, width=300, height=100, bg=FRAME_BGs[1])
    frame2.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
    tk.Label(frame2, text="Data di Nascita", bg=FRAME_BGs[1]).grid(row=0, column=0, padx=10, pady=10)
    #Day
    subframe_day = tk.Frame(master=frame2, width=20, height=20, bg=FRAME_BGs[1])
    subframe_day.grid(row=0, column=1, pady=10, padx=5)
    day = tk.Entry(subframe_day)
    day.insert(tk.END, '1')
    day.pack()
    #Month
    month=ttk.Combobox(frame2, values=list(MONTHS.keys()))
    month.grid(row=0, column=2)
    month.current(0)
    #Year
    subframe_year = tk.Frame(master=frame2, width=20, height=20, bg=FRAME_BGs[1])
    subframe_year.grid(row=0, column=3, padx=5, pady=10)
    year = tk.Entry(subframe_year)
    year.insert(tk.END, '1960')
    year.grid(row=0, column=0)

    frame3 = tk.Frame(master=window_compute, width=300, height=100, bg=FRAME_BGs[2])
    frame3.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
    #City
    tk.Label(frame3, text="Luogo di nascita", bg=FRAME_BGs[2]).grid(row=0, column=0)
    city = tk.Entry(frame3)
    city.insert(tk.END, 'Atri')
    city.grid(row=0, column=1, padx=10, pady=10)

    frame4 = tk.Frame(master=window_compute, width=300, height=100, bg=FRAME_BGs[2])
    frame4.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
    #Compute button
    button = tk.Button(frame4, text='CALCOLA', command=compute_pressed)
    button.pack()

    window_compute.mainloop()


def button_reading():
    """Creation of window for reading of sex, birthday and city from fiscal code"""

    global fiscal_code
    window_reading = tk.Tk()
    window_reading.title('Lettura Codice Fiscale')
    
    '''Frame'''
    frame = tk.Frame(master=window_reading, width=300, height=100, bg=FRAME_BGs[0])
    frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
    #Fiscal code
    tk.Label(frame, text="Codice Fiscale", bg=FRAME_BGs[0]).grid(row=0, column=0, padx=10, pady=40)
    fiscal_code = tk.Entry(frame)
    fiscal_code.insert(tk.END, 'RSSMRA60A01A488G')
    fiscal_code.grid(row=0, column=1, padx=40, pady=10)
    #Analysis button
    button = tk.Button(frame, text='ANALIZZA', command=read_pressed)
    button.grid(row=0, column=2, padx=10, pady=10)

    window_reading.mainloop()


def compute_pressed():
    """Callback for computation of fiscal code"""
    compute_code(first_name.get(),last_name.get(),sex.get(),day.get(),month.get(),year.get(),city.get())

def read_pressed():
    """Callback for analysis of fiscal code"""
    read_code(fiscal_code.get())


#Creation of main window of the program
window = tk.Tk()
window.title('Codice Fiscale')
window.geometry()
#Button for computation of fiscal code
compute_button = tk.Button(window, text='Calcolo', command=button_compute)
compute_button.grid(row=0, column=0, padx=30, pady=30)
#Button for analysis of fiscal code
reading_button = tk.Button(window, text='Lettura', command=button_reading)
reading_button.grid(row=0, column=1, padx=30, pady=30)

window.mainloop()