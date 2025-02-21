# code refernece  https://github.com/codefirstio/tkinter-data-entry/blob/main/main.py


import tkinter
from tkinter import ttk
from tkinter import messagebox

def enter_data():
    global WORKORDER, title
    accepted = accept_var.get()
    
    if accepted=="Accepted":
        # User info
        WORKORDER = first_name_entry.get()
        
        
        if WORKORDER:
            title = title_combobox.get()
        
            
            # Course info
        
            
            print("WORKORDER: ", WORKORDER)
            print("OPERATOR: ", title)
        
            print("------------------------------------------")
        else:
            tkinter.messagebox.showwarning(title="Error", message="WORKORDER INFO TRENGES.")
    else:
        tkinter.messagebox.showwarning(title= "Error", message="ALT ER SJKET OG RIKTIG")
    return WORKORDER, title

""" #result = enter_data()
if result:
    WORKORDER, title = result
    print("WORKORDER:", WORKORDER)
    print("OPERATOR:", title) """
window = tkinter.Tk()
window.title("TEST&SETUP Data Entry")

frame = tkinter.Frame(window)
frame.pack()

# Saving User Info
user_info_frame =tkinter.LabelFrame(frame, text="TEST_SETUP_AM5000", bg="yellow",font=("Helvetica", 16))
user_info_frame.grid(row= 0, column=0, padx=20, pady=10)

first_name_label = tkinter.Label(user_info_frame, text="WORKORDER")
first_name_label.grid(row=0, column=0)


first_name_entry = tkinter.Entry(user_info_frame)

first_name_entry.grid(row=1, column=0)


title_label = tkinter.Label(user_info_frame, text="OPERATOR")
title_combobox = ttk.Combobox(user_info_frame, values=["", "Kenneth Andersen", "Steinar  Hansen", "Ann Kristin Johnsen","Conny Bokeli Saga","Mikael Eriksson","Ragnar Christer Iversen","Are Hotvedt","Janne Rismyhr","Uyen Skjuve","Åsmund Tørnquist Johansen","Hege Margrethe Dalen","Synnøve Lid Frebergsvik","Chris-Helen Echrehaug ","Maja Kaczorowska","Niclas Malterud",""])
title_label.grid(row=0, column=2)
title_combobox.grid(row=1, column=2)


for widget in user_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)



# Accept terms
terms_frame = tkinter.LabelFrame(frame, text="SJEKK &RIKTIG")
terms_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)

accept_var = tkinter.StringVar(value="Not Accepted")
terms_check = tkinter.Checkbutton(terms_frame, text= "ALT ER RIKTIG",
                                variable=accept_var, onvalue="Accepted", offvalue="Not Accepted")
terms_check.grid(row=0, column=0)

# Button
button = tkinter.Button(frame, text="Enter data", command= enter_data)
button.grid(row=3, column=0, sticky="news", padx=20, pady=10)

window.mainloop()




