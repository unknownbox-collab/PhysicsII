from sqlite3 import converters
from unittest import result
import numpy as np
import matplotlib.pyplot as plt
import math, random, copy, pygame, sys

G = 9.8
WHITE   =  (255, 255, 255)
ORANGE  =  (255, 127, 0  )
YELLOW  =  (255, 255, 0  )
BLACK   =  (0,   0,   0  )
BLUE    =  (0,   0,   255)
RED     =  (255, 0,   0  )
SKYBLUE =  (135, 206, 235)
SLIVER  =  (192, 192, 192)
BROWN   =  (206, 139, 84)
SPEED   =  5

def getDistance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

class PVector:
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
    
    def __add__(self,other):
        x,y = self.x + other.x , self.y + other.y
        return PVector(x,y)

    def __sub__(self,other):
        x,y = self.x - other.x , self.y - other.y
        return PVector(x,y)
    
    def __truediv__(self,other):
        return PVector(self.x/other, self.y/other)

    def __mul__(self,other):
        return PVector(self.x*other, self.y*other)

    
    def convert(self):
        theta = math.atan2(self.y,self.x) * 180 / math.pi
        value = (self.x**2 + self.y**2)**0.5
        return Vector(theta,value)
    
    def tuple(self):
        return self.x,self.y
    
    def __repr__(self) -> str:
        return f'Position({self.x},{self.y})'

class Vector:
    def __init__(self,theta,value) -> None:
        self.theta = theta
        self.value = value
    
    def __add__(self,other):
        S = self.convert()
        O = other.convert()
        return (S+O).convert()
    
    def __sub__(self,other):
        S = self.convert()
        O = other.convert()
        return (S-O).convert()
    
    def __truediv__(self,other):
        return Vector(self.theta,self.value/other)

    def __mul__(self,other):
        return Vector(self.theta,self.value*other)

    def convert(self):
        x = math.cos(math.radians(self.theta)) * self.value
        y = math.sin(math.radians(self.theta)) * self.value
        return PVector(x,y)
    
    def __repr__(self) -> str:
        return f'Vector({self.theta},{self.value})'

class WeightCenter:
    def __init__(self,master,x,y) -> None:
        self.master = master
        self.x = x
        self.y = y
        self.force = Vector(0,0)

    def addForce(self, force):
        self.force += force
    
    def getPosition(self,x,y,degree):
        resultX = x + self.x * math.cos(math.radians(degree))
        resultY = y + self.y * math.sin(math.radians(degree))
        return resultX, resultY

GRAVITY = Vector(90, G)

class Mass:
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.width = 10
        self.height = 40
        self.degree = 90
        self.m = 100
        self.forcePos = [0,0]
        self.weightCenter = [WeightCenter(self,0,20),WeightCenter(self,0,-20)]
        self.minForce = PVector(0,0)
        self.sumForce = Vector(0,0)
        self.skin = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
        pygame.draw.rect(self.skin, BROWN, pygame.Rect(0, 0, self.width, self.height))

    def gravity(self):
        for i in range(len(self.weightCenter)):
            self.weightCenter[i].addForce(GRAVITY/len(self.weightCenter))
    
    def getTouch(self,force,pos):
        sumX = []
        sumY = []
        self.forcePos = []
        for i in range(len(self.weightCenter)):
            weightCenter = self.weightCenter[i]
            l = getDistance(weightCenter.getPosition(self.x, self.y, self.degree),pos)
            self.weightCenter[i].addForce(force/l)
            converter = weightCenter.force.convert()
            sumX.append(converter.x)
            sumY.append(converter.y)
        if sumX[0] > sumX[1]:
            self.forcePos.append(0)
        else:
            self.forcePos.append(1)
        if sumY[0] > sumY[1]:
            self.forcePos.append(0)
        else:
            self.forcePos.append(1)
        self.minForce = PVector(min(sumX),min(sumY))
        self.sumForce = PVector(max(sumX)-min(sumX),max(sumY)-min(sumY))
        print(self.minForce)
        print(self.sumForce)
    
    def move(self):
        self.x += self.minForce.x
        self.y += self.minForce.y * math.sin(math.radians(self.degree))
        self.degree += 180*math.atan2(self.sumForce.y, self.sumForce.x)/(math.pi**3)
        print(self.degree)
    
    def draw(self,screen):
        skin = pygame.transform.rotate(self.skin, self.degree-90)
        screen.blit(skin,(self.x-self.width/2,self.y-self.height/2))

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

pygame.init()
pygame.display.set_caption("물리학 II")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
wood = Mass(500,250)
wood.getTouch(Vector(10,10),(500,200))

while True:
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.fill(BLACK)
    #wood.gravity()
    wood.move()
    wood.draw(screen)
    pygame.display.update()
