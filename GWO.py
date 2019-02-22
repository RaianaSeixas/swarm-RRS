"""GWO - Gray Wolf Optimization

O vetor X eh otimizado com X1, X2 e X3 associado as classes alfa, beta e delta

O vetor a_k decai linearmente 

A matriz A_kp vai de para zero (o que gera um espiral de aproximacao)
...
It's a beautiful day 

Don't let it get away 

It's a beautiful day
...
"""
import numpy as np

###################### Main
'''
import Function
#Fun=Function.Schwefel
#Fun=Function.Rosenbrock
Fun=Function.Shubert

NPAR=200 #Lobos
ITE=50 #ITERACOES
PAR=2 #NUM DE PARAMETROS A SER OTIMIZADOS
MAX=[10,10] # MAXIMO DE CADA PARAMETRO
MIN=[-10,-10] # MINIMO DE CADA PARAMETRO
'''

'''
FOBJ gera vetorialmente os valores com a funcao objetivo escalar
em outras palavras gera para populacao o valor da funcao 
a ser otimizada
'''
def FOBJ(X,Fun):
    rows = X.shape[0]
    fobj=np.zeros(rows)
    for i in range(rows):
        fobj[i]=Fun(X[i,])
    return fobj

'''Enxame retorna a populacao aleatoria com todos valores entre MIN e MAX'''
def Enxame(PAR,NPAR,MAX,MIN):
    x=np.zeros((NPAR, len(MAX)))
    for j in range(len(MAX)):
        for i in range(NPAR):
            x[i,j]=MIN[j]+(MAX[j]-MIN[j])*np.random.random()
    return x

''' 
Fit ordena os vetores do que fornece MIN a MAX valor de FOBJ : 
        eh necessario para encontrar alfa, beta e delta (lobos)
'''
def FIT(X):
    fit=np.argsort(X)
    return fit

''' 
Matriz_AC 
  retorna matriz A decrescente q vai 2 a zero
  retorna matriz C
  A decrescente q vai 2 a zero
  C aleatoria q vai de 
'''
def Matriz_AC(a,PAR,NPAR):
  A=np.zeros((NPAR, PAR))
  C=np.zeros((NPAR, PAR))
  for j in range(PAR):
    for i in range(NPAR):
      A[i,j]=a*(2*np.random.random()-1)
      C[i,j]=2*np.random.random()
  return A,C

# retorna quem sao os lobos alfa, beta e delta
def Alfa_Beta_Delta(x,Fun):
  ycal=FOBJ(x,Fun)
  Ind=FIT(ycal) # ajusta para encontrar o indice dos os lobos alfa, beta e delta
  Alfa=x[Ind[0],]
  Beta=x[Ind[1],]
  Delta=x[Ind[2],]
  return Alfa,Beta,Delta

# atualiza a matriz de populacoes
def New_X(k,ITE,PAR,NPAR,Alfa,Beta,Delta,X,MAX,MIN):
  a=2*(k-ITE)/(1-ITE) # parametro que varia de 2 a zero linermente: gera espiral
  A1,C1=Matriz_AC(a,PAR,NPAR)# matriz da espiral e matrix aletoria range dobro
  A2,C2=Matriz_AC(a,PAR,NPAR) # idem A1,C1
  A3,C3=Matriz_AC(a,PAR,NPAR) # idem A1,C1
  X1=np.zeros((NPAR, PAR)) # sera utilizado com base no alfa
  X2=np.zeros((NPAR, PAR)) # sera utilizado com base no beta
  X3=np.zeros((NPAR, PAR)) # sera utilizado com base no delta
  for j in range(PAR):
    for i in range(NPAR):
      D1=abs(Alfa[j]*C1[i,j]-X[i,j])
      D2=abs(Beta[j]*C2[i,j]-X[i,j])
      D3=abs(Delta[j]*C3[i,j]-X[i,j])
      X1=Alfa[j]-A1[i,j]*D1
      X2=Beta[j]-A2[i,j]*D2
      X3=Delta[j]-A3[i,j]*D3
      X[i,j]=(X1+X2+X3)/3  # posicao provavel da presa q cada lobo enxerga
   
      if(X[i,j]> MAX[j]):
        X[i,j]=MAX[j]
      if(X[i,j]< MIN[j]):
        X[i,j]=MIN[j]
  return X

def GWO(ITE,PAR,NPAR,MAX,MIN,Fun): # realiza todas interacoes do GWO
  k=1 #contador de iteracoes
  x=Enxame(PAR,NPAR,MAX,MIN) # inicializa lobos
  Alfa,Beta,Delta=Alfa_Beta_Delta(x,Fun) #encontra Alfa,Beta e Delta (lobos)
  while(k<=ITE):
    x=New_X(k,ITE,PAR,NPAR,Alfa,Beta,Delta,x,MAX,MIN) # atualiza lobos
    k=k+1 # atualiza iteracoes
    Alfa,Beta,Delta=Alfa_Beta_Delta(x,Fun) # atualiza alfa,beta e delta...
    
  FOBEST=Fun(Alfa)
  y=FOBJ(x,Fun)
  return Alfa,FOBEST,x,y

'''
###################### Main parte 2

Alfa,ycal,x=GWO(ITE,PAR,NPAR,MAX,MIN,Fun)
  
print("Lobos=",NPAR," Iteracoes=",ITE,"   x=",Alfa,"fobj=",ycal,"\n")
'''