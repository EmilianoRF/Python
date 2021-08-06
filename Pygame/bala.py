
class Bala:
    def __init__(self,imagen,x,y,xS,yS):
        self.imagen = imagen
        self.x = x
        self.y = y
        self.xV = xS
        self.yV = yS
        self.imgRect = imagen.get_rect()
        self.hitbox = (x,y,imagen.get_rect().w,imagen.get_rect().h)
        self.tiempoVuelo = 0
        self.tiempoVueloMax = 50
        
    def setX(self,x):
        self.x=x
    def setY(self,y):
        self.y=y
    def getImg(self):
        return self.imagen   
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getX(self):
        return self.x
    def mover(self):
        self.x+=self.xV
        self.y+=self.yV
        self.hitbox = (self.x,self.y,self.imagen.get_rect().w,self.imagen.get_rect().h)
        self.tiempoVuelo+=1
    def setVelX(self,vel):
        self.xV = vel
    def setVelY(self,vel):
        self.yV = vel
    def getHitbox(self):
        return self.hitbox
        #print(self.hitbox)
    def getRect(self):
        self.imgRect.topleft = (self.x,self.y)
        return self.imgRect
    def resetTiempoVuelo(self):
        self.tiempoVuelo = 0
    def getTiempoVuelo(self):
        return self.tiempoVuelo
    def setTiempoVueloMax(self,val):
        self.tiempoVueloMax = val