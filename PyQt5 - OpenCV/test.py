import cv2 
import numpy as np
import imutils


modFile = "./model/res10_300x300_ssd_iter_140000.caffemodel"
configFile = "./model/deploy.prototxt.txt"

net = cv2.dnn.readNetFromCaffe(configFile,modFile)

video_capture = cv2.VideoCapture(0)

while True:
    
    ret,frame = video_capture.read()
    frame = imutils.resize(frame,width=750)
    cv2.flip(frame,1,frame)
    
    (h,w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame,(300,300)),1.0,(300,300),(104.0,177.0,123.0))
    
    net.setInput(blob)
    detections = net.forward()
    
    for i in range (0,detections.shape[2]):
        confidence = detections[0,0,i,2]
        
        if confidence < 0.5:
            continue
        
        box = detections[0,0,i,3:7]*np.array([w,h,w,h])
        (startX,startY,endX,endY) = box.astype("int")
        
        cv2.rectangle(frame,(startX,startY),(endX,endY),(0,0,255),2)
    
    cv2.imshow("frame",frame)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord("q"):
        break

cv2.destroyAllWindows()
video_capture.release()