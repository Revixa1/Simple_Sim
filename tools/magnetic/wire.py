'''
    This is the wire class.
    It's a class made to simulate a 3d wire with a DC current flowing trought it.
    You can set the geometry by giving a list of points the wire takes in some coords, in the current's direction. (Source+ to Source-)
    You can also calculate the magnetic field that would be mesured by a vector magnetometor at a certain distance from the wire.

    There are somme settings that can be modified like the number of turns of the wire (if it's a loop)
    and the resolution/number of points of the wire to calculate from. 

    
'''



import numpy as np
from scipy import interpolate


class Wire:

    #initialisation of the wire object
    def __init__(self,geom,amp=30,sensorPos=[1,0,0],resolution=1000,loopTurns=1): # arguments are a list of point representing the wire geometry, the amps passing trought the wire (mean, default 30A) and the sensor's position
        self.mu0=1e-7   #permeability of air
        self.setAmp(amp)
        self.setGeom(geom,resolution,loopTurns)
        self.setSensorPos(sensorPos)

	
    def setAmp(self,amp):#method to change the current flowing in the wire
        self.amp=amp

    def setGeom(self,geom,resolution,loopTurns):#method to set the geometry
        self.geom=geom
        self.resolution=resolution# setting how many points the wire has for calculation
        self.loopTurns=loopTurns# setting how many turns of wire there is

        # This part makes a 3d spline from the given wire geometry. 
        self.u=  np.cumsum(np.r_[[0], np.linalg.norm(np.diff(self.geom, axis=0), axis=1)]) 
        self.sx=interpolate.InterpolatedUnivariateSpline(self.u, self.geom[:,0])
        self.sy=interpolate.InterpolatedUnivariateSpline(self.u, self.geom[:,1])
        self.sz=interpolate.InterpolatedUnivariateSpline(self.u, self.geom[:,2])
        self.uu = np.linspace(self.u[0], self.u[-1], resolution)  #here we define the number of points to use
        self.xx = self.sx(self.uu)
        self.yy = self.sy(self.uu)
        self.zz = self.sz(self.uu)
        self.xx2=np.diff(self.xx)#these are the derivatives of the positions. It's to form the vectors were each points of te wires are going. are going
        self.yy2=np.diff(self.yy)
        self.zz2=np.diff(self.zz)


    def setSensorPos(self,sensorPos): # method to set the sensor's position in the same coords 
        self.sensorPos=sensorPos


    #method to calculate the magnetic field made by the wire at the sensor's position
    def getField(self):
        self.Bsum=0 # initialise the Sommation of the field.
        for loopturns in range(0,self.loopTurns):#get field again and add to Bsum if it has multiple loops
            for N in range(1,self.resolution,1): 
                rvec=np.array([(self.sensorPos[0]-self.xx[N]),(self.sensorPos[1]-self.yy[N]),(self.sensorPos[2]-self.zz[N])])#vector from point in wire to sensor
                rscalar=np.sqrt((self.sensorPos[0]-self.xx[N])**2+(self.sensorPos[1]-self.yy[N])**2+(self.sensorPos[2]-self.zz[N])**2)#scalar of that vector
                runit=rvec/rscalar#unit vector of the wire/sensor vector
                wirepatch=np.array([self.xx2[N-1],self.yy2[N-1],self.zz2[N-1]])#assembling the direction vector of a point in the wire.
                unitwirepatch=wirepatch/np.linalg.norm(wirepatch)#making the direction vector a unit vector
                I=self.amp*wirepatch#Building the current vector flowing trough the wire
                
                B=np.cross(I,runit[:,0])/(np.linalg.norm(runit)**2)#Biosavard Law minus the permeability
                #B=np.cross(B,runit)
                self.Bsum=self.Bsum+B
            #print(Z_record.shape)
        self.Bsum=(self.mu0/(4*np.pi))*self.Bsum #final part of the biosavard law.
        self.Bsum=np.array(self.Bsum).reshape(3,1) # reshaping the vector for compatibility (methodology)
        return self.Bsum

   
    
''' 
   def update(amp=self.amp,sensorPos,self.sensorPos)
        setAmp(amp)
        setSensorPos(sensorPos)
        getField()
'''  
	
		
