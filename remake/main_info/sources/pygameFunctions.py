import pygame
pygame.font.init()
myFont = pygame.font.SysFont("monospace", 20)
fancyFont = pygame.font.SysFont("calibri", 22)

def pygameSleep(seconds):
    ticks = 0
    while ticks < seconds*60:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
        ticks += 1
        clock.tick(60)

def textObjects(text,font,colour=(255,255,255)):
    textSurface = font.render(text,True,colour)
    return(textSurface, textSurface.get_rect())

def messageDisplay(text,colour=(255,255,255)):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = textObjects(text,largeText,colour)
    TextRect.center = (display_width/2),(display_height/2)
    screen.blit(TextSurf, TextRect)
    pygame.display.update()
def simpleText(inputText,co=(0,0),colour=(150,150,150),simpleFont = myFont):
    text = simpleFont.render(inputText, True, colour)
    screen.blit(text,co)

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
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1: return True        
    else: pygame.draw.rect(screen, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("calibri",20)
    textSurf, textRect = textObjects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)
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
def score(header,score,co=(0,0),colour=(255,255,255)):
    font = pygame.font.SysFont("calibri", 22)
    text = font.render(header + ": " + str(score), True, white)
    screen.blit(text,co)

def interfaceShow(text,xDisp=0,yDisp=0):
    textList = text.split('\n')
    c = 0
    for pS in textList:
        simpleText(pS,(xDisp,c*20+yDisp),(0,0,0),fancyFont)
        c += 1
def PDU(): pygame.display.update()
