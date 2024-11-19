'''
    This is the drone class for magnetic simulation.
    As of this first prototype, dipoles can be added to the solid frame(geometry) of the drone.
    The sensor's position is set within the drones coords.
    This means the sensor moves with the drone and so are the dipoles added to the drone.
    There is also a magnetic signature map included in this class. For the purpose of this first prototype, it's all that is needed. But in the future it would be better to separate them.

'''

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import ppigrf

import magsignature as magsig
import geometry as geo



class Drone:

    #initialise a drone
    def __init__(self,sensorpos):
        self.magsigDrone=magsig.MagSignature(sensorpos)#create the magnetic signature of the drone
        self.set_sensor_pos(sensorpos)#set sensor position in the drone coords
        self.set_worldTransform()#initialise the transform matrix between the world and the drone

        
        self.magsigMap=magsig.MagSignature(self.get_World_sensor_pos())# create a magnetic signature in world coords to simulate a geological magnetic map
        self.setBe() #initialise the eath's magnetic field
        
        self.csvloaded=False#initialise the state if a csv file is loaded or not. (default is false)
        
    #set the sensor's position 
    def set_sensor_pos(self,sensorpos):
        self.sensorpos=np.array(sensorpos).reshape(3,1)
        self.magsigDrone.set_SensorPosition(self.sensorpos)

        
    # setting the transform between the world coords and the drone coords (thetax as a default of 180deg because the drone's coords have z going down while upright)
    def set_worldTransform(self,x=0,y=0,z=0,thetax=np.deg2rad(180),thetay=0,thetaz=0):
        self.wTdrone=geo.TranslationMatrix(thetax,thetay,thetaz,x,y,z)

    # get the sensors position in world coords
    def get_World_sensor_pos(self):
        return geo.Transformation(self.wTdrone,self.sensorpos)
        
    # load the mesured strenght of the mag sources and there positions from csv file(spread sheet)
    def loadDronefromcsv(self,filename):
        self.csvdata=np.genfromtxt(filename,delimiter=';')
        
        cmTOm=0.01  #unit conversion from cm to m

        #get the positions of every sources
        self.Xcsv=self.csvdata[3:,1]*cmTOm 
        self.Ycsv=self.csvdata[3:,2]*cmTOm
        self.Zcsv=self.csvdata[3:,3]*cmTOm

        #get the strenght of every sources
        self.T=self.csvdata[3:,4]*1e-6 #*1e-6 because the mesurments are in µT
        
        self.mesuredistance=0.01 #distance at wich the sensor reads the source

        self.csvloaded=True #state to say the csv file has been loaded

    def csvMag(self,rx,ry,rz):
    
        summing=0 #intitialise the summed value 
        j=0 #initialise the iteretor value
        for iT in self.T:
            summing=summing+((iT)/(((1+self.mesuredistance)+np.sqrt((rx-self.Xcsv[j])**2+(ry-self.Ycsv[j])**2+(rz-self.Zcsv[j])**2))**3)) #sum every sources from the csv to the sensors position.
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
        
    #add a wire manualy to the drone
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

        
        self.magsigDrone.set_Sensor_Vector()#set the position of the sensor to every dipoles in the drone. (should change if sensor doesn't move)
        self.set_drone_pos(x,y,z,thetax,thetay,thetaz)#set the position of the drone in the world coords
        self.set_worldTransform(self.x,self.y,self.z,self.thetax,self.thetay,self.thetaz)#create the transformation matrix between the world and the drone coords
        self.magsigMap.set_SensorPosition(self.get_World_sensor_pos())#set the sensors position in the world coords
        self.magsigMap.set_Sensor_Vector() #set the position of the sensor to every dipoles in the world signature
        self.magsigDrone.setBe(self.transformWorldtoDrone(self.Be))
        
        self.magsigDrone.resB(amp)#calculate the field of the drone
        self.magsigMap.resB()#calculate the field of the world map

        self.TF=self.magsigDrone.TF+self.magsigMap.TF # add the fields
        
        if(self.csvloaded):
                    self.TF=self.TF+self.csvMag(x,y,z) #add this field if the csv is loaded
        
    #update the sensors position in the drone coords and calculate the scalar strenght of the field
    def updateDroneMap(self,x,y,z,thetax=0,thetay=0,thetaz=0,amp=30): #mapping the drone alone

        self.set_sensor_pos([x,y,z])# change the sensor's position
                
        self.magsigDrone.set_Sensor_Vector()# set the position of the sensor to every dipoles in the drone.
        
        self.magsigDrone.resB(amp)#calculate de field of the drone
        
        self.TF=self.magsigDrone.TF

        if(self.csvloaded):
            self.TF=self.TF+self.csvMag(x,y,z)#add this field if the csv is loaded

    def showDrone(self,pathx=[],pathy=[],pathz=[]):#Show the drone's position in the world with the path it has made so far and all the magnetic components attached to the drone

        fig=plt.figure()
        ax=fig.add_subplot(111,projection='3d')
        ax.set(xlabel='X(m)',ylabel='Y(m)',zlabel='Z(m)',title='Drone components illustration')

        worldsensorpos=self.get_World_sensor_pos()
        ax.plot(worldsensorpos[0],worldsensorpos[1],worldsensorpos[2],'vg',ms=10)#show where the sensor is

        
        if(len(self.magsigDrone.wirelist)):
            for i in self.magsigDrone.wirelist:
                plotgeom=np.empty((len(i.xx),3),dtype=float)
                #print(plotgeom[0,:].shape)
                a=0
                for j in i.xx:
                    
                    plotgeom[a,:]=self.transformDronetoWorld(np.array([i.xx[a],i.yy[a],i.zz[a]]))# show the wire on the drone in the world coords
                    a=a+1
                ax.plot(plotgeom[:,0],plotgeom[:,1],plotgeom[:,2],'b')
    
        if(self.csvloaded):
            plotgeom=np.empty((len(self.Xcsv),3),dtype=float)
            a=0
            for j in self.Xcsv:
                plotgeom[a,:]=self.transformDronetoWorld(np.array([self.Xcsv[a],self.Ycsv[a],self.Zcsv[a]]))# show the magnetic sources from csv on the drone in the world coords
                ax.plot(plotgeom[a,0],plotgeom[a,1],plotgeom[a,2],'ok',ms=self.T[a]*1e4)
                a=a+1
                
        if(len(pathx)):
            ax.plot(pathx,pathy,pathz,'r') #show the path the drone has taken 
            
    #transform vector from drone coords to world coords
    def transformDronetoWorld(self,vector):
        return geo.Transformation(self.wTdrone,vector).reshape(3)
        
    #transform vector from world coords to drone coords
    def transformWorldtoDrone(self,vector):
        return geo.Transformation(self.wTdrone.transpose(),vector).reshape(3)
        

    #loading flight data from csv
    def loadFlightData(self, filename):
        self.flightdata=np.genfromtxt(filename,delimiter=',')
        self.time=self.flightdata[1:,0]
        self.Mag1=self.flightdata[1:,1]
        self.Mag2=self.flightdata[1:,2]
        self.lat=self.flightdata[1:,3]
        self.lon=self.flightdata[1:,4]
        self.GyrX=self.flightdata[1:,5]
        self.GyrY=self.flightdata[1:,6]
        self.GyrZ=self.flightdata[1:,7]
        self.AccX=self.flightdata[1:,8]
        self.AccY=self.flightdata[1:,9]
        self.AccZ=self.flightdata[1:,10]
        self.MagX=self.flightdata[1:,11]
        self.MagY=self.flightdata[1:,12]
        self.MagZ=self.flightdata[1:,13]
        self.Curr=self.flightdata[1:,14]
        self.Roll=self.flightdata[1:,15]
        self.Pitch=self.flightdata[1:,16]
        self.Yaw=self.flightdata[1:,17]
        self.Alt=self.flightdata[1:,18]


    #set the magnetic field of the earth for the equations
    def setBe(self,lon=-75.552067,lat=45.406838,h= 0.0,date = datetime(2023, 10, 20)):

        Be,Bn,Bu=ppigrf.igrf(lon,lat,h,date)
        
        self.Be=np.concatenate((Be,Bn,Bu),axis=0)*1e-9
        
        self.sBe= np.sqrt(self.Be.reshape(1,3).dot(self.Be))
        self.magsigDrone.setBe(self.transformWorldtoDrone(self.Be))#the drone changes orrientation in the earth's magnetic field so you have to switch Be from world coords to drone coords
        self.magsigMap.setBe(self.Be)
        
