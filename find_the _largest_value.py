AA=input("Enter the numbers=>")
ln=None
print('Before',ln)
for thing in AA :
    if ln is None :
        ln=thing
    elif thing>ln :
        print(thing,'>',ln)
        ln=thing
print('After\n','The largest Number',ln)
print('Done!')