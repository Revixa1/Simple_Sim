
'''
    This is a class to represent a solid frame(geometry) with dipoles inside of it.
    It can be used by it self to see what that frame's magnetic signature looks like.
    It can also be used with other frames to, perhaps simlulate a sensor in the real world.  

'''


import numpy as np
from icecream import ic
import ppigrf

import dipole
import geometry as geo
from datetime import datetime



class MagSignature:


    #init the magnetic signature
    def __init__(self,sensorpos):
        self.dipolelist = [] #initialise the list of dipoles for this magnetic signature
        self.set_SensorPosition(sensorpos) #set the sensors position in this frame
        self.set_TranslationMatrix() #initialise the transformation matrix
        self.setBe() #initialise the eath's magnetic field

    #method to load a spread sheet (csv format) of dipoles. this includes position, 
    def loadFromCSV(self,filename):
        pass

    #add a dipole to the signature
    def newDipole(self,dipole):
        self.dipolelist.append(dipole)

    #set the sensor vector to all dipoles
    def set_Sensor_Vector(self):
        for i in self.dipolelist:
            i.set_sensorVector(geo.Transformation(self.aTb,self.sensorpos-i.get_Dipole_pos()))

    
    #set the translation matrix 
    def set_TranslationMatrix(self,x=0,y=0,z=0,thetax=0,thetay=0,thetaz=0):
        self.aTb=geo.TranslationMatrix(thetax,thetay,thetaz,x,y,z)
        #ic(self.aTb)

    #get the scalar output from the sensor and the totalfield.
    def resB(self):
        phresB=0
        self.c1,self.c2,self.c3=0,0,0
        self.c4,self.c5,self.c6,self.c7,self.c8,self.c9=0,0,0,0,0,0
        for i in self.dipolelist:
            #ic(i.get_vB())
            phresB=phresB+i.get_vB()
            i.get_C()
            self.c1=self.c1+i.C1
            self.c2=self.c2+i.C2
            self.c3=self.c3+i.C3
            self.c4=self.c4+i.C4
            self.c5=self.c5+i.C5
            self.c6=self.c6+i.C6
            self.c7=self.c7+i.C7
            self.c8=self.c8+i.C8
            self.c9=self.c9+i.C9
            
            
        #ic(phresB)
        self.resultantB=phresB+self.Be
        self.res_sB=np.sqrt(self.resultantB.reshape(1,3).dot(self.resultantB))
        self.TFperm=self.c1*self.Be[0]/self.sBe+self.c2*self.Be[1]/self.sBe+self.c3*self.Be[2]/self.sBe
        self.TFind=self.c4*self.Be[0]**2/self.sBe+self.c5*self.Be[0]*self.Be[1]/self.sBe+self.c6*self.Be[0]*self.Be[1]/self.sBe+self.c7*self.Be[1]**2/self.sBe+self.c8*self.Be[1]*self.Be[2]/self.sBe+self.c9*self.Be[2]**2/self.sBe
        self.TF=self.TFperm[0,0]+self.TFind[0,0]# sum all parts of the TotalField (TFpermanent,TFinduced,TFelectric,TFeddycurrents,(TFgeomagnetic,TFoceanswell,TFionosphere,TFgeology))
        #ic(self.TF)
        #ic(self.resultantB.reshape(1,3).dot(self.Be)/self.sBe)
        #ic(self.TF/(self.resultantB.reshape(1,3).dot(self.Be)/self.sBe))
        return self.resultantB

    #The sensor position in a (aTb) coords
    def set_SensorPosition(self,sensorpos):
        
        self.sensorpos=np.array(sensorpos).reshape(3,1)

    #set the magnetic field of the earth for the equations
    def setBe(self,lon=-75.552067,lat=45.406838,h= 0.0,date = datetime(2023, 10, 20)):

        Be,Bn,Bu=ppigrf.igrf(lon,lat,h,date)
        
        self.Be=np.concatenate((Be,Bn,Bu),axis=0)*1e-9
        
        self.sBe= np.sqrt(self.Be.reshape(1,3).dot(self.Be))

   
        
