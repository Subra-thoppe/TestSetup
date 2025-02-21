# code refernece  https://github.com/codefirstio/tkinter-data-entry/blob/main/main.py


import tkinter
from tkinter import ttk
from tkinter import messagebox

def enter_data():
    global WORKORDER, opr,skapno #, Antall, skapno
    accepted = accept_var.get()
    
    if accepted=="Accepted":
        # User info
        WORKORDER = WO_entry.get()
        
        
        if WORKORDER:
            opr =opr_combobox.get()
            #Antall=antall_name_entry .get()
            skapno=skapno_name_entry.get()
            #Manufacdate=manufacdate_name_entry.get()
            # Course info
        
            
            print("WORKORDER: ", WORKORDER)
            print("OPERATOR: ", opr)
            #print("antall: ", Antall)
            print("Skap no", skapno)
            print("------------------------------------------")
        else:
            tkinter.messagebox.showwarning(title="Error", message=" INFO TRENGES.")
    else:
        tkinter.messagebox.showwarning(title= "Error", message="ALT ER SJKET OG RIKTIG")
    return WORKORDER, opr,skapno #,Antall,skapno
#,Manufacdate

""" #result = enter_data()
if result:
    WORKORDER, title = result
    print("WORKORDER:", WORKORDER)
    print("OPERATOR:", title) """
window = tkinter.Tk()
window.title("Kalibrering - Data Entry")

frame = tkinter.Frame(window)
frame.pack()

# Saving User Info
user_info_frame =tkinter.LabelFrame(frame, text="KALIBRERING_AM5000")
user_info_frame.grid(row= 0, column=0, padx=20, pady=10)

WO_label = tkinter.Label(user_info_frame, text="WORKORDER (ex.224505)")
WO_label.grid(row=0, column=0)
WO_entry = tkinter.Entry(user_info_frame)
WO_entry.grid(row=1, column=0)

""" antall_name_label = tkinter.Label(user_info_frame, text="Antall_Sensorer")
antall_name_label.grid(row=0, column=3)
antall_name_entry = tkinter.Entry(user_info_frame)
antall_name_entry.grid(row=1, column=3)
 """
skapno_name_label = tkinter.Label(user_info_frame, text="Skapno ( ex.K0)")
skapno_name_label.grid(row=0, column=4)
skapno_name_entry = tkinter.Entry(user_info_frame)
skapno_name_entry.grid(row=1, column=4)


opr_label = tkinter.Label(user_info_frame, text="OPERATOR")
opr_combobox = ttk.Combobox(user_info_frame, values=["", "Kenneth Andersen", "Steinar  Hansen", "Ann Kristin Johnsen","Conny Bokeli Saga","Mikael Eriksson","Ragnar Christer Iversen","Are Hotvedt","Janne Rismyhr","Uyen Skjuve","Åsmund Tørnquist Johansen","Hege Margrethe Dalen","Synnøve Lid Frebergsvik","Chris-Helen Echrehaug ","Maja Kaczorowska","Niclas Malterud",""])
opr_label.grid(row=0, column=2)
opr_combobox.grid(row=1, column=2)




WO_entry = tkinter.Entry(user_info_frame)

WO_entry.grid(row=1, column=0)

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




