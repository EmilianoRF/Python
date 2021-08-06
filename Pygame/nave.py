import pygame
from bala import *

class Nave:
    def __init__(self, imagen,imagenHit,x,y):
        self.images=[imagen,imagenHit]
        self.imagesRect = [imagen.get_rect(),imagenHit.get_rect()]
        self.hitbox = (x,y,imagen.get_rect().w,imagen.get_rect().h)
        self.x = x
        self.y = y
        self.hitoff = 6
        self.xS = 0
        self.yS = 0
        self.currentImg = self.images[0]
        self.invulnerable = False
        self.balas = []
        self.balaImg = pygame.image.load('Data/Balas/Jugador/b1.png').convert_alpha()
        self.balaEsc = 30
        self.balaImg = pygame.transform.scale(self.balaImg,(int(self.balaEsc/3),int(self.balaEsc/2.5)))
        self.balaspeed = 0.5
    def setX(self,val):
        self.x=val
    def getImg(self):
        return self.currentImg   
    def setY(self,y):
        self.y= y
    def getY(self):
        return self.y
    def getX(self):
        return self.x
    def mover(self,dt):
        #print('velX:',self.xS)
        #print('X antes:',self.x)
        self.x+=self.xS
        #print('X despues:',self.x)
        self.y+=self.yS
        self.hitbox = (self.x+self.hitoff*1.5,self.y+self.hitoff*2,self.images[0].get_rect().w-self.hitoff*3,self.images[0].get_rect().h-self.hitoff*3)
        #print(self.x, self.y)
    def setVelX(self,vel):
        #print(self.xS)
        self.xS = vel
        #sprint(self.xS)
    def getVelX(self):
        return self.xS
    def setVelY(self,vel):
        self.yS = vel
    def getVelY(self):
        return self.yS
    def getHitbox(self):
        return self.hitbox
    def colision(self):
        self.currentImg = self.images[1]
        return pygame.time.get_ticks()
    def resetImg(self):
        self.currentImg = self.images[0]
    def setInvulnerable(self,val):
        self.invulnerable = val
    def esInvulnerable(self):
        return self.invulnerable
    def disparar(self,dt):
        self.balas.append(Bala(self.balaImg,self.x+5,self.y-15,0,-self.balaspeed*dt))
        self.balas.append(Bala(self.balaImg,self.x+50,self.y-15,0,-self.balaspeed*dt))




