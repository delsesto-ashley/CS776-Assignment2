
import Individual
import Evaluator
import random
import Utils

class Population(object):

	def	__init__(self, options):
		self.options = options
		self.individuals = []
		self.min = -1
		self.max = -1
		self.avg = -1
		self.minObj = -1
		self.maxObj = -1
		self.avgObj = -1
		self.maxChrom = []
		# initialize population with randomly generated Individuals
		for i in range(options.populationSize):
			self.individuals.append(Individual.Individual(options))
		self.evaluate()

	def evaluate(self):
		for ind in self.individuals:
			ind.fitness, ind.objective = Evaluator.Evaluate(ind,self.options.evalNum)
			
	def printPop(self):
		i = 0
		for ind in self.individuals:
			print(i, end=": ")
			print (ind.chromosome, " Fit: ", ind.fitness)
			i = i+1
		self.report("")

	def report(self, gen):
		print (gen, self.min, self.avg, self.max)

	def statistics(self):
		self.sumFitness = 0
		self.sumObjective = 0
		self.min = self.individuals[0].fitness
		self.max = self.individuals[0].fitness
		self.minObj = self.individuals[0].objective
		self.maxObj = self.individuals[0].objective
		self.avg = 0
		self.avgObj = 0
		for ind in self.individuals:
			self.sumFitness += ind.fitness
			self.sumObjective += ind.objective
			if ind.fitness < self.min:
				self.min = ind.fitness
			if ind.fitness > self.max:
				self.max = ind.fitness
				self.maxChrom = ind.chromosome
			if ind.objective < self.minObj:
				self.minObj = ind.objective
			if ind.objective > self.maxObj:
				self.maxObj = ind.objective
		self.avg = self.sumFitness/len(self.individuals)
		self.avgObj = self.sumObjective/len(self.individuals)

	def select(self):
		randFraction = self.sumFitness * random.random()
		sum = 0
		i = 0
		for ind in self.individuals:
			sum += ind.fitness
			if randFraction <= sum:
				return (i, ind)
			i = i + 1
		print("Selection failed")
		return (len(self.individuals) - 1, self.individuals[-1])

	def generation(self, child):
		for i in range(0, len(self.individuals), 2):
			x, p1 = self.select()
			x, p2 = self.select()
			c1 = child.individuals[i]
			c2 = child.individuals[i + 1]
			self.xover1Pt(p1, p2, c1, c2)			
			c1.mutate(self.options)
			c2.mutate(self.options)

	def xover1Pt(self, p1, p2, c1, c2):
		for i in range(self.options.chromosomeLength):
			c1.chromosome[i] = p1.chromosome[i]
			c2.chromosome[i] = p2.chromosome[i]
		if Utils.flip(self.options.pCross):
			xp = Utils.randInt(1, self.options.chromosomeLength)
			for i in range(xp, self.options.chromosomeLength):
				c1.chromosome[i] = p2.chromosome[i]
				c2.chromosome[i] = p1.chromosome[i]
