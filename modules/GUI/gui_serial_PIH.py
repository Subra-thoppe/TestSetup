import tkinter as tk

def get_input():
    global SVEIS_PIH,SVEIS_PHT, ECT,ManuDate #serialno,
    #,ELECTRONIKK
    #serialno = entry1.get()
    SVEIS_PIH = entry2.get()
    """ ch_index_PIH = SVEIS_PIH .find("_")
    substring2_PIH=SVEIS_PIH[ch_index_PIH:]
    print(substring2_PIH[1:])
    if(substring2_PIH!='PIH'):
        print("Enter PIH sertifikat") """

    SVEIS_PHT = entry3.get()
    """ ch_index_PHT = SVEIS_PHT .find("_")
    substring2_PHT=SVEIS_PHT[ch_index_PHT:]
    print(substring2_PHT[1:])
    if(substring2_PHT!='PHT'):
        print("Enter PHT sertifikat")
 """


    ECT= entry4.get()
    """ ch_index_ECT = ECT .find("_")
    substring2_ECT=SVEIS_PHT[ch_index_ECT:]
    print(substring2_ECT[1:])
    if(substring2_ECT!='ECT'):
        print("Enter EDDY CURRETN SERTIFIKAT(ECT) sertifikat") """


    ManuDate= entry5.get()


    #ELECTRONIKK=entry5.get()
    #print("serialno:", serialno )
    print("SVEIS_PIHNo:",SVEIS_PIH )
    print("SVEIS_PHT:", SVEIS_PHT)
    print("ECT",ECT)
    return SVEIS_PIH,SVEIS_PHT,ECT, ManuDate#,serialno,
#,ELECTRONIKK
    




def create_window():
    # Create the main window
    global entry2,entry3,entry4 ,entry5 #, entry1,
    root = tk.Tk()
    root.title("PIH DETAILJER")

    """     # Create and place the first label and entry
    label1 = tk.Label(root, text="SerialNo:")
    label1.grid(row=0, column=0, padx=10, pady=10)
    entry1 = tk.Entry(root)
    entry1.grid(row=0, column=1, padx=10, pady=10)
    """
    # Create and place the second label and entry
    label2 = tk.Label(root, text="SVEISPROSEDURE:-PIH",  fg="green",font=("Helvetica", 16))
    label2.grid(row=1, column=0, padx=10, pady=10)
    entry2 = tk.Entry(root)
    entry2.grid(row=1, column=1, padx=10, pady=10)

    # Create and place the second label and entry
    label3 = tk.Label(root, text="SVEISPROSEDURE:-PHT", fg="blue",font=("Helvetica", 16))
    label3.grid(row=2, column=0, padx=10, pady=10)
    entry3 = tk.Entry(root)
    entry3.grid(row=2, column=1, padx=10, pady=10)

    # Create and place the second label and entry
    label4 = tk.Label(root, text="EDDYCURRENT-ECT", fg="purple",font=("Helvetica", 16))
    label4.grid(row=3, column=0, padx=10, pady=10)
    entry4 = tk.Entry(root)
    entry4.grid(row=3, column=1, padx=10, pady=10)
    
    # Create and place the second label and entry
    label5 = tk.Label(root, text="ManufacturingDate", fg="Orange",font=("Helvetica", 16))
    label5.grid(row=4, column=0, padx=10, pady=10)
    entry5 = tk.Entry(root)
    entry5.grid(row=4, column=1, padx=10, pady=10)
   
    # Create and place the button
    button = tk.Button(root, text="Bekreft og trykk ", command=get_input)
    button.grid(row=5, column=0, columnspan=2, pady=10)

    # Run the application
    root.mainloop()
#create_window()
#get_input()
