from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt
from shapely import Point, LineString,LinearRing
from shapely.plotting import plot_line, plot_points
import shapely as sp
import geometry as geo
from scipy.interpolate import Rbf
import magplotting as magplt


fig=plt.figure()
ax=fig.add_subplot(111,projection='3d')
# sampling
x=np.array([    [0.07,    0.03,  -0.08],
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
                [0.07,    0.03,  -0.08]
                ])



'''
[0,0,-0.001],
                [1,0,-0.001],
                [1,1,-0.001],
                [0,1,-0.001],
                [0,0,0],
              
                [1,0,0],
                [1,1,0],
                [0,1,0],
                [0,0,0.001],
             
                [1,0,0.001],
                [1,1,0.001],
                [0,1,0.001],
                [0,0,0.002],
           
                [1,0,0.002],
                [1,1,0.002],
                [0,1,0.002],
                [0,0,0.003],
              
                [1,0,0.003],
                [1,1,0.003],
                [0,1,0.003],
                [0,0,0.004]])            
'''
box=np.array([[-0.5,-0.5,-0.5],
              [0.5,0.5,0.5]])

u=  np.cumsum(np.r_[[0], np.linalg.norm(np.diff(x, axis=0), axis=1)])










rbfi_x = Rbf(u, x[:,0], function='cubic')
rbfi_y = Rbf(u, x[:,1], function='cubic')
rbfi_z = Rbf(u, x[:,2], function='cubic')


sx=interpolate.InterpolatedUnivariateSpline(u, x[:,0])
sy=interpolate.InterpolatedUnivariateSpline(u, x[:,1])
sz=interpolate.InterpolatedUnivariateSpline(u, x[:,2])

uu = np.linspace(u[0], u[-1], 1000)
xx = sx(uu)
yy = sy(uu)
zz = sz(uu)

xx2=np.diff(xx)
yy2=np.diff(yy)
zz2=np.diff(zz)




xxx=rbfi_x(uu)
yyy=rbfi_y(uu)
zzz=rbfi_z(uu)

N=2
plt.ion()
ax.set_box_aspect((1,1,1))
ax.set(xlabel='x(m)',ylabel='y(m)',zlabel='z(m)')
ax.plot(box[:,0],box[:,1],box[:,2],"or")
ax.plot(xx, yy, zz, "b")
ax.plot(x[:,0],x[:,1],x[:,2],'ok')
plt.pause(0.1)
plt.ioff()

X,Y,X_record,Y_record,Z_record,xdatapoints,ydatapoints,zdatapoints,xmin,xmax,ymin,ymax,zmin,zmax,delta,zdelta,height_record=magplt.setup_mesh(-3,3.11,-3,3.11,-1,1,0.5,1)
Xn=np.arange(xmin,xmax+delta,delta)
Yn=np.arange(ymin,ymax+delta,delta)
Zn=np.arange(zmin,zmax+zdelta,zdelta)

mu0=1e-7
iz=0
for rz in Zn:
    ix=0
    for rx in Xn:
        iy=0
        for ry in Yn:
            Bsum=0
            for loopturns in range(0,1):
                for N in range(1,1000,1):
                    rvec=np.array([(rx-xx[N]),(ry-yy[N]),(rz-zz[N])])
                    rscalar=np.sqrt((rx-xx[N])**2+(ry-yy[N])**2+(rz-zz[N])**2)
                    runit=rvec/rscalar
                    wirepatch=np.array([xx2[N-1],yy2[N-1],zz2[N-1]])
                    unitwirepatch=wirepatch/np.linalg.norm(wirepatch)
                    I=30*wirepatch
                    B=np.cross(I,runit)/(np.linalg.norm(runit)**2)
                    #B=np.cross(B,runit)
                    Bsum=Bsum+B
            #print(Z_record.shape)
            Bsum=(mu0/(4*np.pi))*Bsum+50e-6
            Z_record[iz,iy,ix]=np.sqrt(Bsum[0]**2+Bsum[1]**2+Bsum[2]**2)
    
            iy=iy+1
    
    
    
            
        ix=ix+1
    
    height_record[iz]=rz
    print(iz)
    iz=iz+1


for j in range(0,zdatapoints):
    fig1=plt.figure()
    fig2=plt.figure()
    bx=fig2.add_subplot(111)
    magplt.scalarMap(fig1,X,Y,Z_record[j,:],height_record[j])
    bx.contour(X,Y,Z_record[j,:])
    plt.show(block=False)
   
    
    

#ax.plot(xxx,yyy,zzz)

'''for N in range(1,1000,10):
    
    for theta in np.arange(0,2*np.pi,2*np.pi):
        aTb=geo.TranslationMatrix(np.arctan2(zz2[N-1],yy2[N-1])+theta,np.arctan2(xx2[N-1],zz2[N-1]),np.arctan2(yy2[N-1],xx2[N-1]))
        v_a=geo.Transformation(aTb,np.array([0,1,0]))
        wirepatch=np.array([xx2[N-1],yy2[N-1],zz2[N-1]])
        unitwirepatch=wirepatch/np.linalg.norm(wirepatch)

        #B=np.sum((mu0*I)/(rscalar*2*np.pi))
        
        
        x3=np.array([xx[N],xx[N]+v_a[0,0]])
        y3=np.array([yy[N],yy[N]+v_a[1,0]])
        z3=np.array([zz[N],zz[N]+v_a[2,0]])
        ax.plot(x3,y3,z3,'r')
        plt.pause(0.001)
        #print(np.arctan2(xx2[N-1],zz2[N-1])-(np.pi/2))
    
    #print(x3)
        #print(np.sqrt((x3[1]-x3[0])**2+(y3[1]-y3[0])**2+(z3[1]-z3[0])**2))

'''    
  
    


#print(ring.coords)
#print(x)
#x=np.diff(x)
#y = np.ceil(np.sin(x))-0.5


# spline trough all the sampled points
#t = interpolate.BSpline(x[:,0], x[:,1],1)

#x2 = np.linspace(0, 10, 100)

#y2 = interpolate.splev(x2, t)
#y2= np.diff(y)
#x22=np.diff(x2)
#x22=np.append(x22,0)
#y2=np.append(y2,0)
#plt.ion()
#N=12
'''for N in np.arange(0,100-1,1):
    #print(np.rad2deg(np.arctan2(y[N+1]-y[N],x[N+1]-x[N])))
    #x3=np.array([x[N],x[N]+1*np.sin(np.arctan2(y[N],x[N]))])
    x3=np.array([x[N],x[N]+1*np.cos(np.arctan2(y2[N],x22[N])+np.deg2rad(90))])
    x4=np.array([x[N],x[N]+-1*np.cos(np.arctan2(y2[N],x22[N])+np.deg2rad(90))])
    #y3=np.array([y[N],y[N]+1*np.cos(np.arctan2(y[N],x[N]))])
    y3=np.array([y[N],y[N]+1*np.sin(np.arctan2(y2[N],x22[N])+np.deg2rad(90))])
    y4=np.array([y[N],y[N]+-1*np.sin(np.arctan2(y2[N],x22[N])+np.deg2rad(90))])
'''
    # plot

#ax.set_aspect('equal', adjustable='box')
#ax.plot(ring[:,0],ring[:,1])#x[:,0], t(x[:,1]), 'g', x[:,0], x[:,1], 'b')#,x3,y3,'r',x4,y4,'m')
#ax.plot(sx,sy,sz,'r')

magplt.waitClosePlots()



    
    
