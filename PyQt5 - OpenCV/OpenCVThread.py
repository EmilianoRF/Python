
import cv2 
import numpy as np
import imutils

import copy
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *


class OpenCVThread(QThread):
    
    # variable que emite la señal de la imagen
    image = pyqtSignal(QPixmap)
    # variable que emite la señal del movimiento
    mover = pyqtSignal(int,int)
    
    def __init__(self, parent = None):
        super(OpenCVThread,self).__init__(parent)

        # se carga el modelo de nn a utilizar
        self.modFile = "./model/res10_300x300_ssd_iter_140000.caffemodel"
        #prototxt contiene la descripcion de la neural network utilizada
        self.configFile = "./model/deploy.prototxt.txt"
        
        #arreglo que almacena los vertices de los frames
        self.positions = []
        # variable que almacena la cantidad de frames leidos
        self.interval = 0
        self.xmin = 0
        self.ymin = 0
        self.minInterval = 1
        self.camStatus = True
        self.threadactive = True

    def setXmin(self,deltax):
            self.xmin=deltax
    def setYmin(self,deltay):
            self.ymin=deltay
    def setFrames(self,interval):
            self.minInterval = interval  
    
    def releaseCam(self,val):
        self.camStatus = val 
        
    def stop(self):
        self.threadactive = False
        self.wait()
        
    def killthread(self):
        self.thread.stop()
    
    def setXdefault(self,val):
        self.xmin=val
    def setXdefault(self,val):
        self.ymin=val          
    
    def getDelta(self,ini, final):
        # el origen de coordenadas esta en la esquina
        # superior izquierda
        retorno = 'n'
        deltay = final[1]-ini[1]
        deltax = (final[0]-ini[0])
        # se determina cual delta fue mayor
        # para establecer la prioridad del movimiento
        if abs(deltax) > abs(deltay):
            if deltax > self.xmin:
                retorno = 'd'
            elif deltax < 0:
                xmin= (-1)*self.xmin
                if deltax < xmin:
                    retorno ='i'
        else:    
            if deltay > self.ymin:
                retorno = 'b'
            elif deltay < 0:
                ymin = (-1)*self.ymin
                if deltay < ymin:
                    retorno = 'a'

        return retorno

    def run(self):
        
        cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        
        if self.camStatus:
            
            # el modelo encargado del análisis de la imagen es GoogleLeNet
            # Caffe es el framework utilizado para interactuar con el modelo
            
            # se carga el modelo
            net = cv2.dnn.readNetFromCaffe(self.configFile,self.modFile)
            
            while self.threadactive:
                ret,frame = cap.read()
                frame = imutils.resize(frame,width=800,height=800)
                # se espeja
                cv2.flip(frame,1,frame)
                
                # se toman las dimensiones de la imagen
                
                (h,w) = frame.shape[:2]
                
                # factores involucrados en el preprosesamiento de la imagen
                # necesario para utilizar el modelo
                
                meanSubtraction = (104.0,177.0,123.0)
                scaleFactor = 1.0
                dimension = (300,300)
                
                # se genera la imagen para enviar al clasificador
                
                blob = cv2.dnn.blobFromImage(frame,scaleFactor,dimension,meanSubtraction)
                
                # se envía la imagen
                
                net.setInput(blob)
                
                # se obtienen las detecciones en un arreglo
                
                detecciones = net.forward()
                
                # se recorre el arreglo de detecciones
                for i in range (0,detecciones.shape[2]):
                    
                    certeza = detecciones[0,0,i,2]
                    
                    if certeza < 0.5:
                        continue
                    else:
                        npa = np.array([w,h,w,h])
                        
                        #print("detecciones:" , detecciones[0,0,i,3:7])
                        faceCoord = detecciones[0,0,i,3:7]*npa
                        #print("box:", box)
                        
                        # se obtienen las coordeandas de los 4 vertices que limitan la cara
                        # como enteros
                        (startX,startY,endX,endY) = faceCoord.astype("int")
                                      
                        # se dibujan circulos en los 4 vertices del cuadrado que limita la cara
                        tickness = 10
                        radius = 2
                        color = (0,0,255)
                        cv2.circle(frame,(startX,startY),radius,color,tickness)
                        cv2.circle(frame,(startX,endY),radius,color,tickness)
                        cv2.circle(frame,(endX,endY),radius,color,tickness)
                        cv2.circle(frame,(endX,startY),radius,color,tickness)
                        
                        #se agrega el punto al arreglo de vertices
                        self.positions.append((endX,endY))
                        # variable que representa la cantidad de frames almacenados
                        self.interval += 1
                        
                        if self.interval > self.minInterval:
                            #se resetea la cantidad de frames
                            self.interval = copy.copy(0)
                            #se determina si hubo movimiento
                            delta = self.getDelta(self.positions[len(self.positions)-2],
                                            self.positions[len(self.positions)-1])
                            #se resetea el arreglo
                            self.positions = copy.deepcopy([])
                            if delta == 'd':
                                #print("DERECHA!")
                                self.mover.emit(1,0)
                            elif delta == 'i':
                                #print("IZQUIERDA!")
                                self.mover.emit(-1,0)
                            elif delta == 'a':
                                #print("ARRIBA!")
                                self.mover.emit(0,1)
                            elif delta == 'b':
                                #print("ABAJO!")
                                self.mover.emit(0,-1)
                            elif delta == 'n':
                                pass
                            
                #se convierte el frame a QPixmap para poder dibujarla en el label de mainWindow
                
                height, width, colors = frame.shape
                
                # bytesPerLine representa la cantidad de bytes requeridos por los pixeles de una imagen
                # en una fila. En este caso cada pixel esta compuesto por 3 bytes (BGR), entonces el total 
                # de bytes por fila es 3* ancho de la ventana
                
                bytesPerLine = 3 *width
                
                # se convierte la imagen de BGR a RGB
                
                cv2.cvtColor(frame, cv2.COLOR_BGR2RGB, frame)   
                
                # se crea una Qimg a partir del frame y luego se convierte a QPixmap para
                # enviarla al label de la cámara en la GUI                                        
                
                QImg = QImage(frame.data, width, height, bytesPerLine,QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(QImg)
                #se emite la imagen  
                self.image.emit(pixmap)
        else:
            cv2.release()   
            cv2.destroyAllWindows()
