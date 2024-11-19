#test unitaire dipole pour les bons signes
'''
	description: 	Test de la classe dipole afin de déterminer si le champ B et les coeff du TotalField 
					sont correct dans leur amplitude et leur signe.
					Test sans champ de la terre et avec(TFperm).
'''
import numpy as np
import matplotlib.pyplot as plt
from icecream import ic
from matplotlib import cm
from matplotlib.ticker import EngFormatter

import dipole
import magsignature as magsig

import ppigrf
from datetime import datetime

import plotly.graph_objects as go




lat=    45.406838
lon=   -75.552067
h= 0.0
date = datetime(2023, 10, 20)
Be,Bn,Bu=ppigrf.igrf(lon,lat,h,date)

Be=np.concatenate((Be,Bn,Bu),axis=0)*1e-9

sBe= np.sqrt(Be.reshape(1,3).dot(Be))




lowdist,highdist,ddist=-3,3,0.1
zlowdist,zhighdist,zddist=-1,1,2
datapoints=int((highdist- lowdist)/ddist)+1
zdatapoints=int((zhighdist- zlowdist)/zddist)+1
#ic(datapoints)

dipolex=dipole.Dipole(1e-9,0,0,0,0,0,0,0,0)
dipoley=dipole.Dipole(0,1e-9,0,1,0,0)
dipolez=dipole.Dipole(0,0,1e-9,0,0,0)


magsig1=magsig.MagSignature([0,0,0])
magsig1.newDipole(dipolex)
#ic(dipolex.m)
#ic( np.arange(-1,1.1,2))
#ic(np.arange(lowdist,highdist+ddist,ddist).shape)




#figx=plt.figure()

#ax=figx.add_subplot(1,1,1,projection='3d')

#ax.set(xlabel="X",ylabel="Y",title="X moment isolated scalar")


rz=-1#<-------------------------------------------------------------------------Distance in z of the sensor


figxTF=plt.figure()
axtf=figxTF.add_subplot(1,1,1)
axtf.set(xlabel="X",ylabel="Y",title="X moment as TF at height"+str(rz))

figy=plt.figure()
ay=figy.add_subplot(1,1,1)
ay.set(xlabel="X",ylabel="Y",title="Y moment isolated scalar  at height"+str(rz))

figz=plt.figure()
az=figz.add_subplot(1,1,1)
az.set(xlabel="X",ylabel="Y",title="Z moment isolated scalar  at height"+str(rz))

figzTF=plt.figure()
aztf=figzTF.add_subplot(1,1,1)
aztf.set(xlabel="X",ylabel="Y",title="Z moment as TF  at height"+str(rz))


X1=np.zeros((datapoints*datapoints**zdatapoints),dtype=float)
Y1=np.zeros((datapoints*datapoints**zdatapoints),dtype=float)
Z1=np.zeros((datapoints*datapoints**zdatapoints),dtype=float)
Z1x=np.zeros((datapoints*datapoints**zdatapoints),dtype=float)
Z1y=np.zeros((datapoints*datapoints**zdatapoints),dtype=float)
Z1z=np.zeros((datapoints*datapoints**zdatapoints),dtype=float)
#ic(X1.shape)

X11=np.zeros((datapoints,datapoints),dtype=float)
Y11=np.zeros((datapoints,datapoints),dtype=float)
Z11=np.zeros((datapoints,datapoints),dtype=float)

X2=np.zeros((datapoints,datapoints),dtype=float)
Y2=np.zeros((datapoints,datapoints),dtype=float)
Z2=np.zeros((datapoints,datapoints),dtype=float)

X3=np.zeros((datapoints,datapoints),dtype=float)
Y3=np.zeros((datapoints,datapoints),dtype=float)
Z3=np.zeros((datapoints,datapoints),dtype=float)

X31=np.zeros((datapoints,datapoints),dtype=float)
Y31=np.zeros((datapoints,datapoints),dtype=float)
Z31=np.zeros((datapoints,datapoints),dtype=float)




ix=0

X=np.arange(lowdist,highdist+ddist,ddist)
Y=np.arange(lowdist,highdist+ddist,ddist)
Z=np.arange(lowdist,highdist+ddist,ddist)

X,Y,Z= np.meshgrid(X,Y,Z)
#ic(Z)

for rx in np.arange(lowdist,highdist+ddist,ddist):
	iy=0
	for ry in np.arange(lowdist,highdist+ddist,ddist):

		dipolex.set_sensorVector([rx,ry,rz])
		dipoley.set_sensorVector([rx,ry,rz])
		dipolez.set_sensorVector([rx,ry,rz])

		magsig1.set_TranslationMatrix(rx,ry,rz)
		magsig1.set_Sensor_Vector()
		magsig1.resB()

		dipolex.get_C()
		dipolez.get_C()
		#ic(dipolez.C1[0,0])

		#xB=dipolex.get_vB()
		#X1[ix,iy]=rx
		#Y1[ix,iy]=ry
		#Z1x[ix,iy]=xB[0,0]
		#Z1y[ix,iy]=xB[1,0]
		#Z1z[ix,iy]=xB[2,0]


		X11[ix,iy]=rx
		Y11[ix,iy]=ry
		Z11[ix,iy]=magsig1.TF#dipolex.C1[0,0]*Be[0,0]/sBe[0,0]+dipolex.C2[0,0]*Be[1,0]/sBe[0,0]+dipolex.C3[0,0]*Be[2,0]/sBe[0,0]
		
		X2[ix,iy]=rx
		Y2[ix,iy]=ry
		Z2[ix,iy]=dipoley.get_sB()

		X3[ix,iy]=rx
		Y3[ix,iy]=ry
		Z3[ix,iy]=dipolez.get_sB()
		
		X31[ix,iy]=rx
		Y31[ix,iy]=ry
		Z31[ix,iy]=dipolez.C1[0,0]*Be[0,0]/sBe[0,0]+dipolez.C2[0,0]*Be[1,0]/sBe[0,0]+dipolez.C3[0,0]*Be[2,0]/sBe[0,0]

		
		#ic(Z.shape)
		#ic(X)
		
		iy+=1
	ix+=1

iz=0
ix=0
iy=0
for rz in np.arange(zlowdist,zhighdist+zddist,zddist):
	for rx in np.arange(lowdist,highdist+ddist,ddist):		
		for ry in np.arange(lowdist,highdist+ddist,ddist):
	
			dipolex.set_sensorVector([rx,ry,rz])
			
			xB=dipolex.get_vB()
			X1[iy]=rx
			Y1[iy]=ry
			Z1[iy]=rz
			Z1x[iy]=xB[0,0]
			Z1y[iy]=xB[1,0]
			Z1z[iy]=xB[2,0]
			#ic(xB[0,0])
			#ic(Z1x.shape)
			iy+=1
		
		ix+=1
#iz+=1


df={
	"x":X1,
	"y":Y1,
	"z":Z1,
	'u':Z1x,
	'v':Z1y,
	'w':Z1z
	
}

#ic(df)

fig = go.Figure(data=go.Cone(
    x=df["x"],
    y=df["y"],
    z=df["z"],
    u=df["u"],
    v=df["v"],
   	w=df["w"],
    sizemode="scaled",
    sizeref=10))

fig.update_layout(
      scene=dict(domain_x=[0, 1],
                 camera_eye=dict(x=-1.57, y=1.36, z=0.58)))

fig.show()

#ax.quiver(X,Z,Y,Z1x,Z1y,Z1z,length=0.1)
axtf.contour(X11,Y11,Z11,50)

ay.contour(X2,Y2,Z2,20)

az.contour(X3,Y3,Z3,20)
aztf.contour(X31,Y31,Z31,20)

plt.show(block=False)
plt.pause(0.01)

fignums=plt.get_fignums()
#ic(len(fignums))
while(len(fignums)==len(plt.get_fignums())):
	#ic(len(plt.get_fignums()))
	plt.pause(1)
	plt.pause(0.1)

plt.close("all")


#ic(len(plt.get_fignums()))
	
				
	

