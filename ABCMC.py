# -*- coding: utf-8 -*-
"""ABCOptim_jan_02_2019.ipynb

Original file is located at
    https://colab.research.google.com/github/ucfilho/Codigos_Teste/blob/master/ABCOptim_jan_02_2019.ipynb
"""

import numpy as np
from random import randint


###################### Main
'''
import Function
Fun=M_Function.Rosenbrock

NPAR=30 #PARTICULAS
ITE=300 #ITERACOES
PAR=2 #NUM DE PARAMETROS A SER OTIMIZADOS
MAX=[2,2] # MAXIMO DE CADA PARAMETRO
MIN=[-2,-2] # MINIMO DE CADA PARAMETRO
ntrail=25 #numero de buscas ate abandonar uma fonte de alimento
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
Fitness gera vetorialmente os valores com a funcao fitness
equivale a quantidade de nectar da fonte
'''
def FIT(X,Fun):
    rows = X.shape[0]
    fit=np.zeros(rows)
    fit=np.copy(FOBJ(X,Fun))
    for i in range(rows):
        if(fit[i]>=0):
            fit[i]=1/(fit[i]+1)
        else:
            fit[i]=1+abs(fit[i])
    return fit

'''
probablilidade usada para roleta q atualizacao das onlookers 
semelhante ao genetico
'''

def PROB(x,Fun):
    rows=x.shape[0]
    fit=np.zeros(rows)
    prob=np.zeros(rows)
    fit=FIT(x,Fun)
    soma=np.sum(fit)
    
    for i in range(rows):
        prob[i] = fit[i]/soma

    return prob

'''
Obtem a melhor escolha greedy search
'''
def GetBest(x,xbest,Fun):
    ycal=FOBJ(x,Fun)
    best=np.argmin(ycal)
    yref=Fun(xbest)
    if(yref<ycal[best]):
        GBEST=xbest
    else:
        GBEST=x[best,]
    return GBEST

'''
employed bee phase
'''
def EmployedBee(xo,x,MAX,MIN,Fun) :
    NPAR = xo.shape[0]
    PAR= xo.shape[1]
    V=np.zeros((NPAR, len(MAX)))

    for j in range(PAR):
        for i in range(NPAR):
            fi=np.random.uniform(low=-1.0, high=1.0, size=None)
            rd=randint(0, (NPAR-1))
            V[i,j]=xo[i,j]+(xo[i,j] -x[rd,j])*fi # candidata a solucao
            if (V[i,j]>MAX[j]):
              V[i,j]=np.copy(MAX[j]) # restringe a busca para o intervalo
            if (V[i,j]<MIN[j]):
              V[i,j]=np.copy(MIN[j]) # restringe a busca para o intervalo
              
    YCAL=FOBJ(xo,Fun)
    YV=FOBJ(V,Fun)
    for i in range(NPAR):
        if(YV[i]<YCAL[i]):
            x[i,]=np.copy(V[i,])

    return x

'''
onlooker bee phase
'''
def OnlookerBee(xo,x,MAX,MIN,Fun): #OnlookerBee(xo,x_Employed)
    NPAR = xo.shape[0]
    #PAR = xo.shape[1]
    prob=PROB(x,Fun)
    #best=np.argmax(prob)
    
    for i in range(NPAR):
      rd=randint(0, (NPAR-1))
      #rd=best
      if(prob[rd] > prob[i]):
        fi=np.random.uniform(low=-1.0, high=1.0, size=None)
        Xmi=xo[i,]+fi*(xo[i,]-x[rd,])
        xo[i,]=np.copy(Xmi)
    xo=np.clip(xo,MAX,MIN)
    
    return xo

'''
scout bee phase
'''
#def ScoutBee(trial,x,ntrail,MAX,MIN):
def ScoutBee(x,MAX,MIN):
    PAR = x.shape[0]
    NPAR = x.shape[1]
    for i in range(PAR):
        for j in range(NPAR):
            x[i,j]=MIN[j]+(MAX[j]-MIN[j])*np.random.random()
    return x

'''
Metodo que alterna e coordena o uso employers,onlooker, scout bees
e greedy search

'''
def ABCOPtim(ITE,PAR,ntrail,NPAR,MAX,MIN,Fun):

    trial=1 # inicializa contador p abandonar fonte de alimento
    xbest=Enxame(PAR,1,MAX,MIN)[0,] #inicializa xbest
    xo=Enxame(PAR,NPAR,MAX,MIN) # inicializa employed bee-parte 1
    vbest_old=Fun(xbest)
    vbest_new=Fun(xbest)
    
    for i in range(ITE):
      x=Enxame(PAR,NPAR,MAX,MIN) # inicializa employed bee-parte 1
      if(vbest_new==vbest_old):
        trial=trial+1
      if(trial==ntrail):
        xo=Enxame(PAR,NPAR,MAX,MIN) # abandona a fonte de alimento antiga
        trial=0
      x_Employed=EmployedBee(xo,x,MAX,MIN,Fun)
      xbest=GetBest(x_Employed,xbest,Fun)
      vbest_new=Fun(xbest)
      xo=Enxame(PAR,NPAR,MAX,MIN) # inicializa OnlookerBee
      x_Onlooker=OnlookerBee(xo,x_Employed,MAX,MIN,Fun)
      xbest=GetBest(x_Onlooker,xbest,Fun)
      x_Scout=Enxame(PAR,NPAR,MAX,MIN) # inicializa ScoutBee ( a rigor so esta linha basta)
      xbest=GetBest(x_Scout,xbest,Fun)
      
      FOBEST=Fun(xbest)
      y=FOBJ(x_Employed,Fun)
    return xbest,FOBEST,x_Employed,y


################### Main parte 2
'''
for i in range(6):
    print("resolucao",i+1," ")
    xbest=ABCOPtim(Fun,ITE,PAR,ntrail,NPAR,MAX,MIN)
    print("vetor",xbest,"funcao", Fun(xbest),"\n")
'''    
