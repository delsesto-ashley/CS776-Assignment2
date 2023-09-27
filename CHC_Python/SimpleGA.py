
import random
import secrets
import Options
from Population import Population
import sys,getopt
import matplotlib.pyplot as plt
import numpy as np
import math

class Rngs:
	def __init__(self):
		self.seeds = []

	def CreateSeeds(self,numSeeds):
		if(len(self.seeds)):
			self.seeds.clear()
		for i in range(numSeeds):
			self.seeds.append(secrets.randbits(128))

class SimStats:
	def __init__(self):
		self.all = []
		self.avg = []
		self.indices = []
		self.bestChromosomes = []
		self.bestFitnesses = []
		self.bestGenerations = []
		for i in range(3):
			self.all.append([])
			self.avg.append([])
		self.lGen = 0
		self.lSeeds = 0

	def FindAvg(self):
		self.lGen = len(self.all[0][0])
		self.lSeeds = len(self.all[0])
		tNum = 0
		for x in range(3):
			for z in range(self.lGen):
				for y in range(self.lSeeds):
					tNum += self.all[x][y][z]
				tNum = tNum/self.lSeeds
				self.avg[x].append(tNum)
				tNum = 0
		for x in range(self.lGen):
			self.indices.append(x)

	def WriteToFile(self,x):
		fName = 'CHC_Function_' + str(x) + '_data.txt'
		with open(fName,'w') as f:
			f.write("Gen\t"+"Min\t" + "Max\t" + "AVG\n")
			for i in range(self.lGen):
				f.write(str(i) + "\t" + str(self.avg[0][i]) + "\t" + str(self.avg[1][i]) + "\t" + str(self.avg[2][i]) + "\n")

	def BestToFile(self,x):
		fName = 'CHC_Function_' + str(x) + '_best_chromosome_per_seed.txt'
		with open(fName,'w') as f:
			f.write("Seed IDX\t" + "Generation\t" + "Fitness\t" + "Chromosome\n")
			for i in range(self.lSeeds):
				f.write(str(i) + "\t" + str(self.bestGenerations[i]) + "\t" + str(self.bestFitnesses[i]) + "\t")
				for j in range(len(self.bestChromosomes[i])):
					f.write(str(self.bestChromosomes[i][j]) + "\t")
				f.write("\n")
class GA:

	def __init__(self,rSeed,functNum):
		self.options = Options.Options(rSeed)
		self.options.setForFunction(functNum)
		random.seed(rSeed)
		self.minList = []
		self.maxList = []
		self.avgList = []
		self.bestGen = 0
		self.bestFit = -1
		self.bestChrom = []

	def Init(self):
		self.parent = Population(self.options)
		self.parent.evaluate()
		self.parent.statistics()
		self.parent.report(0)
		self.minList.append(self.parent.min)
		self.maxList.append(self.parent.max)
		self.avgList.append(self.parent.avg)
		self.bestFit = self.parent.max
		self.bestChrom = self.parent.maxChrom
		self.child = Population(self.options)
		return

	def Run(self):
		for	i in range(1, self.options.maxGen):
			self.parent.CHCGeneration(self.child)
			self.child.statistics()
			self.child.report(i)
			self.minList.append(self.child.min)
			self.maxList.append(self.child.max)
			self.avgList.append(self.child.avg)
			if self.child.max > self.bestFit:
				self.bestFit = self.child.max
				self.bestGen = i
				self.bestChrom = self.child.maxChrom
			tmp = self.parent
			self.parent = self.child
			self.child = tmp
		self.parent.printPop()
		return


if __name__ == "__main__":
	functionNum = 1
	numSeeds = 30
	seedBank = Rngs()
	seedBank.CreateSeeds(numSeeds)
	allStats = SimStats()
	for i in range(numSeeds):
		print("Seed Number: ",seedBank.seeds[i])
		ga = GA(seedBank.seeds[i],functionNum)
		ga.Init()
		ga.Run()
		allStats.all[0].append(ga.minList)
		allStats.all[1].append(ga.maxList)
		allStats.all[2].append(ga.avgList)
		allStats.bestChromosomes.append(ga.bestChrom)
		allStats.bestFitnesses.append(ga.bestFit)
		allStats.bestGenerations.append(ga.bestGen)
	allStats.FindAvg()
	allStats.WriteToFile(functionNum)
	allStats.BestToFile(functionNum)
