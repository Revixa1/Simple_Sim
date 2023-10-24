import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import EngFormatter

def scalarMap(fig,X_points,Y_points,Z_points,zheight):
    
    plt.ioff()
    
    ax = fig.add_subplot(111,projection='3d')
    
    formatterax = EngFormatter(unit='T')
    ax.zaxis.set_major_formatter(formatterax)
    ax.set(xlabel="posx(m)",ylabel="posY(m)",zlabel="sB(T)",title="scalar Map at "+str(zheight)+"m in z")
    return ax.plot_surface(X_points,Y_points,Z_points,cmap=cm.viridis,linewidth=0, antialiased=False)
    

def waitClosePlots():
    while(plt.get_fignums()):
            plt.pause(0.001)
    
