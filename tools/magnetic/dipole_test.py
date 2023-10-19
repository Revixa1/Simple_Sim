import numpy as np
from icecream import ic
import matplotlib.pyplot as plt
from matplotlib import cm



rx,ry,rz= 0,0,0.3
mu0=10e-4

lowdist,highdist,ddist=-3,3,0.1
datapoints=int((highdist-lowdist)/ddist)

pausetime=0.001


fig=plt.figure()
ax = fig.add_subplot(111,projection='3d')

fig2=plt.figure()
bx= fig2.add_subplot(3,1,1)
by=fig2.add_subplot(3,1,2)
bz=fig2.add_subplot(3,1,3)

plt.ion()

for rz in np.arange(lowdist,highdist,ddist):

    DX=np.empty((0,0),dtype=float)
    DY=np.empty((0,0),dtype=float)
    BX=np.empty((0,0),dtype=float)
    BY=np.empty((0,0),dtype=float)
    BZ=np.empty((0,0),dtype=float)
    DZ=np.empty((0,0),dtype=float)
    
    #ic(DZ.shape)
    
    
    
    
    
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
                
                m=np.array([0,0,1]).reshape(1,3)
                
                B=  (mu0/(4*np.pi) * (3 *((m.dot(r_vector)).dot(r_unit.reshape(1,3))-m)/r_scalar**3)).reshape(3,1)
                #ic(B)
                
                DX=np.append(DX,rx)
                DY=np.append(DY,ry)
                BX=np.append(BX,B[0])
                BY=np.append(BY,B[1])
                BZ=np.append(BZ,B[2])

                #bx.plot(DY,BX)
                #by.plot(DY,BY)
                #bz.plot(DY,BZ)
                #plt.pause(pausetime)
                
                loop_DZ=np.append(loop_DZ,np.linalg.norm(B))


               
                #ic(loop_DZ.shape)
                #ax.plot(rx,ry,zs=B[2,:],marker='*',color='b')
                #ax.plot(rx,ry,np.linalg.norm(B),marker='o',color='b')


        bx.set(ylabel="Bx(T)")
        by.set(ylabel="By(T)")
        bz.set(ylabel="Bz(T)",xlabel="posY(m)")
        
        
        bx.plot(DY,BX)
        by.plot(DY,BY)
        bz.plot(DY,BZ)
        plt.pause(pausetime)
        bx.clear()
        by.clear()
        bz.clear()
        BX=np.empty((0,0),dtype=float)
        BY=np.empty((0,0),dtype=float)
        BZ=np.empty((0,0),dtype=float)
        DY=np.empty((0,0),dtype=float)


        DZ=np.append(DZ,loop_DZ)
        #ic(DZ)
        i=i+1

    #ic(datapoints)    
    DZ=DZ.reshape(i,datapoints) 
    
    #ic(DZ.shape)
    ax.clear()
    ax.plot_surface(X,Y,DZ,cmap=cm.viridis,linewidth=0, antialiased=False)
    plt.show()
    plt.pause(pausetime)
    
