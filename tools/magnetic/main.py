import dipole
import numpy as np
from icecream import ic
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import EngFormatter

import magplotting as magplt
import time
import magsignature as magsig



def main():

    lowdist,highdist,ddist=-3,3.1,0.1
    datapoints=int((highdist-lowdist)/ddist)+1
    
    pausetime=0.001
    
    

    
    fig2=plt.figure()
    bx= fig2.add_subplot(3,1,1)
    by=fig2.add_subplot(3,1,2)
    bz=fig2.add_subplot(3,1,3)
    fig2.suptitle("Simulated Vector Mesurments")
    
    

    
    


    rz=1
    #ic(DZ.shape)
    
    
    
    
    
    X = np.arange(lowdist,highdist,ddist)
    Y = np.arange(lowdist,highdist,ddist)
    X, Y = np.meshgrid(X, Y)
    
    
    dipole1= dipole.Dipole(0,0,0.001,2,0,0)
    dipole2= dipole.Dipole(0,0,0.001,0,2,0)
    dipole3= dipole.Dipole(0,0,0.001,-2,0,0)
    dipole4= dipole.Dipole(0,0,0.001,0,-2,0)
    dipole5= dipole.Dipole(0,0,0.001,0,0,0)

    testSignature=magsig.MagSignature()
    testSignature.newDipole(dipole1)
    testSignature.newDipole(dipole2)
    testSignature.newDipole(dipole3)
    testSignature.newDipole(dipole4)
    testSignature.newDipole(dipole5)

    
    
    for rz in np.arange(-2,3,1):
        plt.ion()
        i=0
        DX=np.empty((0,0),dtype=float)
        DY=np.empty((0,0),dtype=float)
        BX=np.empty((0,0),dtype=float)
        BY=np.empty((0,0),dtype=float)
        BZ=np.empty((0,0),dtype=float)
        DZ=np.empty((0,0),dtype=float)
        for rx in np.arange(lowdist,highdist,ddist):
            loop_DZ=np.empty((0),dtype=float)
                
                
            for ry in np.arange(lowdist,highdist,ddist):
        
                testSignature.set_TranslationMatrix(rx,ry,rz)
                testSignature.set_Sensor_Vector()
                testSignature.resB()
                
    
    
                DX=np.append(DX,rx)
                DY=np.append(DY,ry)
                BX=np.append(BX,testSignature.resultantB[0])
                BY=np.append(BY,testSignature.resultantB[1])
                BZ=np.append(BZ,testSignature.resultantB[2])
    
                loop_DZ=np.append(loop_DZ,testSignature.res_sB)
            
            bx.set(ylabel="Bx(T)")
            by.set(ylabel="By(T)")
            bz.set(ylabel="Bz(T)",xlabel="posY(m)")
            
            bx.plot(DY,BX)
            by.plot(DY,BY)
            bz.plot(DY,BZ)
            plt.pause(pausetime)
            bx.clear()
            by.clear()
            bz.clear()
            
            BX=np.empty((0,0),dtype=float)
            BY=np.empty((0,0),dtype=float)
            BZ=np.empty((0,0),dtype=float)
            DY=np.empty((0,0),dtype=float)
    
    
            DZ=np.append(DZ,loop_DZ)
            #ic(DZ)
            i=i+1
    
    
        #ic(datapoints)    
        DZ=DZ.reshape(i,datapoints) 
        #ic(DZ.shape)
        
        fig1=plt.figure()
        magplt.scalarMap(fig1,X,Y,DZ,rz)
        plt.show(block=False)
    



    
    magplt.waitClosePlots()
    
    
        
        

        

if __name__ == "__main__":
    main()
