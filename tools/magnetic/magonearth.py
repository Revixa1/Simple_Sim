import numpy as np
import magsignature as magsig
import ppigrf
from datetime import datetime


lat=    45.406838
lon=   -75.552067
h= 0.01
date = datetime(2023, 10, 20)
Be,Bn,Bu=ppigrf.igrf(lon,lat,h,date)

Be=np.concatenate((Be,Bn,Bu),axis=0)
sBe= np.sqrt(Be.reshape(1,3).dot(Be))



class MagOnEarth:
