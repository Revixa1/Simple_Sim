#!/usr/bin/env python3.11

import matplotlib.pyplot as plt
import numpy as np
from icecream import ic

phasor = lambda t,phi: np.cos(2*np.pi*t-phi)
ic(phasor(0,0))
phaseA= lambda t:phasor(t,0)
phaseB= lambda t:phasor(t,np.deg2rad(120))
phaseC= lambda t:phasor(t,np.deg2rad(240))

alpha=lambda t:(2/3)*(phaseA(t)-phaseB(t)/2-phaseC(t)/2)
beta=lambda t:(2/3)*(phaseB(t)*(np.sqrt(3)/2)+phaseC(t)*(-np.sqrt(3)/2))

M3ph=lambda t:np.array([[phaseA(t),0,0],[0,phaseB(t),0],[0,0,phaseC(t)]])
Tclark=2/3*np.array([[1,-(0.5),-(0.5)],[0,np.sqrt(3)/2,-np.sqrt(3)/2]])
ic(M3ph(0))

ic(phaseA(0))
fig=plt.figure()
fig2=plt.figure()

ax=fig.add_subplot(311)
bx=fig.add_subplot(312)
cx=fig2.add_subplot(111)


cx.set_xlim(-1,1)
cx.set_ylim(-1,1)
cx.set_aspect('equal', adjustable='box')

plt.ion()

time=np.arange(0,10,0.01)
t=[]
signalA=[]
signalB=[]
signalC=[]
signalAlpha=[]
signalBeta=[]


origin = np.array([[0, 0, 0],[0, 0, 0]])
originAdd=np.array([[0],[0]])

circle2 = plt.Circle((0, 0), 1, color='k', fill=False,linestyle='--')
cx.add_patch(circle2)

for i in time:
    
    if len(signalA)>100:
        t.pop(0)
        signalA.pop(0)
        signalB.pop(0)
        signalC.pop(0)
        signalAlpha.pop(0)
        signalBeta.pop(0)
    
    
    t.append(i)

    Data=Tclark.dot(M3ph(i))
    ic(Data)
    signalA.append(phaseA(i))
    signalB.append(phaseB(i))
    signalC.append(phaseC(i))
    signalAlpha.append(alpha(i))
    signalBeta.append(beta(i))
    ax.clear()
    bx.clear()
    cx.clear()
    bx.plot(t,signalAlpha)
    bx.plot(t,signalBeta)
    ax.plot(t,signalA)
    ax.plot(t,signalB)
    ax.plot(t,signalC)
    soa=np.array([[0,0,Data[0,0],Data[1,0]],[0,0,Data[0,1],Data[1,1]],[0,0,Data[0,2],Data[1,2]]])
    X,Y,U,V=zip(*soa)
    cx.quiver(*originAdd,alpha(i),beta(i),color='g', angles='xy', scale_units='xy', scale=1)
    cx.quiver(X,Y,U,V, angles='xy', scale_units='xy', scale=1)
  
    #cx.quiver(*originAdd,sum(Data[0,0:3]),sum(Data[1,0:3]),color='r', angles='xy', scale_units='xy', scale=1)
    cx.add_patch(circle2)
    plt.pause(0.0001)
    
    

ax.clear()
