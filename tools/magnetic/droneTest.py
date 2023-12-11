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

    #Setting the programms info shown from the terminal about it's usage with "--help" option
    parser=argparse.ArgumentParser(description='Program to map the DC fields of a drone',prog='DroneMagMaper')
    parser.add_argument('-csv','--csvfilename',metavar='F',type=str,help='the file name off the scalar reading on the drone components')
    args=parser.parse_args()
    
    #setting to pause the programm in seconds to let the plots do there work
    pausetime=0.001

    #initialising every variables needed to make a scalar map.
    X,Y,X_record,Y_record,Z_record,xdatapoints,ydatapoints,zdatapoints,xmin,xmax,ymin,ymax,zmin,zmax,delta,zdelta,height_record=magplt.setup_mesh(-3,3,-3,3,-0.15,0.15,0.1,0.15)
    
    

 
    
    
    

        
    

 


    # Drone setup
    Drone1=drone.Drone([-0.75,0,0])#init drone with sensor position in drone coords

    #creating the geometry of a current carring wire
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

    #adding a wire to the drone                
    Drone1.newWire(wire.Wire(wiregeom1,resolution=100,loopTurns=1))

    #Drone1.newDipole(dipole.Dipole(1e-6,0,0,1,0,0))

    #Drone1.newDipole(dipole.Dipole(1e-6,0,0,1,0,0))
   



    #======csv scalar mesurements projection============
    if(args.csvfilename):#only load the csv if a file name has been given
        Drone1.loadDronefromcsv(args.csvfilename)
        #print(csvdata)
        #print(csvdata[3:,4])
    
    
    #=================================================


    
    Drone1.showDrone()#show the drones DC magnetic sources and the wire shape
  

    #height iterator to move in the arrays of the map recordings
    iz=0

    #for loop for height
    for rz in np.arange(zmin,zmax+zdelta,zdelta):
        
        plt.ion()#make plots interactive for the vector ploting
        #reseting variables and arrays
        i=0


        DZ=np.empty((ydatapoints,xdatapoints),dtype=float)




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
                
                Drone1.updateDroneMap(rx,ry,rz)#change the position of the sensor in the drone coords and recalculate the field
                
                loop_DZ=np.append(loop_DZ,Drone1.TF)#variable to store the field value for the scalar map
       
            
            
           
            
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
