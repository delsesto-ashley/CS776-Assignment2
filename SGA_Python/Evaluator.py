
import Individual
import math
import random

def EvaluateF1(individual):
	val = 0
	values = []
	for i in range(individual.partitions):
		x = decode(individual.chromosome,int(i*individual.partitionSize),int((i+1)*individual.partitionSize))
		values.append(individual.minValue + x*individual.precision)
		val += values[i]*values[i]
	return (80 - val),val

def EvaluateF2(individual):
	val = 0
	values = []
	for i in range(individual.partitions):
		x = decode(individual.chromosome,int(i*individual.partitionSize),int((i+1)*individual.partitionSize))
		values.append(individual.minValue + x*individual.precision)
	tVal1 = values[0]*values[0] - values[1]
	tVal2 = (1-values[1])*(1-values[1])
	val = (100*tVal1*tVal1)+tVal2
	return (4000 - val),val

def EvaluateF3(individual):
	val = 0
	values = []
	for i in range(individual.partitions):
		x = decode(individual.chromosome,int(i*individual.partitionSize),int((i+1)*individual.partitionSize))
		values.append(individual.minValue + x*individual.precision)
		val += math.floor(values[i])
	return (25 - abs(int(val))),val

def EvaluateF4(individual):
	val = 0
	values = []
	for i in range(individual.partitions):
		x = decode(individual.chromosome,int(i*individual.partitionSize),int((i+1)*individual.partitionSize))
		values.append(individual.minValue + x*individual.precision)
		val1 = values[i]*values[i]
		val += (i+1)*(val1*val1)
		r = random.gauss(0,1)
		val += r
	return 10/abs(val),val

def EvaluateF5(individual):
	val = 0.002
	values = []
	for i in range(individual.partitions):
		x = decode(individual.chromosome,int(i*individual.partitionSize),int((i+1)*individual.partitionSize))
		values.append(individual.minValue + x*individual.precision)
	for j in range(individual.subParameters):
		tVal = 0
		for i in range(individual.partitions):
			tIndiv = (values[i]-individual.a[i][j])*(values[i]-individual.a[i][j])
			tVal += (tIndiv*tIndiv*tIndiv)
		val += 1/(j+1+tVal)
	return 1/val,val

def Evaluate(individual,eNum):
	lVal = []
	rVal = 0
	val = 0
	if eNum <= 1:
		rVal, val = EvaluateF1(individual)
	elif eNum == 2:
		rVal, val = EvaluateF2(individual)
	elif eNum == 3:
		rVal, val = EvaluateF3(individual)
	elif eNum == 4:
		rVal, val = EvaluateF4(individual)
	else:
		rVal, val = EvaluateF5(individual)
	return rVal, val

def decode(chrom, start, end):
	sum = 0
	for i in range(start, end):
		sum += chrom[i] * math.pow(2, i-start)
	return sum
