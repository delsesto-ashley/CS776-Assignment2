
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
		self.allObj = []
		self.avg = []
		self.avgObj = []
		self.indices = []
		self.bestChromosomes = []
		self.bestFitnesses = []
		self.bestGenerations = []
		for i in range(3):
			self.all.append([])
			self.avg.append([])
			self.allObj.append([])
			self.avgObj.append([])
		self.lGen = 0
		self.lSeeds = 0

	def FindAvg(self):
		self.lGen = len(self.all[0][0])
		self.lSeeds = len(self.all[0])
		tNum = 0
		tNum1 = 0
		for x in range(3):
			for z in range(self.lGen):
				for y in range(self.lSeeds):
					tNum += self.all[x][y][z]
					tNum1 += self.allObj[x][y][z]
				tNum = tNum/self.lSeeds
				tNum1 = tNum1/self.lSeeds
				self.avg[x].append(tNum)
				self.avgObj[x].append(tNum1)
				tNum = 0
				tNum1 = 0
		for x in range(self.lGen):
			self.indices.append(x)

	def MakeGraph(self,x,fType):
		X = np.asarray(self.indices)
		Y = []
		if fType:
			for i in range(3):
				Y.append(np.asarray(self.avg[i]))
		else:
			for i in range(3):
				Y.append(np.asarray(self.avgObj[i]))
		plt.plot(X,Y[0],color='r',label='min')
		plt.plot(X,Y[1],color='g',label='max')
		plt.plot(X,Y[2],color='b',label='avg')
		plt.legend()
		plt.xlabel("Generation")
		if fType:
			plt.ylabel("Fitness")
			plt.title("Fitness Graph for Function " + str(x))
			plt.savefig("Fitness_Function_" + str(x) + ".png")
		else:
			plt.ylabel("Output")
			plt.title("Objective Function Graph for Function " + str(x))
			plt.savefig("Objective_Function_" + str(x) + ".png")
		plt.clf()

	def WriteToFile(self,x):
		fName = 'SGA_Function_' + str(x) + '_data.txt'
		with open(fName,'w') as f:
			f.write("Gen\t"+"Min\t" + "Max\t" + "AVG\n")
			for i in range(self.lGen):
				f.write(str(i) + "\t" + str(self.avg[0][i]) + "\t" + str(self.avg[1][i]) + "\t" + str(self.avg[2][i]) + "\n")

	def BestToFile(self,x):
		fName = 'SGA_Function_' + str(x) + '_best_chromosome_per_seed.txt'
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
		self.minObjList = []
		self.maxObjList = []
		self.avgObjList = []

	def Init(self):
		self.parent = Population(self.options)
		self.parent.evaluate()
		self.parent.statistics()
		self.parent.report(0)
		self.minList.append(self.parent.min)
		self.maxList.append(self.parent.max)
		self.avgList.append(self.parent.avg)
		self.minObjList.append(self.parent.minObj)
		self.maxObjList.append(self.parent.maxObj)
		self.avgObjList.append(self.parent.avgObj)
		self.bestFit = self.parent.max
		self.bestChrom = self.parent.maxChrom
		self.child = Population(self.options)
		return

	def Run(self):
		for	i in range(1, self.options.maxGen):
			self.parent.generation(self.child)
			self.child.evaluate()
			self.child.statistics()
			self.child.report(i)
			self.minList.append(self.child.min)
			self.maxList.append(self.child.max)
			self.avgList.append(self.child.avg)
			self.minObjList.append(self.child.minObj)
			self.maxObjList.append(self.child.maxObj)
			self.avgObjList.append(self.child.avgObj)
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
	functionNum = 4
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
		allStats.allObj[0].append(ga.minObjList)
		allStats.allObj[1].append(ga.maxObjList)
		allStats.allObj[2].append(ga.avgObjList)
		allStats.bestChromosomes.append(ga.bestChrom)
		allStats.bestFitnesses.append(ga.bestFit)
		allStats.bestGenerations.append(ga.bestGen)
	allStats.FindAvg()
	allStats.WriteToFile(functionNum)
	allStats.BestToFile(functionNum)
	allStats.MakeGraph(functionNum,0)
	allStats.MakeGraph(functionNum,1)
