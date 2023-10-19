import numpy as np
from icecream import ic
import matplotlib.pyplot as plt
from matplotlib import cm



rx,ry,rz= 0,0,0.3
mu0=10e-4

lowdist,highdist,ddist=-6,6,0.5
datapoints=int((highdist-lowdist)/ddist)

pausetime=0.01


fig=plt.figure()
ax = fig.add_subplot(111,projection='3d')
plt.ion()

for rz in np.arange(lowdist,highdist,ddist):

    DX=np.empty((1,0),dtype=float)
    DY=np.empty((1,0),dtype=float)
    DZ=np.empty((0,0),dtype=float)
    ic(DZ.shape)
    
    
    
    
    
    X = np.arange(lowdist,highdist,ddist)
    Y = np.arange(lowdist,highdist,ddist)
    X, Y = np.meshgrid(X, Y)
    i=0
    
    for rx in np.arange(lowdist,highdist,ddist):
        loop_DZ=np.empty((0),dtype=float)
        
        for ry in np.arange(lowdist,highdist,ddist):
    
                r_vector=np.array([rx,ry,rz]).reshape(3,1)
                r_scalar=np.linalg.norm(r_vector)
                r_unit=r_vector/ np.linalg.norm(r_vector)
                
                m=np.array([0,0.5,-0.5]).reshape(1,3)
                
                B=  (mu0/(4*np.pi) * (3 *((m.dot(r_vector))-m)/r_scalar**3)).reshape(3,1)
                #ic(B)
                
                DX=np.append(DX,rx)
                DY=np.append(DY,ry)
                
                loop_DZ=np.append(loop_DZ,np.linalg.norm(B))
                ic(loop_DZ.shape)
                #ax.plot(rx,ry,zs=B[2,:],marker='*',color='b')
                #ax.plot(rx,ry,np.linalg.norm(B),marker='o',color='b')
        DZ=np.append(DZ,loop_DZ)
        ic(DZ)
        i=i+1

    ic(datapoints)    
    DZ=DZ.reshape(i,datapoints) 
    
    ic(DZ.shape)  
    ax.plot_surface(X,Y,DZ,cmap=cm.coolwarm,linewidth=0, antialiased=False)
    plt.show()
    plt.pause(pausetime)
    plt.cla()
