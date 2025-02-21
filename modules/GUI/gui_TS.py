import tkinter as tk

def get_input():
    global serialno,MembraneNo ,ToplidNo, Husno #, Elektronikk
    serialno = entry1.get()
    MembraneNo = entry2.get()
    ToplidNo = entry3.get()
    Husno=entry4.get()
    #Elektronikk=entry5.get()
    #Elektronikk='xxx'
    print("serialno:", serialno )
    print("MembraneNo:", MembraneNo)
    print("Toplid No:", ToplidNo)
    print("huS No:", Husno)
    return serialno,MembraneNo,ToplidNo, Husno #, Elektronikk
    




def create_window():
    # Create the main window
    global entry1,entry2,entry3,entry4 #, entry5
    root = tk.Tk()
    root.title("SerialNo,MembraneNo,ToplidNo")

    # Create and place the first label and entry
    label1 = tk.Label(root, text="SerialNo:", bg="yellow",font=("Helvetica", 16))
    label1.grid(row=0, column=0, padx=10, pady=10)
    entry1 = tk.Entry(root)
    entry1.grid(row=0, column=1, padx=10, pady=10)

    # Create and place the second label and entry
    label2 = tk.Label(root, text="MembraneNo:",bg="cyan",font=("Helvetica", 16))
    label2.grid(row=1, column=0, padx=10, pady=10)
    entry2 = tk.Entry(root)
    entry2.grid(row=1, column=1, padx=10, pady=10)

    # Create and place the second label and entry
    label3 = tk.Label(root, text="TOPLID No:",bg="orange",font=("Helvetica", 16))
    label3.grid(row=2, column=0, padx=10, pady=10)
    entry3 = tk.Entry(root)
    entry3.grid(row=2, column=1, padx=10, pady=10)


    # Create and place the second label and entry
    label4 = tk.Label(root, text="HOUSING  No:",bg="green",font=("Helvetica", 16))
    label4.grid(row=3, column=0, padx=10, pady=10)
    entry4 = tk.Entry(root)
    entry4.grid(row=3, column=1, padx=10, pady=10)


    """     # Create and place the second label and entry
    label5 = tk.Label(root, text="Elektronikk Batch  No:")
    label5.grid(row=4, column=0, padx=10, pady=10)
    entry5 = tk.Entry(root)
    entry5.grid(row=4, column=1, padx=10, pady=10) """

    # Create and place the button
    button = tk.Button(root, text="Bekreft og trykk ", command=get_input)
    button.grid(row=5, column=0, columnspan=2, pady=10)

    # Run the application
    root.mainloop()
#create_window()
