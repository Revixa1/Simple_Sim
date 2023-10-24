import numpy as np
from icecream import ic

def TranslationMatrix(thetax=0,thetay=0,thetaz=0,x=0,y=0,z=0):

    Rotz = lambda theta: np.array(          [[np.cos(theta),-np.sin(theta),0],
                                             [np.sin(theta),np.cos(theta), 0],
                                             [0,           0,             1]])
       
       
    Roty = lambda theta: np.array(          [[np.cos(theta),0,-np.sin(theta)],
                                             [0,            1,             0],
                                             [np.sin(theta),0,np.cos(theta)]])
       
    Rotx= lambda theta: np.array(       [[1,          0,               0],
                                         [0,np.cos(theta),-np.sin(theta)],
                                         [0,np.sin(theta),np.cos(theta)]])                         
   
    
    aRb=(Rotz(thetaz).dot(Roty(thetay))).dot(Rotx(thetax))
    #ic(aRb)
    
    
    
                    
    aTb=aRb
    #ic(aTb)
    trans=np.array([x,y,z]).reshape(3,1)
    #ic(trans.shape)
    aTb=np.concatenate((aTb,trans),axis=1) 
    #ic(aTb) 
    trans=np.array([0,0,0,1]).reshape(1,4)
    #ic(trans)
    aTb=np.concatenate((aTb,trans),axis=0)
                        
    
    #ic(aTb)

    return aTb

def Transformation(aTb,v_b):
    
    v_b= v_b.reshape(3,1)
    v_b= np.concatenate((v_b,np.array([1]).reshape(1,1)),axis=0)
    #ic(v_b)
    v_a= aTb.dot(v_b)
    #ic(v_a)
    v_a=np.array(v_a[0:3]).reshape(3,1)
    return v_a
