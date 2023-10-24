import numpy as np
from icecream import ic


class Dipole:


    def __init__(self,mx,my,mz,x,y,z,mu0=10e-4):
        self.mu0=mu0
        self.set_magMoment(mx,my,mz)
        self.set_sensorVector()
        self.set_Dipole_pos([x,y,z])
        

    def set_sensorVector(self,sensorVector=[0,0,0]):
        #ic(sensorVector)
        self.r_vector=np.array(sensorVector).reshape(3,1)
        #ic(self.r_vector)
        self.r_scalar=np.linalg.norm(self.r_vector)
        self.r_unit=self.r_vector/ np.linalg.norm(self.r_vector)

    def set_magMoment(self,mx,my,mz):
        self.m=np.array([mx,my,mz]).reshape(1,3)

    def get_vB(self):
        self.B=  (self.mu0/(4*np.pi) * (3 *((self.m.dot(self.r_vector)).dot(self.r_unit.reshape(1,3))-self.m)/self.r_scalar**3)).reshape(3,1)
        return self.B
        
    def get_sB(self):
        self.sB=np.linalg.norm(self.get_vB())
        return self.sB

    def set_Dipole_pos(self,posvecteur):
        self.dipole_position=np.array(posvecteur).reshape(3,1)

    def get_Dipole_pos(self):
        return self.dipole_position
    

    
