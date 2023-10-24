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

    #area of calculation
    lowdist,highdist,ddist=-3,3.1,0.1
    datapoints=int((highdist-lowdist)/ddist)+1
    
    lowheight,highheight,dheight=-1,2,1
    heightpoints=int((highheight-lowheight)/dheight)

    #setting to let the plots plot
    pausetime=0.001
    
    

    #setting up the interactive vector plot
    fig2=plt.figure()
    bx= fig2.add_subplot(3,1,1)
    by=fig2.add_subplot(3,1,2)
    bz=fig2.add_subplot(3,1,3)
    fig2.suptitle("Simulated Vector Mesurments")
    
    
    
    
    
    # needed for 3d scalar map
    X = np.arange(lowdist,highdist,ddist)
    Y = np.arange(lowdist,highdist,ddist)
    X, Y = np.meshgrid(X, Y)

    # init of the memory of the maps to plot all off them at the same time
    X_record= np.empty((heightpoints,datapoints,datapoints),dtype=float)
    Y_record= np.empty((heightpoints,datapoints,datapoints),dtype=float)
    Z_record= np.empty((heightpoints,datapoints,datapoints),dtype=float)
    height_record=np.empty((heightpoints),dtype=float)


    # test dipoles setup
    testSignature=magsig.MagSignature()
    testSignature.newDipole(dipole.Dipole(0,0,0.001,2,0,0))
    testSignature.newDipole(dipole.Dipole(0,0,0.001,0,2,0))
    testSignature.newDipole(dipole.Dipole(0,0,0.001,-2,0,0))
    testSignature.newDipole(dipole.Dipole(0,0,0.001,0,-2,0))
    testSignature.newDipole(dipole.Dipole(0,0,0.001,0,0,0))
    testSignature.newDipole(dipole.Dipole(0.005,0,0,0,0,0))

    #height iterator to move in the arrays of the map recordings
    iz=0

    #for loop for height
    for rz in np.arange(lowheight,highheight,dheight):
        
        plt.ion()#make plots interactive for the vector ploting
        #reseting variables and arrays
        i=0
        DX=np.empty((0,0),dtype=float)
        DY=np.empty((0,0),dtype=float)
        BX=np.empty((0,0),dtype=float)
        BY=np.empty((0,0),dtype=float)
        BZ=np.empty((0,0),dtype=float)
        DZ=np.empty((0,0),dtype=float)

        #for loop for x position on the map
        for rx in np.arange(lowdist,highdist,ddist):
            loop_DZ=np.empty((0),dtype=float)#reset arrays of z value on scalar map
                
            #for loop for y position on the map    
            for ry in np.arange(lowdist,highdist,ddist):

                '''
                Change translation matrix to the right translation values 
                Set the distance of the sensor to all dipoles
                Calculate the field at the sensor for this coordinate
                '''
                testSignature.set_TranslationMatrix(rx,ry,rz)
                testSignature.set_Sensor_Vector()
                testSignature.resB()
                
    
                #append the arrays with data
                DX=np.append(DX,rx)
                DY=np.append(DY,ry)
                BX=np.append(BX,testSignature.resultantB[0])
                BY=np.append(BY,testSignature.resultantB[1])
                BZ=np.append(BZ,testSignature.resultantB[2])
    
                loop_DZ=np.append(loop_DZ,testSignature.res_sB)

            #reset the labels for the vector graphs
            bx.set(ylabel="Bx(T)")
            by.set(ylabel="By(T)")
            bz.set(ylabel="Bz(T)",xlabel="posY(m)")

            #plot the vector graphs interactively
            bx.plot(DY,BX)
            by.plot(DY,BY)
            bz.plot(DY,BZ)
            plt.pause(pausetime)
            bx.clear()
            by.clear()
            bz.clear()


            

            #reset the vector graphs data
            BX=np.empty((0,0),dtype=float)
            BY=np.empty((0,0),dtype=float)
            BZ=np.empty((0,0),dtype=float)
            DY=np.empty((0,0),dtype=float)
    
            #append the map data for one line in x coords to the set of the map
            DZ=np.append(DZ,loop_DZ)
    
    
        # shape data for plot usage and record it
        DZ=DZ.reshape(datapoints,datapoints) 
        
        X_record[iz,:]= X
        Y_record[iz,:]= Y
        Z_record[iz,:]= DZ
        height_record[iz]=rz
        iz+=1
    
    #plot every maps at the end
    for j in range(0,heightpoints):
        fig1=plt.figure()
        magplt.scalarMap(fig1,X_record[j,:],Y_record[j,:],Z_record[j,:],height_record[j])
        plt.show(block=False)

    #wait that every plots are closed to end program
    magplt.waitClosePlots()
    
    
        
        

        

if __name__ == "__main__":
    main()
