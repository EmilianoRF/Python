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

import cv2

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    
    
    # dimensiones del widget de opengl
    windowWidth = 400
    windowHeight = 400
    # factor de escala para la resolucion interna
    scale = 20
    # dimensiones internas
    w = round(windowWidth/scale)
    h = round(windowHeight/scale)
    # variable snake
    s = snake.Snake(w/2,h/2)
    # se genera la comida
    food = snake.foodLocation(w,h)
    #
    face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
    cap = cv2.VideoCapture(0)
    
    
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(911, 694)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.WindowOpenGL = QtWidgets.QOpenGLWidget(self.centralwidget)
        self.WindowOpenGL.setGeometry(QtCore.QRect(20, 70,self.windowWidth,self.windowHeight))
        self.WindowOpenGL.setObjectName("WindowOpenGL")
        self.WindowOpenCV = QtWidgets.QLabel(self.centralwidget)
        self.WindowOpenCV.setGeometry(QtCore.QRect(450, 70, 400, 400))
        self.WindowOpenCV.setObjectName("WindowOpenCV")
        self.WindowOpenCV.setScaledContents(True)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 911, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.WindowOpenCV.setText(_translate("MainWindow", "TextLabel"))
        
        # se inicializan las funciones de OpenGL
        self.WindowOpenGL.initializeGL 
        self.WindowOpenGL.resizeGL(self.windowWidth,self.windowHeight)
        self.WindowOpenGL.paintGL = self.paintGL
        

        # se setea la tasa de refresco de la pantalla
        timer = QTimer(self.centralwidget)
        timer.timeout.connect(self.WindowOpenGL.update) 
        timer.start(100)
        
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
                    
        # se toma la imagen desde la camara
        ret,frame = self.cap.read()
        # se espeja
        cv2.flip(frame,1,frame)
        #se hace una copia de la imagen en escala de grises para poder usar
        #cascade
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=4, minSize=(30, 30))
        #se dibuja un cuadrado en las coordenadas donde se detecto la cara
        for (x,y,w,h) in faces:
            roi_gray = gray[y:y+h,x:x+w]
            color =(255,0,0)
            stroke = 2
            cv2.rectangle(frame,(x,y),(x+w,y+h),color,stroke)
            
        #se convierte el frame a QPixmap para poder dibujarla
        #en el label de mainWindow
        height, width, bytesPerComponent = frame.shape
        bytesPerLine = 3 *width
        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB, frame)                                           
        QImg = QImage(frame.data, width, height, bytesPerLine,QImage.Format_RGB888)
        
        pixmap = QPixmap.fromImage(QImg)
        #se dibuja el frame
        self.WindowOpenCV.setPixmap(pixmap)
        
        #cv2.imshow('frame',frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
        

  
    def draw(self):

        # lectura de las teclas del teclado
        self.keyEvent()

        # se actualizan las coordenadas de los cuadrados
        self.s.update(self.w,self.h)
        # se obtienen las coordenadas de los cuadrados
        coord = self.s.getCoord()

        # si checkea que se coma la comida
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
        glColor3f(0,1,0);
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
