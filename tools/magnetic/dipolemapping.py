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

    
    #setting to let the interactive and non blocking plots plot
    pausetime=0.001

    #setting up all variables and lists related to creating the data and recording it
    X,Y,X_record,Y_record,Z_record,xdatapoints,ydatapoints,zdatapoints,xmin,xmax,ymin,ymax,zmin,zmax,delta,zdelta,height_record=magplt.setup_mesh(-3,3,-3,3,-1,1,0.1,2)
    
    #ic(ydatapoints)

    #setting up the interactive vector plot
    fig2=plt.figure()
    bx= fig2.add_subplot(4,1,1)
    by=fig2.add_subplot(4,1,2)
    bz=fig2.add_subplot(4,1,3)
    bs=fig2.add_subplot(4,1,4)
    fig2.suptitle("Simulated Vector Mesurments")
    


    # test dipoles setup
    testSignature=magsig.MagSignature([0,0,0])#init magsig with sensor position
    testSignature.newDipole(dipole.Dipole(0,0,1*1e0,2,0,0))
    testSignature.newDipole(dipole.Dipole(0,0,1*1e0,0,2,0))
    testSignature.newDipole(dipole.Dipole(0,0,1*1e0,-2,0,0))
    testSignature.newDipole(dipole.Dipole(0,2.5e7*1e-9,0,-500,-500,0))
    testSignature.newDipole(dipole.Dipole(1e-9,0,0,0,0,0))
   

    #height iterator to move in the arrays of the map recordings
    iz=0

    #for loop for height
    for rz in np.arange(zmin,zmax+zdelta,zdelta):
        
        plt.ion()#make plots interactive for the vector ploting
        #reseting variables and arrays
        i=0
        DX=np.empty((0,0),dtype=float)
        DY=np.empty((0,0),dtype=float)
        BX=np.empty((0,0),dtype=float)
        BY=np.empty((0,0),dtype=float)
        BZ=np.empty((0,0),dtype=float)
        BS=np.empty((0,0),dtype=float)
        DZ=np.empty((ydatapoints,xdatapoints),dtype=float)

        bx.clear()
        by.clear()
        bz.clear()

        #for loop for x position on the map
        ix=0
        for rx in np.arange(xmin,xmax+delta,delta):
            loop_DZ=np.empty((0),dtype=float)#reset arrays of z value on scalar map
                
            #for loop for y position on the map    
            for ry in np.arange(ymin,ymax+delta,delta):

                '''
                Change translation matrix to the right translation values 
                Set the distance of the sensor to all dipoles
                Calculate the field at the sensor for this coordinate
                '''
                #testSignature.set_SensorPosition([rx,ry,rz])#move the sensor in a coords (if you want to)
                testSignature.set_TranslationMatrix(rx,ry,rz)#set the distance and angle between a and b coords
                #testSignature.dipolelist[0].set_Dipole_pos([-500+iz*500,-500+iz*500,0]) # move a dipole in it's referenc coords (if you want)
                testSignature.set_Sensor_Vector()
                testSignature.resB()
                
    
                #append the arrays with data
                DX=np.append(DX,rx)
                DY=np.append(DY,ry)
                BX=np.append(BX,testSignature.resultantB[0])
                BY=np.append(BY,testSignature.resultantB[1])
                BZ=np.append(BZ,testSignature.resultantB[2])
                BS=np.append(BS,testSignature.dipolelist[0].get_sB())

                #ic(testSignature.TFperm)
                loop_DZ=np.append(loop_DZ,testSignature.TFperm)

            #reset the labels for the vector graphs
            bx.set(ylabel="Bx(T)")
            by.set(ylabel="By(T)")
            bz.set(ylabel="Bz(T)")
            bs.set(ylabel="Bs(T)",xlabel="posY(m)")

            #plot the vector graphs interactively
            bx.plot(DY,BX)
            by.plot(DY,BY)
            bz.plot(DY,BZ)
            bs.plot(DY,BS)
            plt.pause(pausetime)
            bx.clear()
            by.clear()
            bz.clear()
            bs.clear()

            
            
           
            

            #reset the vector graphs data
            BX=np.empty((0,0),dtype=float)
            BY=np.empty((0,0),dtype=float)
            BZ=np.empty((0,0),dtype=float)
            BS=np.empty((0,0),dtype=float)
            DY=np.empty((0,0),dtype=float)
            
            #append the map data for one line in x coords to the set of the map
            DZ[:,ix]=loop_DZ
            #ic(DZ)
            ix+=1
    
        # shape data for plot usage and record it
        #DZ=DZ.reshape(ydatapoints,xdatapoints) 
        
        X_record[iz,:]= X
        Y_record[iz,:]= Y
        Z_record[iz,:]= DZ
        height_record[iz]=rz
        iz+=1
        #ic(iz)
    
    #plot every maps at the end
    #ic(height_record)
    for j in range(0,zdatapoints):
        fig1=plt.figure()
        magplt.scalarMap(fig1,X_record[j,:],Y_record[j,:],Z_record[j,:],height_record[j])
        plt.show(block=False)

    #wait that every plots are closed to end program
    magplt.waitClosePlots()
    
    
        
        

        

if __name__ == "__main__":
    main()
