
import random
import copy

class vect4:
    def __init__(self,x_iz=0,x_der=0,y_in=0,y_sup=0):
        self.x_iz = x_iz
        self.x_der = x_der
        self.y_in = y_in
        self.y_sup = y_sup

def toVec4(x,y):
        xi = x 
        xd = x + 1
        ys = y+ 1
        #inferior
        yi = y  
        return vect4(xi,xd,yi,ys)


def foodLocation(width,height):
    x = random.randint(5,width-5)
    y = random.randint (5,height-5)
    #print(x,y)
    return toVec4(x,y)

def addVec(v1: vect4,v2: vect4):
    retorno = vect4()
    
    retorno.x_iz = v1.x_iz + v2.x_iz
    retorno.x_der = v1.x_der + v2.x_der
    retorno.y_in = v1.y_in + v2.y_in
    retorno.y_sup = v1.y_sup + v2.y_sup

    return retorno

class Snake:
    def  __init__(self,x,y):
        
        self.body = []
        self.len = 1
        #se agrega el primer elemento   
        self.body.append(toVec4(x,y)) 
        #speed
        self.xspeed = 0
        self.yspeed = 0
        # cola
        self.tail = []

    
    def update(self,width,height):
                         
        if(self.onRange(width,height)):
            
            #se copia el ultimo elemento y se lo desplaza
            head = copy.deepcopy(self.body[len(self.body)-1])
            head.x_iz+= self.xspeed
            head.x_der+= self.xspeed
            head.y_in+= self.yspeed
            head.y_sup+= self.yspeed
            #se crea un arreglo auxiliar
            aux=[]
            #se crea un arreglo nuevo que tiene los mismos elementos
            #que body excepto el primer elemento
            largo = len(self.body)
            for index in range(1,largo,1):
                aux.append(self.body[index])
            #ahora body tiene los mismos elementos salvo el primer item
            self.body = copy.deepcopy(aux)
            #se agrega el ultimo item desplazado al final del arreglo
            self.body.append(head)
            
        else:
            self.body = copy.deepcopy([])
            self.body.append(toVec4(random.randint(0,width),random.randint(0,height)))
            self.xspeed = 0
            self.yspeed = 0
            self.len = 1
        
    def getCoord(self):
        return self.body

    
    def setSpeed(self,xs,ys):
        self.xspeed = xs
        self.yspeed = ys
        
    def onRange(self,width,height):
        retorno = True
        if self.body[len(self.body)-1].x_iz < 0 or self.body[len(self.body)-1].y_in < 0:
            retorno = False
        elif self.body[len(self.body)-1].x_der > width  or self.body[len(self.body)-1].y_sup > height:
            retorno = False
        return retorno
    
    def eat(self,pos : vect4):
        retorno = False
        if  self.body[len(self.body)-1].x_iz == pos.x_iz and \
            self.body[len(self.body)-1].x_der == pos.x_der and \
            self.body[len(self.body)-1].y_in == pos.y_in and \
            self.body[len(self.body)-1].y_sup == pos.y_sup :
                retorno = True
        return retorno
    
    def getLen(self):
        return self.len
    
    def grow(self):
        # se copia el ultimo elemento del arreglo y se incerta
        #nuevamente al final
        head = self.body[len(self.body)-1]
        self.body.append(head)
        self.len+=1
    
    def currDir(self):
        retorno = ''
        if self.xspeed == 1:
            retorno = 'd'
        elif self.xspeed == -1:
            retorno = 'i'
        elif self.yspeed == 1:
            retorno = 'b'
        elif self.yspeed == -1:
            retorno = 'a'   
        return retorno
             
