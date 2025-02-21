def guiserial(serial_trimmed_list):
    import tkinter
    from tkinter import ttk
    from tkinter import messagebox
    #import Niva5_MaterialsertifikatSjekk as matsersjekk

    def enter_data():
        global title
        accepted = accept_var.get()
        
        if accepted=="Accepted":
        
            title = title_combobox.get()
                
            print("SerialNo: ", title)
            """ if title=='YES':
                continuestatus='TRUE'
            elif title=='NO':
                continuestatus='FALSE' """
            print("------------------------------------------")
        
        else:
            tkinter.messagebox.showwarning(title= "Error", message="You have not accepted the terms")
        
        return title

    window = tkinter.Tk()
    window.title("Material Sertifikat Sjekk")

    frame = tkinter.Frame(window)
    frame.pack()

    # Saving User Info
    user_info_frame =tkinter.LabelFrame(frame, text="")
    user_info_frame.grid(row= 0, column=0, padx=20, pady=10)

    title_label = tkinter.Label(user_info_frame, text="Velg Serial no")
    title_combobox = ttk.Combobox(user_info_frame, values=serial_trimmed_list)
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
    return title
#window.destroy()
#print(title)


#window.close()

""" serial_trimmed_list=['22167', '22169', '22171', '22173', '22175', '22177', '22179', '22181', '22183', '22185', '22187', '22189', '22191', '22193', '22195', '22197', '22199', '22201', '22203', '22205', '22207', '22209', '22211', '22213', '22215', '22217', '22219', '22221', '22223', '22225']
selectedno=guiserial(serial_trimmed_list)
print(selectedno)
index = serial_trimmed_list.index(str(selectedno))
del serial_trimmed_list[index]
print( serial_trimmed_list) """