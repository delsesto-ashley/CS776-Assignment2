import random
import Utils
import math

class Individual:
	def __init__(self, options):
		self.chromosome = []
		self.chromosomeLength = options.chromosomeLength
		self.minValue = options.minValue
		self.maxValue = options.maxValue
		self.partitions = options.partitions
		self.subParameters = options.subParameters
		self.a = options.a
		self.partitionSize = int(self.chromosomeLength/self.partitions)
		self.precision = float((self.maxValue - self.minValue)/(math.pow(2,self.partitionSize)-1))
		self.fitness = -1
		self.objective = -1
		for i in range(options.chromosomeLength):
			self.chromosome.append(random.choice((0, 1)))

	def mutate(self, options):
		for i in range(options.chromosomeLength):
			if Utils.flip(options.pMut):
				self.chromosome[i] = 1 - self.chromosome[i]

	def myCopy(self, ind):
		self.fitness = ind.fitness
		self.chromosomeLength = ind.chromosomeLength # this should not change!
		self.objective = ind.objective
		for i in range(self.chromosomeLength):
			self.chromosome[i] = ind.chromosome[i]

