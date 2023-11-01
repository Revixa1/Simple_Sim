'''
    This is the drone class for magnetic simulation.
    As of this first prototype, dipoles can be added to the solid frame(geometry) of the drone.
    The sensor's position is set within the drones coords.
    This means the sensor moves with the drone and so are the dipoles added to the drone.
    There is also a magnetic signature map included in this class. For the purpose of this first prototype, it's all that is needed. But in the future it would be better to separate them.

'''

import numpy as np

import magsignature as magsig
import geometry as geo


class Drone:

    #initialise a drone
    def __init__(self,sensorpos):
        self.set_sensor_pos(sensorpos)#set sensor position in the drone coords
        self.magsigDrone=magsig.MagSignature(self.sensorpos)#create the magnetic signature of the drone
        self.set_worldTransform()#initialise the transform matrix between the world and the drone
        
        self.magsigMap=magsig.MagSignature(self.get_World_sensor_pos())# create a magnetic signature in world coords to simulate a geological magnetic map

    #set the sensor's position 
    def set_sensor_pos(self,sensorpos):
        self.sensorpos=np.array(sensorpos).reshape(3,1)

        
    # setting the transform between the world coords and the drone coords
    def set_worldTransform(self,x=10,y=10,z=10,thetax=0,thetay=0,thetaz=0):
        self.wTdrone=geo.TranslationMatrix(thetax,thetay,thetaz,x,y,z)

    # get the sensors position in world coords
    def get_World_sensor_pos(self):
        return geo.Transformation(self.wTdrone,self.sensorpos)
        
    # load sensor and dipoles positions from csv file(spread sheet)
    def loadDronefromcsv(self,filename):
        pass
        
    #load map to simulate environment
    def loadMap(self,filename):
        pass

    #add a dipole manualy to the drone
    def newDipole(self,dipole):
        self.magsigDrone.newDipole(dipole)

    #add a dipole manualy to the map
    def newMapDipole(self,dipole):
        self.magsigMap.newDipole(dipole)
        
    # set the drone's position in world coords    
    def set_drone_pos(self,x,y,z,thetax=0,thetay=0,thetaz=0):
        self.x=x
        self.y=y
        self.z=z
        self.thetax=thetax
        self.thetay=thetay
        self.thetaz=thetaz

    #update all required positions of the drone and it's magnetic calculations
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
    
