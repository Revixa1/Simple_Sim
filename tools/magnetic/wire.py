import numpy as np
from scipy import interpolate


class Wire:

    def __init__(self,geom,amp=30,sensorPos=[1,0,0]):
        self.mu0=1e-7
        self.setAmp(amp)
        self.setGeom(geom)
        self.setSensorPos(sensorPos)

	
    def setAmp(self,amp):
        self.amp=amp

    def setGeom(self,geom,resolution=1000,loopTurns=1):
        self.geom=geom
        self.resolution=resolution
        self.loopTurns=loopTurns
        self.u=  np.cumsum(np.r_[[0], np.linalg.norm(np.diff(self.geom, axis=0), axis=1)])
        self.sx=interpolate.InterpolatedUnivariateSpline(self.u, self.geom[:,0])
        self.sy=interpolate.InterpolatedUnivariateSpline(self.u, self.geom[:,1])
        self.sz=interpolate.InterpolatedUnivariateSpline(self.u, self.geom[:,2])
        self.uu = np.linspace(self.u[0], self.u[-1], resolution)
        self.xx = self.sx(self.uu)
        self.yy = self.sy(self.uu)
        self.zz = self.sz(self.uu)
        self.xx2=np.diff(self.xx)
        self.yy2=np.diff(self.yy)
        self.zz2=np.diff(self.zz)

    def setSensorPos(self,sensorPos):
        self.sensorPos=sensorPos


    def getField(self):
        self.Bsum=0
        for loopturns in range(0,self.loopTurns):
            for N in range(1,self.resolution,1):
                rvec=np.array([(self.sensorPos[0]-self.xx[N]),(self.sensorPos[1]-self.yy[N]),(self.sensorPos[2]-self.zz[N])])
                rscalar=np.sqrt((self.sensorPos[0]-self.xx[N])**2+(self.sensorPos[1]-self.yy[N])**2+(self.sensorPos[2]-self.zz[N])**2)
                runit=rvec/rscalar
                wirepatch=np.array([self.xx2[N-1],self.yy2[N-1],self.zz2[N-1]])
                unitwirepatch=wirepatch/np.linalg.norm(wirepatch)
                I=self.amp*wirepatch
                
                B=np.cross(I,runit[:,0])/(np.linalg.norm(runit)**2)
                #B=np.cross(B,runit)
                self.Bsum=self.Bsum+B
            #print(Z_record.shape)
        self.Bsum=(self.mu0/(4*np.pi))*self.Bsum
        self.Bsum=np.array(self.Bsum).reshape(3,1)
        return self.Bsum

    
''' 
   def update(amp=self.amp,sensorPos,self.sensorPos)
        setAmp(amp)
        setSensorPos(sensorPos)
        getField()
'''  
	
		
