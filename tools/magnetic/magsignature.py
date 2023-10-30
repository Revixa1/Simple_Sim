import numpy as np
import dipole
import geometry as geo
from icecream import ic

import ppigrf
from datetime import datetime


#lat=    45.406838
#lon=   -75.552067
#h= 0.0
#date = datetime(2023, 10, 20)
#Be,Bn,Bu=ppigrf.igrf(lon,lat,h,date)

#Be=np.concatenate((Be,Bn,Bu),axis=0)*1e-9

#sBe= np.sqrt(Be.reshape(1,3).dot(Be))




class MagSignature:


    
    def __init__(self,sensorpos):
        self.dipolelist = []
        self.set_SensorPosition(sensorpos)
        self.set_TranslationMatrix()
        self.setBe()

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
        self.TF=self.TFperm[0,0]+self.TFind[0,0]
        #ic(self.TF)
        #ic(self.resultantB.reshape(1,3).dot(self.Be)/self.sBe)
        #ic(self.TF/(self.resultantB.reshape(1,3).dot(self.Be)/self.sBe))
        return self.resultantB

    #The sensor position in a (aTb) coords
    def set_SensorPosition(self,sensorpos):
        
        self.sensorpos=np.array(sensorpos).reshape(3,1)

    def setBe(self,lon=-75.552067,lat=45.406838,h= 0.0,date = datetime(2023, 10, 20)):

        Be,Bn,Bu=ppigrf.igrf(lon,lat,h,date)
        
        self.Be=np.concatenate((Be,Bn,Bu),axis=0)*1e-9
        
        self.sBe= np.sqrt(self.Be.reshape(1,3).dot(self.Be))

   
        
