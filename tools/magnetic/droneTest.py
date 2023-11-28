'''
    Testing program for the drone class

'''

import numpy as np
from icecream import ic
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import EngFormatter
import argparse


import drone
import dipole
import magplotting as magplt
import wire






def main():

    parser=argparse.ArgumentParser(description='Program to map the DC fields of a drone',prog='DroneMagMaper')
    parser.add_argument('-csv','--csvfilename',metavar='F',type=str,help='the file name off the scalar reading on the drone components')
    args=parser.parse_args()
    #setting to let the plots plot
    pausetime=0.001

    
    X,Y,X_record,Y_record,Z_record,xdatapoints,ydatapoints,zdatapoints,xmin,xmax,ymin,ymax,zmin,zmax,delta,zdelta,height_record=magplt.setup_mesh(-3,3,-3,3,0.2,0.2,0.1,0.2)
    
    #ic(ydatapoints)

    #setting up the interactive vector plot
    fig2=plt.figure()
    bx= fig2.add_subplot(4,1,1)
    by=fig2.add_subplot(4,1,2)
    bz=fig2.add_subplot(4,1,3)
    bs=fig2.add_subplot(4,1,4)
    fig2.suptitle("Simulated Vector Mesurments")
    
    
    

        
    

 


    # Drone setup
    Drone1=drone.Drone([-1,0,0])#init drone with sensor position in drone coords
    
    wiregeom1=np.array([[0.07,    0.03,  -0.08],
                         [0.09,    0.08,  -0.08],
                         [0.11,    0.05,  -0.05],
                         [0.14,   0.08,  0],
                         [0.06,   0.08,  0.1],
                         [0.08,    0.02,  0],
                         [0.08,   0,  0],
                         [0.08,    -0.02,  0],
                         [0.06,   -0.08,  0.10],
                         [0.14,   -0.08,  0],
                         [0.11,    -0.05,  -0.05],
                         [0.09,    -0.08,  -0.08],
                         [0.07,    -0.03,  -0.08],
                         [0.14,    -0.06,  -0.03],
                         [0.1,    -0.08,   0.08],
                         [0.06,    -0.01,   0],
                         [-0.03,    -0.02,   -0.1],
                         [-0.03,    0.02,   -0.1],
                         [0.06,    0.01,   0],
                         [0.1,    0.08,   0.08],
                         [0.14,    0.06,  -0.03],
                         [0.07,    0.03,  -0.08]])                       

                    
    Drone1.newWire(wire.Wire(wiregeom1))
    Drone1.magsigDrone.wirelist[0].setGeom(wiregeom1,100)



    #======csv scalar mesurements projection============
    Drone1.loadDronefromcsv(args.csvfilename)
    #print(csvdata)
    #print(csvdata[3:,4])
    
    
    #=================================================


    
    Drone1.showDrone()
    #Drone1.newWire(wire.Wire(wiregeom2))

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
                
                Drone1.updateDroneMap(rx,ry,rz,30)
                
                
                
                Drone1.TF=Drone1.TF
                #append the arrays with data
                DX=np.append(DX,rx)
                DY=np.append(DY,ry)
                BX=np.append(BX,Drone1.TF)
                BY=np.append(BY,Drone1.TF)
                BZ=np.append(BZ,Drone1.TF)
                BS=np.append(BS,Drone1.TF)

                #ic(testSignature.TFperm)
                loop_DZ=np.append(loop_DZ,Drone1.TF)
            '''
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
            '''
            
            
           
            

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
