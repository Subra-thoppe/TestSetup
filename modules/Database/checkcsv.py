from csv import DictReader
filename=r'C:\Scansense\AM5000\python-lib\programs\log\224834_K0_1200_Verification_95_2024-12-06 -jeya.csv'
""" fulldata={}
with open (filename, 'r') as file:
        for i in csv.DictReader(file):
            fulldata.update(dict(i))
            print (dict(i))
        print(fulldata) """

""" alldata=[]
with open (filename, 'r') as file:
        #for line in csv.DictReader(file):
        for line in csv.DictReader(file, fieldnames=('Channel','Loop','Date','Time','Temp_set','Pressure_set','ThermalChamber','PressureController','PressureReference','Serialnumber','ExpectedmA','MinmA','MaxmA','MinDeltamA','MaxDeltamA','MinFSmA','MaxFSmA','StatusmA','mAs')):
            
            print(line)
             
            alldata.append(line) """
#print(alldata)
""" sorted_data = sorted(alldata, key=lambda k: k["Channel"])
print(sorted_data) """

""" with open (filename, 'r') as file:
        #for line in csv.DictReader(file):


        dict_reader = DictReader(file)
     
        list_of_dict = list(dict_reader)
   
        print(list_of_dict) """



""" with open (filename, 'r') as file:
        #for line in csv.DictReader(file):


       
        line = file.readline()
        print(line) """

""" #working
import numpy as np
data = np.genfromtxt(filename, delimiter=';', names=True, dtype=None, encoding='utf-8')
names = data['Channel'].tolist()
occupations = data['Loop'].tolist()
print(names)
print(occupations) """




 
# Importing csv module
import csv
import pandas as pd  
 

###--------------
## dictionary no tworking dont try it 
######################
with open(filename, 'r') as x:
    csv_reader = csv.reader(x, delimiter=";")
    dictreader = csv.DictReader(x, delimiter=";")
    fieldnames1=dictreader.fieldnames
    next(csv_reader)
    veridata= list(csv_reader)
 
sorted_verdata = sorted(veridata, key=lambda x: x[9])
serialno_column = [row[fieldnames1.index("Serialnumber")] for row in sorted_verdata ]
uniqueserailnolist=list(dict.fromkeys(serialno_column))  # need to maintain ocurance order so dont use set
print(uniqueserailnolist)
#print(sorted_verdata[0:15])

exit()
skaptemp=sorted_verdata[5][6]
print(skaptemp)

df = pd.read_csv(filename, delimiter=';')

df.sort_values('Channel')
#print(df)
""" print(df['Serialnumber'][1:29])
print(df['Serialnumber'][30:58])
 """