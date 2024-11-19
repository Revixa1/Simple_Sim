import numpy as np
import dipole
from datetime import datetime
import ppigrf
from icecream import ic

lat=    45.406838
lon=   -75.552067
h= 0.0
date = datetime(2023, 10, 20)
Be,Bn,Bu=ppigrf.igrf(lon,lat,h,date)

Be=np.concatenate((Be,Bn,Bu),axis=0)

sBe= np.sqrt(Be.reshape(1,3).dot(Be))


R=np.array([0,0,1]).reshape(3,1)
sR=np.sqrt(R.reshape(1,3).dot(R))


dipole1=dipole.Dipole(0,0,1,0,0,0)
dipole1.set_sensorVector(R)
dipole1.get_vB()
dipole1.get_sB()
out=np.sqrt((dipole1.B+Be)**2)
sout=np.sqrt(out.reshape(1,3).dot(out))


ic(sBe*np.sqrt(1+2*((dipole1.B.reshape(1,3).dot(Be)**2)/(sBe**2))+(dipole1.sB**2/sBe**2)))
bsout=sBe*np.sqrt(1+2*((dipole1.B.reshape(1,3).dot(Be)**2)/(sBe**2))+(dipole1.sB**2/sBe**2))
ic(sout)
ic(sout-sBe)

Tyout= sBe+(dipole1.B.reshape(1,3).dot(Be)/sBe)+(dipole1.sB/sBe)**2
ic(Tyout)

ic(sout==Tyout)


TFperm=(3*(dipole1.m.reshape(1,3).dot(R))*(R.reshape(1,3).dot(Be))/(sBe*sR**5))-(dipole1.m.reshape(1,3).dot(Be)/(sBe*sR**3))
ic(TFperm)

TF=((4*np.pi*1e-7)/(4*np.pi*sBe))*((3*(dipole1.m.reshape(1,3).dot(R))*(R.reshape(1,3).dot(Be))/(sR**5))-(dipole1.m.reshape(1,3).dot(Be)/(sR**3)))
ic(TF)
