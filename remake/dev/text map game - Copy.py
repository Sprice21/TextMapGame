import time,random,os,pygame,math,pickle,copy

display_height = 840       
display_width = 1620

pygame.init()
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Light-Absent Enclosed Area of Space")
clock = pygame.time.Clock()

pygame.font.init()
myfont = pygame.font.SysFont("monospace", 20)
fancyFont = pygame.font.SysFont("calibri", 22)
#FreeMono, Monospace
from colours import *

def save(thisFileName,stockpileLootDict):
    with open("saves\\"+thisFileName+".dat",'wb') as file:
        pickle.dump((table,inventoryDict,stockpileLootDict,seenSet,(gridW,gridH)),file,protocol=2)

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
def pygameSleep(seconds):
    ticks = 0
    while ticks < seconds*60:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
        ticks += 1
        clock.tick(60)
#options
sandboxMode = False

def textObjects(text,font,colour=white):
    textSurface = font.render(text,True,colour)
    return(textSurface, textSurface.get_rect())

def messageDisplay(text,colour=white):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = textObjects(text,largeText,colour)
    TextRect.center = (display_width/2),(display_height/2)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
def simpleText(inputText,co=(0,0),colour=lightgray,simpleFont = myfont):
    #font = pygame.font.SysFont("monospace", 20)
    text = simpleFont.render(inputText, True, colour)
    gameDisplay.blit(text,co)
# co (x*67,y*20+40)

def CMD(Command=""):
    tempFun = lambda: os.system(str(Command)); tempFun()
CMD("title game")
print("105")
itemDict = {"cloth":2,"meat":5,"timber":5,"thatch":5,"stone":10,"leather":3,"coal":6,"iron":8,"steel":10,"gold":12,"flint":6,"cured meat":5,
            "tanned leather":3,"iron sword":3,"steel sword":20,"leather shirt":30,"leather pants":10,"hunting rifle":10,"rifle bullets":25,"flesh":2,
            "crawler":100,"fuel":5}
sSectorGridW = 3
sSectorGridH = 3

sGridW = 135*sSectorGridW
sGridH = 40*sSectorGridH

gridW,gridH = sGridW*sSectorGridW, sGridH*sSectorGridH

uX = math.floor(gridW/2)
uY = math.floor(gridH/2)

playerArmor = 1
playerHealth = 20
playerMaxHealth = 20

playerWeaponDamage = 5
playerWeaponName = "fists"

playerPrecision = 2
playerStrength = 2
playerAgility = 2
playerDefence = 2

transportMode = 0
consoleMode = False
##seenSet = {(uX,uY)}

def getPos():
    global uX,uY
    return (uX,uY)
#============================================
#making map template
#============================================
table = []
for y in range(gridH):
##    print(y)
    row = []
    for x in range(gridW):
        row.append(',')
    table.append(row)
def getTable(table):
    x,y = getPos()
    out = []

    for n in range(y-math.floor(sGridH/2),y+math.floor(sGridH/2)):
        if n < 0 or n >= len(table):
            layer = [' ']*sGridH
        else:
            layer = []
            for n2 in range(x-math.floor(sGridW/2),x+math.floor(sGridW/2)):
                if n2 < 0 or n2 >= len(table):
                    layer.append(' ')
                else:
                    layer.append(table[n][n2])
        out.append(layer)
    return out,y-math.floor(sGridH/2),x-math.floor(sGridW/2)

#============================================
#basic mechanics
#============================================
buildingNameList = ['H','c','W','I','S','O']
def showTablePers():
    global seenSet, transportMode
    (x,y) = getPos()
    buildingPS = []
    tempTableObject = getTable(table)
    c = tempTableObject[1]
    for a in tempTableObject[0]:
        pS = ""
        c1 = tempTableObject[2]
        buildingPS = []
        if c == y:
            for b in a:
                if c1 == x:
                    pS = pS + '■'#■
                else:
                    if (c1,c) in seenSet:
                        if b in buildingNameList:
                            buildingPS.append([b,(c1,c)])
                            pS = pS + ' '
                        else:
                            pS = pS + b
                    else:
                        pS = pS + ' '
                c1 += 1
        else:
            for b in a:
                if (c1,c) in seenSet:
                    if b in buildingNameList:
                        buildingPS.append([b,(c1,c)])
                        pS = pS + 'a'
                    else:
                        pS = pS + b
                else:
                    pS = pS + 'a'
                c1 += 1
        for inX,letter in enumerate(pS):
            if letter != ' ':
                pygame.draw.rect(gameDisplay,black,(inX*11,c*20+40,12,39))
        simpleText(pS,(0,20*c+40),lightgray)
        print(pS)
        c += 1
        for bPS in buildingPS:
            simpleText(bPS[0],(bPS[1][0]*12,bPS[1][1]*20+40),white,fancyFont)
    if transportMode == 0:
        charColour = white
    elif transportMode == 1:
        charColour = red
    else:
        charColour = white
    simpleText('■',(x*12,y*20+40),charColour)
def locationValid(x,y):
    if x >= gridW or x < 0 or y >= gridH or y < 0:
        return False
    else:
        return True
def locationBuildValid(x,y,mode=0):
    if x > gridW or x < 0 or y >= gridH or y <0:
        return False
    else:
        if table[y][x] not in buildingNameList and table[y][x] != '#' and table[y][x] != 'P' :
            return True
        else:
            return False

def inLocationValid(x,y,inGridW,inGridH):
    if x >= inGridW or x < 0 or y >= inGridH or y < 0:
        return False
    else:
        return True
def inSetLocationBuildValid(x,y,inGridW,inGridH,inTable):
    if x > inGridW or x < 0 or y >= inGridH or y <0:
        return False
    else:
        if inTable[y][x] not in buildingNameList and inTable[y][x] != '#' and inTable[y][x] != 'P' :
            return True
        else:
            return False

def seeArea(x,y,radius=3):
    global seenSet
    c,w = 0,0
    for d in range(y-radius,y+radius+1):
        for r in range(x-w,x+w+1):
            seenSet.add((r,d))
        if c >= radius:
            w -= 1
        else:
            w += 1
        c += 1

def exactDistance(co1,co2):
    length = abs(co1[0]-co2[0])
    height = abs(co1[1]-co2[1])
    return(math.sqrt(length**2+height**2))
def pickRandElement(li):
    return li[random.randrange(0,len(li))]
#============================================
#Map add mechanics
#============================================
def inLocationBuildValid(x,y):
    if x >= gridW or x < 0 or y >= gridH or y <0:
        return False
    else:
        return True
def inCircleFill(inTable,center,radius,char):
    co1 = (center[0]-radius,center[1]-radius)
    co2 = (center[0]+radius,center[0]+radius)
    for y in range(co1[1],co2[1]):
        for x in range(co1[0],co2[0]):
            if exactDistance(center,(x,y)) < radius-0.5 and inLocationBuildValid(x,y):
                inTable[y][x] = char
    return inTable
#i made this function badly, soz
def inGetNeighbours(inX,inY,proxyTable,mode=0):#1-%2, 2-show mode
    if inX == 0:
        xRange = [0,1]
    elif inX + 1 == gridH:
        xRange = [gridH-2,gridH-1]
    else:
        xRange = myRange(inX-1,inX+2)

    if inY == 0:
        yRange = [0,1]
    elif inY + 1 == gridW:
        yRange = [gridW-2,gridW-1]
    else:
        yRange = myRange(inY-1,inY+2)

    outList = []
    for y in yRange:
        for x in xRange:
            if (x,y) != (inX,inY):
                if mode == 1:
                    outList.append(proxyTable[x][y]%2)
                elif mode == 2:
                    outList.append(math.floor(proxyTable[x][y]/2))
                else:
                    outList.append(proxyTable[x][y])
    return outList

def genList(showProgess=False):
    terrainTypeList = [",",';','=',"'"]
    proxyTable = []
    for y in range(gridH):
        row = []
        for x in range(gridW):
            row.append(",")
        proxyTable.append(row)
    tempVar = sSectorGridW*sSectorGridH
    numberOfThings = 0#random.randrange(math.floor(tempVar*1.2),math.floor(tempVar*1.6)+1)
    for n in range(numberOfThings):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
        gameDisplay.fill(black)
        messageDisplay(str(round(n/numberOfThings*100,1))+"% Done")
        pygame.display.update()
        proxyTable = inCircleFill(proxyTable,(random.randrange(1,gridW),random.randrange(1,gridH)),random.randrange(20,gridW*2+21),pickRandElement(terrainTypeList))
    c = 0
    for y in proxyTable:
        c1 = 0
        for x in y:
            tempNeighbours = inGetNeighbours(c,c1,proxyTable)
            grassAmount = itemInAmount(",",tempNeighbours)
            tallGrassAmount = itemInAmount(";",tempNeighbours)
            sandAmount = itemInAmount("=",tempNeighbours)
            rockAmount = itemInAmount("'",tempNeighbours)
            if grassAmount == 8:
                if random.randrange(1,5) == 1:
                    proxyTable[c][c1] = ';'
            elif tallGrassAmount == 8:
                if random.randrange(1,5) == 1:
                    proxyTable[c][c1] = ','
            elif sandAmount == 8:
                if random.randrange(1,21) == 1:
                    proxyTable[c][c1] = '-'
            elif rockAmount in [7,8]:
                if random.randrange(1,8) == 1:
                    proxyTable[c][c1] = '.'
            
            if sandAmount in [1,2,3,4,5,6]:
                if random.randrange(1,4) == 1:
                    proxyTable[c][c1] = '='
            elif grassAmount in [1,2,3,4,5,6]:
                if random.randrange(1,4) == 1:
                    proxyTable[c][c1] = ','
            if proxyTable[c][c1] == ',':
                if random.randrange(1,51) == 1:
                    proxyTable[c][c1] = 'H'
            c1 += 1
        c += 1
    for n in range(2):
        c = 0
        for y in proxyTable:
            c1 = 0
            for x in y:
                tempNeighbours = inGetNeighbours(c,c1,proxyTable)
                grassAmount = itemInAmount(",",tempNeighbours)
                tallGrassAmount = itemInAmount(";",tempNeighbours)
                sandAmount = itemInAmount("=",tempNeighbours)
                rockAmount = itemInAmount("'",tempNeighbours)
                
                if sandAmount in [1,2,3,4,5,6]:
                    if random.randrange(1,4) == 1:
                        proxyTable[c][c1] = '='
                elif grassAmount in [1,2,3,4,5,6]:
                    if random.randrange(1,4) == 1:
                        proxyTable[c][c1] = ','
                
                c1 += 1
            c += 1
    return proxyTable
           
def squareFill(co1,co2,char):
    global table
    for y in range(co1[1],co2[1]):
        for x in range(co1[0],co2[0]):
            if locationBuildValid(x,y):
                table[y][x] = char
def diamondFill(center,radius,char):
    global table
    c = 0
    w = 0
    for d in range(center[1]-radius,center[1]+radius+1):
        for r in range(center[0]-w,center[0]+w+1):
            if locationBuildValid(r,d):
                table[d][r] = char
        if c >= radius:
            w -= 1
        else:
            w += 1
        c += 1
def circleFill(center,radius,char):
    global table
    co1 = (center[0]-radius,center[1]-radius)
    co2 = (center[0]+radius,center[0]+radius)
    for y in range(co1[1],co2[1]):
        for x in range(co1[0],co2[0]):
            if exactDistance(center,(x,y)) < radius-0.5 and locationBuildValid(x,y):
                table[y][x] = char
builtList = []
def mapBuildingPopulate(char,amount=1,withinRange = None,withinRangeOf = None):
    global builtList, table
    if withinRange == None:
        for a in range(amount):
            placed = False
            while not placed:
                tryCo = (random.randrange(0,gridW),random.randrange(0,gridH))
                if not tryCo == (uX,uY) and not tryCo in builtList:
                    table[tryCo[1]][tryCo[0]] = char
                    builtList.append(tryCo)
                    placed = True
    else:
        for a in range(amount):
            placed = False
            while not placed:
                tryCo = (random.randrange(0,gridW),random.randrange(0,gridH))
                if not tryCo == (uX,uY) and not tryCo in builtList and exactDistance(tryCo,withinRangeOf) < withinRange:
                    table[tryCo[1]][tryCo[0]] = char
                    builtList.append(tryCo)
                    placed = True  
def mapBuild(version=1):
    global table
    table[math.floor(gridH/2)][math.floor(gridW/2)] = 'S'
    squareFill((1,1),(18,18),'='); diamondFill((8,8),6,','); circleFill((80,15),18,"'"); circleFill((75,30),7,"'")
    mapBuildingPopulate('H',1,4,(uX,uY))
    mapBuildingPopulate('H',2,20,(uX,uY)); mapBuildingPopulate('H',3,40,(uX,uY)); mapBuildingPopulate('H',2); mapBuildingPopulate('c',7); mapBuildingPopulate('W',1); mapBuildingPopulate('I',1)


def inPathBuild(inTable,fromCo,toCo):
    xDist = abs(fromCo[0]-toCo[0])+5
    yDist = abs(fromCo[1]-toCo[1])+5
    inGridW = len(inTable[0])
    inGridH = len(inTable)
    closestList = [exactDistance(fromCo,toCo),toCo]
    for yCo in range(fromCo[1]-yDist,fromCo[1]+yDist):
        for xCo in range(fromCo[0]-xDist,fromCo[0]+xDist):
            if inLocationValid(xCo,yCo,inGridW,inGridH):
                if inTable[yCo][xCo] == '#':
                    if exactDistance(fromCo,(xCo,yCo)) < closestList[0]:
                        closestList = [exactDistance(fromCo,(xCo,yCo)),(xCo,yCo)]
    if random.randrange(1,3) == 2: #side-down
        for xCo in myRange(fromCo[0],closestList[1][0]):
            if inSetLocationBuildValid(xCo,fromCo[1],inGridW,inGridH,inTable):
                inTable[fromCo[1]][xCo] = '#'
        for yCo in myRange(fromCo[1],closestList[1][1]):
            if inSetLocationBuildValid(closestList[1][0],yCo,inGridW,inGridH,inTable):
                inTable[yCo][closestList[1][0]] = '#'
    else: #down-side
        for yCo in myRange(fromCo[1],closestList[1][1]):
            if inSetLocationBuildValid(fromCo[0],yCo,inGridW,inGridH,inTable):
                inTable[yCo][fromCo[0]] = '#'
        for xCo in myRange(fromCo[0],closestList[1][0]):
            if inSetLocationBuildValid(xCo,closestList[1][1],inGridW,inGridH,inTable):
                inTable[closestList[1][1]][xCo] = '#'
    return inTable
    
#============================================
#visual/screen mechanics
#============================================
def text_objects(text,font,colour=white):
    textSurface = font.render(text,True,colour)
    return(textSurface, textSurface.get_rect())

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

def returnButton(msg,x,y,w,h,ic,ac):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1:
            return True        
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("calibri",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)
def simButton(msg,x,y,w,h,ic,ac = None):
    pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
    if ac != None:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
    if msg == '<' or msg == '>':
        smallText = pygame.font.SysFont("comicsansms",20)
    else:
        smallText = pygame.font.SysFont("calibri",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)
def score(header,score,co=(0,0),colour=white):
    font = pygame.font.SysFont("calibri", 22)
    text = font.render(header + ": " + str(score), True, white)
    gameDisplay.blit(text,co)
def screenReset(water):
    gameDisplay.fill(black)
    score("Water",water)
    
    pygame.display.update()
#===========================================
#intro menu
#===========================================
introChoiceList = [["Save File 1",'1'],["Save File 2",'2'],["Save File 3",'3'],["Save File 4",'4'],["Save File 5",'5'],["Save File 6",'6']]
menuExit = False
print("534")
while not menuExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); quit()
        for c,item in enumerate(introChoiceList):
            if returnButton(item[0],1100,c*50+55,100,20,red,darkred) == True:
                startMode = item[1]
                menuExit = True
        if returnButton("Generate New",900,55,150,20,green,darkgreen) == True:
            startMode = "gen"
            menuExit = True
        pygame.display.update()
    clock.tick(60)
if startMode == 'gen':
    tempLi = [["Sector Width ",5],["Sector Height",5]]
    tempLi2 = [['/\\','up1'],['\\/','down1']]
    inventoryDict = {"meat":5,"timber":2}
    stockpileLootDict= {"cured meat":5}
    uSX = math.floor(sSectorGridW/2)
    uSY = math.floor(sSectorGridH/2)
    seenSet = {(uX,uY)}
    backupSeenSet = copy.deepcopy(seenSet)
    menuExit = False
    gameDisplay.fill(black)
    tempBar = 0
    tempTicks = 0
    while not menuExit:
        change = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
        simButton("Generate New",900,55,150,20,darkgreen)
        for c,item0 in enumerate(tempLi):
            simpleText(tempLi[c][0]+' '*4+str(tempLi[c][1]),(750,c*50+90))
            for c1,item in enumerate(tempLi2):
                if returnButton(item[0],1000,c1*25+80+c*50,30,20,black,darkgray) == True and tempTicks > tempBar:
                    tempBar = tempTicks + 10
                    change = (c,c1)
        if returnButton("complete",925,230,100,20,red,darkred):
            menuExit = True
        if change != None:
            if change[1] == 0:
                change = (change[0],-2)
            tempLi[change[0]][1] -= change[1]
            if tempLi[change[0]][1] < 5:
                tempLi[change[0]][1] = 5
        pygame.display.update()
        gameDisplay.fill(black)
        tempTicks +=1
        clock.tick(60)
    sSectorGridW,sSectorGridH = tempLi[0][1],tempLi[1][1]
    gameDisplay.fill(black)
    messageDisplay("Generating map")
    pygame.display.update()

    table = []
    for y in range(gridH):
        row = []
        for x in range(gridW):
            row.append('.')
        table.append(row)
        
    #auto-gen terrain
    tempStore = genList()
    table = []
    builtList = [(uX,uY)]
    for y in range(gridH):
        row = []
        for x in range(gridW):
            if tempStore[y][x] in buildingNameList:
                builtList.append((x,y))
            row.append(tempStore[y][x])
        table.append(row)
    mapBuild()
    mapStore = table
else:
    with open("saves\\"+"SaveFile"+str(startMode)+".dat",'rb') as file:
        table,inventoryDict,stockpileLootDict,seenSet,(gridW,gridH,sSectorGridW,sSectorGridH) = pickle.load(file)
    table = wholeTableConvert(table,1)
    backupSeenSet = copy.deepcopy(seenSet)

    
#============================================
#Feature mechanics
#============================================
def DialogueChain(DiaList=[]):
    for n in range(int(len(DiaList)/2)):
        print(DiaList[n*2]); time.sleep(DiaList[n*2+1])
def lootListGeneration(source="",lootQuality=1):
    outDict = {}
    if source == "OldHuman":
        if random.randrange(1,6) > 3:
            outDict['cured meat'] = random.randrange(1,3)
        if random.randrange(1,6) > 1:
            outDict['meat'] = random.randrange(2,5)
        if random.randrange(1,6) > 1:
            outDict['cloth'] = random.randrange(3,9)
        if random.randrange(1,6) > 3:
            outDict['timber'] = random.randrange(1,3)
            outDict['thatch'] = random.randrange(1,5)
    elif source == "Outpost":
        outDict['cured meat'] = random.randrange(2,7)
    elif source == "Troll":
        outDict["flesh"] = random.randrange(3,9)
        if random.randrange(1,12) > 2:
            outDict["iron sword"] = 1
    elif source == "AngryMaxine":
        outDict["fuel"] = random.randrange(8,63)
        outDict["car"] = 1
    else:
        raise ValueError
    return(outDict)

def weightEvaluation(Dict):
    weightCounter = 0
    for myItem in Dict:
        weightCounter += itemDict[myitem] * Dict[myItem]
    return(weightCounter)

def itemModify(inputDict,itemLi,mode):#(returns value of lootlList, changes value of inventoryDict) =0 - transfers from inventory =1 - transfers to inventory
    global inventoryDict
    if mode == 0:
        if itemLi[0] in inputDict:
            preVal = inputDict[itemLi[0]]
        else:
            preVal = 0
        inputDict[itemLi[0]] = preVal + itemLi[1]
        inventoryDict[itemLi[0]] -= itemLi[1]
        if inventoryDict[itemLi[0]] < 0:
            inventoryDict[itemLi[0]] = 0
            inputDict[itemLi[0]] -= 1
    elif mode == 1:
        if itemLi[0] in inventoryDict:
            preVal = inventoryDict[itemLi[0]]
        else:
            preVal = 0
        inventoryDict[itemLi[0]] = preVal + itemLi[1]
        inputDict[itemLi[0]] -= itemLi[1]
        if inputDict[itemLi[0]] < 0:
            inputDict[itemLi[0]] = 0
            inventoryDict[itemLi[0]] -= 1
    return(inputDict)

def transferButton(msg,x,y,w,h,ic,ac,inputDict,itemLi,mode):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    moddedOut = False
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1:
            out = itemModify(inputDict,itemLi,mode)
            moddedOut = True
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)
    if not moddedOut:
        out = False
    return(out)

def interfaceShow(text,xDisp=0,yDisp=0):
    textList = text.split('\n')
    c = 0
    for pS in textList:
        simpleText(pS,(xDisp,c*20+yDisp),white,fancyFont)
        c += 1
        
#combat part
def checkEnemyAlive(enemyHealth,EnemyNameDefiniteArticle,EnemyName,BattleXPReward):
    if enemyHealth <= 0:
        print(EnemyNameDefiniteArticle + EnemyName + " is now on 0 health.")
        print("---------------------------Player Turn over---------------------------")
        print("You defeated " + EnemyNameDefiniteArticle.lower() + EnemyName + "!")
        print("---------------------------Battle over--------------------------------")
        print("Exp Gained: " + str(BattleXPReward) + "exp")
        print("======================================================================")
        return False
    else:
        return True
def checkPlayerAlive(playerHealth,BattleDeathMessage):
    if playerHealth <= 0:
        print("You are now on 0 health.")
        print("---------------------------Enemy Turn over----------------------------")
        print("You died and lost the battle.")
        print(BattleDeathMessage)
        print("---------------------------Battle over--------------------------------")
        return False
    else:
        return True
playerHealth = 20
combatChoiceList = [["Attack",'a'],["Channel",'c'],["Defend",'d'],["Recover",'r'],["Items",'i'],["Magic",'g']]
def Combat(EnemyMoveset,BattleDeathMessage,EnemyNameIndefiniteArticle,EnemyNameDefiniteArticle,EnemyName,EnemyPrecision,EnemySpeed,EnemyArmor,EnemyMaxHealth,EnemyAttackDamage,BattleXPReward):
    global playerHealth
    tempTicks = 0
    tempBar = 0
    EnemyHealth = EnemyMaxHealth
    Turn = 0
    BattleActive = 1
    EnemyMaxHealth = EnemyHealth
    EnemyChanneled = 0
    PlayerChanneled = 0
    AttackIntroString = random.randrange(1,5)
    print('='*70)
    print("Name: " + EnemyName + " || " + "Health: " + str(EnemyHealth))
    print("Armor: " + str(EnemyArmor))
    print('='*70)
    if AttackIntroString == 1:
        print(EnemyNameIndefiniteArticle + EnemyName + " attacks you!")
    elif AttackIntroString == 2:
        print("WABAM, it's " + EnemyNameIndefiniteArticle + EnemyName + "!")
    elif AttackIntroString == 3:
        print(EnemyNameIndefiniteArticle + EnemyName + " randomly appears from somewhere? How quaintly convenient.")
    elif AttackIntroString == 4:
        print("You spot " + EnemyNameIndefiniteArticle + EnemyName + " and manage to get the jump on it. ")
        if (((playerWeaponDamage * ((playerStrength/10)+1))/2) - EnemyArmor) > 0:
            print("You attack " + EnemyName.lower() + " for " + str(((playerWeaponDamage * ((playerStrength/10)+1))/2) - EnemyArmor) + " damage.")
            EnemyHealth = EnemyHealth - (((playerWeaponDamage * ((playerStrength/10)+1)/2)) - EnemyArmor)
            if checkEnemyAlive(EnemyHealth,EnemyNameDefiniteArticle,EnemyName,BattleXPReward):
                print(EnemyNameDefiniteArticle + EnemyName + " is now on " + str(EnemyHealth) + " health.")
                EnemyHealth = EnemyHealth - ((((playerStrength/10)+1)/2) - EnemyArmor)
            else:
                BattleActive = 0
        print("The " + EnemyName + " is now on " + str(EnemyHealth) + " health.")
    elif AttackIntroString == 5:
        print("You get the jump on " + EnemyNameIndefiniteArticle + EnemyName + ".")
        if (((playerWeaponDamage * ((Player.Strength/10)+1))/2) - EnemyArmor) > 0:
            print("You attack " + EnemyName.lower() + " for " + str(((playerWeaponDamage * ((playerStrength/10)+1))/2) - EnemyArmor) + " damage.")
            EnemyHealth = EnemyHealth - (((playerWeaponDamage * ((playerStrength/10)+1)/2)) - EnemyArmor)
            if checkEnemyAlive(EnemyHealth,EnemyNameDefiniteArticle,EnemyName,BattleXPReward) == True:
                print(EnemyNameDefiniteArticle + EnemyName + " is now on " + str(EnemyHealth) + " health.")
                EnemyHealth = EnemyHealth - ((((playerStrength/10)+1)/2) - EnemyArmor)
            else:
                BattleActive = 0
                print("======================================================================")
    if checkEnemyAlive(EnemyHealth,EnemyNameDefiniteArticle,EnemyName,BattleXPReward) == True:
        print("======================================================================")
        while BattleActive == 1:
            PlayerAttackChoice = ""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); quit()
            EnemyTurnActive = 1
            TurnActive = 1
            EnemyAttackChoice = random.randrange(1,4)
            while EnemyChanneled == 1 and EnemyMoveset == 1 and EnemyAttackChoice == 3:
                EnemyAttackChoice = 1
            while EnemyMaxHealth == EnemyHealth and EnemyMoveset == 0 and EnemyAttackChoice == 3:
                EnemyAttackChoice = random.randrange(1,3)
            if EnemyMoveset == 2:
                EnemyAttackChoice = 0
            if EnemyName == "Hero's Bane":
                if Turn == 0:
                    EnemyAttackChoice = 3
                elif Turn == 1:
                    if EnemyChanneled == 1:
                        EnemyAttackChoice = 1
                    else:
                        EnemyAttackChoice = 3
                    print("\nSmall Note: For combat you can use the first letter of the action (eg. Attack is a and defend is d)\n")
                else:
                    EnemyAttackChoice = 1                            
#Moveset0 1=Attack, 2=Defend, 3=Recover Moveset1 1=Attack, 2=Defend, 3=Channel, Moveset2 1=No moves
            while TurnActive == 1:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit(); quit()
                EnemyTurnActive = 1
                if EnemyHealth > 0:
                    EnemyHealthShow = round(EnemyHealth, 2)
                else:
                    EnemyHealthShow = 0
                pygame.draw.rect(gameDisplay, white, (606,46,606,306)); pygame.draw.rect(gameDisplay, black,(609,49,600,300))
                simpleText("Chara",(615,55),blue)
                if PlayerChanneled > 0:
                    simButton('charged',615,135,100,20,darkyellow)
                else:
                    simButton('charged',615,135,100,20,darkgray)
                simpleText("Health:"+str(playerHealth)+"/"+str(playerMaxHealth),(615,105),white,fancyFont)
                simpleText(EnemyNameDefiniteArticle+EnemyName,(615,155),red)
                simpleText("Health:"+str(EnemyHealthShow)+"/"+str(EnemyMaxHealth),(615,205),white,fancyFont)
                PMpS = ''
                PMpSColour = red
                for c,item in enumerate(combatChoiceList):
                    if returnButton(item[0],1100,c*50+55,100,20,red,darkred) == True and tempTicks >= tempBar:
                        tempBar = tempTicks + 60
                        PlayerAttackChoice = item[1]
                        PMpS = item[0]

                
                pygame.display.update()
                if PlayerAttackChoice == "a":
                    TurnActive = 0
                    Turn = Turn + 1
                    print("You have chosen to attack " + EnemyNameDefiniteArticle.lower() + EnemyName + "!")
                    if random.randrange(0,101) <= playerPrecision + 5 or PlayerChanneled == 1:
                        if PlayerChanneled == 1:
                            print("Because of your channeled focus and concentration, you got a critical attack")
                            PlayerChanneled = 0
                        else:
                            print("You got a critical hit!")
                        if EnemyAttackChoice == 2:
                            print("Your critical hit means that your attacks land on " + EnemyNameDefiniteArticle.lower() + EnemyName + " despite it being in a defensive position.")
                        if ((playerWeaponDamage * (((playerStrength/10)+1))*2)-EnemyArmor) > 0:
                            print("You attacked " + EnemyNameDefiniteArticle.lower() + EnemyName + " for " + str(((playerWeaponDamage * ((playerStrength/10)+1))*2)-EnemyArmor) + " damage.")
                            EnemyHealth = EnemyHealth - (((playerWeaponDamage * ((playerStrength/10)+1))*2)-EnemyArmor)
                            if checkEnemyAlive(EnemyHealth,EnemyNameDefiniteArticle,EnemyName,BattleXPReward) == True:
                                print(EnemyNameDefiniteArticle + EnemyName + " is now on " + str(EnemyHealth) + " health.")
                                print("---------------------------Player Turn over---------------------------")
                                if EnemyMoveset == 0:
                                    if EnemyAttackChoice == 3:
                                        print(EnemyNameDefiniteArticle + EnemyName + " attempted to recover health, but was interrupted by your attack.")
                                        print("---------------------------Enemy Turn over----------------------------")
                                        EnemyTurnActive = 0
                                elif EnemyMoveset == 1:
                                    if EnemyAttackChoice == 3:
                                        print(EnemyNameDefiniteArticle + EnemyName + " attempted to channel focus and concentration, but was interrupted by your attack.")
                                        print("---------------------------Enemy Turn over----------------------------")
                                        EnemyTurnActive = 0
                                if EnemyAttackChoice == 2:
                                    print("---------------------------Enemy Turn over----------------------------")
                                    EnemyTurnActive = 0
                            else:
                                BattleActive = 0
                        else:
                            print(EnemyNameDefiniteArticle + EnemyName + "'s armor is too strong for your attack. You did no damage.")
                            if EnemyMoveset == 0:
                                if EnemyAttackChoice == 3:
                                    print(EnemyNameDefiniteArticle + EnemyName + " attempted to recover health, but was interrupted by your attack.")
                                    print("---------------------------Enemy Turn over----------------------------")
                                    EnemyTurnActive = 0
                            elif EnemyMoveset == 1:
                                if EnemyAttackChoice == 3:
                                    print(EnemyNameDefiniteArticle + EnemyName + " attempted to channel focus and concentration, but was interrupted by your attack.")
                                    print("---------------------------Enemy Turn over----------------------------")
                                    EnemyTurnActive = 0
                    else:
                        if random.randrange(0,101) <= EnemySpeed + 15:
                            PMpSColour = darkgray
                            print(EnemyNameDefiniteArticle + EnemyName + " avoided your attack.")
                            print("---------------------------Player Turn over---------------------------")
                        else:
                            if EnemyAttackChoice == 2:
                                print(EnemyNameDefiniteArticle + EnemyName + " is in a defensive stance, your attacks will do less damage.")
                                if ((playerWeaponDamage * (((playerStrength/10)+1))/2)-EnemyArmor) > 0:
                                    print("You attacked " + EnemyNameDefiniteArticle.lower() + EnemyName + " for " + str(((playerWeaponDamage * ((playerStrength/10)+1))/2)-EnemyArmor) + ".")
                                    EnemyHealth = EnemyHealth - (((playerWeaponDamage * ((playerStrength/10)+1))/2)-EnemyArmor)
                                    if checkEnemyAlive(EnemyHealth,EnemyNameDefiniteArticle,EnemyName,BattleXPReward) == True:
                                        print(EnemyNameDefiniteArticle + EnemyName + " is now on " + str(EnemyHealth) + " health.")
                                        print("---------------------------Player Turn over---------------------------")                                               
                                        print("---------------------------Enemy Turn over----------------------------")
                                        EnemyTurnActive = 0
                                    else:
                                        BattleActive = 0
                                else:
                                    print(EnemyNameDefiniteArticle + EnemyName + "'s armor is too strong for your attack. You did no damage.")
                                    if EnemyMoveset == 0:
                                        if EnemyAttackChoice == 3:
                                            print(EnemyNameDefiniteArticle + EnemyName + " attempted to recover health, but was interrupted by your attack.")
                                            print("---------------------------Enemy Turn over----------------------------")
                                            EnemyTurnActive = 0
                                    elif EnemyMoveset == 1:
                                        if EnemyAttackChoice == 3:
                                            print(EnemyNameDefiniteArticle + EnemyName + " attempted to channel focus and concentration, but was interrupted by your attack.")
                                            print("---------------------------Enemy Turn over----------------------------")
                                            EnemyTurnActive = 0

                            elif (playerWeaponDamage * ((playerStrength/10)+1)) - EnemyArmor > 0:
                                print("You attacked " + EnemyNameDefiniteArticle.lower() + EnemyName + " for " + str(((playerWeaponDamage * ((playerStrength/10)+1))-EnemyArmor)) + " damage.")
                                EnemyHealth = EnemyHealth - ((playerWeaponDamage * ((playerStrength/10)+1))-EnemyArmor)
                                if checkEnemyAlive(EnemyHealth,EnemyNameDefiniteArticle,EnemyName,BattleXPReward) == True:
                                    print(EnemyNameDefiniteArticle + EnemyName + " is now on " + str(EnemyHealth) + " health.")
                                    print("---------------------------Player Turn over---------------------------")
                                    if EnemyMoveset == 0:
                                        if EnemyAttackChoice == 3:
                                            print(EnemyNameDefiniteArticle + EnemyName + " attempted to recover health, but was interrupted by your attack.")
                                            print("---------------------------Enemy Turn over----------------------------")
                                            EnemyTurnActive = 0
                                    elif EnemyMoveset == 1:
                                        if EnemyAttackChoice == 3:
                                            print(EnemyNameDefiniteArticle + EnemyName + " attempted to channel focus and concentration, but was interrupted by your attack.")
                                            print("---------------------------Enemy Turn over----------------------------")
                                            EnemyTurnActive = 0
                                else:
                                    BattleActive = 0
                            else:
                                print(EnemyNameDefiniteArticle + EnemyName + "'s armor is too strong for your attack. You did no damage.")
                                if EnemyMoveset == 0:
                                    if EnemyAttackChoice == 3:
                                        print(EnemyNameDefiniteArticle + EnemyName + " attempted to recover health, but was interrupted by your attack.")
                                        print("---------------------------Enemy Turn over----------------------------")
                                        EnemyTurnActive = 0
                                elif EnemyMoveset == 1:
                                    if EnemyAttackChoice == 3:
                                        print(EnemyNameDefiniteArticle + EnemyName + " attempted to channel focus and concentration, but was interrupted by your attack.")
                                        print("---------------------------Enemy Turn over----------------------------")
                                        EnemyTurnActive = 0
                elif PlayerAttackChoice == "c":
                    TurnActive = 0
                    Turn = Turn + 1
                    print("You have chosen to try and channel your focus and concentration.")
                    if EnemyAttackChoice == 1:
                        print("You attempted to channel focus and concentration, but were interrupted by " + EnemyNameDefiniteArticle + EnemyName + "’s attack.")
                        print("---------------------------Player Turn over---------------------------")
                    else:
                        if PlayerChanneled == 1:
                            print("You tried to channel, but you are already channeled, and it had no effect.")
                            print("---------------------------Player Turn over---------------------------")
                        else:
                            print("You channeled your focus and concentration")
                            PlayerChanneled = 1
                            print("---------------------------Player Turn over---------------------------")
                elif PlayerAttackChoice == "d":
                    TurnActive = 0
                    Turn = Turn + 1
                    print("You have chosen to defend from " + EnemyNameDefiniteArticle.lower() + EnemyName + "!")
                    if not EnemyAttackChoice == 1:
                        print("But no attack occurred.")
                    print("---------------------------Player Turn over---------------------------")
                elif PlayerAttackChoice == "r":
                    TurnActive = 0
                    Turn = Turn + 1
                    print("You have selected to try and recover.")
                    if EnemyAttackChoice == 1:
                        print("You attempted to recover, but were interrupted by " + EnemyNameDefiniteArticle + EnemyName + "'s attack")
                        print("---------------------------Player Turn over---------------------------")
                    else:
                        PlayerRecoverySelection = random.randrange(1,11)
                        if PlayerRecoverySelection >= 1 and PlayerRecoverySelection <= 4:
                            playerHealth = playerHealth + (playerMaxHealth/10)
                            if Playerhealth > playerMaxHealth:
                                Playerhealth = playerMaxHealth
                            print("You recovered a small amount of health."); time.sleep(1*TT0)
                            print("You are now on " + str(playerHealth) + " health.")
                        elif PlayerRecoverySelection >= 5 and PlayerRecoverySelection <= 9:
                            playerHealth = playerHealth + (playerMaxHealth/4)
                            if playerHealth > playerMaxHealth:
                                playerHealth = playerMaxHealth
                            print("You recovered a substantial amount of health.")
                            print("You are now on " + str(playerHealth) + " health.")
                        elif PlayerRecoverySelection == 10:
                            playerHealth = playerHealth + (playerMaxHealth/4)
                            if playerHealth > playerMaxHealth:
                                playerHealth = playerMaxHealth
                            print("You recovered a substantial amount of health.")
                            print("You are now on " + str(playerHealth) + " health.")
                        print("---------------------------Player Turn over---------------------------")
                elif PlayerAttackChoice == "i":
                    usableItems = False
                    for item in inventoryDict:
                        if item in combatUsableItemList and inventoryDict[item] > 0:
                            usableItems = True
                    if usableItems:
                        Turn += 1
                        tempVar1 = combatInventoryInterface()
                        if tempVar1 in combatUsableItemList:
                            TurnActive = 0
                            if tempVar1 == "cured meat":
                                playerHealth += 10
                        else:
                            TurnActive = 0
                        EnemyTurnActive = 0
                        screenReset(20)
                    else:
                        TurnActive = 0
                        EnemyTurnActive = 0
                        print("no usable items")
                elif PlayerAttackChoice == "m":
                    Turn = Turn + 1
                    print("You have chosen to use magic.")
                    print("---------------------------Player Turn over---------------------------")
                else:
                    EnemyTurnActive = 0
#EnemyTurn
                if EnemyTurnActive == 1 and BattleActive == 1:
                    if EnemyAttackChoice == 0:
                        if EnemyMaxHealth*0.75 < EnemyHealth:
                            print(EnemyNameDefiniteArticle + EnemyName + " sits idly by. It has no wish to harm you.")
                        elif EnemyMaxHealth/2 < EnemyHealth:
                            print(EnemyNameDefiniteArticle + EnemyName + " is not doing much.")
                        elif EnemyMaxHealth*0.25 < EnemyHealth:
                            if random.randrange(1,3) == 1:
                                print(EnemyNameDefiniteArticle + EnemyName + " is looking around nervously.")
                            else:
                                print(EnemyNameDefiniteArticle + EnemyName + " is looking around fearfully")
                        else:
                            print(EnemyNameDefiniteArticle + EnemyName + " is in an extremely panicked state, but will not attack you.")
                    elif EnemyAttackChoice == 1:
                        EnemyTurnActive = 0
                        print(EnemyNameDefiniteArticle + EnemyName + " has chosen to attack you.")
                        if random.randrange(0,101) <= EnemyPrecision + 5 or EnemyChanneled == 1:
                            if EnemyChanneled == 1:
                                print("Because of " + EnemyNameDefiniteArticle + EnemyName + "s channeled focus and concentration, it got a critical hit.")
                                EnemyChanneled = 0
                            else:
                                print(EnemyNameDefiniteArticle + EnemyName + " got a critical hit!")
                            if PlayerAttackChoice == "d":
                                print(EnemyNameDefiniteArticle + EnemyName + "'s critical hits mean that its attacks land on you despite you being in a defensive position.")
                            if ((EnemyAttackDamage*2)-playerArmor) > 0:
                                print(EnemyNameDefiniteArticle + EnemyName + " attacked you for " + str(((EnemyAttackDamage*2)-playerArmor)) + " damage.")
                                playerHealth = playerHealth - ((EnemyAttackDamage*2)-playerArmor)
                                if checkPlayerAlive(playerHealth,BattleDeathMessage) == True:
                                    print("You are now on " + str(playerHealth) + " health.")
                                else:
                                    BattleActive = 0
                            else:
                                print("Your armor is too strong for " + EnemyNameDefiniteArticle + EnemyName + "'s attacks. It did no damage to you.")
                        else:
                            EnemySpeedCheck = random.randrange(0,101)
                            if PlayerAttackChoice == "c":
                                EnemySpeedCheck = 101
                            if EnemySpeedCheck <= playerAgility + 15:
                                EMpSColour = darkgray
                                print("You avoided " + EnemyNameDefiniteArticle + EnemyName + "'s attacks.")
                            else:
                                if PlayerAttackChoice == "d":
                                    print("You are in a defensive stance, " + EnemyNameDefiniteArticle + EnemyName + "'s attacks will do less damage.")
                                    if ((EnemyAttackDamage/2)-playerArmor) > 0:
                                        print(EnemyNameDefiniteArticle + EnemyName + " attacked you for " + str(((EnemyAttackDamage/2)-playerArmor)) + " damage.")
                                        playerHealth = playerHealth - ((EnemyAttackDamage/2) - playerArmor)
                                        if checkPlayerAlive(playerHealth,BattleDeathMessage) == True:
                                            print("You are now on " + str(playerHealth) + " health.")
                                        else:
                                            BattleActive = 0
                                    else:
                                        print("Your armor is too strong for " + EnemyNameDefiniteArticle + EnemyName + "'s attacks. It did no damage to you.")
                                else:
                                    if (EnemyAttackDamage - playerArmor) > 0:
                                        print(EnemyNameDefiniteArticle + EnemyName + " attacked you for " + str(EnemyAttackDamage - playerArmor) + " damage.")
                                        playerHealth = playerHealth - (EnemyAttackDamage - playerArmor)
                                        if checkPlayerAlive(playerHealth,BattleDeathMessage) == True:
                                            print("You are now on " + str(playerHealth) + " health.")
                                        else:
                                            BattleActive = 0
                                    else:
                                        print("Your armor is too strong for " + EnemyNameDefiniteArticle + EnemyName + "'s attacks. It did no damage to you.")
                    elif EnemyAttackChoice == 2:
                        print(EnemyNameDefiniteArticle + EnemyName + " has chosen to defend.")
                        print("But no attack occured.")
                        EnemyTurnActive = 0
                    elif EnemyAttackChoice == 3:
                        if EnemyMoveset == 0:
                            print(EnemyNameDefiniteArticle + EnemyName + " has chosen to recover.")
                            EnemyRecoverySelection = random.randrange(1,11)
                            if EnemyRecoverySelection >= 1 and EnemyRecoverySelection <= 4:
                                EnemyHealth += (EnemyMaxHealth/10)
                                if EnemyHealth > EnemyMaxHealth:
                                    EnemyHealth = EnemyMaxHealth
                                print(EnemyNameDefiniteArticle + EnemyName + " recovered a small amount of health.")
                                print(EnemyNameDefiniteArticle + EnemyName + " is now on " + str(EnemyHealth) + " health.")
                            elif EnemyRecoverySelection >= 5 and EnemyRecoverySelection <= 9:
                                EnemyHealth = EnemyHealth + (EnemyMaxHealth/4)
                                if EnemyHealth > EnemyMaxHealth:
                                    EnemyHealth = EnemyMaxHealth
                                print(EnemyNameDefiniteArticle + EnemyName + " recovered a substantial amount of health.")
                                print(EnemyNameDefiniteArticle + EnemyName + " is now on " + str(EnemyHealth) + " health.")
                            elif EnemyRecoverySelection == 10:
                                EnemyHealth = EnemyHealth + (EnemyMaxHealth/4)
                                if EnemyHealth > EnemyMaxHealth:
                                    EnemyHealth = EnemyMaxHealth
                                print(EnemyNameDefiniteArticle + EnemyName + " recovered a substantial amount of health.")
                                print(EnemyNameDefiniteArticle + EnemyName + " is now on " + str(EnemyHealth) + " health.")
                            EnemyTurnActive = 0
                        elif EnemyMoveset == 1:
                            print(EnemyNameDefiniteArticle + EnemyName + " has chosen to channel focus and concentration.")
                            EnemyChanneled = 1
                            EnemyTurnActive = 0
                    EnemyTurnActive = 1
                    if EnemyHealth > 0:
                        EnemyHealthShow = round(EnemyHealth, 2)
                    else:
                        EnemyHealthShow = 0
                    pygame.draw.rect(gameDisplay, white, (606,46,606,306)); pygame.draw.rect(gameDisplay, black,(609,49,600,300))
                    simpleText("Chara",(615,55),blue)
                    if PlayerChanneled > 0:
                        simButton('charged',615,135,100,20,darkyellow)
                    else:
                        simButton('charged',615,135,100,20,darkgray)
                    simpleText("Health:"+str(playerHealth)+"/"+str(playerMaxHealth),(615,105),white,fancyFont)
                    simpleText(EnemyNameDefiniteArticle+EnemyName,(615,155),red)
                    simpleText("Health:"+str(EnemyHealthShow)+"/"+str(EnemyMaxHealth),(615,205),white,fancyFont)
                    for c,item in enumerate(combatChoiceList):
                        if item[1] == PlayerAttackChoice:
                            simButton(item[0],1100,c*50+55,100,20,darkred)
                        else:
                            simButton(item[0],1100,c*50+55,100,20,red)
                    pygame.display.update()
                    print("---------------------------Enemy Turn over----------------------------"); time.sleep(1)
                tempTicks += 1
                if TurnActive == 0:
                    EMpS = ""
                    EMpSColour = red
                    if EnemyMoveset == 0:
                        if EnemyAttackChoice == 1:
                            EMpS = "attack"
                        elif EnemyAttackChoice == 2:
                            EMpS = "defend"
                        elif EnemyAttackChoice == 3:
                            EMpS = "recover"
                    elif EnemyMoveset == 1:
                        if EnemyAttackChoice == 1:
                            EMpS = "attack"
                        elif EnemyAttackChoice == 2:
                            EMpS = "defend"
                        elif EnemyAttackChoice == 3:
                            EMpS = "channel"
                    pygame.draw.rect(gameDisplay, white, (606,46,606,306)); pygame.draw.rect(gameDisplay, black,(609,49,600,300))
                    simpleText("Chara",(615,55),blue)
                    if PlayerChanneled > 0:
                        simButton('charged',615,135,100,20,darkyellow)
                    else:
                        simButton('charged',615,135,100,20,darkgray)
                    simpleText("Health:"+str(playerHealth)+"/"+str(playerMaxHealth),(615,105),white,fancyFont)
                    simpleText(EnemyNameDefiniteArticle+EnemyName,(615,155),red)
                    simpleText("Health:"+str(EnemyHealthShow)+"/"+str(EnemyMaxHealth),(615,205),white,fancyFont)
                    for c,item in enumerate(combatChoiceList):
                        if item[1] == PlayerAttackChoice:
                            simButton(item[0],1100,c*50+55,100,20,darkred)
                        else:
                            simButton(item[0],1100,c*50+55,100,20,red)
                    simButton(EMpS,750,155,100,20,red); simButton(PMpS,750,55,100,20,PMpSColour); pygame.display.update()
                    pygameSleep(2)
                    #Moveset0 1=Attack, 2=Defend, 3=Recover Moveset1 1=Attack, 2=Defend, 3=Channel, Moveset2 1=No moves
        else:
            BattleActive = 0


def lootInterface(lootPileDict = {},returnLPD = False,specialExit=False):
    global inventoryDict
    
    pygame.draw.rect(gameDisplay, white, (6,46,606,306)); pygame.draw.rect(gameDisplay, black,(9,49,600,300))
    finished = False
    escPressed = False
    tempTicks = 0
    tempBar = 0
    while not finished:
        buttonPressed = False
        if escPressed:
            outDict = {}
            for myItem in inventoryDict:
                if inventoryDict[myItem] != 0:
                    outDict[myItem] = inventoryDict[myItem]
            inventoryDict = outDict
            break
        eventList = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    escPressed = True
                elif event.key == pygame.K_t:
                    for myItem in inventoryDict:
                        itemModify(lootPileDict,[myItem,inventoryDict[myItem]],0)
                        pygame.draw.rect(gameDisplay, white, (6,46,606,306)); pygame.draw.rect(gameDisplay, black,(9,49,600,300))
                    pygame.display.update()
                elif event.key == pygame.K_e:
                    for item in lootPileDict:
                        itemModify(lootPileDict,[item,lootPileDict[item]],1)
                        pygame.draw.rect(gameDisplay, white, (6,46,606,306)); pygame.draw.rect(gameDisplay, black,(9,49,600,300))
        if not escPressed:
            tempID = inventoryDict
            tempLPD = lootPileDict
            c = 0
            for myItem in tempID:
                interfaceShow(str(myItem),10,c*30+50); interfaceShow(str(inventoryDict[myItem]),130,c*30+50)
                c += 1
            c = 0
            for item in tempLPD:
                interfaceShow(str(item),270,c*30+50); interfaceShow(str(lootPileDict[item]),390,c*30+50)
                c += 1
            c = 0
            for myItem in tempID:
                tempDict = transferButton('>',160,c*30+50,30,20,green,darkgreen,lootPileDict,[myItem,1],0)
                if tempDict != False and tempTicks >= tempTicks:
                    buttonPressed = True
                    lootPileDict = tempDict
                    pygame.draw.rect(gameDisplay, white, (6,46,606,306)); pygame.draw.rect(gameDisplay, black,(9,49,600,300))
                c += 1
            c = 0
            for item in tempLPD:
                tempDict = transferButton('<',420,c*30+50,30,20,green,darkgreen,lootPileDict,[item,1],1)
                if tempDict != False and tempTicks >= tempTicks:
                    buttonPressed = True
                    lootPileDict = tempDict
                    pygame.draw.rect(gameDisplay, white, (6,46,606,306)); pygame.draw.rect(gameDisplay, black,(9,49,600,300))
                c += 1
            if returnButton('finish',500,60,100,20,red,darkred) == True:
                buttonPressed = True
                outDict = {}
                for myItem in inventoryDict:
                    if inventoryDict[myItem] != 0:
                        outDict[myItem] = inventoryDict[myItem]
                inventoryDict = outDict
                finished = True
            if returnButton('transfer all',500,90,100,20,red,darkred) == True:
                buttonPressed = True
                for myItem in inventoryDict:
                    itemModify(lootPileDict,[myItem,inventoryDict[myItem]],0)
                    pygame.draw.rect(gameDisplay, white, (6,46,606,306)); pygame.draw.rect(gameDisplay, black,(9,49,600,300))
            if returnButton('take all',500,120,100,20,red,darkred) == True:
                buttonPressed = True
                for item in lootPileDict:
                    itemModify(lootPileDict,[item,lootPileDict[item]],1)
                    pygame.draw.rect(gameDisplay, white, (6,46,606,306)); pygame.draw.rect(gameDisplay, black,(9,49,600,300))
            if specialExit:
                if returnButton(specialExit[0],500,160,100,20,red,darkred):
                    return specialExit[1]
                    break
            #simButton time
            if buttonPressed:
                tempBar = tempTicks + 60
                tempID = inventoryDict
                tempLPD = lootPileDict
                c = 0
                for myItem in tempID:
                    interfaceShow(str(myItem),10,c*30+50); interfaceShow(str(inventoryDict[myItem]),130,c*30+50)
                    c += 1
                c = 0
                for item in tempLPD:
                    interfaceShow(str(item),270,c*30+50); interfaceShow(str(lootPileDict[item]),390,c*30+50)
                    c += 1
                c = 0
                for myItem in tempID:
                    simButton('>',160,c*30+50,30,20,green,darkgreen)
                    c += 1
                c = 0
                for item in tempLPD:
                    simButton('<',420,c*30+50,30,20,green,darkgreen)
                    c += 1
                simButton('finish',500,60,100,20,red,darkred)
                simButton('transfer all',500,90,100,20,red,darkred)
                simButton('take all',500,120,100,20,red,darkred)
            pygame.display.update()
            clock.tick(15)
    if escPressed or finished:
        if returnLPD:
            outDict = {}
            for item in lootPileDict:
                if lootPileDict[item] != 0:
                    outDict[item] = lootPileDict[item]
            return(outDict)
    tempTicks += 1
usableItemList = ["cured meat","car"]

##def storeThing():
##    text = ''
##    tempVar = wholeTableConvert(table,1)
##    for y in tempVar:
##        for x in y:
##            text = text + x
##        text = text + '\n'
##    with open("map.txt",'w') as file:
##        file.write(text)

def inventoryInterface():
    global inventoryDict, playerHealth, transportMode
    escPressed = False
    tempTick = 0
    tempBar = 0
    while not escPressed:
        pygame.draw.rect(gameDisplay, white, (1256,46,236,306)); pygame.draw.rect(gameDisplay, black,(1259,49,230,300))
        itemPressed = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    escPressed = True
        tempID = inventoryDict
        simpleText("Health:"+str(playerHealth)+"/"+str(playerMaxHealth),(1262,50),white,fancyFont)
        for c,myItem in enumerate(tempID):
            interfaceShow(str(myItem),1262,c*30+80); interfaceShow(str(inventoryDict[myItem]),1392,c*30+80)
            if myItem in usableItemList and inventoryDict[myItem] > 0:
                if returnButton("use",1420,c*30+80,60,20,green,darkgreen) == True:
                    itemPressed = myItem
            else:
                simButton("use",1420,c*30+80,60,20,darkgray)
        if itemPressed != None and tempTick >= tempBar:
            tempBar = tempTick + 60
            if itemPressed == "cured meat":
                inventoryDict["cured meat"] -= 1
                playerHealth += 10
                if playerHealth > playerMaxHealth:
                    playerHealth = playerMaxHealth
            elif itemPressed == "car":
                tempLoc = getPos()
                if transportMode == 1:
                    transportMode = 0
                elif transportMode == 0:
                    transportMode = 1
                
                showTablePers(); PDU()
                
        pygame.display.update()
        tempTick += 1

combatUsableItemList = ["cured meat","bolas"]
def reverseIn(element,li):
    li = li[::-1]
    for c,item in enumerate(li):
        if item == element:
            return c
def combatInventoryInterface():
    global inventoryDict
    pygame.draw.rect(gameDisplay, white, (1256,46,236,306)); pygame.draw.rect(gameDisplay, black,(1259,49,230,300))
    escPressed = False
    tempTick = 0
    tempBar = 0
    itemPressed = None
    while itemPressed == None:
        pygame.draw.rect(gameDisplay, white, (1256,46,236,306)); pygame.draw.rect(gameDisplay, black,(1259,49,230,300))
        itemPressed = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    escPressed = True
        tempID = inventoryDict
        simpleText("Health:"+str(playerHealth)+"/"+str(playerMaxHealth),(1262,50),white,fancyFont)
        for c,myItem in enumerate(tempID):
            interfaceShow(str(myItem),1262,c*30+80); interfaceShow(str(inventoryDict[myItem]),1392,c*30+80)
            if myItem in combatUsableItemList and inventoryDict[myItem] > 0:
                if returnButton("use",1420,c*30+80,60,20,green,darkgreen) == True:
                    itemPressed = myItem
            else:
                simButton("use",1420,c*30+80,60,20,darkgray)
        if itemPressed != None and tempTick >= tempBar:
            inventoryDict["cured meat"] -= 1
            tempBar = tempTick + 60
        pygame.display.update()
        tempTick += 1
    return(itemPressed)
def wildHouse(difficulty=1,lootQuality=1):
    print("You have entered a feral house."); time.sleep(1)
    if random.randrange(1,6) > 2 + difficulty: 
        DialogueChain(["You hear a faint pair of footsteps.",1,"You are attacked by an overgrown human.",1])
    else:
        print("The house appears to be uninhabited."); time.sleep(1)
    DialogueChain(["Water replenished.",1,"You search the house for supplies",1])

def boardReset(inpWater):
    global seenSet
    gameDisplay.fill(black); score("Water",inpWater)
    seenSet = {(uX,uY)}
    seeArea(uX,uY,2)
    showTablePers(uX,uY); pygame.display.update()

def gLDeadCheck(health,water=20):
    if health > 0:
        if water > 0:
            return False
        else:
            return True
    else:
        return True
def PDU():
    pygame.display.update()
keySet = set()
def keySetMake(li):
    global keySet
    for event in pygame.event.get():
        print("hi1")
        for key,item in li:
            print(key,item,event)
            if event.type == pygame.KEYDOWN and event.key == key:
                keySet.add(item)
            elif event.type == pygame.KEYUP and event.key == key:
                if item in keySet:
                    keySet.remove(item)

#============================================
#(py)game
#============================================
gameDisplay.fill(black)
seeArea(uX,uY,2); showTablePers()
spawnPos = (uX,uY)
simpleText("hey")#FreeMono, Monospace
progressStore = (table,inventoryDict,stockpileLootDict,seenSet,(gridW,gridH))

movesLi = [[pygame.K_UP,"up"],[pygame.K_DOWN,"down"],[pygame.K_RIGHT,"right"],[pygame.K_LEFT,"left"],[pygame.K_w,"up"],[pygame.K_s,"down"],[pygame.K_d,"right"],[pygame.K_a,"left"]]
pygame.display.update()
def gameLoop():
    global seenSet, stockpileLootDict, inventoryDict, playerHealth, table, progressStore, backupSeenSet, keySet, transportMode, uX,uY
    keySet = set()
    uX = math.floor(gridW/2)
    uY = math.floor(gridH/2)

    table[math.floor(gridH/2)][math.floor(gridW/2)] = 'S'
    transportMode = 0
    inventoryList = []
    maxWeight = 100
    weight = 0
    maxHealth = 20
    playerHealth = maxHealth
    maxWater = 2000
    water = maxWater

    seeArea(uX,uY,2)
    
    GameExit, NextTurn, moved, keyUp = False, False, False, False
    
    preTile = 'S'
    moves = 0
    mainTicks = 0
    while not GameExit:
        eventTypeList = []
        if transportMode == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); quit()
                if NextTurn == False:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                            if locationValid(uX+1,uY):
                                uX += 1
                                NextTurn = True
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                            if locationValid(uX-1,uY):
                                uX -= 1
                                NextTurn = True
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                            if locationValid(uX,uY+1):
                                uY += 1
                                NextTurn = True
                        elif event.key == pygame.K_UP or event.key == pygame.K_w:
                            if locationValid(uX,uY-1):
                                uY -= 1
                                NextTurn = True
                        elif event.key == pygame.K_i:
                            inventoryInterface()
                            screenReset(water)
                if event.type == pygame.KEYUP:
                    keyUp = True
        elif transportMode == 1:
            moved = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); quit()
                for key,item in movesLi:
                    if event.type == pygame.KEYDOWN and event.key == key:
                        keySet.add(item)
                    elif event.type == pygame.KEYUP and event.key == key:
                        if item in keySet:
                            keySet.remove(item)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                    inventoryInterface(); screenReset(water); PDU()
            if (not ("right" in keySet and "left" in keySet)) and ("right" in keySet or "left" in keySet) and mainTicks%2 == 0:
                if "right" in keySet:
                    if locationValid(uX+1,uY):
                        uX += 1
                    elif uSX > 0:
                        uX = 0
                        uSX -= 1
                    moved = True
                elif "left" in keySet:
                    if locationValid(uX-1,uY):
                        uX -= 1
                    elif uSX < sectorGridW-1:
                        uX = gridW - 1
                        uSX += 1
                    moved = True
            if (not ("up" in keySet and "down" in keySet)) and ("up" in keySet or "down" in keySet) and mainTicks%2 == 0:
                if "up" in keySet:
                    if locationValid(uX,uY-1):
                        uY -= 1
                    elif uSY < sectorGridH-1:
                        uY = gridH - 1
                        uSY += 1
                    moved = True
                elif "down" in keySet:
                    if locationValid(uX,uY+1):
                        uY += 1
                    elif uSY > 0:
                        uY = 0
                        uSY -= 1
                    moved = True
        if (keyUp and transportMode == 0) or (moved and transportMode == 1):
            keyUp = False
            if NextTurn or moved:
                moves += 1
                if transportMode != 1:
                    if preTile == '#':
                        if random.randrange(1,51) == 1:
                            screenReset(water)
                            Combat(1,"It laughs.","a ","The ","Troll",10,10,1,5,4,10); screenReset(water)
                            if not gLDeadCheck(playerHealth):
                                lootInterface(lootListGeneration("Troll"))
                    elif preTile == '=':
                        if random.randrange(1,101) == 1:
                            screenReset(water)
                            Combat(1,"She turns you into fuel.","","The ","Angry Maxine",10,10,1,50,4,10); screenReset(water)
                            if not gLDeadCheck(playerHealth):
                                lootInterface(lootListGeneration("AngryMaxine"))
                    else:
                        if random.randrange(1,4) + (moves % 3) == 1:
                            screenReset(water)
                            Combat(1,"It laughs.","a ","The ","Troll",10,10,1,random.randrange(5,20,5),4,10); screenReset(water)
                            if not gLDeadCheck(playerHealth):
                                lootInterface(lootListGeneration("Troll"))
                NextTurn = False
                print(len(getTable(table)[0]))
                seeArea(uX,uY,2+transportMode)
                if transportMode != 1:
                    water -=1
                screenReset(water)
                if water <= 0:
                    GameExit = True
                tileTempVar = table[uY][uX]
                if tileTempVar in buildingNameList and (transportMode != 1 or tileTempVar == 'S') :
                    keySet = set()
                    if tileTempVar == 'H':
                        messageDisplay("Entering house"); PDU()
                        table = inPathBuild(table,(uX,uY),(math.floor(gridW/2),math.floor(gridH/2)))
                        pygameSleep(1)
                        water = maxWater
                        pygame.draw.rect(gameDisplay,black,(0,0,200,30))
                        score("Water",water); pygame.display.update()
                        if not gLDeadCheck(playerHealth):
                            lootInterface(lootListGeneration("OldHuman"))
                        table[uY][uX] = 'o'
                    elif tileTempVar == 'S':
                        water = maxWater
                        screenReset(water)
                        table = listReplace(table,'o','O',2)
                        pygame.draw.rect(gameDisplay,black,(0,0,200,30))
                        backupSeenSet = copy.deepcopy(backupSeenSet)
                        
                        score("Water",water); pygame.display.update()
                        tempVar = lootInterface(stockpileLootDict,True,["save","save"])
                        if tempVar == 'save':
                            introChoiceList = [["Save File 1",'1'],["Save File 2",'2'],["Save File 3",'3'],["Save File 4",'4'],["Save File 5",'5'],["Save File 6",'6']]
                            menuExit = False
                            while not menuExit:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit(); quit()
                                    for c,item in enumerate(introChoiceList):
                                        if returnButton(item[0],1100,c*50+55,100,20,red,darkred) == True:
                                            startMode = item[1]
                                            menuExit = True
                                    pygame.display.update()
                                clock.tick(60)
                            save("SaveFile"+startMode,stockpileLootDict)
                        else:
                            stockpileLootDict = tempVar
                    elif tileTempVar == 'O':
                        water = maxWater
                        score("Water",water); pygame.display.update()
                        lootInterface(lootListGeneration("Outpost"))
                        table[uY][uX] = 'o'
                screenReset(water)
                preTile = table[uY][uX]
                GameExit = gLDeadCheck(playerHealth,water)
        clock.tick(60)
        mainTicks += 1

while True:
    gameLoop()
    messageDisplay("You died!")
    pygame.display.update()
    seenSet = copy.deepcopy(backupSeenSet)
    inventoryDict = set()
    uX,uY = math.floor(gridW/2), math.floor(gridH/2)
    pygameSleep(4)
    gameDisplay.fill(black)#; showTablePers(); PDU()
save()

