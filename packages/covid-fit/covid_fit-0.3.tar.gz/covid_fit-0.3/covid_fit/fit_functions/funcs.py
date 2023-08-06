#!/usr/local/bin/python3

import numpy as np

def gompertz_func_fit(x,a,b,c):
    return c*np.exp(-a*np.exp(-b*x)) 

def gompertz_func(x, pars):
    a = pars[0]
    b = pars[1]
    c = pars[2]
    return c*np.exp(-a*np.exp(-b*x)) 
################################################
###############################################
##############################################
def gompertz_der_func_fit(x,a,b,c):
    return a*b*c*np.exp(-a*np.exp(-b*x) - b*x) 

def gompertz_der_func(x, pars):
    a = pars[0]
    b = pars[1]
    c = pars[2]
    return a*b*c*np.exp(-a*np.exp(-b*x) - b*x) 
################################################
###############################################
##############################################
def logistic_func_fit(x,N,xmax,b):
    return N/(1+np.exp(-(x-xmax)/b))

def logistic_func(x, pars):
    N = pars[0]
    xmax = pars[1]
    b = pars[2]
    return N/(1+np.exp(-(x-xmax)/b))
################################################
###############################################
##############################################
def logistic_der_func_fit(x,N,xmax,b):
    return ((N/b)*np.exp(-(x-xmax)/b))/((1+np.exp(-(x-xmax)/b))**2)

def logistic_der_func(x, pars):
    N = pars[0]
    xmax = pars[1]
    b = pars[2]
    return ((N/b)*np.exp(-(x-xmax)/b))/((1+np.exp(-(x-xmax)/b))**2)
################################################
###############################################
##############################################

def logistic_gen_func_fit(x,a,m,n,tau):
    return a*( (1+m*np.exp(-x/tau))/ (1+n*np.exp(-x/tau)) )

def logistic_gen_func(x, pars):
    a = pars[0]
    m = pars[1]
    n = pars[2]
    tau = pars[3]
    return a*( (1+m*np.exp(-x/tau))/ (1+n*np.exp(-x/tau)) )

def logistic_gen_der_func_fit(x,a,m,n,tau):
    return (a/(1+n*np.exp(-x/tau))**2) * \
                    ( (n/tau)*np.exp(-x/tau) - (m/tau)*np.exp(-x/tau) )

def logistic_gen_der_func(x, pars):
    a = pars[0]
    m = pars[1]
    n = pars[2]
    tau = pars[3]
    return (a/(1+n*np.exp(-x/tau))**2) * \
                    ( (n/tau)*np.exp(-x/tau) - (m/tau)*np.exp(-x/tau) )
################################################
###############################################
##############################################
def lin_func_fit(x, a,b):
    return a + b * x

def lin_func(x, pars):
    intercept = pars[0]
    coeff = pars[1]
    return intercept + coeff * x
################################################
###############################################
##############################################
def exp_func_fit(x, a,b):
    return a*np.exp(b*x)

def exp_func(x, pars):
    a = pars[0]
    b = pars[1]
    return a*np.exp(b*x)
################################################
###############################################
##############################################
map_func = {'linear':{'get_fit':lin_func_fit,
                     'get_values':lin_func,
                     'p0':None},
            'exponential':{'get_fit':exp_func_fit,
                     'get_values':exp_func,
                     'p0':None},
            
            'gompertz':{'get_fit':gompertz_func_fit,
                     'get_values':gompertz_func,
                       'p0':[10,1,100]},
            'gompertz_der':{'get_fit':gompertz_der_func_fit,
                     'get_values':gompertz_der_func,
                       'p0':[10,1,100]},
            
            'logistic':{'get_fit':logistic_func_fit,
                     'get_values':logistic_func,
                       'p0':None}, 
            'logistic_der':{'get_fit':logistic_der_func_fit,
                     'get_values':logistic_der_func,
                       'p0':None}, 
            
            'logistic_gen':{'get_fit':logistic_gen_func_fit,
                     'get_values':logistic_gen_func,
                       'p0':None}, 
            'logistic_gen_der':{'get_fit':logistic_gen_der_func_fit,
                     'get_values':logistic_gen_der_func,
                       'p0':None}, 
                 }