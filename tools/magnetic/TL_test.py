import numpy as np
from icecream import ic
import matplotlib.pyplot as plt






def TranslationMatrix(thetax=0,thetay=0,thetaz=0,x=0,y=0,z=0):

    Rotz = lambda theta: np.array([[np.cos(theta),-np.sin(theta),0],
                                             [np.sin(theta),np.cos(theta),0],
                                             [0,           0,             1]])
       
       
    Roty = lambda theta: np.array([[np.cos(theta),0,-np.sin(theta)],
                                             [0,          1,           0],
                                             [np.sin(theta),0,np.cos(theta)]])
       
    Rotx= lambda theta: np.array([[1,          0,                0],
                                         [0,np.cos(theta),-np.sin(theta)],
                                         [0,np.sin(theta),np.cos(theta)]])                         
   
    
    aRb=(Rotz(thetaz).dot(Roty(thetay))).dot(Rotx(thetax))
    ic(aRb)
    
    
    
                    
    aTb=aRb
    ic(aTb)
    trans=np.array([x,y,z]).reshape(3,1)
    ic(trans.shape)
    aTb=np.concatenate((aTb,trans),axis=1) 
    ic(aTb) 
    trans=np.array([0,0,0,1]).reshape(1,4)
    ic(trans)
    aTb=np.concatenate((aTb,trans),axis=0)
                        
    
    ic(aTb)

    return aTb

def Transformation(aTb,v_b):
    
    v_b= v_b.reshape(3,1)
    v_b= np.concatenate((v_b,np.array([1]).reshape(1,1)),axis=0)
    ic(v_b)
    v_a= aTb.dot(v_b)
    ic(v_a)
    v_a=v_a[0:3]
    return v_a



fig=plt.figure()
ax = fig.add_subplot(111,projection="3d")


plt.ion()


for thetaz in np.arange(0,2*np.pi,0.01):

    
    ax.set(xlim=(-1, 1), ylim=(-1, 1))
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    worldTheli=TranslationMatrix(thetaz,thetaz,thetaz,np.cos(thetaz),0,np.sin(thetaz))


    v_Helidipole_heli=np.array([1,0,0]).reshape(3,1)
    ic(v_Helidipole_heli )
    v_Helidipole_world= Transformation(worldTheli,v_Helidipole_heli )
    ic(v_Helidipole_world)
    
    v_Helisensor_heli=np.array([0,0,0]).reshape(3,1)
    v_Helisensor_world=Transformation(worldTheli,v_Helisensor_heli )
    
    Points=np.concatenate((v_Helisensor_world,v_Helidipole_world),axis=1)
    ic(Points)
    ic(Points[0,:])
    # Plot
    
    #ax.scatter(Points[0,:], Points[1,:], Points[2,:])
    
    ax.plot(Points[0,:], Points[1,:], zs=Points[2,:])
    plt.show()
    
    plt.pause(0.01)
    #plt.cla()
    

plt.ioff()
plt.show()









