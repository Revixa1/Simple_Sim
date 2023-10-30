import numpy as np

import magsignature as magsig
import geometry as geo


class Drone:

    def __init__(self,sensorpos):
        self.set_sensor_pos(sensorpos)
        self.magsigDrone=magsig.MagSignature(self.sensorpos)
        self.set_worldTransform()
        
        self.magsigMap=magsig.MagSignature(self.get_World_sensor_pos())
        
    def set_sensor_pos(self,sensorpos):
        self.sensorpos=np.array(sensorpos).reshape(3,1)

        
    # setting the transform between the world coords and the drone coords
    def set_worldTransform(self,x=10,y=10,z=10,thetax=0,thetay=0,thetaz=0):
        self.wTdrone=geo.TranslationMatrix(thetax,thetay,thetaz,x,y,z)

    def get_World_sensor_pos(self):
        return geo.Transformation(self.wTdrone,self.sensorpos)
        
        
    def loadDronefromcsv(self,filename):
        pass

    def loadMap(self,filename):
        pass

    def newDipole(self,dipole):
        self.magsigDrone.newDipole(dipole)

    def newMapDipole(self,dipole):
        self.magsigMap.newDipole(dipole)
        
        
    def set_drone_pos(self,x,y,z,thetax=0,thetay=0,thetaz=0):
        self.x=x
        self.y=y
        self.z=z
        self.thetax=thetax
        self.thetay=thetay
        self.thetaz=thetaz

    def update(self,x,y,z,thetax=0,thetay=0,thetaz=0):
        self.magsigDrone.set_Sensor_Vector()
        self.set_drone_pos(x,y,z,thetax,thetay,thetaz)
        self.set_worldTransform(self.x,self.y,self.z,self.thetax,self.thetay,self.thetaz)
        #self.get_World_sensor_pos()
        self.magsigMap.set_SensorPosition(self.get_World_sensor_pos())
        self.magsigMap.set_Sensor_Vector()

        
        self.magsigDrone.resB()
        self.magsigMap.resB()

        self.TF=self.magsigDrone.TF+self.magsigMap.TF
    
