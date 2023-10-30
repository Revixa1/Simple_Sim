import numpy as np
from icecream import ic


class Dipole:


    def __init__(self,mx,my,mz,x,y,z,kl=0,kt=0,kv=0,mu0=1e-7):
        self.mu0=mu0
        self.set_magMoment(mx,my,mz)
        self.set_Dipole_pos([x,y,z])
        self.set_sensorVector()
        self.set_inducedMoment(kl,kt,kv)
        

    def set_sensorVector(self,sensorVector=[0,0,1]):
        #ic(sensorVector)
        self.r_vector=np.array(sensorVector).reshape(3,1)
        #ic(self.r_vector)
        self.r_scalar=np.linalg.norm(self.r_vector)
        self.r_unit=self.r_vector/ np.linalg.norm(self.r_vector)
        #ic(self.r_unit.shape)

    def set_magMoment(self,mx,my,mz):
        self.m=np.array([mx,my,mz]).reshape(3,1)

    def set_inducedMoment(self,kl,kt,kv):
        self.kl=kl
        self.kt=kt
        self.kv=kv
    

    def get_vB(self):
        self.B=  (self.mu0/(4*np.pi) * (3 *((self.m.reshape(1,3).dot(self.r_vector)).dot((self.r_unit-self.m).reshape(1,3)))/self.r_scalar**3)).reshape(3,1)
        return self.B
        
    def get_sB(self):
        self.sB=np.linalg.norm(self.get_vB())
        return self.sB

    def set_Dipole_pos(self,posvecteur):
        self.dipole_position=np.array(posvecteur).reshape(3,1)

    def get_Dipole_pos(self):
        return self.dipole_position

    def get_C(self):
        #ic(self.m.shape)
        self.C1=    (3*self.r_vector[0]*(self.m.reshape(1,3).dot(self.r_vector))/(self.r_scalar**5)) - (self.m[0]/(self.r_scalar**3))
        self.C2=    (3*self.r_vector[1]*(self.m.reshape(1,3).dot(self.r_vector))/(self.r_scalar**5)) - (self.m[1]/(self.r_scalar**3))
        self.C3=    (3*self.r_vector[2]*(self.m.reshape(1,3).dot(self.r_vector))/(self.r_scalar**5)) - (self.m[2]/(self.r_scalar**3))
        
        self.C4=    (3*self.r_vector[0]**2*self.kl/self.r_scalar**5)-(self.kl/self.r_scalar**3)
        self.C5=    (3*self.r_vector[0]*self.r_vector[1]*(self.kl+self.kt)/self.r_scalar**5)
        self.C6=    (3*self.r_vector[0]*self.r_vector[2]*(self.kl+self.kv)/self.r_scalar**5)
        self.C7=    (3*self.r_vector[1]**2*self.kt/self.r_scalar**5)-(self.kt/self.r_scalar**3)
        self.C8=    (3*self.r_vector[1]*self.r_vector[2]*(self.kt+self.kv)/self.r_scalar**5)
        self.C9=    (3*self.r_vector[2]**2*self.kv/self.r_scalar**5)-(self.kv/self.r_scalar**3)
    
