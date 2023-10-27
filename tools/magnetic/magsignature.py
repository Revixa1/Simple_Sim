import numpy as np
import dipole
import geometry as geo
from icecream import ic

import ppigrf
from datetime import datetime


lat=    45.406838
lon=   -75.552067
h= 0.0
date = datetime(2023, 10, 20)
Be,Bn,Bu=ppigrf.igrf(lon,lat,h,date)

Be=np.concatenate((Be,Bn,Bu),axis=0)*1e-9

sBe= np.sqrt(Be.reshape(1,3).dot(Be))




class MagSignature:


    
    def __init__(self,sensorpos):
        self.dipolelist = []
        self.set_SensorPosition(sensorpos)
        self.aTb=self.set_TranslationMatrix()

    def loadFromCSV(self,filename):
        pass

    def newDipole(self,dipole):
        self.dipolelist.append(dipole)

    def set_Sensor_Vector(self):
        for i in self.dipolelist:
            i.set_sensorVector(geo.Transformation(self.aTb,self.sensorpos-i.get_Dipole_pos()))

    
    
    def set_TranslationMatrix(self,x=0,y=0,z=0,thetax=0,thetay=0,thetaz=0):
        self.aTb=geo.TranslationMatrix(thetax,thetay,thetaz,x,y,z)
        #ic(self.aTb)
        
    def resB(self):
        phresB=0
        self.c1,self.c2,self.c3=0,0,0
        for i in self.dipolelist:
            #ic(i.get_vB())
            phresB=phresB+i.get_vB()
            i.get_C()
            self.c1=self.c1+i.C1
            self.c2=self.c2+i.C2
            self.c3=self.c3+i.C3
            
        #ic(phresB)
        self.resultantB=phresB+Be
        self.res_sB=np.sqrt(self.resultantB.reshape(1,3).dot(self.resultantB))
        self.TFperm=self.c1*Be[0]/sBe+self.c2*Be[1]/sBe+self.c3*Be[2]/sBe
        
        #ic(self.TF)
        #ic(self.resultantB.reshape(1,3).dot(Be)/sBe)
        #ic(self.TF/(self.resultantB.reshape(1,3).dot(Be)/sBe))
        return self.resultantB

    #The sensor position in a (aTb) coords
    def set_SensorPosition(self,sensorpos):
        
        self.sensorpos=np.array(sensorpos).reshape(3,1)
