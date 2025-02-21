import tkinter
from tkinter import ttk
from tkinter import messagebox

def enter_data():
    global continuestatus, accepted, title 
    accepted = accept_var.get()
    
    if accepted=="Accepted":
       
        title = title_combobox.get()
               
        print("Title: ", title)
        if title=='YES':
            continuestatus='TRUE'
        elif title=='NO':
            continuestatus='FALSE'
        print("------------------------------------------")
    
    else:
        tkinter.messagebox.showwarning(title= "Error", message="You have not accepted the terms")
       
    return continuestatus, accepted, title 
def create_window():
    window = tkinter.Tk()
    window.title("PADC - OVERSTYRING")

    frame = tkinter.Frame(window)
    frame.pack()

    # Saving User Info
    user_info_frame =tkinter.LabelFrame(frame, text="")
    user_info_frame.grid(row= 0, column=0, padx=20, pady=10)

    title_label = tkinter.Label(user_info_frame, text="PADC - overstyr?")
    title_combobox = ttk.Combobox(user_info_frame, values=["YES", "NO"])
    title_label.grid(row=0, column=2)
    title_combobox.grid(row=1, column=2)

    # Saving Course Info
    courses_frame = tkinter.LabelFrame(frame)
    courses_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

    # Accept terms
    terms_frame = tkinter.LabelFrame(frame, text="")
    terms_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)

    accept_var = tkinter.StringVar(value="Not Accepted")
    terms_check = tkinter.Checkbutton(terms_frame, text= "Bekreft",
                                    variable=accept_var, onvalue="Accepted", offvalue="Not Accepted")
    terms_check.grid(row=0, column=0)

    # Button
    button = tkinter.Button(frame, text="Enter data", command= enter_data)
    button.grid(row=3, column=0, sticky="news", padx=20, pady=10)

    window.mainloop()
    #window.destroy()
    #print(continuestatus)


    #window.close()

#create_window()