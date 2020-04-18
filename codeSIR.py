#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 14:48:58 2020

@author: jmurray
"""
# uses the euler method to numerically solve coupled first order ODE's
# for the SIR ODE model using the euler method
# S = Susceptible, I = Infected, R = Removed (recovered/deceased/immune)
# dS/dt = -alpha*S*I, dI/dt = alpha*S*I-beta*I, dR/dt=beta*I
# where S+I+R=constant=total population

# importing packages
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import math

#initializing parameters
# time step
dt = 0.01
# infection rate (probability per time step individual becomes infected)
alpha = 0.02
# remove rate (probability per time step individual is removed)
beta = 0.3
# total population
totpop = 100
# total time
tottime = 20
# initial percent susceptible
ps = 0.98
# initial percent infected
pi = 0.02
# chose to start with all infected or susceptible (assume no natural immunity)

niter = int(math.ceil(tottime/dt))
t = np.arange(0, tottime, dt)   
s = np.zeros(niter)
i = np.zeros(niter)
 
s[0] = ps*totpop
i[0] = pi*totpop

for j in range(niter-1):
    dsdt=-alpha*s[j]*i[j]
    didt=alpha*s[j]*i[j]-beta*i[j]
    s[j+1] = s[j] + dt*dsdt  
    i[j+1] = i[j] + dt*didt  
    
r = totpop-s-i

# plotting
fig = plt.figure()
plt.plot(t, s, 'k o')
plt.plot(t, i, 'r +')
plt.plot(t, r, 'b *')
plt.plot(t, r+s+i, 'g')
plt.title('simple SIR ode model')
plt.xlabel('time')
plt.ylabel('populations')
plt.show()
