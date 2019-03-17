import pygame as pg
from pygame.locals import *
from math import sqrt
from random import randint

pg.init()
pg.display.set_caption('Monte Carlo Playground')
clock = pg.time.Clock()
pg.font.init()
font = pg.font.Font('font.ttf', 20)

width = 1000
heigth = 700
screen = pg.display.set_mode((width, heigth))

UGREY = (40,40,40)
GREY = (15,15,15)
GREEN = (105, 255, 35)
PURPLE = (255, 25, 255)

scopes = []
points = []
mcPoints = []
buttons = []

pointsPS = 10
speed = 10
inarea = 1
notfit = 0
scale = 66
area = (660/scale)*(660/scale)
calcArea = 0

mcPerSecCap = 'Points/s: '+str(pointsPS)
mcPerSecRen = font.render(mcPerSecCap, False, (255,255,255))
animSpeedCap = 'Speed: '+str(speed)
animSpeedRen = font.render(animSpeedCap, False, (255,255,255))
totalAreaCap = 'Total Area: '+str(round(area,5))
totalAreaRen = font.render(totalAreaCap, False, (255,255,255))
scaleCap = 'Scale: '+str(scale)
scaleRen = font.render(scaleCap, False, (255,255,255))
allPointsCap = 'All Points: '+str(len(mcPoints))
allPointsRen = font.render(allPointsCap, False, (255,255,255))
fittingCap = 'Fitting: '+str(inarea)
fittingRen = font.render(fittingCap, False, GREEN)
notFittingCap = 'Not Fitting: '+str(notfit)
notFittingRen = font.render(notFittingCap, False, PURPLE)
calcAreaCap = 'Area: '+str(calcArea)
calcAreaRen = font.render(calcAreaCap, False, (255, 0, 0))

on = True

class PlayB:
    def __init__(self, x,y,s,c,a):
        self.x = x
        self.y = y
        self.s = s
        self.padding = 10
        self.color = c
        self.bgc = UGREY
        self.action = a

    def draw(self):
        p = self.padding
        pg.draw.rect(screen, self.bgc, (self.x - p, self.y-p, self.s+p*2, self.s+p*2))
        pg.draw.polygon(screen, self.color, ((self.x,self.y), (self.x+self.s, self.y+self.s/2), (self.x, self.y+self.s)))

    def doAction(self):
        self.action()

class PauseB:
    def __init__(self, x,y,s,c,a):
        self.x = x
        self.y = y
        self.s = s
        self.padding = 10
        self.color = c
        self.bgc = UGREY
        self.action = a

    def draw(self):
        p = self.padding
        pg.draw.rect(screen, self.bgc, (self.x - p, self.y-p, self.s+p*2, self.s+p*2))
        pg.draw.rect(screen, self.color, (self.x, self.y, self.s, self.s))

    def doAction(self):
        self.action()

class Button:
    def __init__(self, x,y,s,c,a,param):
        self.x = x
        self.y = y
        self.s = s
        self.padding = 0
        self.color = c
        self.bgc = UGREY
        self.action = a
        self.param = param

    def draw(self):
        p = self.padding
        pg.draw.rect(screen, self.bgc, (self.x-p, self.y-p, self.s+p*2, self.s+p*2))

    def doAction(self):
        self.action(self.param)

class EraseB:
    def __init__(self, x,y,s,c,a):
        self.x = x
        self.y = y
        self.s = s
        self.padding = 10
        self.color = c
        self.bgc = UGREY
        self.action = a

    def draw(self):
        p = self.padding
        pg.draw.rect(screen, self.bgc, (self.x - p, self.y-p, self.s+p*2, self.s+p*2))
        pg.draw.line(screen, self.color, (self.x, self.y), (self.x+self.s, self.y+self.s), 7)
        pg.draw.line(screen, self.color, (self.x+self.s, self.y), (self.x, self.y+self.s), 7)

    def doAction(self):
        self.action()

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.r = 7
        self.drag = False

    def draw(self):
        x = pg.mouse.get_pos()[0]
        y = pg.mouse.get_pos()[1]
        if self.drag:
            if x<320:
                self.x = 320
            elif x>width-20:
                self.x = width-20
            else:
                self.x = x

            if y<20:
                self.y = 20
            elif y>heigth-20:
                self.y = heigth-20
            else:
                self.y = y

        pg.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.r)

    def __gt__(self, other):
        return self.x > other.x
    
    def __lt__(self, other):
        return self.x < other.x

    def __eq__(self, other):
        return self.x == other.x

class McPoint:
    def __init__(self, x, y, r):
        global inarea
        self.x = x
        self.rx = self.x-320
        self.y = y
        self.ry = heigth-20-self.y
        self.r = r
        self.color = PURPLE

        for scope in scopes:
            if scope[0]<=self.x<=scope[1]:
                if self.ry <= self.rx*scope[2]+scope[3]:
                    inarea += 1
                    self.color = GREEN
                    break

    def draw(self):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.r)

def drawMenuBg(color):
    pg.draw.rect(screen, color, (0,0,300,heigth))

def drawBgMesh(scale, color):
    for i in range(680,0,-scale):
        pg.draw.line(screen, color, (300,i),(width,i))
    for j in range(320,width,scale):
        pg.draw.line(screen, color, (j,0),(j,heigth))

def drawAxis(scale, color):
    pg.draw.line(screen, color, (320,heigth-20), (320,20), 2)
    pg.draw.line(screen, color, (320,20),(330,40), 2)
    pg.draw.line(screen, color, (320,20),(310,40), 2)
    pg.draw.line(screen, color, (320,heigth-20),(width-20,heigth-20), 2)
    pg.draw.line(screen, color, (width-20,heigth-20),(width-40,heigth-30), 2)
    pg.draw.line(screen, color, (width-20,heigth-20),(width-40,heigth-10), 2)
    
def connectPoints(color):
    points.sort()
    for i in range(len(points)-1):
        pg.draw.line(screen, color, (points[i].x, points[i].y),(points[i+1].x,points[i+1].y), 5)

def fill(color):
    pList = []
    pList.append((points[0].x, heigth-20))
    for point in points:
        pList.append((point.x, point.y))

    pList.append((points[-1].x, heigth-20))

    pg.draw.polygon(screen, color, pList)

def getScopes():
    points.sort()
    for i in range(len(points)-1):
        x = points[i].x - 320
        x1 = points[i+1].x - 320
        y = heigth-20-points[i].y
        y1 = heigth-20-points[i+1].y
        a = (y-y1)/(x-x1)
        b = (y)-(a*x)
        scopes.append((points[i].x, points[i+1].x, a, b))

def clearMcPoints():
    global mcPoints,inarea,allPointsRen,allPointsCap,fittingCap,fittingRen,notFittingCap,notFittingRen,calcAreaCap,calcAreaRen
    inarea = 1
    calcArea = 0
    notfit = 0
    mcPoints = []
    allPointsCap = 'All Points: '+str(len(mcPoints))
    allPointsRen = font.render(allPointsCap, False, (255,255,255))
    fittingCap = 'Fitting: '+str(inarea)
    fittingRen = font.render(fittingCap, False, GREEN)
    notFittingCap = 'Not Fitting: '+str(notfit)
    notFittingRen = font.render(notFittingCap, False, PURPLE)
    calcAreaCap = 'Area: '+str(round(calcArea, 8))
    calcAreaRen = font.render(calcAreaCap, False, (255, 0, 0))

def setAnimPlay():
    global animPlay, pauseB, playB, scopes
    scopes = []
    getScopes()
    playB.bgc = GREY
    pauseB.bgc = UGREY
    animPlay = True
    
def setAnimPause():
    global animPlay, pauseB, playB
    getScopes()
    playB.bgc = UGREY
    pauseB.bgc = GREY
    animPlay = False

def setSpeed(value):
    global speed 
    temp = speed + value
    if 0<temp<101:
        speed = temp
    updateCaps()

def setPoints(value):
    global pointsPS
    temp = pointsPS + value
    if 0<temp<1001:
        pointsPS = temp
    updateCaps()

def setScale(value):
    global scale, area
    temp = scale + value
    if 1<temp<661:
        scale = temp
        area = (660/scale)*(660/scale)
    updateCaps()

def updateCaps():
    global mcPerSecCap,mcPerSecRen,animSpeedCap,animSpeedRen,scaleCap,scaleRen,totalAreaCap,totalAreaRen
    mcPerSecCap = 'Points/s: '+str(pointsPS)
    mcPerSecRen = font.render(mcPerSecCap, False, (255,255,255))
    animSpeedCap = 'Speed: '+str(speed)
    animSpeedRen = font.render(animSpeedCap, False, (255,255,255))
    scaleCap = 'Scale: '+str(scale)
    scaleRen = font.render(scaleCap, False, (255,255,255))
    totalAreaCap = 'Total Area: '+str(round(area, 5))
    totalAreaRen = font.render(totalAreaCap, False, (255,255,255))

points.append(Point(320, heigth-20))
points.append(Point(width-20, heigth-20))

playB = PlayB(25, heigth-100, 50, (0,255,0), setAnimPlay)
pauseB = PauseB(125, heigth-100, 50, (244, 182, 66), setAnimPause)
eraseB = EraseB(225, heigth-100, 50, (0, 255, 212), clearMcPoints)
buttons.append(Button(30,60,25,UGREY,setPoints,1))
buttons.append(Button(60,60,25,UGREY,setPoints,-1))
buttons.append(Button(90,60,25,UGREY,setPoints,100))
buttons.append(Button(120,60,25,UGREY,setPoints,-100))
buttons.append(Button(30,120,25,UGREY,setSpeed,1))
buttons.append(Button(60,120,25,UGREY,setSpeed,-1))
buttons.append(Button(30,180,25,UGREY,setScale,1))
buttons.append(Button(60,180,25,UGREY,setScale,-1))
buttons.append(Button(90,180,25,UGREY,setScale,100))
buttons.append(Button(120,180,25,UGREY,setScale,-100))

animPlay = False
delay = 0

while(on):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit()
            on = False

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
            flag = True
            evx = pg.mouse.get_pos()[0]
            evy = pg.mouse.get_pos()[1]
            if len(points)>2:
                for point in points:
                    temp = sqrt((evx-point.x)*(evx-point.x) + (evy-point.y)*(evy-point.y))
                    if point.r >= temp and not animPlay:
                        points.remove(point)
                        flag = False
                        break

            if flag and 320<evx<width-20 and 20<evy<heigth-20 and not animPlay:
                points.append(Point(pg.mouse.get_pos()[0],pg.mouse.get_pos()[1]))

        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            evx = pg.mouse.get_pos()[0]
            evy = pg.mouse.get_pos()[1]
            for point in points:
                temp = sqrt((evx-point.x)*(evx-point.x) + (evy-point.y)*(evy-point.y))

                if point.r >= temp and not animPlay:
                    point.drag = True
                    break

            for button in buttons:
                if button.x<=evx<=button.x+button.s and button.y<=evy<=button.y+button.s:
                    button.bgc = GREY
                    button.doAction()
                    break

            if playB.x<=evx<=playB.x+playB.s and playB.y<=evy<=playB.y+playB.s:
                clearMcPoints()
                playB.doAction()

            if eraseB.x<=evx<=eraseB.x+eraseB.s and eraseB.y<=evy<=eraseB.y+eraseB.s:
                eraseB.doAction()
                eraseB.bgc = GREY
                
            if pauseB.x<=evx<=pauseB.x+pauseB.s and pauseB.y<=evy<=pauseB.y+pauseB.s:
                pauseB.doAction()

        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            for point in points:
                point.drag = False

            for button in buttons:
                button.bgc = UGREY

            eraseB.bgc = UGREY

    if len(mcPoints)>0:
        calcArea = area*inarea/len(mcPoints)
        notfit = len(mcPoints)-inarea

    if animPlay:
        allPointsCap = 'All Points: '+str(len(mcPoints))
        allPointsRen = font.render(allPointsCap, False, (255,255,255))
        fittingCap = 'Fitting: '+str(inarea)
        fittingRen = font.render(fittingCap, False, GREEN)
        notFittingCap = 'Not Fitting: '+str(notfit)
        notFittingRen = font.render(notFittingCap, False, PURPLE)
        calcAreaCap = 'Area: '+str(round(calcArea, 8))
        calcAreaRen = font.render(calcAreaCap, False, (255, 0, 0))

        delay += 1
        if delay >= speed:
            for i in range(pointsPS):
                mcPoints.append((McPoint(randint(320,width-20), randint(20, heigth-20), 3)))
            delay = 0

    screen.fill((0,0,0))
    drawMenuBg((20,20,20))
    fill((21, 15, 81))
    for point in mcPoints:
        point.draw()
    drawBgMesh(scale, (50,50,50))
    drawAxis(20, (255,255,255))
    connectPoints(pg.Color(200,200,200))

    screen.blit(mcPerSecRen, (30,30))
    screen.blit(animSpeedRen, (30,90))
    screen.blit(scaleRen, (30,150))
    screen.blit(totalAreaRen, (30,250))
    screen.blit(allPointsRen, (30,310))
    screen.blit(fittingRen, (30,370))
    screen.blit(notFittingRen, (30,430))
    screen.blit(calcAreaRen, (30,490))
    for button in buttons:
        button.draw()
    playB.draw()
    pauseB.draw()
    eraseB.draw()

    for point in points:
        point.draw()

    pg.display.flip()
    clock.tick(60)
