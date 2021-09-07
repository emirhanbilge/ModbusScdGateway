s = open('XXVerileri.txt','r')
a = s.read().split("\n")


freq = 400.0
T = 1.0/400.0

file = open("output2.csv","a")
for i in a :
    file.write(str(round(T,4)))
    file.write(",")
    file.write(str(i))
    file.write("\n")
    T += 1.0/400.0