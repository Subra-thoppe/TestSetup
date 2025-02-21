  # find if nivå 5 WO 
Niva5_find='Isopod G6 4-20 mA Single 1200bar, Ready for Cal'
if Niva5_find.find(',')!=-1:
    s1= Niva5_find.split(',')

    print(s1)
#exit()
    if (s1[1]=='Calibrated'):
        print('True')
    else:
        print("ikke nivå 5 WO")
else:
    print("sjekk WO nummer")
