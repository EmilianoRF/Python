import numpy as np
from matplotlib import pyplot as plt

# vector de 1000 frecuencias entre 10^-2 a 10^9
f =  np.logspace(1,7,1000)
# declaracion de omega
w = 2*np.pi*f
# declaracion de s
s= 1.0j*w
# variables del circuito
R1,C1 = 1000,100e-9
T1 = R1*C1
R2,C2 = 51000,220e-12
T2 = R2*C2

# funcion de transferencia A(s)
Ajw =(R1/R2)*((s*T1)/((s*T2+1)*(s*T1+1)))

# modulo en decibeles de A(s)
db_mag =20*np.log10(np.abs(Ajw))
# fase de A(s)
fase = np.arctan2(np.imag(Ajw),np.real(Ajw))*180/np.pi

##############################################################################

# DIAGRAMA DE AMPLITUD TEÓRICO

plt.figure()

# declaracion de k
k=np.empty(1000)
k.fill(20*np.log10(R2/R1))

# declaracion de los demas factores de primer orden
l1 = 20*np.log10(np.abs(s*T1))
l2 = 20*np.log10(1/np.abs((s*T2+1)))
l3 = 20*np.log10(1/np.abs((s*T1+1)))


# plot del modulo de A(s)
ftransferencia = k+l1+l2+l3
plt.semilogx(f,ftransferencia)

# Estilo de las lineas de los factores de primer orden
linea ='dashed'
# plots en escala logaritmica
plt.semilogx(f,k,linestyle=linea)
plt.semilogx(f,l1,linestyle=linea)
plt.semilogx(f,l2,linestyle=linea)
plt.semilogx(f,l3,linestyle=linea)

# Parametros de los ejes

plt.legend(['A(jw)','R2/R1','sT1','1/(sT2+1)','1/(sT1+1)'],loc='best')
plt.grid(False)
plt.xlabel("Frecuencia [Hz]")
plt.ylabel("Amplitud [db]")
plt.ylim(-80,60)
plt.yticks(np.arange(-80,60,20))
plt.grid(True,linestyle='dashed')

# Se guarda la figura
#plt.savefig('amplitud solo.png', dpi=900)

##############################################################################

# DIAGRAMA DE FASE TEÓRICO

plt.figure()

# k para la fase
kf=np.empty(1000)
kf.fill(180)
# Declaración del resto de los factores
l1f= np.arctan2(np.imag(s*T1),np.real(s*T1))*180/np.pi+180
l2f= np.arctan2(np.imag(1/(s*T2+1)),np.real(1/(s*T2+1)))*180/np.pi+180
l3f= np.arctan2(np.imag(1/(s*T1+1)),np.real(1/(s*T1+1)))*180/np.pi +180

# Funciones auxiliares para el plot
l1faux= np.arctan2(np.imag(s*T1),np.real(s*T1))*180/np.pi
l2faux= np.arctan2(np.imag(1/(s*T2+1)),np.real(1/(s*T2+1)))*180/np.pi+180
l3faux= np.arctan2(np.imag(1/(s*T1+1)),np.real(1/(s*T1+1)))*180/np.pi

ftransferencia_aux = l1faux+l2faux+l3faux
plt.semilogx(f,ftransferencia_aux)

plt.semilogx(f,kf,linestyle=linea)
plt.semilogx(f,l1f,linestyle=linea)
plt.semilogx(f,l2f,linestyle=linea)
plt.semilogx(f,l3f,linestyle=linea)

# Parametros de los ejes

plt.legend(['A(jw)','R2/R1','sT1','1/(sT2+1)','1/(sT1+1)'],loc='best')
plt.grid(False)
plt.xlabel("Frecuencia [Hz]")
plt.ylabel("Fase [°]")
plt.yticks(np.arange(80,290,20))
plt.grid(True,linestyle='dashed')

# Se guarda la figura
#plt.savefig('fase solo.png', dpi=900)


##############################################################################


# DIAGRAMA DE AMPLITUD CON VALORES MEDIDOS

plt.figure()

# Valores de frecuencias usados
frecuencias=np.array([150,1500,4875,8250,11625,15000,150000])

# Amplitudes medidas
amplitudes=np.array([12,31,33,32,31,29,10])

# Se grafica la curva teórica
plt.semilogx(f,ftransferencia,color='gray',linestyle='dashed')

# Se grafican los puntos medidos y la curva que los une
plt.semilogx(frecuencias,amplitudes,color='red')
plt.scatter(frecuencias,amplitudes,color='red')

# Parámetros de los ejes
plt.xlabel("Frecuencia [Hz]")
plt.ylabel("Amplitud [db]")
plt.ylim(-20,60)
plt.yticks(np.arange(-20,60,20))
plt.grid(True,linestyle='dashed')
plt.legend(['Teórica','Simulada'],loc='best')

# Se guarda la figura
#plt.savefig('amplitud medida.png', dpi=900)

##############################################################################

# DIAGRAMA DE FASE CON VALORES MEDIDOS

plt.figure()

# Valores de fase medidos
fase_medida=np.array([273,220,189,150.6,135.8,127,94])

plt.semilogx(f,ftransferencia_aux,color='gray',linestyle='dashed')

# Se grafican los puntos medidos y la curva que los une
plt.semilogx(frecuencias,fase_medida,color='red')
plt.scatter(frecuencias,fase_medida,color='red')

# Parámetros de los ejes
plt.grid(True,linestyle='dashed')
plt.xlabel("Frecuencia [Hz]")
plt.ylabel("Fase [°]")
plt.yticks(np.arange(80,290,20))
plt.legend(['Teórica','Simulada'],loc='best')

# Se guarda la figura
#plt.savefig('fase medida.png', dpi=900)

plt.show()
