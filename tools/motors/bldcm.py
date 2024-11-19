import numpy as np
import matplotlib.pyplot as plt
from icecream import ic


#bldc motor model from https://core.ac.uk/download/pdf/53188902.pdf
#
# |Vas| |Rs 0 0||ia| |Laa Lab Lac||d_ia| |ea|
# |Vbs|=|0 Rs 0||ib|+|Lba Lbb Lbc||d_ib|+|eb|
# |Vcs| |0 0 Rs||ic| |Lca Lcb Lcc||d_ic| |ec|
#
# V>=RM*I>+LM*dI>+E>
# (RM for Resistance matrix and V> for Voltage Vector)
# |ea|       |f_as(theta_r)|
# |eb|=wm*hm*|f_bs(theta_r)|
# |ec|       |f_cs(theta_r)|
#
# E>=wm*hm*F_theta>
#
# Simplifications:
#    
#    |L-M  0    0 |
# LM=| 0  L-M   0 |
#    | 0   0   L-M|
#
# Vxs:Input voltage by phases (Voltage)
# ix:current by phases (Amperes)
# Lxx:inductance of a phase
# Lxy:inductance between 2 phases
# ex:backEMF(voltage)
# wm:motor rotational speed (rad/s)
# hm:flux linkage constant
# theta_r: motor position(rad)
# f_xs: input voltage shape (ex:trapezoidal)



RM=lambda R:   np.array([[R,0,0],[0,R,0],[0,0,R]])
LM=lambda L,M: np.array([[L-M,0,0],[0,L-M,0],[0,0,L-M]])


f_s=lambda theta,psy: np.sin(theta-psy)
f_as=lambda theta: f_s(theta,0)
f_bs=lambda theta: f_s(theta,np.radians(120))
f_cs=lambda theta: f_s(theta,np.radians(-120))

V_s=lambda f,amp,t,psy: amp*np.sin(f*2*np.pi*t-psy)+amp
V_as=lambda f,amp,t:V_s(f,amp,t,0)
V_bs=lambda f,amp,t:V_s(f,amp,t,np.radians(120))
V_cs=lambda f,amp,t:V_s(f,amp,t,np.radians(-120))

u=lambda f,amp,t,Tl: np.array([V_as(f,amp,t),V_bs(f,amp,t),V_cs(f,amp,t),Tl,0])
e=lambda wm,hm,theta: wm*hm*np.array([f_as(theta),f_bs(theta),f_cs(theta),0,0])

V_vec=lambda amp,t: np.array([V_bs(amp,t),V_as(amp,t),V_cs(amp,t)])

#State-Space Model: dx=Ax+Bu+C_1e then y=C_2x+(Du->0)
#   | ia  |    |Vas|
#   | ib  |    |Vbs|   |ea|
# x=| ic  |  u=|Vcs| e=|eb|
#   | wm  |    |Tl |   |ec|
#   |theta|    
#


A_base=lambda R,L,M,J,P,B:       np.array([[-R/(L-M),0,0,0,0],[0,-R/(L-M),0,0,0],[0,0,-R/(L-M),0,0],[0,0,0,-B/J,0],[0,0,0,P/2,0]])
A_nonlinear=lambda R,L,M,hm,J,theta: np.array([[0,0,0,-hm/J*f_as(theta),0],[0,0,0,-hm/J*f_bs(theta),0],[0,0,0,-hm/J*f_cs(theta),0],[hm/J*f_as(theta),hm/J*f_bs(theta),hm/J*f_cs(theta),0,0],[0,0,0,0,0]])


B_base=lambda L,M: np.array([[1/(L-M),0,0,0,0],[0,1/(L-M),0,0,0],[0,0,1/(L-M),0,0],[0,0,0,1/(L-M),0],[0,0,0,0,0]])
C_1=lambda L,M: np.array([[-1/(L-M),0,0,0,0],[0,-1/(L-M),0,0,0],[0,0,-1/(L-M),0,0],[0,0,0,0,0],[0,0,0,0,0]])

#C_2=np.array([[1,0,0,0,0],[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1]])


X=np.array([0,0,0,0,0])
dX=np.array([0,0,0,0,0])
Tfin=10
Nbstep=100000
Tstep=Tfin/Nbstep
time=np.linspace(0,Tfin,Nbstep)
t_before=0


Rm=0.7
Lm=0.00272
Mm=0.0015
Jm=0.000284
Pm=4
hm=0.105
amp=126
Bm=0.00001
freqin=lambda t: -60*np.exp(-t/(Tfin))+60
Tl=1

A_lin=A_base(Rm,Lm,Mm,Jm,Pm,Bm)
Bs=B_base(Lm,Mm)
C_in=C_1(Lm,Mm)
#C=C_2




plt.ion()
fig=plt.figure()
ax=fig.add_subplot(311)
bx=fig.add_subplot(312)
cx=fig.add_subplot(313)


time_record=[]
X_record=[[],[],[],[],[]]
V_record=[[],[],[]]
for t in time:
    
    dX=(A_lin+A_nonlinear(Rm,Lm,Mm,hm,Jm,X[4])).dot(X)+Bs.dot(u(freqin(t),amp,t,Tl))+C_in.dot(e(X[3],hm,X[4]))
    X=X+dX*(Tstep)
    t_before=t
    #ic(t)
    time_record.append(t)

    V_record[0].append(u(freqin(t),amp,t,Tl)[0])
    V_record[1].append(u(freqin(t),amp,t,Tl)[1])
    V_record[2].append(u(freqin(t),amp,t,Tl)[2])
    X_record[0].append(X[0])
    X_record[1].append(X[1])
    X_record[2].append(X[2])
    X_record[3].append(X[3])
    X_record[4].append(X[4])
    #ic(X_record)
    
    #plt.pause(0.001)
    
ax.plot(time_record,X_record[0],'r')
ax.plot(time_record,X_record[1],'b')
ax.plot(time_record,X_record[2],'g')
bx.plot(time_record,X_record[3],'r')
#bx.plot(time_record,X_record[4],'b')
cx.plot(time_record,V_record[0],'r')
cx.plot(time_record,V_record[1],'b')
cx.plot(time_record,V_record[2],'g')
while(1):
    plt.pause(0.001)
