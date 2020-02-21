
import numpy as numpy
import cv2
import copy
import os

face_cascade = cv2.CascadeClassifier(
    'cascades/data/haarcascade_frontalface_alt2.xml')

cap = cv2.VideoCapture(0)

#arreglo que almacena los vertices de los frames
posiciones = []
# variable que almacena la cantidad de frames 
# leidos
intervalo = 0


def getDelta(ini, final):

    # el origen de coordenadas esta en la esquina
    # superior izquierda
    retorno = 'n'

    deltay = final[1]-ini[1]
    deltax = (final[0]-ini[0])
    # se determina cual delta fue mayor
    # para establecer la prioridad del movimiento
    if abs(deltax) > abs(deltay):
        xmin = 30
        if deltax > xmin:
            retorno = 'd'
        elif deltax < 0:
                retorno ='i'
    else:    
        ymin = 30
        if deltay > ymin:
            retorno = 'b'
        elif deltay < 0:
                retorno = 'a'

    return retorno


while(True):

    ret, frame = cap.read()
    cv2.flip(frame, 1, frame)
    #se convierte la imagen a escala de grises para poder
    #clasificarla
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.15, minNeighbors=3)

    for(x, y, w, h) in faces:

        # se dibuja el el cuadrado donde esta la cara        
        #color = (255, 0, 0)
        #stroke = 2
        #cv2.rectangle(frame, (x, y), (x+w, y+h), color, stroke)
        
        # se dibujan los vertices que detectan la cara

        # punto inferior derecho
        infd = "x:{}".format(x+w) + "y:{}".format(y+h)
        cv2.putText(frame, infd, (x+w, y+h),1,1.5,(0,0,255),2)
        # punto inferior izquierdo
        infi = "x:{}".format(x) + "y:{}".format(y+h)
        cv2.putText(frame, infi, (x, y+h),1,1.5,(0,0,255),2)
        # punto superior derecho
        supd = "x:{}".format(x+w) + "y:{}".format(y)
        cv2.putText(frame, supd, (x+w, y),1,1.5,(0,0,255),2)
        # punto superior izquierdo
        supi = "x:{}".format(x) + "y:{}".format(y)
        cv2.putText(frame, supi, (x, y),1,1.5,(0,0,255),2)

        #se agrega el punto al arreglo de vertices
        posiciones.append((x, y))
        
        # variable que representa la cantidad de frames
        # almacenados
        intervalo += 1
        
        if intervalo > 13:
            #se resetea la cantidad de frames
            intervalo = copy.copy(0)
            #se analizan los movimientos
            delta = getDelta(posiciones[0],
                             posiciones[len(posiciones)-1])
            #se resetea el arreglo
            posiciones = copy.deepcopy([])
            if delta == 'd':
                print("DERECHA!")
            elif delta == 'i':
                print("IZQUIERDA!")
            elif delta == 'a':
                print("ARRIBA!")
            elif delta == 'b':
                print("ABAJO!")
            elif delta == 'n':
                def clear(): return os.system('cls')
                clear()
    cv2.imshow('test', frame)
    
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
