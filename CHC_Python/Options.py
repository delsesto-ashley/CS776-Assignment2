import math
class Options:

	def __init__(self,rSeed):
		self.chromosomeLength = -1
		self.populationSize = -1
		self.maxGen = -1
		self.pCross = -1
		self.pMut = -1
		self.infile = ""
		self.randomSeed = rSeed
		self.minValue = -1
		self.maxValue = -1
		self.partitions = -1
		self.subParameters = -1
		self.evalNum = -1
		self.a = []
		self.chcLambda = 2

	def setForFunction(self,fNum):
		self.evalNum = fNum
		if fNum <= 1:
			self.populationSize = 50
			self.maxGen = 100
			self.pCross = 0.667
			self.pMut = 0.001
			self.chromosomeLength = 30
			self.minValue = -5.12
			self.maxValue = 5.11
			self.partitions = 3
		elif fNum == 2:
			self.populationSize = 50
			self.maxGen = 100
			self.pCross = 0.67
			self.pMut = 0.001
			self.chromosomeLength = 24
			self.minValue = -2.048
			self.maxValue = 2.047
			self.partitions = 2
		elif fNum == 3:
			self.populationSize = 74
			self.maxGen = 150
			self.pCross = 0.67
			self.pMut = 0.0001
			self.chromosomeLength = 50
			self.minValue = -5.12
			self.maxValue = 5.11
			self.partitions = 5
		elif fNum == 4:
			self.populationSize = 120
			self.maxGen = 250
			self.pCross = 0.67
			self.pMut = 0.001
			self.chromosomeLength = 96
			self.minValue = -1.28
			self.maxValue = 1.27
			self.partitions = 12
		else:
			self.populationSize = 50
			self.maxGen = 100
			self.pCross = 0.67
			self.pMut = 0.001
			self.chromosomeLength = 34
			self.minValue = -65.536
			self.maxValue = 65.535
			self.partitions = 2
			self.subParameters = 25
			tList1 = []
			tList2 = []
			tempList = [-32, -16, 0, 16, 32]
			for i in range(self.subParameters):
				tList1.append(tempList[i%5])
				tList2.append(tempList[int(math.floor(i/5))])
			self.a.append(tList1)
			self.a.append(tList2)


