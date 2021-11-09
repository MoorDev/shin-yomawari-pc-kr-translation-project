f= open("번역.txt","r", encoding="utf-8")
fw= open("StringListDataBase_en.dat.txt",'w',encoding="utf-16")
lines = f.readlines()
print(len(lines))
for i in range(len(lines)):
    if (i%2)==0:
        data = "#### %d ####\n" % (i/2+1)
        fw.write(data)
    string = lines[i]
    fw.write(string)

f.close()
fw.close()
