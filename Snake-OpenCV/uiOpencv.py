from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import *

import cv2
import render
from OpenCVThread import *

class Ui_MainWindow(object):
    
    def __init__(self):
    # dimensiones del widget de opengl
        self.windowWidth = 400
        self.windowHeight = 400
        
        self.graficador = render.Render(self.windowWidth,self.windowHeight)
        
        #self.face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
        #self.cap = cv2.VideoCapture(0)
        self.thread = OpenCVThread()

    
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

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.retranslateUi(MainWindow)
        
        #se genera un nuevo hilo para la lectura del video de la camara
        self.thread.image.connect(self.updateLabel)
        self.thread.start()
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.WindowOpenCV.setText(_translate("MainWindow", "TextLabel"))
        
        # se inicializan las funciones de OpenGL
        self.WindowOpenGL.initializeGL 
        self.WindowOpenGL.resizeGL(self.windowWidth,self.windowHeight)
        self.WindowOpenGL.paintGL = self.graficador.paint()
        
        # se setea la tasa de refresco de la pantalla
        timer = QTimer(self.centralwidget)
        timer.timeout.connect(self.WindowOpenGL.update) 
        timer.start(100)
    #se actualiza el label con la imagen tomada de la camara   
    def updateLabel(self, image):
        self.WindowOpenCV.setPixmap(image)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
