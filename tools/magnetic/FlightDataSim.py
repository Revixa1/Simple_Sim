import numpy as np
from icecream import ic
import matplotlib.pyplot as plt
from matplotlib import cm
import argparse
from datetime import datetime


import drone
import wire



def main():


    #Setting the programms info shown from the terminal about it's usage with "--help" option
    parser=argparse.ArgumentParser(description='Program to do compensation on the drone\' flight data', prog='DroneMagCompensation')
    parser.add_argument('-csv','--csvfilename',metavar='F',type=str,help='the file name off the scalar reading on the drone components')
    parser.add_argument('-fd','--flightdata',metavar='F',type=str,help='the file name off the flight data')
    
    args=parser.parse_args()




    #===Drone Creation===
    Drone1=drone.Drone([-0.75,0,0])
    #========csv scalar mesurements projection============
    if(args.csvfilename):#only load the csv if a file name has been given
        Drone1.loadDronefromcsv(args.csvfilename)
    #========FlightData===========
    if(args.flightdata):#only load the csv if a file name has been given
        Drone1.loadFlightData(args.flightdata)
        
    #========Wire=========
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




    #show the drones DC magnetic sources, the wire shape and where the sensor is
    Drone1.showDrone()


    fig= plt.figure()
    ax=fig.add_subplot(111,projection='3d')
    
    lat=[]
    lon=[]
    xl=[]
    yl=[]
    alt=[]
    zl=[]
    roll=[]
    pitch=[]
    yaw=[]
    curr=[]
    Mag=[]
    j=0
    for i in range(0,len(Drone1.time)):

        if(not np.isnan(Drone1.lat[i]) and not np.isnan(Drone1.Mag1[i])):
            #ic(Drone1.lat[i])
        
            if(j==0):
                latini=Drone1.lat[i]
                lonini=Drone1.lon[i]
                altini=Drone1.Alt[i]
                xini,yini=latlon_to_xy(latini,lonini)
         
                         
            lat=np.append(lat,Drone1.lat[i])
            xl=np.append(xl,latlon_to_xy(Drone1.lat[i],Drone1.lon[i])[0]-xini)
            lon=np.append(lon,Drone1.lon[i])
            yl=np.append(yl,latlon_to_xy(Drone1.lat[i],Drone1.lon[i])[1]-yini)
            alt=np.append(alt,Drone1.Alt[i])
            zl=np.append(zl,Drone1.Alt[i]-altini)
            roll=np.append(roll,Drone1.Roll[i])
            pitch=np.append(pitch,Drone1.Pitch[i])
            yaw=np.append(yaw,Drone1.Yaw[i])
            curr=np.append(curr,Drone1.Curr[i]) 
            Mag=np.append(Mag,(Drone1.Mag1[i]+Drone1.Mag2[i])/2)

            
                

            
            
            if(not j%1000):
                xact,yact=latlon_to_xy(lat[j],lon[j])
                Drone1.updateMap(xl[j],yl[j],zl[j],np.deg2rad(roll[j]+180),np.deg2rad(pitch[j]),np.deg2rad(yaw[j]),curr[j])
                ic(xl[j])
                ic(yl[j])
                ic(alt[j])
                
                Drone1.showDrone(xl,yl,zl)
            j=j+1
                
    

    ax.plot(xl,yl,Mag)
    plt.show()
    
  
        






def latlon_to_xy(lat,lon):
    R=63710
    x = R * np.cos(lat) * np.cos(lon)
    y = R * np.cos(lat) * np.sin(lon)
    z = R *np.sin(lat)
    return x,y
if __name__ == "__main__":
    main()
