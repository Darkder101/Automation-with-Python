# r = read
# a = append 
# w = write
# x = create

# read - error if does not exist 

f = open("names.txt" , "a")
f.write("Neil \n")
f.close()

f = open("names.txt")
print(f.read())
f.close()

