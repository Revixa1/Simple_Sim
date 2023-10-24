import numpy as np
import dipole
import geometry as geo
from icecream import ic

class MagSignature:


	
	def __init__(self):
		self.dipolelist = []
		self.aTb=self.set_TranslationMatrix()

	def loadFromCSV(self,filename):
		pass

	def newDipole(self,dipole):
		self.dipolelist.append(dipole)

	def set_Sensor_Vector(self):
		#ic(self.dipolelist)
		for i in self.dipolelist:
			#ic(i.get_Dipole_pos())
			
			i.set_sensorVector(geo.Transformation(self.aTb,np.array([0,0,0]).reshape(3,1)-i.get_Dipole_pos()))
			#ic(i.r_vector)
			
		
	def set_TranslationMatrix(self,x=0,y=0,z=0,thetax=0,thetay=0,thetaz=0):
		self.aTb=geo.TranslationMatrix(thetax,thetay,thetaz,x,y,z)
		#ic(self.aTb)
		
	def resB(self):
		phresB=0
		for i in self.dipolelist:
			#ic(i.get_vB())
			phresB=phresB+i.get_vB()
		#ic(phresB)
		self.resultantB=phresB
		self.res_sB=np.linalg.norm(self.resultantB)
		return self.resultantB
