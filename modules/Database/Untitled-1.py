#for i in range(100):
    #print(i/20)

l1=[1,2,3,4,5]

l3=[]
for n in range(1,5):
    l3.extend(l1)

    
print(l3)
print(sorted(l3))
newlsit=[]
l1=[1,2,3,4,5]
for n in range(1,5):
    newlsit.append(l1[0])
for n in range(1,5):
    newlsit.append(l1[1])
#print(newlsit)
def interleave_lists(list1, list2, times):
    result = []
    for _ in range(times):
        interleaved = [item for pair in zip(list1, list2) for item in pair]
        result.extend(interleaved)
    return result

r""" es=interleave_lists(l1, l1, 15)
print(res) """