from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import *

import cv2
import render
import FilesManager
from OpenCVThread import *


class Ui_MainWindow(object):
    
    def __init__(self):
        # variable que controla el thread donde se ejecuta el codigo de opencv
        self.cvThread = OpenCVThread()
        # se abre el archivo de configuraciones
        self.ConfigFile = FilesManager.FileManager("config.txt")
        # se leen las configuraciones para ser cargadas en la UI
        self.Configurations = self.ConfigFile.getConfigurations()
        # se inicializan los parámetros por defecto
        self.parameters = {
            "windowWidth" : 600,
            "windowHeight" : 600,
            "defaultXmin" : self.getDefault("defaultXmin"),
            "defaultYmin" : self.getDefault("defaultYmin"),
            "defaultFrames" : self.getDefault("defaultFrames"),
            "defaultGLtimer" : self.getDefault("defaultGLtimer")
        }
        # elemento encargado de dibujar en el widget de opengl
        self.graficador = render.Render(self.parameters["windowWidth"],self.parameters["windowWidth"])
        # variable que controla la tasa de refresco del widget de opengl
        self.timer = QTimer()
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1350, 788)
        MainWindow.setMinimumSize(QtCore.QSize(1350, 788))
        MainWindow.setMaximumSize(QtCore.QSize(1350, 788))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.WindowOpenGL = QtWidgets.QOpenGLWidget(self.centralwidget)
        self.WindowOpenGL.setGeometry(QtCore.QRect(50, 50, 600, 600))
        self.WindowOpenGL.setObjectName("WindowOpenGL")
        self.WindowOpenCV = QtWidgets.QLabel(self.centralwidget)
        self.WindowOpenCV.setGeometry(QtCore.QRect(670, 50, 600, 600))
        self.WindowOpenCV.setAutoFillBackground(True)
        self.WindowOpenCV.setFrameShape(QtWidgets.QFrame.Box)
        self.WindowOpenCV.setFrameShadow(QtWidgets.QFrame.Plain)
        self.WindowOpenCV.setText("")
        self.WindowOpenCV.setObjectName("WindowOpenCV")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(340, 670, 231, 71))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_4.addWidget(self.label_2, 0, 0, 1, 1)
        self.deltaY = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.deltaY.setFont(font)
        self.deltaY.setObjectName("deltaY")
        self.gridLayout_4.addWidget(self.deltaY, 0, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        self.sliderY = QtWidgets.QSlider(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(1)
        self.sliderY.setFont(font)
        self.sliderY.setOrientation(QtCore.Qt.Horizontal)
        self.sliderY.setObjectName("sliderY")
        self.gridLayout_3.addWidget(self.sliderY, 1, 0, 1, 1)
        self.layoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_2.setGeometry(QtCore.QRect(600, 670, 240, 71))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.layoutWidget_2)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.sliderFrames = QtWidgets.QSlider(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(1)
        self.sliderFrames.setFont(font)
        self.sliderFrames.setOrientation(QtCore.Qt.Horizontal)
        self.sliderFrames.setObjectName("sliderFrames")
        self.gridLayout_5.addWidget(self.sliderFrames, 2, 0, 1, 1)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_6.addWidget(self.label_3, 0, 0, 1, 1)
        self.frameNum = QtWidgets.QLineEdit(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.frameNum.setFont(font)
        self.frameNum.setObjectName("frameNum")
        self.gridLayout_6.addWidget(self.frameNum, 0, 1, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_6, 1, 0, 1, 1)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(80, 670, 231, 71))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.deltaX = QtWidgets.QLineEdit(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.deltaX.setFont(font)
        self.deltaX.setObjectName("deltaX")
        self.gridLayout.addWidget(self.deltaX, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.sliderX = QtWidgets.QSlider(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(1)
        self.sliderX.setFont(font)
        self.sliderX.setOrientation(QtCore.Qt.Horizontal)
        self.sliderX.setObjectName("sliderX")
        self.gridLayout_2.addWidget(self.sliderX, 1, 0, 1, 1)
        self.layoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget_4.setGeometry(QtCore.QRect(870, 670, 240, 71))
        self.layoutWidget_4.setObjectName("layoutWidget_4")
        self.gridLayout_13 = QtWidgets.QGridLayout(self.layoutWidget_4)
        self.gridLayout_13.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.sliderGL = QtWidgets.QSlider(self.layoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(1)
        self.sliderGL.setFont(font)
        self.sliderGL.setOrientation(QtCore.Qt.Horizontal)
        self.sliderGL.setObjectName("sliderGL")
        self.gridLayout_13.addWidget(self.sliderGL, 2, 0, 1, 1)
        self.gridLayout_14 = QtWidgets.QGridLayout()
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.label_7 = QtWidgets.QLabel(self.layoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout_14.addWidget(self.label_7, 0, 0, 1, 1)
        self.glFrame = QtWidgets.QLineEdit(self.layoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.glFrame.setFont(font)
        self.glFrame.setObjectName("glFrame")
        self.gridLayout_14.addWidget(self.glFrame, 0, 1, 1, 1)
        self.gridLayout_13.addLayout(self.gridLayout_14, 1, 0, 1, 1)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(1150, 670, 95, 65))
        self.widget.setObjectName("widget")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.makeDefault = QtWidgets.QPushButton(self.widget)
        self.makeDefault.setObjectName("makeDefault")
        self.gridLayout_7.addWidget(self.makeDefault, 0, 0, 1, 1)
        self.reset = QtWidgets.QPushButton(self.widget)
        self.reset.setObjectName("reset")
        self.gridLayout_7.addWidget(self.reset, 1, 0, 1, 1)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    # Se inicializan las funciones de OpenCv   
    ############################################################################################################################        
        #se pasan los valores por defecto
        self.cvThread.setXmin(self.parameters["defaultXmin"])
        self.cvThread.setYmin(self.parameters["defaultYmin"])
        #se conecta el widget de opengl y el label de la cámara
        self.cvThread.image.connect(self.updateLabel)
        self.cvThread.mover.connect(self.graficador.move)
        #se genera un nuevo hilo para la lectura del video de la camara
        self.cvThread.start()
    ############################################################################################################################           

    # Se inicializan los sliders
    ############################################################################################################################
        # SLIDER X
        self.initSliderX()
        # SLIDER Y
        self.initSliderY()
        # SLIDER FRAMES
        self.initSliderFrames()
        # SLIDER OpenGL Timer
        self.initSliderGL()
    ############################################################################################################################ 
               
    # Se conectan las señales con sus respectivas respuestas
    ############################################################################################################################ 
        # Manejo de los botones
        self.makeDefault.clicked.connect(self.setdefault)
        self.reset.clicked.connect(self.resetValues)
        # se toman los valores de los sliders y se envian al thread de opencv
        self.sliderX.valueChanged.connect(self.updateXmin)
        self.sliderY.valueChanged.connect(self.updateYmin)
        self.sliderFrames.valueChanged.connect(self.updateFrames)
        self.sliderGL.valueChanged.connect(self.updateTimer)
    ############################################################################################################################
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Test - PyQt5/OpenCV"))
        self.label_2.setText(_translate("MainWindow", "Sensitivity y :"))
        self.label_3.setText(_translate("MainWindow", "Frame interval :"))
        self.label.setText(_translate("MainWindow", "Sensitivity x :"))
        self.label_7.setText(_translate("MainWindow", "OpenGL RR :"))
        self.makeDefault.setText(_translate("MainWindow", "Set as default"))
        self.reset.setText(_translate("MainWindow", "Reset"))

        
        # se inicializan las funciones de OpenGL
        self.WindowOpenGL.initializeGL 
        self.WindowOpenGL.resizeGL(self.parameters["windowWidth"],self.parameters["windowHeight"])
        self.WindowOpenGL.paintGL = self.graficador.paint()
        
        # se setea la tasa de refresco de la pantalla
        self.timer.setParent(self.centralwidget)
        self.timer.timeout.connect(self.WindowOpenGL.update) 
        self.timer.start(self.parameters["defaultGLtimer"])
        
    # Definiciones de las respuestas a las señales
    ############################################################################################################################ 
    def updateLabel(self, image):
        self.WindowOpenCV.setPixmap(image)
        
    def updateXmin(self,val):
        self.cvThread.setXmin(val)
        self.deltaX.setText(str(float(val)))
        
    def updateYmin(self,val):
        self.cvThread.setYmin(val)
        self.deltaY.setText(str(float(val)))
        
    def updateFrames(self,val):
        self.cvThread.setFrames(val)
        self.frameNum.setText(str(val))
        
    def updateTimer(self,val):
        self.timer.start(val*10)
        self.glFrame.setText(str(val*10)+ ' ms')
        
    def setdefault(self):
        # se setean los parametros actuales como aquellos por defecto
        self.parameters["defaultXmin"] =  self.sliderX.value()
        self.parameters["defaultYmin"] =  self.sliderY.value()
        self.parameters["defaultFrames"] =  self.sliderFrames.value()
        self.parameters["defaultGLtimer"] =  self.sliderGL.value()*10
        # se ignoran las dimensiones al escribir en el archivo
        exclusiones = {"windowWidth","windowHeight"}
        # diccionario auxiliar para la escritura
        wr_parameters = {}
        for key in self.parameters:
            if key not in exclusiones:
                wr_parameters[key] = self.parameters[key]
        # se escribe en el archivo
        self.ConfigFile.writeFile(wr_parameters)
        
    def resetValues(self):
        self.initSliderX()
        self.initSliderY()
        self.initSliderFrames()
        self.initSliderGL()
    ############################################################################################################################
    
    # Definiciones de las funciones de inicialización de los sliders
    ############################################################################################################################
    def initSliderX(self):
        self.sliderX.setMinimum(1)
        self.sliderX.setMaximum(30)
        self.sliderX.setSingleStep(1)
        self.sliderX.setSliderPosition(self.parameters["defaultXmin"])
        #se setea el valor inicial en el display de texto junto con otras propieades
        if self.parameters["defaultXmin"] == 0:
            self.deltaX.setText("N/A")
        else:
            self.deltaX.setText(str(self.parameters["defaultXmin"])+".0")
        self.deltaX.setEnabled(False)
        self.deltaX.setAlignment(QtCore.Qt.AlignCenter)
        
    def initSliderY(self):
        self.sliderY.setMinimum(1)
        self.sliderY.setMaximum(20)
        self.sliderY.setSingleStep(1)
        self.sliderY.setSliderPosition(self.parameters["defaultYmin"])
        #se setea el valor inicial en el display de texto junto con otras propieades
        if self.parameters["defaultYmin"] == 0:
            self.deltaY.setText("N/A")
        else:
            self.deltaY.setText(str(self.parameters["defaultYmin"])+".0")
        self.deltaY.setEnabled(False)
        self.deltaY.setAlignment(QtCore.Qt.AlignCenter)
        
    def initSliderFrames(self):
        self.sliderFrames.setMinimum(1)
        self.sliderFrames.setMaximum(30)
        self.sliderFrames.setSingleStep(1)
        self.sliderFrames.setSliderPosition(self.parameters["defaultFrames"])
        #se setea el valor inicial en el display de texto junto con otras propieades
        if self.parameters["defaultFrames"] == 0:
            self.frameNum.setText("N/A")
        else:
            self.frameNum.setText(str(self.parameters["defaultFrames"]))
        self.frameNum.setEnabled(False)
        self.frameNum.setAlignment(QtCore.Qt.AlignCenter)
        
    def initSliderGL(self):
        self.sliderGL.setMinimum(5)
        self.sliderGL.setMaximum(25)
        self.sliderGL.setSliderPosition(int(self.parameters["defaultGLtimer"]/10))
        #se setea el valor inicial en el display de texto junto con otras propieades
        if self.parameters["defaultGLtimer"] == 0:
            self.glFrame.setText("N/A")
        else:
            self.glFrame.setText(str(self.parameters["defaultGLtimer"])+' ms')
        self.glFrame.setEnabled(False)
        self.glFrame.setAlignment(QtCore.Qt.AlignCenter)
        
    ############################################################################################################################       
   
    # Funciones extras
    ############################################################################################################################ 


    # funcion que retorna el valor de la configuración buscada
    def getDefault(self,tipo):
        retorno = 0
        for key in self.Configurations:
            # si el tipo corresponde con alguna key
            if tipo in key:
                # si el valor asociado es un numero
                if self.Configurations[key].isnumeric():
                    retorno = int(self.Configurations[key])
                    break  
        return retorno
    ############################################################################################################################ 

'''
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
'''