'''
    This is the drone class for magnetic simulation.
    As of this first prototype, dipoles can be added to the solid frame(geometry) of the drone.
    The sensor's position is set within the drones coords.
    This means the sensor moves with the drone and so are the dipoles added to the drone.
    There is also a magnetic signature map included in this class. For the purpose of this first prototype, it's all that is needed. But in the future it would be better to separate them.

'''

import numpy as np
import matplotlib.pyplot as plt

import magsignature as magsig
import geometry as geo



class Drone:

    #initialise a drone
    def __init__(self,sensorpos):
        self.magsigDrone=magsig.MagSignature(sensorpos)#create the magnetic signature of the drone
        self.set_sensor_pos(sensorpos)#set sensor position in the drone coords
        self.set_worldTransform()#initialise the transform matrix between the world and the drone
        
        self.magsigMap=magsig.MagSignature(self.get_World_sensor_pos())# create a magnetic signature in world coords to simulate a geological magnetic map

        self.csvloaded=False
        
    #set the sensor's position 
    def set_sensor_pos(self,sensorpos):
        self.sensorpos=np.array(sensorpos).reshape(3,1)
        self.magsigDrone.set_SensorPosition(self.sensorpos)

        
    # setting the transform between the world coords and the drone coords
    def set_worldTransform(self,x=0,y=0,z=0,thetax=np.deg2rad(180),thetay=0,thetaz=0):
        self.wTdrone=geo.TranslationMatrix(thetax,thetay,thetaz,x,y,z)

    # get the sensors position in world coords
    def get_World_sensor_pos(self):
        return geo.Transformation(self.wTdrone,self.sensorpos)
        
    # load sensor and dipoles positions from csv file(spread sheet)
    def loadDronefromcsv(self,filename):
        self.csvdata=np.genfromtxt(filename,delimiter=',')
        
        cmTOm=0.01
        
        self.Xcsv=self.csvdata[3:,1]*cmTOm
        self.Ycsv=self.csvdata[3:,2]*cmTOm
        self.Zcsv=self.csvdata[3:,3]*cmTOm
        
        self.T=self.csvdata[3:,4]*1e-6
        self.mesuredistance=0.01

        self.csvloaded=True

    def csvMag(self,rx,ry,rz):
        summing=0
        j=0
        for iT in self.T:
            summing=summing+(iT*self.mesuredistance)/(np.sqrt((rx-self.Xcsv[j])**2+(ry-self.Ycsv[j])**2+(rz-self.Zcsv[j])**2))**3
            j=j+1
        return summing
        
        
    #load map to simulate environment
    def loadMap(self,filename):
        pass

    #add a dipole manualy to the drone
    def newDipole(self,dipole):
        self.magsigDrone.newDipole(dipole)

    #add a dipole manualy to the map
    def newMapDipole(self,dipole):
        self.magsigMap.newDipole(dipole)

    def newWire(self,wire):
        self.magsigDrone.newWire(wire)
        
    # set the drone's position in world coords    
    def set_drone_pos(self,x,y,z,thetax=0,thetay=0,thetaz=0):
        self.x=x
        self.y=y
        self.z=z
        self.thetax=thetax
        self.thetay=thetay
        self.thetaz=thetaz

    #update all required positions of the drone and it's magnetic calculations
    def updateMap(self,x,y,z,thetax=0,thetay=0,thetaz=0,amp=30): #drone flying and mapping over terrain

        
        self.magsigDrone.set_Sensor_Vector()
        self.set_drone_pos(x,y,z,thetax,thetay,thetaz)
        self.set_worldTransform(self.x,self.y,self.z,self.thetax,self.thetay,self.thetaz)
        #self.get_World_sensor_pos()
        self.magsigMap.set_SensorPosition(self.get_World_sensor_pos())
        self.magsigMap.set_Sensor_Vector()

        
        self.magsigDrone.resB(amp)
        self.magsigMap.resB()

        self.TF=self.magsigDrone.TF+self.magsigMap.TF
        
        if(self.csvloaded):
                    self.TF=self.TF+self.csvMag(x,y,z)
        
    
    def updateDroneMap(self,x,y,z,thetax=0,thetay=0,thetaz=0,amp=30): #mapping the drone alone

        self.set_sensor_pos([x,y,z])
                
        self.magsigDrone.set_Sensor_Vector()
        #self.set_drone_pos(x,y,z,thetax,thetay,thetaz)
        self.magsigDrone.resB(amp)
        
        self.TF=self.magsigDrone.TF

        if(self.csvloaded):
            self.TF=self.TF+self.csvMag(x,y,z)

    def showDrone(self):

        fig=plt.figure()
        ax=fig.add_subplot(111,projection='3d')
        ax.set(xlabel='X(m)',ylabel='Y(m)',zlabel='Z(m)',title='Drone components illustration')
        
        for i in self.magsigDrone.wirelist:
            plotgeom=np.empty((len(i.xx),3),dtype=float)
            #print(plotgeom[0,:].shape)
            a=0
            for j in i.xx:
                
                plotgeom[a,:]=self.transformDronetoWorld(np.array([i.xx[a],i.yy[a],i.zz[a]]))
                a=a+1
            ax.plot(plotgeom[:,0],plotgeom[:,1],plotgeom[:,2],'b')

        if(self.csvloaded):
            plotgeom=np.empty((len(self.Xcsv),3),dtype=float)
            a=0
            for j in self.Xcsv:
                plotgeom[a,:]=self.transformDronetoWorld(np.array([self.Xcsv[a],self.Ycsv[a],self.Zcsv[a]]))
                ax.plot(plotgeom[a,0],plotgeom[a,1],plotgeom[a,2],'ok',ms=self.T[a]*1e4)
                a=a+1
            

    def transformDronetoWorld(self,vector):
        return geo.Transformation(self.wTdrone,vector).reshape(3)
        
