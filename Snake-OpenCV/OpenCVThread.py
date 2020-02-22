
import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class OpenCVThread(QThread):
    """
    Runs a counter thread.
    """
    image = pyqtSignal(QPixmap)
    def run(self):
        cap = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
        while True:
            ret,frame = cap.read()
            # se espeja
            cv2.flip(frame,1,frame)
            #se hace una copia de la imagen en escala de grises para poder usar
            #cascade
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=3)
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
            #se emite la imagen  
            self.image.emit(pixmap)