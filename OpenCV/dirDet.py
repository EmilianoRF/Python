
import numpy as numpy
import cv2
import copy
import os

face_cascade = cv2.CascadeClassifier(
    'cascades/data/haarcascade_frontalface_alt2.xml')

cap = cv2.VideoCapture(0)

posicionesReferencia = []
intervaloReferencia = 0
posiciones = []
intervalo = 0
xref = 0
yref = 0
href = 0
wref = 0


def deltax(ini, final):
    xmin = 15
    deltax = final[0]-ini[0]
    if deltax > xmin:
        return 'd'
    else:
        xmin = copy.copy(-xmin)
        if deltax < xmin:
            return 'i'
        else:
            return 'n'


def promedio(arr):
    ha = 0
    wa = 0
    xa = 0
    ya = 0
    for point in arr:
        xa += point[0]
        ya += point[1]
        wa += point[2]
        ha += point[3]
    x = xa/len(arr)
    y = ya/len(arr)
    w = wa/len(arr)
    h = ha/len(arr)

    return x, y, w, h


def cercaRef(arr):
  #  global xref
   # global yref
    margen = 3.1
    if abs(xref-arr[0]) < margen or abs(yref-arr[1]) < margen:
        return True
    else:
        return False


while(True):

    ret, frame = cap.read()
    cv2.flip(frame, 1, frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.5, minNeighbors=5)

    for(x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        #img_item = 'my-image'+str(intervalo)+'.png'

        # cv2.imwrite(img_item,roi_gray)
        color = (255, 0, 0)
        stroke = 2
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, stroke)
        if intervaloReferencia < 20:
            intervaloReferencia += 1
            posicionesReferencia.append((x, y, w, h))
        if intervaloReferencia == 20:
            xref, yref, wref, href = promedio(posicionesReferencia)
            intervaloReferencia += 1
        else:
            posiciones.append((x, y))
            intervalo += 1
            if intervalo > 2:
                # cercaRef(posiciones[len(posiciones)-1])
                # if cercaRef(posiciones[len(posiciones)-1]):
                intervalo = copy.copy(0)
                #posiciones[len(posiciones)-2], posiciones[len(posiciones)-1]
                dx = deltax(posiciones[len(posiciones)-2],
                            posiciones[len(posiciones)-1])
                posiciones = copy.deepcopy([])
                if dx == 'd':
                    print("DERECHA!")
                elif dx == 'i':
                    print("IZQUIERDA!")
                elif dx == 'n':
                    def clear(): return os.system('cls')
                    clear()
    cv2.imshow('test', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
