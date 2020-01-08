import pygame,math,pickle
from copy import deepcopy
from random import randrange

displayHeight = 900       
displayWidth = 1500


dw,dh = displayWidth,displayHeight

hDH = displayHeight//2
hDW = displayWidth//2

pygame.init()
screen = pygame.display.set_mode((displayWidth,displayHeight))
pygame.display.set_caption("A Dark Place")
clock = pygame.time.Clock()

pygame.font.init()
myfont = pygame.font.SysFont("monospace", 20)
fancyFont = pygame.font.SysFont("calibri", 22)
smallFont = pygame.font.SysFont("calibri", 10)
from main_info.sources.colours import *
from main_info.sources.functions import *

#============================================
#visual/screen mechanics
#============================================

def transpRect(colour,rect,wi,opacity=200):
    surface = pygame.Surface(rect[2:], pygame.SRCALPHA, 32)
    pygame.draw.rect(surface,list(colour)+[opacity],[0]*2+rect[2:],wi)
    screen.blit(surface,rect[:2])
    
def colourMix(c1,c2,transparency=0.2):
    tr = [transparency*2,2-(transparency*2)]
    return tuple([int((c1[n]*tr[0]+c2[n]*tr[1])//2) for n in range(3)])

def rEnumerate(li):
    return [[c,i] for c,i in enumerate(li)][::-1]

def pygameSleep(seconds):
    ticks = 0
    while ticks < seconds*60:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
        ticks += 1
        clock.tick(60)

def textObjects(text,font,colour=white):
    textSurface = font.render(text,True,colour)
    return(textSurface, textSurface.get_rect())

def messageDisplay(text,colour=white):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = textObjects(text,largeText,colour)
    TextRect.center = (display_width/2),(display_height/2)
    screen.blit(TextSurf, TextRect)
    pygame.display.update()
def simpleText(inputText,co=(0,0),colour=lightgray,simpleFont = myfont,surf=screen):
    text = simpleFont.render(inputText, True, colour)
    surf.blit(text,co)
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1 and action != None: action()         
    else: pygame.draw.rect(screen, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("calibri",20)
    textSurf, textRect = textObjects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

def returnButton(msg,x,y,w,h,ic,ac):
    out = False
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1: out = True        
    else: pygame.draw.rect(screen, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("calibri",20)
    textSurf, textRect = textObjects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)
    return out
    
def simButton(msg,x,y,w,h,ic,ac = None):
    pygame.draw.rect(screen, ic,(x,y,w,h))
    if ac != None:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(screen, ac,(x,y,w,h))
    if msg == '<' or msg == '>': smallText = pygame.font.SysFont("calibri",20)
    else:
        smallText = pygame.font.SysFont("calibri",20)
    textSurf, textRect = textObjects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)
     
def score(header,score,co=(0,0),colour=white):
    font = pygame.font.SysFont("calibri", 22)
    text = font.render(header + ": " + str(score), True, white)
    screen.blit(text,co)

def interfaceShow(text,xDisp=0,yDisp=0):
    textList = text.split('\n')
    c = 0
    for pS in textList:
        simpleText(pS,(xDisp,c*20+yDisp),white,fancyFont)
        c += 1
def PDU(): pygame.display.update()

def swap(i,it): return it[(it.index(i)+1)%2]
def dictFlatten(d): return [d[k] for k in d]
def specSplit(st,spChar, exclusion=[]):
    eDict = {}
    for i in exclusion: eDict[i] = False
    out = [st]
    invalid = True
    while invalid:
        invalid = False
        for c,l in enumerate(out[-1]):
            if l in eDict: eDict[l] = swap(eDict[l],[True,False])
            if l == spChar and not any(dictFlatten(eDict)):
                invalid = True
                break
        if invalid: out = out[:-1] + [out[-1][:c]] + [out[-1][c+1:]]
    return out

#Reading info
def readLootTable(loc,alt=None):
    if loc == None: lines = alt
    else:
        with open(loc,'r') as f:
            lines = f.read().splitlines()[1:]
    outDict = {}
    lT = False
    for line in lines:
        if lT and line == "/l//": lT = False
        elif line == "/l//": lT = True
        elif lT:
            line = specSplit(line,' ',['\"'])
            outDict[line[0].replace('\"','')] = max(0,randrange(int(line[1].split(',')[0]),int(line[1].split(',')[1])))
        
    return outDict
def readEncounterScript(loc):
    out = []
    with open(loc,'r') as f:
        lines = f.read().splitlines()[1:]
    outDict = {}
    lT = False
    c = 0
    while c < len(lines):
        line = lines[c]
        c += 1
##    for line in lines:
        if lT and line == "/e//":
            lT = False; break
        elif line == "/e//":
            lT = True
            stage = 0# 0 - r(-), 1 - "-" , 2 - #\n#
            sInfo = [0,0,-1]
        elif lT:
            if stage == 0 and line[0] == 'r':
                print(line[2:-2])
                if (randrange(0,100) <= int(line[2:-2])):
                    options = []
                    stage = 1
                    sInfo[1] = c
                    sInfo[0] = 1
            elif stage == 1:
                if '"' in line and line[0] == 'd':
                    line = line.split('"')
                    if len(line) == 3: options.append( (c,line[1],'',0) )
                    else:
                        options.append( (c,line[1],line[3],int(line[4])) )
                if c == len(lines) or line[0] == 'r':
##                    c = sInfo[1]
                    choiceC = encounterInterface(options)
                    c = options[choiceC][0]
                    stage = 2
                    out = []
            elif stage == 2 and sInfo[2] < 1:
                if line == '#':
                    if sInfo[2] < 1:sInfo[2] += 1
                elif sInfo[2] > -1:
                    if '/' in line: out.append('/'+line)
                    else: out.append(line)
##    print(out)
    return out
    
                

##pygame.draw.rect(screen, white, (6,46,606,306)); pygame.draw.rect(screen, black,(9,49,600,300))

def encounterInterface(choices):
##    inv = user.inventory
    menuExit = False
    keys = pygame.key.get_pressed()
    while not menuExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and (keys[pygame.K_LALT] or keys[pygame.K_RALT])): pygame.quit(); quit()
        pygame.draw.rect(screen, white, (6,46,606,306),3); pygame.draw.rect(screen, black,(9,49,600,300))
        for c,choice in enumerate(choices):
            if choice[3] != 0: simpleText("uses " + str(choice[3]) + 'x' + choice[2].capitalize(), (330,52 + c*40) , white , fancyFont)
            if returnButton(choice[1],20,52+c*40,300,20,green,darkgreen) and (choice[3] == 0 or (choice[2] in user.inventoryDict and user.inventoryDict[choice[2]] >= choice[3])):
                out = c
                if choice[3] != 0: user.inventoryDict[choice[2]] -= choice[3]
                dictClear(user.inventoryDict,0)
                menuExit = True
        PDU()
        clock.tick(60)
    return out

save = 1
def autoFight(p,e):
    with open("main_info\\save_data\\save1\\user\\CombatScript.txt",'r') as f:
        txt = f.read().splitlines()
    for c,line in rEnumerate(txt):
        if line[0] == '#':
            del txt[c]
    for line in txt:
        if line[0] == '/' :
            for c,l in enumerate(line[1:]):
                if l == '/':
                    break
            c += 1
            com = line[1:c]
            line = line[c+1:]
            if com[0] == '!': can = True; com = com[1:]
            else: can = False
            got = False
            if com in ["all","else"]: got = True
            elif com == "charged" and p.channel: got = True
            elif com[:2] == "p<" and p.health < int(com[2:]): got = True
            elif com[:2] == "e<" and e.health < int(com[2:]): got = True

            if (got and (not can)) or ((not got) and can):
                choice = line[0]
                break
    return choice

#starting info
buildingNameList = ['H','c','W','I','S','O','P']
with open("main_info\\sources\\buildings\\_Directory.txt",'r') as f:
    txt = f.read().splitlines()
buildingKeyDict = {}
for l in txt:
    l = l.replace('\"','').split(':')
    buildingKeyDict[l[0]] = l[1]
rBuildingKeyDict = {}
for k in buildingKeyDict:
    rBuildingKeyDict[buildingKeyDict[k]] = k

itemDict = {}
with open("main_info\\sources\\items\\WeightIndex.txt",'r') as f:
    txt = f.read().splitlines()
for line in txt:
    line = specSplit(line,' ',['\"'])
    itemDict[line[0].replace('\"','')] = int(line[1])

usableItemList = ["cured meat","crawler"]
combatUsableItemList = ["cured meat","bolas"]
builtList = []

dirDict = {pygame.K_LEFT:[-1,0],pygame.K_RIGHT:[1,0],pygame.K_UP:[0,-1],pygame.K_DOWN:[0,1],pygame.K_a:[-1,0],pygame.K_d:[1,0],pygame.K_w:[0,-1],pygame.K_s:[0,1]}

combatChoiceList = [["Attack",'a'],["Channel",'c'],["Defend",'d'],["Recover",'r'],["Items",'i']]
aLi = [i[1] for i in combatChoiceList]
aDict = {}
for s,a in combatChoiceList:
    aDict[a] = s
conflictDict = {
'c':['a','A'],
'r':['a','A'],
'a':['d']
}
dim = [dw,dh]

craftingRecipesDict = {}
with open("main_info\\sources\\items\\Crafting.txt",'r') as f:
    lines = f.read().splitlines()
temp = ''
for line in lines:
    if line[0] == '=':
        if temp != '':
            craftingRecipesDict[temp[:-1]] = tempN
        tempN = line[1:]
        temp = ''
    else:
        temp += line + '\n'
craftingRecipesDict[temp[:-1]] = tempN

print(craftingRecipesDict)

for k in craftingRecipesDict:
    print(','.join([line.split('"')[1]+" x "+line.split('"')[2] for line in k.splitlines()]) + " = " + craftingRecipesDict[k].split('"')[1] + " x " + craftingRecipesDict[k].split('"')[2])

def dictClear(tDict,cri):
    out = []
    for key in tDict:
        if tDict[key] == cri:
            out.append(key)
    for key in out:
        del tDict[key]
class Enemy:
    channel = 0
    def __init__(self,name="troll",articles=['a',"the"],skill=[1,1],maxHealth=20,damage=3,armour=2):
        self.maxHealth,self.health = tuple([maxHealth]*2)
        self.precision, self.speed = tuple(skill)
        self.inDefArt, self.defArt = tuple(articles)
        self.name,self.damage,self.armour = name,damage,armour
    def isAlive(self):
        if self.health > 0: return True
        else: return False

class Town:
    def __init__(self,pPlayer):
        self.pPlayer = pPlayer
        self.population = 0
    def interact(self):
        menuExit = False
        while not menuExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); quit()

            pygame.draw.rect(screen, white, (6,46,606,306)); pygame.draw.rect(screen, black,(9,49,600,300))
            if returnButton("Exit",500,250,100,20,red,darkred): menuExit = True
            PDU()
class Player:
    autoFight = False
    inventoryDict = {"meat":5,"timber":2}
    stockpileLootDict= {"cured meat":5}
    stockpileSyncLi = []
    craftingDict = {}
    seenSet = set(); transportMode = 0
    pos = 20,20
    maxHealth,health = tuple([40]*2); precision, speed = 1,1; damage,armour = 4,2
    maxThirst = 20
    thirst = maxThirst
    omni = False
    transportMode = 1
    buildTile = 'o'
    compass = [1,0]
    def checkAlive(self):
        if self.health > 0 and self.thirst > 0: return True
        else: return False
    def seeArea(self,co,radius=3):
        x,y = tuple(co)
        c,w = 0,0
        for d in range(y-radius,y+radius+1):
            for r in range(x-w,x+w+1):
                self.seenSet.add((r,d))
            if c >= radius: w -= 1
            else: w += 1
            c += 1        
    def move(self,change):
        preTile = self.cMap.tile(self.pos)
        prePos = self.pos
        self.pos = [self.pos[n]+change[n] for n in range(len(change))]
        self.pos = [limit(self.pos[0],self.cMap.gridW-1,0),limit(self.pos[1],self.cMap.gridH-1,0)]
        if self.pos != prePos:
            if self.transportMode == 0:
                if preTile == '#': self.thirst = max(self.thirst-0.2,0)
                else: self.thirst = max(self.thirst-1,0)
            if not self.omni: self.seeArea(self.pos)
            tile = self.cMap.tile(self.pos)
            if tile == 'S':
                screen.fill(black)
                self.thirst = self.maxThirst
                self.cMap.showPers(user)
                self.interact(self.stockpileLootDict,1)
                for p,t in self.stockpileSyncLi:
                    self.cMap.table[p[1]][p[0]] = t
            elif tile in buildingKeyDict:
                screen.fill(black)
                self.encounter("building",buildingKeyDict[tile])
            if self.transportMode == 0:
                with open("main_info\\sources\\encounters\\Chance.txt",'r') as f:
                    txt = f.read().splitlines()[1:]
                sto = None
                for l in txt:
                    if l[0] == '/':
                        cTile = l[1:].replace('\"','')
                    elif cTile == tile:
                        l = l.split(':')
                        if chance(int(l[1]),100):
                            sto = l[0]
                            break
                if sto != None: self.encounter("creature",sto)
        
    def receiveKey(self,inEvent,mode=0):
        if mode == 0:
            if inEvent.type == pygame.KEYDOWN:
                k = inEvent.key
                if k in dirDict:
                    cha = dirDict[k]
                    self.move(cha)
                elif k == pygame.K_t:
                    if self.transportMode == 0: self.transportMode = 1
                    else: self.transportMode = 0
        elif mode == 1:
            keys = pygame.key.get_pressed()
            for k in dirDict:
                if keys[k]:
                    self.move(dirDict[k])

    breathingCycle = [0.6,1]
    breathingTB = [3,2]
    def passive(self,mode=None):
        if self.cMap.time == 2400: self.cMap.time = 0
        else: self.cMap.time += 1
        update = False
        if mode in [None]:
            if self.transportMode == 1:
                keys = pygame.key.get_pressed()
                for k in dirDict:
                    if keys[k]:
                        self.move(dirDict[k])
                        update = True
        if mode in [None]:
            co1 = self.pos
            co2 = self.cMap.center
            if co1 != co2:
                if co2[0] != co1[0]: self.compass = [pos(co2[0]-co1[0]),(co2[1]-co1[1])/(co2[0]-co1[0])*pos(co2[0]-co1[0])]
                else: self.compass = [0,pos(co2[1]-co1[1])]     
        if mode in [None,1]:    
            self.breathingCycle[0] += 0.01*self.breathingCycle[1]
            if self.breathingCycle[0] >= self.breathingTB[0]:
                self.breathingCycle = [self.breathingTB[0],-1]
            elif self.breathingCycle[0] <= self.breathingTB[1]:
                self.breathingCycle = [self.breathingTB[1],1]
                
        return update
    def inventoryInterface(self):
        escPressed = False
        tempTick = 0
        tempBar = 0
        deleteMenu = False
        while not escPressed:
            screen.fill(black)
            self.passive(1)
            self.cMap.showPers(self)
            #h-w, 840 - 1620; 1256
            pygame.draw.rect(screen, white, (dw-364,46,236,306)); pygame.draw.rect(screen, black,(dw-361,49,230,300))
            itemPressed = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        escPressed = True
                        
            simpleText("Health:"+str(self.health)+"/"+str(self.maxHealth),(dw-358,50),white,fancyFont)
            for c,myItem in enumerate(self.inventoryDict):
                interfaceShow(str(myItem),dw-358,c*30+80); interfaceShow(str(self.inventoryDict[myItem]),dw-228,c*30+80)
                if myItem in usableItemList and self.inventoryDict[myItem] > 0:
                    if returnButton("use",dw-200,c*30+80,60,20,green,darkgreen) == True:
                        itemPressed = myItem
                else: simButton("use",dw-200,c*30+80,60,20,darkgray)
                
            if itemPressed != None and tempTick >= tempBar:
                tempBar = tempTick + 60
                if itemPressed == "cured meat":
                    self.inventoryDict["cured meat"] -= 1
                    self.health = min(self.maxHealth,self.health + 10)
                elif itemPressed == "crawler":
                    self.transportMode = (self.transportMode+1)%2
            if returnButton("Bin",1420,300,60,20,red,darkred):
                print("tb implemented")
                
            pygame.display.update()
            tempTick += 1
        dictClear(self.inventoryDict,0)
                
    def combat(self,enemy):
        self.autoFight = False
        player = self
        player.channel = 0
        while player.checkAlive() and enemy.isAlive():
            #choice selection
            enemy.tChoice = aLi[randrange(len(aLi))]
            choiceMade = False
            tempTicks=0
            while not choiceMade:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit(); quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            if self.autoFight: self.autoFight = False
                            else: self.autoFight = True
                if self.autoFight and tempTicks > 30: player.tChoice = autoFight(self,enemy); choiceMade = True
                pygame.draw.rect(screen, white, (606,46,606,306)); pygame.draw.rect(screen, black,(609,49,600,300))
                if player.channel > 0: simButton('charged',615,135,100,20,darkyellow)
                else: simButton('charged',615,135,100,20,darkgray)
                simpleText("Chara",(615,55),blue)
                simpleText("Health:"+str(round(player.health,1))+"/"+str(player.maxHealth),(615,105),white,fancyFont)
                simpleText(enemy.defArt.capitalize()+' '+enemy.name,(615,155),red); simpleText("Health:"+str(round(enemy.health,1))+"/"+str(enemy.maxHealth),(615,205),white,fancyFont)
                PMpS = ''; PMpSColour = red
                for c,item in enumerate(combatChoiceList):
                    if returnButton(item[0],1100,c*50+55,100,20,red,darkred) == True and tempTicks > 60:
                        player.tChoice = item[1]
                        PMpS = item[0]
                        choiceMade = True
                PDU(); tempTicks += 1
            
            #evaluation
            for pers in [player,enemy]:
                if pers.tChoice == 'a' and (chance(4+pers.precision,100) or pers.channel == 1):
                    pers.tChoice = 'A'
            aspect = 1
            tTCList = []
            for pers,oth in [[player,enemy],[enemy,player]]:
                tTC = darkgreen
                tName, OName = ([None,"Player","Enemy"][aspect],[None,"Player","Enemy"][aspect*-1])
                valid = True
                if pers.tChoice in conflictDict:
                    if oth.tChoice in conflictDict[pers.tChoice]:
                        tTC = red
                        valid = False
                if valid:
                    if pers.tChoice == 'A':
                        oth.health = max(0,oth.health - pers.damage*2 + oth.armour//4)
                        pers.channel = 0
                        tTC = yellow
                    elif pers.tChoice == "a":
                        oth.health = max(0,oth.health - pers.damage + oth.armour)
                    elif pers.tChoice == "c":
                        if pers.channel == 0: pers.channel = 1
                        else: tTC = red
                    elif pers.tChoice == 'r':
                        div = 5
                        if chance(2,10): div = 6
                        elif chance(6,10):  div = 4
                        elif chance(1,10): div = 2
                        pers.health = min(pers.maxHealth,pers.health+pers.maxHealth/div)
                    elif pers.tChoice == 'd':
                        if oth.tChoice == 'a': pass
                        else: tTC = red
                tTCList.append(tTC)  
                aspect *= -1

            #showing
            pygame.draw.rect(screen, white, (606,46,606,306)); pygame.draw.rect(screen, black,(609,49,600,300))
            if player.channel > 0: simButton('charged',615,135,100,20,darkyellow)
            else: simButton('charged',615,135,100,20,darkgray)
            simpleText("Chara",(615,55),blue); simpleText("Health:"+str(round(player.health,1))+"/"+str(player.maxHealth),(615,105),white,fancyFont)
            simpleText(enemy.defArt.capitalize()+' '+enemy.name,(615,155),red); simpleText("Health:"+str(round(enemy.health,1))+"/"+str(enemy.maxHealth),(615,205),white,fancyFont)
            PMpS = ''; PMpSColour = red
            for c,item in enumerate(combatChoiceList):
                if returnButton(item[0],1100,c*50+55,100,20,red,darkred) and tempTicks > 60:
                    player.tChoice = item[1]                    
                    choiceMade = True
            simButton(aDict[enemy.tChoice.lower()],616,185,100,20,tTCList[1]); simButton(aDict[self.tChoice.lower()],616,85,100,20,tTCList[0])
            PDU(); tempTicks += 1
            if self.autoFight:pygameSleep(0.5)
            else: pygameSleep(2)
    def encounter(self,eType,key):
        if eType == "building":
            info = [False,None,False]
           #info = [buildpath,changeInto[],replinish thirst]
            with open("main_info\\sources\\buildings\\"+key+".txt",'r') as f:
                lines = f.read().splitlines()[1:]
            extraLines = readEncounterScript("main_info\\sources\\buildings\\"+key+".txt")
            for line in lines+extraLines:
                if line[0] == '/':
                    for c,l in enumerate(line[1:]):
                        if l == '/':
                            break
                    c += 1
                    com = line[1:c]
                    line = line[c+1:]
                    if com == 'a':
                        if line.split(' ')[0] == "BT": info[0] = True
                        elif line.split(' ')[0] == "RPW":info[2] = True
                    elif com == 't': info[1] = line[0]
                    elif com == "tA":
                        info[1] = line[0]
                        self.stockpileSyncLi.append([self.pos,line[2]])
            self.cMap.showPers(self)
            if info[0]:
                self.cMap.pathBuild(self.pos,self.cMap.center)
            if extraLines == []: self.interact(readLootTable("main_info\\sources\\buildings\\"+key+".txt"))
            else: self.interact(readLootTable(None,extraLines))
            if info[1] != None: self.cMap.setTile(self.pos,info[1])
            if info[2]: self.thirst = self.maxThirst
            
        elif eType == "creature":
            info = ["troll",['a',"the"],[1,1],20,3,2]
            with open("main_info\\sources\\encounters\\"+key+".txt",'r') as f:
                lines = f.read().splitlines()[1:]
            for line in lines:
                if line[0] == '/':
                    for c,l in enumerate(line[1:]):
                        if l == '/':
                            break
                    c += 1
                    com = line[1:c]
                    line = line[c+1:]
                    if com == 'n':
                        line = specSplit(line,' ','\"')
                        info[0] = line[0].replace('\"','')
                        info[1][0] = line[1].replace('\"','')
                        info[1][1] = line[2].replace('\"','')
                    elif com == 'st':
                        line = [int(i) for i in line.split(' ')]
                        info[2] = line[:2]
                        info[3:] = line[2:]
            self.combat(Enemy(*info))
            if self.checkAlive():
                self.interact(readLootTable("main_info\\sources\\encounters\\"+key+".txt"))
        dictClear(self.inventoryDict,0)
                    
    def isAlive(self):
        if self.health > 0: return True
        else: return False
        

    def interact(self,lootPileDict,lType=0):
        pygame.draw.rect(screen, white, (6,46,606,306)); pygame.draw.rect(screen, black,(9,49,600,300))
        finished, escPressed, update = False, False, True
        tempTicks, tempBar = 0,-5
        inventoryDict = self.inventoryDict
        kDict = {'t':False,'e':False}
        while not finished:
            buttonPressed = False
            if escPressed or finished:
                dictClear(inventoryDict,0)
                break
            
            eventList = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: escPressed = True
                    elif event.key == pygame.K_t: kDict['t'] = True
                    elif event.key == pygame.K_e: kDict['e'] = True
            if not escPressed:
                tempID = inventoryDict
                tempLPD = lootPileDict
                if update:
                    pygame.draw.rect(screen, white, (6,46,606,306)); pygame.draw.rect(screen, black,(9,49,600,300))
                    for c,myItem in enumerate(tempID): interfaceShow(str(myItem),10,c*30+50); interfaceShow(str(inventoryDict[myItem]),130,c*30+50)
                    for c,item in enumerate(tempLPD): interfaceShow(str(item),270,c*30+50); interfaceShow(str(lootPileDict[item]),390,c*30+50)
                    update = False
                for c,myItem in enumerate(tempID):
                    if returnButton('>',160,c*30+50,30,20,green,darkgreen) and tempBar < tempTicks:
                        self.itemModify(lootPileDict,[myItem,1],0)
                        buttonPressed = True
                for c,item in enumerate(tempLPD):
                    if returnButton('<',420,c*30+50,30,20,green,darkgreen) and tempBar < tempTicks:
                        self.itemModify(lootPileDict,[item,1],1)
                        buttonPressed = True
                if (lType == 2 and returnButton("finish",500,240,100,20,red,darkred)) or (lType != 2 and returnButton('finish',500,60,100,20,red,darkred)):
                    buttonPressed = True
                    finished = True
                if returnButton('transfer all',500,90,100,20,red,darkred) or kDict['t']:
                    kDict['t'] = False
                    buttonPressed = True
                    for myItem in inventoryDict:
                        self.itemModify(lootPileDict,[myItem,inventoryDict[myItem]],0)
                        pygame.draw.rect(screen, white, (6,46,606,306)); pygame.draw.rect(screen, black,(9,49,600,300))
                if returnButton('take all',500,120,100,20,red,darkred) or kDict['e']:
                    kDict['e'] = False
                    buttonPressed = True
                    for item in lootPileDict:
                        self.itemModify(lootPileDict,[item,lootPileDict[item]],1)
                        pygame.draw.rect(screen, white, (6,46,606,306)); pygame.draw.rect(screen, black,(9,49,600,300))
                if lType == 1 and returnButton("town",500,150,100,20,red,darkred):
                    self.town.interact()
                    buttonPressed = True
                if lType == 1 and returnButton("crafting",500,180,100,20,red,darkred):
                    self.interact(self.craftingDict,2)
                    buttonPressed = True
                if lType == 2 and returnButton("craft",500,150,100,20,red,darkred):
                    recps = []
                    for k in craftingRecipesDict:
                        print(k.splitlines())
                        if all([line.split('"')[1] in self.inventoryDict and self.inventoryDict[line.split('"')[1]] >= int(line.split('"')[2]) for line in k.splitlines()]):
                            recps.append([k,craftingRecipesDict])
                    tempMenuExit = False
                    while not tempMenuExit:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT: pygame.quit(); quit()
                        
                        for c,i in enumerate(recps):
                            print(i,c)
                        quit()

                #simButton time
                if buttonPressed:
                    update = True
                    keys = pygame.key.get_pressed()
                    if keys[304]: tempBar = tempTicks
                    else: tempBar = tempTicks + 3
                    tempID = inventoryDict
                    tempLPD = lootPileDict
                    pygame.draw.rect(screen, white, (6,46,606,306)); pygame.draw.rect(screen, black,(9,49,600,300))
                    for c,myItem in enumerate(tempID):
                        interfaceShow(str(myItem),10,c*30+50); interfaceShow(str(inventoryDict[myItem]),130,c*30+50)
                        simButton('>',160,c*30+50,30,20,green,darkgreen)
                    for c,item in enumerate(tempLPD):
                        interfaceShow(str(item),270,c*30+50); interfaceShow(str(lootPileDict[item]),390,c*30+50)
                        simButton('<',420,c*30+50,30,20,green,darkgreen)
                        
                    #simButton('finish',500,60,100,20,red,darkred)
                    (lType == 2 and simButton("finish",500,240,100,20,red,darkred)) or (lType != 2 and simButton('finish',500,60,100,20,red,darkred))
                    simButton('transfer all',500,90,100,20,red,darkred)
                    simButton('take all',500,120,100,20,red,darkred)
                    if lType == 1:
                        simButton("town",500,150,100,20,red,darkred)
                        simButton("crafting",500,180,100,20,red,darkred)
                    elif lType == 2:
                        simButton("craft",500,150,100,20,red,darkred)
                pygame.display.update()
                clock.tick(15)
                tempTicks += 1
        dictClear(lootPileDict,0)
        dictClear(self.inventoryDict,0)
            
    def itemModify(self,inputDict,itemLi,mode):#(returns value of lootlList, changes value of inventoryDict) = 0 - transfers from inventory =1 - transfers to inventory
        if mode == 0:
            if itemLi[0] in inputDict:
                preVal = inputDict[itemLi[0]]
            else:
                preVal = 0
            inputDict[itemLi[0]] = preVal + itemLi[1]
            self.inventoryDict[itemLi[0]] -= itemLi[1]
            if self.inventoryDict[itemLi[0]] < 0:
                self.inventoryDict[itemLi[0]] = 0
                inputDict[itemLi[0]] -= 1
        elif mode == 1:
            if itemLi[0] in self.inventoryDict:
                preVal = self.inventoryDict[itemLi[0]]
            else:
                preVal = 0
            self.inventoryDict[itemLi[0]] = preVal + itemLi[1]
            inputDict[itemLi[0]] -= itemLi[1]
            if inputDict[itemLi[0]] < 0:
                inputDict[itemLi[0]] = 0
                self.inventoryDict[itemLi[0]] -= 1
        return(inputDict)
    def __init__(self,cMap = None):
        self.cMap = cMap
        self.town = Town(self)
    def die(self):
        self.inventoryDict = dict()
        self.pos = self.cMap.center
        self.health = self.maxHealth
        self.thirst = self.maxThirst
        ti = 0
        surface = pygame.Surface([dw,dh], pygame.SRCALPHA, 32)
        pygame.draw.rect(surface,list(black)+[10],[0]*2+[dw,dh])
        for i in range(200):
            pygame.draw.circle(surface,[randrange(170,210),200,randrange(180,220)]+[20],[randrange(0,dim[c]) for c in range(2)],randrange(1,4))
        simpleText("You died!",(dw//2-50,dh//2-9),white,myfont,surface)
        while ti < 100:
            pygame.event.get()
            #inputText,co=(0,0),colour=lightgray,simpleFont = myfont,surf=screen
            screen.blit(surface,[0,0])
            PDU()
            ti += 1
            clock.tick(20)


def lightTime(time,dawn=600,dusk=1900,day=2400,rate=0.525):
    rMode = 0
    illumi = 210
    if (time > dusk) or (time < dawn):
        rMode = 2
##        illumi = 0
    elif (time <= dusk) and (time >= dusk-400):
        rMode = 1
        illumi = (dusk-time)*rate
    elif (time >= dawn) and (time <= dawn+400):
        rMode = 1
        illumi = (time-dawn)*rate
    return rMode,round(illumi,2)


cTDict = {',':(70,210,110),';':yellow}
def colorAssign(tile, default = white):
    cTDict = default
    if tile in cTDict:
        col = cTDict[tile]
    return cTDict
    
tColDict = {',':(70,210,110), ';':yellow}
def elseDict(di,k,el):
    if k in di: return di[k]
    else: return el

class Map:
    table = []
    gridW,gridH = 0,0
    sGridW, sGridH = 135,40
    time = 1200
    
    def showPers(self,p):
        sGridW, sGridH = self.sGridW, self.sGridH
        seen = p.omni
        lightSources = [ [(sGridW//2*12,sGridH//2*20+40),p.breathingCycle[0]] ]#[[(hDW,hDH),p.breathingCycle[0]]]
        seenSet = p.seenSet
        x,y = p.pos
        out = []
        c = 0
        rMode, illumi = lightTime(self.time)
        for n in range(y-sGridH//2,y+sGridH//2):
            if n < 0 or n >= self.gridH: layer = ['-']*sGridW
            else:
                layer = []
                c1 = 0
                for n2 in range(x-sGridW//2,x+sGridW//2):
                    if (n2 < 0) or (n2 >= self.gridW) or ( (not (n2,n) in p.seenSet) and rMode == 0 and not p.omni):
                        layer.append('-')
                    else:
                        layer.append(self.table[n][n2])
                        #lighting
                        if layer[-1] == 'o': lightSources.append([(c1*12,c*20+40),min(200,randrange(160,260))/100])
                        elif layer[-1] == 'S': lightSources.append([(c1*12,c*20+40),min(180,randrange(140,260))/100])
                        elif layer[-1] == 'P': lightSources.append([(c1*12,c*20+40),min(200,randrange(160,260))/100])
                    c1 += 1
            c += 1
            out.append(layer)
        aC = 0
        tempTableObject = [out[:],y-math.floor(sGridH/2),x-math.floor(sGridW/2)]
        c = tempTableObject[1]
        for a in tempTableObject[0]:
            pS = ""; buildingPS = []; aC1 = 0
            c1 = tempTableObject[2]
            for b in a:
                if (c1,c) == (x,y):
                    pS = pS + ' '#■
                    tX,tY = aC1,aC
##                    lightSources.append([(aC1*12,aC*20+40),p.breathingCycle[0]])
                elif seen or (c1,c) in seenSet:
                    if b in buildingNameList: buildingPS.append([b,(aC1,aC)]); pS += ' '
                    else: pS += b
                
                else: pS += ' '
                c1 += 1; aC1 += 1
            if rMode == 0:
                for inX,letter in enumerate(pS):
                    if letter != ' ':
                        col = elseDict(tColDict,letter,white)
                        simpleText(letter,(12*inX,20*aC+40),col)
            elif rMode == 1:
                for inX,letter in enumerate(pS):
                    if letter != ' ':
                        simpleText(letter,(12*inX,20*aC+40),colourMix(elseDict(tColDict,letter,white),tuple([max([illumi]+[155 - (coDistance(iP,(12*inX,20*aC+40)))*iM for iP,iM in lightSources])]*3),illumi/210))
            if rMode == 2:
                for inX,letter in enumerate(pS):
                    if letter != ' ':
                        simpleText(letter,(12*inX,20*aC+40),tuple([max([0]+[155 - (coDistance(iP,(12*inX,20*aC+40)))*iM for iP,iM in lightSources])]*3))

            c += 1; aC += 1
            for bPS in buildingPS:
                simpleText(bPS[0],(bPS[1][0]*12,bPS[1][1]*20+40),tuple([max([0]+[255 - (coDistance(iP,(bPS[1][0]*12,bPS[1][1]*20+40)))*iM for iP,iM in lightSources])]*3),fancyFont)
##                simpleText(bPS[0],(bPS[1][0]*12,bPS[1][1]*20+40),white,fancyFont)
                
        if p.transportMode == 0: charColour = white
        elif p.transportMode == 1: charColour = red
        else: charColour = white

        if [x,y] != self.center:
            rect = [10,10,50,50]
            pos = [35,35]
            while inRect(pos,rect):#compass
                pos = dupleAdd(pos,p.compass)
            pygame.draw.rect(screen,darkgray,rect); pygame.draw.rect(screen,white,rect,3)
            pygame.draw.line(screen,red,(35,35),(limit(pos[0],57,13),limit(pos[1],57,13)))
            pygame.draw.circle(screen,white,(35,35),4)
        else:
            pygame.draw.rect(screen,darkgray,[10,10,50,50]); pygame.draw.rect(screen,white,[10,10,50,50],3)
            pygame.draw.circle(screen,white,(35,35),4)
        pygame.draw.rect(screen,darkgray,[95,10,25,25])
        if p.buildTile in p.inventoryDict: n = p.inventoryDict[p.buildTile]
        else: n = '0'
        pygame.draw.rect(screen,white,[95,10,25,25],3); simpleText(p.buildTile,(102,10),white); simpleText(n,(97,12),white,smallFont)
        d = coDistance(p.pos,self.center)
        pygame.draw.rect(screen,(min(d*2.55,255),max(0,255-(d*2.55)),0),[95,40,25,20]); pygame.draw.rect(screen,white,[95,40,25,20],3)
        pygame.draw.rect(screen,darkgray,[65,10,25,50]); pygame.draw.rect(screen,green,[65,60-50*p.health/p.maxHealth,25,(p.health/p.maxHealth)*50])
        pygame.draw.rect(screen,white,[65,10,25,50],3)

        pygame.draw.rect(screen,darkgray,[10,65,110,20])
        pygame.draw.rect(screen,blue,[10,65,110*p.thirst/p.maxThirst,20])
        pygame.draw.rect(screen,white,[10,65,110,20],3)
        [pygame.draw.rect(screen,lightgray,[24+20*n,66,3,18]) for n in range(5)]
        
        simpleText('■',(tX*12,tY*20+40),charColour)
##        simpleText(str(self.time//1),(10,100))
        
    def locationValid(self,x,y):
        if x >= self.gridW or x < 0 or y >= self.gridH or y < 0: return False
        else: return True
    def locationBuildValid(self,x,y,mode=0):
        if x > self.gridW or x < 0 or y >= self.gridH or y <0:
            return False
        else:
            if self.table[y][x] not in buildingNameList and not self.table[y][x] in ['#','P','p','A','C','c']: return True
            else: return False
    def tile(self,pos):
        return self.table[pos[1]][pos[0]]
    def setTile(self,pos,char):
        self.table[pos[1]][pos[0]] = char
    #shapes
    def squareFill(self,co1,co2,char):
        for y in range(co1[1],co2[1]):
            for x in range(co1[0],co2[0]):
                if self.locationBuildValid(x,y):
                    self.table[y][x] = char
                    
    def diamondFill(self,center,radius,char):
        c,w = 0,0
        for d in range(center[1]-radius,center[1]+radius+1):
            for r in range(center[0]-w,center[0]+w+1):
                if self.locationBuildValid(r,d):
                    self.table[d][r] = char
            if c >= radius:
                w -= 1
            else:
                w += 1
            c += 1
            
    def circleFill(self,center,radius,char):
        co1 = (center[0]-radius,center[1]-radius)
        co2 = (center[0]+radius,center[0]+radius)
        for y in range(co1[1],co2[1]):
            for x in range(co1[0],co2[0]):
                if exactDistance(center,(x,y)) < radius-0.5 and self.locationBuildValid(x,y):
                    self.table[y][x] = char
                    
    def pathBuild(self,fromCo,toCo):
        xDist = abs(fromCo[0]-toCo[0])+5
        yDist = abs(fromCo[1]-toCo[1])+5
        closestList = [exactDistance(fromCo,toCo),toCo]
        for yCo in range(fromCo[1]-yDist,fromCo[1]+yDist):
            for xCo in range(fromCo[0]-xDist,fromCo[0]+xDist):
                if self.locationValid(xCo,yCo):
                    if self.table[yCo][xCo] == '#':
                        if exactDistance(fromCo,(xCo,yCo)) < closestList[0]:
                            closestList = [exactDistance(fromCo,(xCo,yCo)),(xCo,yCo)]
        if randrange(1,3) == 2: #side-down
            for xCo in myRange(fromCo[0],closestList[1][0]):
                if self.locationBuildValid(xCo,fromCo[1]):
                    self.table[fromCo[1]][xCo] = '#'
            for yCo in myRange(fromCo[1],closestList[1][1]):
                if self.locationBuildValid(closestList[1][0],yCo):
                    self.table[yCo][closestList[1][0]] = '#'
        else: #down-side
            for yCo in myRange(fromCo[1],closestList[1][1]):
                if self.locationBuildValid(fromCo[0],yCo):
                    self.table[yCo][fromCo[0]] = '#'
            for xCo in myRange(fromCo[0],closestList[1][0]):
                if self.locationBuildValid(xCo,closestList[1][1]):
                    self.table[closestList[1][1]][xCo] = '#'
                    
    def getNeighbours(self,inX,inY,mode=0):#1-%2, 2-show mode
        outList = []
        for y in [inY-1,inY,inY+1]:
            for x in [inX-1,inX,inX+1]:
                if (x,y) != (inX,inY) and inRect((x,y),[0,0]+[self.gridW,self.gridH]):
                    if mode == 1: outList.append(self.table[x][y]%2)
                    elif mode == 2: outList.append(math.floor(self.table[x][y]/2))
                    else: outList.append(self.able[x][y])
        return outList
    
    def config(self,settings=(500,500)):
        self.gridW, self.gridH = settings
        self.center = [i//2 for i in settings]
        self.generate()
        self.table[self.center[1]][self.center[0]] = 'S'

        with open("main_info\\sources\\buildings\\_directory.txt",'r') as f:
            buildings = f.read().splitlines()
        for l in buildings:
            with open("main_info\\sources\\buildings\\"+l.split(':')[1].replace('\"','')+".txt",'r') as f:
                building = f.read().splitlines()
            for com in building:
                if com[:4] == "/sa/":
                    self.mapBuildingPopulate(l.split(':')[0].replace('\"',''),math.floor((self.gridW*self.gridH)*(float(com[4:])/100)))
                elif com[:4] == "/sn/":
                    self.mapBuildingPopulate(l.split(':')[0].replace('\"',''),int(com[4:].split(' ')[0]),int(com[4:].split(' ')[1]),self.center, int(com[4:].split(' ')[2]))

    thresholds = [
    ['\'',100],
    ["=",200],
    [";",300],
    [",",400]
    ]
    tot = 1000

    peak = tot//2
    def formula(self,x):
        x/= 200
        return self.peak/2*math.cos((x**1.12)/3 + math.sin(x + math.sin(-4.9*x)) + math.atan(x)*3 ) + self.peak//2
    def generate(self):
        gDict = {}
        for l,n in self.thresholds:
            gDict[l] = []
        with open("main_info\\sources\\buildings\\Chance.txt",'r') as f:
                txt = f.read().splitlines()[1:]
        sto = None
        for l in txt:
            if l[0] == '/':
                cTile = l[1:].replace('\"','')
            else:
                l = l.split(':')
                gDict[cTile].append([l[0],float(l[1])])
        with open("main_info\\sources\\buildings\\_Directory.txt",'r') as f:
            txt = f.read().splitlines()

        mDict = {}
        for l in txt:
            l = l.replace('\"','').split(':')
            mDict[l[1]] = l[0]
            

        table = []
        for y in range(self.gridH):
            row = []
            for x in range(self.gridW):
                i = self.formula(y*2) + self.formula((x+100)*3+3)
                add = 0
                for l,ran in self.thresholds:
                    add += ran
                    if i <= add:
                        t = l
                        for b,ch in gDict[l]:
                            if chance(ch,100):
                                if b in mDict: t = mDict[b]
                                else: t = b
                        row.append(t)
                        break
                    
            table.append(row)
        self.table = table
    builtList = []
    def mapBuildingPopulate(self,char,amount=1,withinRange = None,withinRangeOf = None, outOfRange=0):
        if withinRange == None:
            for a in range(amount):
                placed = False
                while not placed:
                    tryCo = (randrange(0,self.gridW),randrange(0,self.gridH))
                    if tryCo != self.center and not tryCo in self.builtList:
                        self.table[tryCo[1]][tryCo[0]] = char
                        self.builtList.append(tryCo)
                        placed = True
        else:
            for a in range(amount):
                placed = False
                while not placed:
                    tryCo = (randrange(0,self.gridW),randrange(0,self.gridH))
                    if tryCo != self.center and not tryCo in self.builtList and outOfRange < exactDistance(tryCo,withinRangeOf) < withinRange:
                        self.table[tryCo[1]][tryCo[0]] = char
                        self.builtList.append(tryCo)
                        placed = True  
    def __init__(self):
        self.config()

def weightEvaluation(Dict): return sum([itemDict[myitem] * Dict[myItem] for myItem in Dict])

def saveGame(location):
    with open(location + ".dat",'wb') as file:
        pickle.dump((gameMap, user, user.seenSet),file,protocol=2)

def importGame(location):
    global gameMap, user
    with open(location + ".dat",'rb') as file:
        gameMap,user,temp = pickle.load(file)
        user.seenSet = deepcopy(temp)

def saveMenu():
    escPressed = False
    while not escPressed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                escPressed = True
        for n in range(1,6):
            if returnButton("Save" + str(n),100,n*30+80,60,20,red,darkred):
                saveGame("main_info\\save_data\\save"+str(n)+"\\save")
            if returnButton("Import" + str(n), 180, n*30+80,80,20, red, darkred):
                importGame("main_info\\save_data\\save"+str(n)+"\\save")
        PDU()


gameMap = Map()
user = Player(gameMap)

def gameLoop():
    gameExit = False
    update = True

    user.pos = gameMap.center
    user.interact(user.stockpileLootDict)
    user.seeArea(user.pos)
    update = True

    while not gameExit:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit(); quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F4 and keys[pygame.K_LALT]:
                    pygame.quit(); quit()
                if event.key == pygame.K_i:
                    user.inventoryInterface()
                elif event.key in dirDict or event.key in [pygame.K_t]:
                    user.receiveKey(event)
                elif event.key == pygame.K_ESCAPE:
                    saveMenu()
                update = True
                
        update = True
        if any([update,user.passive()]):
            screen.fill(black)        
            gameMap.showPers(user)
            PDU()
            update = False
            if not user.checkAlive(): user.die()
        clock.tick(60)
        
gameLoop()
