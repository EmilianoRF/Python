 

class FileManager:
    
    def __init__(self,name = ''):
      self.fileName = name
      
      
    def getConfigurations(self):
          configurations = self.readFile()
          return configurations
    
    def writeFile(self,parameters):
          text = ''
          with open(self.fileName, 'w') as file :
                for key,val in parameters.items():
                      text+=str(key) + " : "+ str(val) +'\n'
                file.write(text)
    
    def readFile(self):
          configurations = {}
          with open(self.fileName, 'r') as file :
              while True:
                  line = file.readline()
                  # se comprueba si se llego al final del archivo
                  if line == '':
                      break
                  else:
                      if line == "\n":
                            continue
                      line = line.strip("\n")
                      line = line.replace(" ","")
                      line = line.split(":")
                      configurations[line[0]] = line[1]
          return configurations
