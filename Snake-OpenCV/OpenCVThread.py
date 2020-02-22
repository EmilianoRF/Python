
import cv2
import copy
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *


class OpenCVThread(QThread):
    
    def __init__(self, parent = None):
        super(OpenCVThread,self).__init__(parent)
        self.face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
        #arreglo que almacena los vertices de los frames
        self.posiciones = []
        # variable que almacena la cantidad de frames leidos
        self.intervalo = 0

    image = pyqtSignal(QPixmap)
    mover = pyqtSignal(int,int)
    
    def getDelta(self,ini, final):
        # el origen de coordenadas esta en la esquina
        # superior izquierda
        retorno = 'n'
        deltay = final[1]-ini[1]
        deltax = (final[0]-ini[0])
        # se determina cual delta fue mayor
        # para establecer la prioridad del movimiento
        if abs(deltax) > abs(deltay):
            xmin = 13
            if deltax > xmin:
                retorno = 'd'
            elif deltax < 0:
                xmin= (-1)*xmin
                if deltax < xmin:
                    retorno ='i'
        else:    
            ymin = 13
            if deltay > ymin:
                retorno = 'b'
            elif deltay < 0:
                ymin = (-1)*ymin
                if deltay < ymin:
                    retorno = 'a'

        return retorno


    def run(self):
        cap = cv2.VideoCapture(0)
        #face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
        while True:
            ret,frame = cap.read()
            # se espeja
            cv2.flip(frame,1,frame)
            #se hace una copia de la imagen en escala de grises para poder usar
            #cascade
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=3)
            #se dibuja un cuadrado en las coordenadas donde se detecto la cara
            for (x,y,w,h) in faces:
                
                stroke = 1
                scale = 1
                # punto inferior derecho
                infd = "x:{}".format(x+w) + "y:{}".format(y+h)
                cv2.putText(frame, infd, (x+w, y+h),1,scale,(0,0,255),stroke)
                # punto inferior izquierdo
                infi = "x:{}".format(x) + "y:{}".format(y+h)
                cv2.putText(frame, infi, (x, y+h),1,scale,(0,0,255),stroke)
                # punto superior derecho
                supd = "x:{}".format(x+w) + "y:{}".format(y)
                cv2.putText(frame, supd, (x+w, y),1,scale,(0,0,255),stroke)
                # punto superior izquierdo
                supi = "x:{}".format(x) + "y:{}".format(y)
                cv2.putText(frame, supi, (x, y),1,scale,(0,0,255),stroke)
                #se agrega el punto al arreglo de vertices
                self.posiciones.append((x, y))
                # variable que representa la cantidad de frames
                # almacenados
                self.intervalo += 1
                
                if self.intervalo > 3:
                    #se resetea la cantidad de frames
                    self.intervalo = copy.copy(0)
                    #se analizan los movimientos
                    delta = self.getDelta(self.posiciones[0],
                                    self.posiciones[len(self.posiciones)-1])
                    #se resetea el arreglo
                    self.posiciones = copy.deepcopy([])
                    if delta == 'd':
                        print("DERECHA!")
                        self.mover.emit(1,0)
                    elif delta == 'i':
                        print("IZQUIERDA!")
                        self.mover.emit(-1,0)
                    elif delta == 'a':
                        print("ARRIBA!")
                        self.mover.emit(0,1)
                    elif delta == 'b':
                        print("ABAJO!")
                        self.mover.emit(0,-1)
                    elif delta == 'n':
                        def clear(): return os.system('cls')
                        clear()
            #se convierte el frame a QPixmap para poder dibujarla
            #en el label de mainWindow
            height, width, bytesPerComponent = frame.shape
            bytesPerLine = 3 *width
            cv2.cvtColor(frame, cv2.COLOR_BGR2RGB, frame)                                           
            QImg = QImage(frame.data, width, height, bytesPerLine,QImage.Format_RGB888)
            
            pixmap = QPixmap.fromImage(QImg)
            #se emite la imagen  
            self.image.emit(pixmap)