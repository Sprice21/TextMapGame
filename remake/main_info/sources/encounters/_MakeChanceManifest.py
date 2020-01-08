from os import listdir
t = listdir()
cDict = {}
for file in t:
    if file[-4:] == ".txt":
        with open(file,'r') as f:
            t = f.read().splitlines()
        if t[0] == "!EM":
            for l in t[1:]:
                if l[:3] == "/s/":
                    for ch in l[3:].split(' '):
                        ch = ch.split(':')
                        if ch[0] in cDict: cDict[ch[0]].append(file[:-4]+':'+ch[1])
                        else: cDict[ch[0]] = [file[:-4]+':'+ch[1]]

out = '!MM Chance\n'
for key in cDict:
    out += '/'+key+'\n'
    for i in cDict[key]:
        out += i + '\n'
with open("Chance.txt",'w') as f:
    f.write(out[:-1])
input("done")
