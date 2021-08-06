import pygame
import os
import random
import math

from bala import *
from enemigo import *
from nave import *

pygame.init()

winW = 900
winH = 600
volumenMusic = 0.1

screen = pygame.display.set_mode((winW,winH))
pygame.display.set_caption('Space game!')
puntos = 0000
myfont = pygame.font.SysFont('Comfortaa', 25,True)
endGame = pygame.font.SysFont('Consolas', 60,True)
clock = pygame.time.Clock()


background_img = []
imagFondo = 15
for img in range(0,imagFondo+1):
    imagen = pygame.image.load('Data/Fondo/Fondo_1/'+str(img)+'.png').convert_alpha()
    background_img.append(pygame.transform.scale(imagen,(900,600)))
backgroundSound =  pygame.mixer.Sound('Data/Fondo/Fondo_1/background.wav')
backgroundSound.set_volume(volumenMusic)
backgroundSound.play(-1)

naveImg = pygame.image.load('Data/Naves/Jugador/n1.png').convert_alpha()
naveImgHit = pygame.image.load('Data/Naves/Jugador/n1_hit.png').convert_alpha()
naveEsc = 60
naveImg = pygame.transform.scale(naveImg,(naveEsc,naveEsc))
naveImgHit = pygame.transform.scale(naveImgHit,(naveEsc,naveEsc))
        
balaImg = pygame.image.load('Data/Balas/Jugador/b1.png').convert_alpha()
balaEsc = 30
balaImg = pygame.transform.scale(balaImg,(int(balaEsc/3),int(balaEsc/2.5)))


enemigoImg = pygame.image.load('Data/Naves/Enemigo/n1.png').convert_alpha()
enemigoImgHit = pygame.image.load('Data/Naves/Enemigo/n1_hit2.png').convert_alpha()
enemigoEsc = 50
enemigoImg = pygame.transform.scale(enemigoImg,(enemigoEsc,enemigoEsc))
enemigoImgHit = pygame.transform.scale(enemigoImgHit,(enemigoEsc,enemigoEsc))

def drawNave(screen,nave,x,y): 
    screen.blit(nave,(x,y))


BALAS = []
points=[]
ENEMIGOS = []
nave = Nave(naveImg, naveImgHit,winW/2-naveEsc/2,winH*0.75-naveEsc/2)


speed = 3.2
balaspeed = 0.5
running = True
mapIndex = 0
tmap = 0
tcol = 0
vidas = 4

t_anim_enemig_explo = 500
t_anim_nave_hit = 300


while running:

    dt = clock.tick(80)


# SE RECORREN LAS IMAGENES DEL BACKGROUND
    tmap+=dt
    if tmap>3*dt:
        if mapIndex<imagFondo:
            mapIndex+=1
        if mapIndex == imagFondo:
            mapIndex=0
        tmap=0
    screen.blit(background_img[mapIndex], (0,0))  
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # PARA DISPARAR CON ESPACIO
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                BALAS.append(Bala(balaImg,nave.getX()+5,nave.getY()-15,0,-balaspeed*dt))
                BALAS.append(Bala(balaImg,nave.getX()+50,nave.getY()-15,0,-balaspeed*dt))
            if event.key == pygame.K_p:
                ENEMIGOS.append(Enemigo(enemigoImg,enemigoImgHit,random.randint(60,winW-60),random.randint(0,winH/4),dt))
            if event.unicode == "+":
                volumenMusic +=0.1
                backgroundSound.set_volume(volumenMusic)
            if event.unicode == "-":
                volumenMusic -=0.1
                backgroundSound.set_volume(volumenMusic)
            if event.key == pygame.K_r:
                vidas = 4
                ENEMIGOS=[]
                puntos=0
                nave.resetImg()
                nave.setX(winW/2-naveEsc/2)
                nave.setY(winH*0.75-naveEsc/2)
                #backgroundSound.stop()
                #backgroundSound.play(-1)
        if event.type == pygame.KEYUP : 
            nave.setVelX(0)
            nave.setVelY(0)

# MIENTRAS EL JUGADOR ESTE VIVO
    if vidas >0:  
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_d]:
            nave.setVelX(speed)
        if keys[pygame.K_a]:
            nave.setVelX(-speed)
        if keys[pygame.K_w]:
            nave.setVelY(-speed)
        if keys[pygame.K_s]:
            nave.setVelY(speed)
        if nave.getX() <=0:
            nave.setX(0)
        if nave.getX() >=winW-naveEsc:
            nave.setX(winW-naveEsc)
        if nave.getY() <=0:
            nave.setY(0)
        if nave.getY() >=winH-naveEsc:
            nave.setY(winH-60)

        
        for enemigo in ENEMIGOS:    
            if enemigo.getOnAnimation() == True:
                current_t = pygame.time.get_ticks()
                enemigo_t = enemigo.getTimeCol()
                if current_t-enemigo_t > t_anim_enemig_explo:
                    enemigo.hide()
            enemigo.Disparar(dt,nave.getX(),nave.getY())
            enemigo.mover()
            #points.append((int(enemigo.getX()),int(enemigo.getY())))
            if enemigo.getX() <=0:
                enemigo.invertirX() 
            if enemigo.getX() >=winW-enemigoEsc:
                enemigo.invertirX()
            if enemigo.getY() <=10:
                enemigo.setY(10)
            if enemigo.getY() >=winH-enemigoEsc:
                enemigo.setY(winH-enemigoEsc)
            
            # CUANDO EL ENEMIGO DISPARA
            if enemigo.onDisparo():
                bala = enemigo.getBala()
                bala.mover()
                screen.blit(enemigo.getBalaImg(),(bala.getX(),bala.getY()))
                if bala.getY()>winH or bala.getY()<0 or bala.getX()<0 or bala.getX()>winW:
                    enemigo.onReload()
            if enemigo.isVisible():
                screen.blit(enemigo.getImg(),(enemigo.getX(),enemigo.getY()))
            #pygame.draw.rect(screen,(0,255,0),enemigo. getHitbox(),2)
            # SE CHECKEA SI LA BALA LE PEGO A LA NAVE
            if enemigo.getBala().getRect().colliderect(nave.getHitbox()):
                if not nave.esInvulnerable():
                    enemigo.onReload()
                    nave.setInvulnerable(True)
                    tcol = nave.colision()
                    vidas-=1
            if enemigo.golpeado():
                enemigo.colision(pygame.time.get_ticks())
                enemigo.setGolpeado(True)
                #del ENEMIGOS[ENEMIGOS.index(enemigo)]
                    
        # CONTROL DE TIEMPO DE LA ANIMACION DE INVULNERABLE
        if pygame.time.get_ticks() - tcol > t_anim_nave_hit:
            nave.resetImg()
            nave.setInvulnerable(False)
                
            
        for bala in BALAS:
            bala.mover()
            screen.blit(bala.getImg(),(bala.getX(),bala.getY()))
            #pygame.draw.rect(screen,(0,255,0),bala.getHitbox(),2)
                            
            if len(ENEMIGOS) == 1:
                if bala.getRect().colliderect(ENEMIGOS[0].getRect()):
                    ENEMIGOS[0].colision(pygame.time.get_ticks())
                    puntos+=10
                        
            for i in range(len(ENEMIGOS)):
                if ENEMIGOS[i].getOnAnimation() == False:
                    if bala.getRect().colliderect(ENEMIGOS[i].getRect()):
                        ENEMIGOS[i].colision(pygame.time.get_ticks())
                        del BALAS[BALAS.index(bala)]
                        puntos+=10
                        break
            if bala.getY() < 0:
                BALAS.pop(0)
        #print('LONGITUD BALAS:',len(BALAS))
        nave.mover(dt)
        #pygame.draw.rect(screen,(0,255,0),nave.getHitbox(),2)
        #drawNave(screen,nave.getImg(),nave.getX(),nave.getY())
        screen.blit(nave.getImg(),(nave.getX(),nave.getY()))
        #for p in points:
        #    pygame.draw.circle(screen, (255,0,0), p, 3)
        for i in range (0,vidas):
            naveVida =  pygame.transform.scale(naveImg,(30,30))
            screen.blit(naveVida,(winW-350+i*35,winH-35))
        textsurface = myfont.render('PUNTOS: '+'%04d' % puntos, True, (255, 204, 102))
        screen.blit(textsurface,(winW-200,winH-30))
    else:
        textsurface = endGame.render('GAME OVER',True, (255, 0, 0))
        text_rect = textsurface.get_rect(center=(winW/2, winH/2))
        screen.blit(textsurface, text_rect)

        


    pygame.display.update()

pygame.quit()