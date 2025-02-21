
def displists(seriallist,Testlist,Resultlist):

    import tkinter as tk
    from tkinter import ttk

    # Create the main window
    root = tk.Tk()
    root.title("COMPTRAC sjekk")

    # Sample data
    """ list1 = ["apple", "banana", "cherry"]
    list2 = [3, 5, 2]
    list3 = ["red", "yellow", "red"] """

    """  seriallist=[0, 0, 0, 0, 1, 1, 1, 1, 1]
    Testlist=['PADC', 'Tempchk', 'mAtest', 'IR-A', 'PADC', 'Tmpchk', 'mAtest', 'IR-B', 'IR-CH-AB']
    Resultlist=['FAIL_Offset', 'PASS_Temp_TADC', 'PASS_Temp_TADC', 'PASS_IR', 'PASS_Offset', 'PASS_Temp_TADC', 'PASS_Temp_TADC', 'PASS_IR', 'PASS_IR'] """
    """ PASSorFAIL=[]
    for i in Resultlist:
        k=i.split('_')[0]
        PASSorFAIL.append(k)
        print(k)

    if 'FAIL' in PASSorFAIL:
        FinalREsult='FAIL'
    else:
        FinalREsult='PASS' """

    # Create a Treeview widget
    tree = ttk.Treeview(root, columns=("Column1", "Column2", "Column3"), show="headings")
    #user_info_frame =tk.LabelFrame(frame, text="COMPTRAC_AM5000", bg="orange",font=("Helvetica", 16))

    tree.heading("Column1", text="Sensor SerialNo")
    tree.heading("Column2", text="Del")
    tree.heading("Column3", text="Sertifikat-No")
   
    # Insert data into the Treeview
    for item1, item2, item3 in zip(seriallist, Testlist, Resultlist):
        tree.insert("", tk.END, values=(item1, item2, item3))
        tree.insert("",tk.END,values="----------------")
        
    # Pack the Treeview widget
    tree.pack()

    # Create a string output
    output_string = "Material sertifikat sjekk"
    #label = tk.Label(root, text=FinalREsult)
    #label.pack()
    # Run the Tkinter event loop
    root.mainloop()

""" 
seriallist=[0, 0, 0, 0, 1, 1, 1, 1, 1]
#seriallist=[0]
Testlist=['PADC', 'Tempchk', 'mAtest', 'IR-A', 'PADC', 'Tmpchk', 'mAtest', 'IR-B', 'IR-CH-AB']
Resultlist=['FAIL_Offset', 'PASS_Temp_TADC', 'PASS_Temp_TADC', 'PASS_IR', 'PASS_Offset', 'PASS_Temp_TADC', 'PASS_Temp_TADC', 'PASS_IR', 'PASS_IR'] 
  
displists(seriallist,Testlist,Resultlist) """