import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import EngFormatter
from icecream import ic
import random

def scalarMap(fig,X_points,Y_points,Z_points,zheight):
    
    plt.ioff()
    
    ax = fig.add_subplot(111,projection='3d')
    
    formatterax = EngFormatter(unit='T')
    ax.zaxis.set_major_formatter(formatterax)
    ax.set(xlabel="posx(m)",ylabel="posY(m)",zlabel="TF(T)",title="scalar Map at "+str(zheight)+"m in z")
    return ax.plot_surface(X_points,Y_points,Z_points,cmap=cm.viridis,linewidth=0, antialiased=False)
    

def waitClosePlots():
    while(plt.get_fignums()):
            plt.pause(0.001)
    
def setup_mesh(xmin=-3,xmax=3,ymin=-3,ymax=3,zmin=-1,zmax=1,delta=0.1,zdelta=1):

    xdatapoints=int((xmax+delta-xmin)/delta)+1
    ydatapoints=int((ymax+delta-ymin)/delta)+1
    zdatapoints=int((zmax+zdelta-zmin)/zdelta)

    Xa = np.arange(xmin,xmax+delta,delta)
    Ya = np.arange(ymin,ymax+delta,delta)
    
    X,Y = np.meshgrid(Xa,Ya)
    
    

    X_record= np.empty((zdatapoints,ydatapoints,xdatapoints),dtype=float)
    Y_record= np.empty((zdatapoints,ydatapoints,xdatapoints),dtype=float)
    Z_record= np.empty((zdatapoints,ydatapoints,xdatapoints),dtype=float)
    height_record=np.empty((zdatapoints),dtype=float)
    
    return X,Y,X_record,Y_record,Z_record,xdatapoints,ydatapoints,zdatapoints,xmin,xmax,ymin,ymax,zmin,zmax,delta,zdelta,height_record

#X,Y,X_record,Y_record,Z_record=setup_mesh(-3,3,-3,3)
#ic(Z_record)
