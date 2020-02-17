from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import *

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import keyboard
import snake
import random

class Ui_MainWindow(object):
    
    # dimensiones del widget de opengl
    windowWidth = 600
    windowHeight = 600
    # factor de escala para la resolucion interna
    scale = 20
    # dimensiones internas
    w = round(windowWidth/scale)
    h = round(windowHeight/scale)
    # variable snake
    s = snake.Snake(w/2,h/2)
    # se genera la comida
    food = snake.foodLocation(w,h)
    
    #print(w,h,'\n')
    
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.openGLWidget = QtWidgets.QOpenGLWidget(self.centralwidget)
        self.openGLWidget.setGeometry(QtCore.QRect(50,50,self.windowWidth,self.windowHeight))
        self.openGLWidget.setObjectName("openGLWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        # se inicializan las funciones de OpenGL
        self.openGLWidget.initializeGL 
        self.openGLWidget.resizeGL(self.windowWidth,self.windowHeight)
        self.openGLWidget.paintGL = self.paintGL

        # se setea la tasa de refresco de la pantalla
        timer = QTimer(self.centralwidget)
        timer.timeout.connect(self.openGLWidget.update) 
        timer.start(150)
        

    def paintGL(self):
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
        # se dibuja
        self.draw()

  
    def draw(self):
        
        # lectura de las teclas del teclado
        self.keyEvent()

        # se actualizan las coordenadas de los cuadrados
        self.s.update(self.w,self.h)
        # se obtienen las coordenadas de los cuadrados
        coord = self.s.getCoord()

        
        if  self.s.eat(self.food):
            self.food = snake.foodLocation(self.w,self.h)
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
        
        
        #se dibuja el cuadrado
        glColor3f(1,0.5,1);
        for cord in coord:
            glBegin(GL_QUADS)
            glVertex2f(cord.x_iz,cord.y_in)
            glVertex2f(cord.x_der,cord.y_in)
            glVertex2f(cord.x_der,cord.y_sup)
            glVertex2f(cord.x_iz,cord.y_sup)
            glEnd()


           
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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())