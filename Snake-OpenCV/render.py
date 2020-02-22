
import keyboard
import snake
import random

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Render:
    
    def __init__(self,winW,winH):
       
        # dimensiones del widget de opengl
        self.windowWidth = winW
        self.windowHeight = winH
        # factor de escala para la resolucion interna
        self.scale = 30
        # dimensiones internas
        self.w = round(self.windowWidth/self.scale)
        self.h = round(self.windowHeight/self.scale)
        # variable snake
        self.s = snake.Snake(self.w/2,self.h/2)
        # se genera la comida
        self.food = snake.foodLocation(self.w,self.h)
    
    # metodo que se retorna a MainWindow
    def paint(self):
        return self.paintgGL    
    
    def paintgGL(self):
        #se setea el puerto de vision
        glViewport(0,0,self.windowWidth,self.windowHeight)
        #se limpia el buffer
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity() 
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity() 
        glOrtho(0,self.w, 0,self.h, -1,1) 
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity() 
        # se dibuja la serpiente y la comida
        self.draw()

  
    def draw(self):
        
        # lectura de las entradas del teclado
        #self.keyEvent()

        # se actualizan las coordenadas de los cuadrados
        self.s.update(self.w,self.h)
        
        # se obtienen las coordenadas de la serpiente
        coord = self.s.getCoord()
        
        #se checkea si la serpiente esta en la posicion de
        # la comida
        if  self.s.eat(self.food):
            #se genera una nueva comida en una posicion aleatoria
            self.food = snake.foodLocation(self.w,self.h)
            #la serpiente crece
            self.s.grow()

        #se dibuja la comida.
        glColor3f(1,0,0);
        glBegin(GL_QUADS);
        glColor3f(1,0,0)
        glVertex2f(self.food.x_iz,self.food.y_in);
        glVertex2f(self.food.x_der,self.food.y_in);
        glVertex2f(self.food.x_der,self.food.y_sup);
        glVertex2f(self.food.x_iz,self.food.y_sup)
        glEnd()
         
        #se dibuja la serpiente
        glColor3f(0,1,0);
        for cord in coord:
            glBegin(GL_QUADS)
            glVertex2f(cord.x_iz,cord.y_in)
            glVertex2f(cord.x_der,cord.y_in)
            glVertex2f(cord.x_der,cord.y_sup)
            glVertex2f(cord.x_iz,cord.y_sup)
            glEnd()
    '''
    # manejo de las flechas del teclado para controlar la direccion
    def keyEvent(self):
        if keyboard.is_pressed('up'):
            self.s.setSpeed(0,1)
        elif keyboard.is_pressed('right'):
            self.s.setSpeed(1,0)
        elif keyboard.is_pressed('left'):
            self.s.setSpeed(-1,0)
        elif keyboard.is_pressed('down'):
            self.s.setSpeed(0,-1)
    '''
    def move(self,x,y):
        if self.s.getLen() == 1:
            self.s.setSpeed(x,y)
        else:
            estado = self.s.currDir()
            nexdir = ''
            if x == 1:
                nexdir = 'd'
            elif x == -1:
                nexdir = 'i'
            elif y == 1:
                    nexdir = 'b'
            elif y == -1:
                nexdir = 'a'
            
            if((estado == 'a' and nexdir == 'b')
            or (estado == 'b' and nexdir == 'a') 
            or (estado == 'd' and nexdir == 'i') 
            or (estado == 'i' and nexdir == 'd')):
                pass
            else:
                self.s.setSpeed(x,y)