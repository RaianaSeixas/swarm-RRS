# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 00:01:34 2017

@author: raiana
"""
import numpy as np

'''Rosembrock Function'''
def Rosenbrock(x):
    fun=0
    a=1.0
    b=100.0
    fun = (a-x[0])**2 + b*(x[1]-x[0]**2)**2
    return fun


#Rosembrock_domain=[-30,30]
# Global Minimum: 0

'''Schubert Function'''

def Shubert(x):
    n=1
    sum1=0
    sum2=0
    for n in range(1,6):
        new1=(n*np.cos((n+1)*x[0]+n))
        new2=(n*np.cos((n+1)*x[1]+n))
        sum1=sum1+new1
        sum2=sum2+new2
    return (sum1*sum2)

# Domain: xi ∈ [-5.12, 5.12] ou [-10,10]
# Global Minimum: -186.7309
 
'''Schwefel Function'''

def Schwefel(x):
    
    summ=0
    for i in range(len(x)):
        new=x[i]*np.sin((np.abs(x[i]))**0.5)
        summ=summ+new
#        print(summ)
    return (418.9829*len(x)-summ)    

        
# n represents the number of dimensions and x_i \in [-500, 500] for i=1,...,n.        
# Global optimum: f(x_i) = 0 for x_i = 420.968746 for i=1,...,n        

