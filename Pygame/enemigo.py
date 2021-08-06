import random
import math
import numpy
import pygame
from bala import *

def genPuntos(n,r,dir):
    tita = numpy.linspace(0, 2*numpy.pi,n)
    puntos = []
    for i in range(0,len(tita)-1):
        y = numpy.cos(tita[i])*0.5
        x = tita[i]*dir*0.5
        puntos.append((x,y))
    return puntos

'''
def genPuntos(n,r,dir):
    tita = numpy.linspace(0, 2*numpy.pi,n)
    puntos = []
    for i in range(0,len(tita)-1):
        x = r * numpy.cos(tita[i])*random.random()
        y = r * numpy.sin(tita[i])*random.random()
        puntos.append((x,y))
    return puntos
'''

class Enemigo:
    def __init__(self, imagen,imagenHit,x,y,dt):
        self.images=[imagen,imagenHit]
        self.imagesRect = [imagen.get_rect(),imagenHit.get_rect()]
        self.x = x
        self.y = y
        self.xS = random.randint(-2,0)+1
        self.dt = dt
        self.hitbox = (x,y,imagen.get_rect().w,imagen.get_rect().h)
        self.pos = 0
        self.dir = random.randint(-2,0)+1
        self.puntos = genPuntos(random.randint(600,700),random.randint(1,3),self.dir)
        self.balaEsc = 30
        self.balaImg = pygame.transform.scale(pygame.image.load('Data/Balas/Enemigo/b1.png').convert_alpha(),(int(self.balaEsc/3),int(self.balaEsc/2.5)))
        self.bala = Bala(self.balaImg,self.x,self.y,0,0)
        self.disparo = False
        self.deltat = 0
        self.factor = random.randint(5,20)
        self.sonidoDisparo =  pygame.mixer.Sound('Data/Sounds/laser9.wav')
        self.ready = False
        self.vmAX = 0.35
        self.currentImg = self.images[0]
        self.tcol = 0   
        self.hitted = False
        self.onAnimation = False
        self.visible = True

    def getImg(self):
        return self.currentImg   
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getX(self):
        return self.x
    def mover(self):
        if not self.hitted:
            self.deltat+=1
            if self.pos < len(self.puntos):
                self.y+=self.puntos[self.pos][1]
                self.pos+=1
            if self.pos == len(self.puntos):
                self.pos = 0
                self.y+=self.puntos[self.pos][1]
            self.x+=self.xS
            self.hitbox = (self.x,self.y,self.images[0].get_rect().w,self.images[0].get_rect().h)
            if self.disparo == False:
                self.bala.setX(self.x+self.images[0].get_rect().w/2)
                self.bala.setY(self.y+self.images[0].get_rect().h/2)
            if self.deltat > self.factor*self.dt:
                self.ready = True
            if self.disparo == True:
                self.deltat = 0

    def setY(self,y):
        self.y = y
    def setX(self,x):
        self.x = x
    def getHitbox(self):
        return self.hitbox
    def getRect(self):
        self.imagesRect[0].topleft = (self.x,self.y)
        return self.imagesRect[0]
    def Disparar(self,dt,x,y):
        if self.ready == True and self.hitted == False:
            if self.disparo == False:
                xvel =(x-self.x)
                #print('xVel:',xvel)
                yvel= (y-self.y)
                #print('yVel:',yvel)
                modVel = numpy.sqrt(xvel*xvel + yvel*yvel)
                #print('modVel:',modVel)
                xvel = (xvel/modVel)*dt*self.vmAX
                yvel = (yvel/modVel)*dt*self.vmAX
                
                #print('xVelFinal:',xvel)
                #print('yVelFinal:',yvel)
                self.bala.setVelX(xvel)
                self.bala.setVelY(yvel)
                self.sonidoDisparo.play()
            self.disparo = True
    def getBala(self):
        return self.bala
    def getBalaImg(self):
        return self.balaImg
    def onDisparo(self):
        return self.disparo
    def onReload(self):
        self.disparo = False
        self.ready = False
    def invertirX(self):
        #for i in range(0,len(self.puntos)-1):
        #    self.puntos[i][0]=self.puntos[i][0]*(-1)
        self.xS=self.xS*(-1)
    def colision(self,t):
        self.currentImg = self.images[1]
        if self.hitted == False:
            self.tcol = t
        self.hitted = True
        self.onAnimation = True
    def resetImg(self):
        self.currentImg = self.images[0]
        self.tcol=0
    def getTimeCol(self):
        return self.tcol
    def golpeado(self):
        return self.hitted
    def setGolpeado(self,val):
        self.hitted = True
    def setAnimationState(self,val):
        self.onAnimation = val
    def getOnAnimation(self):
        return self.onAnimation
    def hide(self):
        self.visible =  False
    def isVisible(self):
        return self.visible
