from random import randrange,random
from math import sqrt
def myRange(start,stop):
    if start < stop: step = 1
    elif start > stop: step = -1
    elif start == stop: return([start])
    if start != stop:
        outLi = []
        c = start
        while c != stop:
            outLi.append(c)
            c += step
        return(outLi)
def WReplace(Inp,Filters,End,CaseSense=0):
    for n in Filters:
        if n == Inp:
            return(End)
    return(Inp)
def listReplace(inpLi,item1,item2,layers=1):
    outLi = []
    if layers == 1:
        for item in inpLi:
            if item == item1:
                outLi.append(item2)
            else:
                outLi.append(item)
    elif layers == 2:
        for bigItem in inpLi:
            layerOutLi = []
            for item in bigItem:
                if item  == item1:
                    layerOutLi.append(item2)
                else:
                    layerOutLi.append(item)
            outLi = outLi + [layerOutLi]
    return(outLi)
def itemInAmount(item,inputList):
    tally = 0
    for element in inputList:
        if element == item:
            tally += 1
    return tally
def exactDistance(co1,co2):
    length = abs(co1[0]-co2[0])
    height = abs(co1[1]-co2[1])
    return(sqrt(length**2+height**2))
def pickRandElement(li):
    return li[randrange(0,len(li))]

def decRandom(start,stop,step):
    li = []
    for n in [start,stop,step]:
        if '.' in str(n):
            li.append(len(str(n).split('.')[1]))
        else: li.append(0)
    smallest = max(*li)
    mult = 10**smallest
    li = [int(i*mult) for i in [start,stop,step]]
    return randrange(li[0],li[1]+li[2],li[2])/mult
def chance(ran,top):
    if top/ran == top//ran:
        if randrange(top/ran) == 1: return True
        else: return False
    else:
        if randrange(top) < ran: return True
        else: return False
    
def inRect(co,rect):
    if co[0] >= rect[0] and co[1] >= rect[1] and co[0] < rect[0]+rect[2] and co[1] < rect[1]+rect[3]: return True
    else: return False
def limit(n,t,b):
    return max(min(n,t),b)

def dupleAdd(d1,d2):
    return tuple(d1[n]+d2[n] for n in range(len(d1)))
def pos(n):
    return abs(n)/n
def coDistance(co1,co2):
    length = abs(co1[0]-co2[0])
    height = abs(co1[1]-co2[1])
    return(sqrt(length**2+height**2))
