__author__ = 'orps'

import math
import random


from scipy.optimize import minimize

class PlantGrowing:
    def __init__(self, light=4, temperature=4, water=1, manure=1, wet=5):
        self.light = light
        self.temperature = temperature
        self.water = water
        self.manure = manure
        self.wet = wet

        self.reinit()

    def reinit(self):
        self.cost = 0
        self.beauty = 0

        #self._isValid

        self.calcLightCost()
        self.calcTempCost()

        self.calcBeauty()
        self.res = self.resultFun()


    def isValid(self):
        return self._isValid

    def getArg(self, i):
        if i == 0:
            return self.light
        if i == 1:
            return self.temperature
        if i == 2:
            return self.water
        if i == 3:
            return self.manure
        if i == 4:
            return self.wet

    def setArg(self, i, val):
        if i == 0:
            self.light = val
        if i == 1:
            self.temperature = val
        if i == 2:
            self.water = val
        if i == 3:
            self.manure = val
        if i == 4:
            self.wet = val

    def cross(self, other):
        sets = [self, other]

        result = PlantGrowing()

        for i in range(0, 5):
            num = int(random.randint(0, 1))
            result.setArg(i, sets[num].getArg(i))

        result.reinit()
        return result


    def mutate(self):
        i = random.randint(0, 1)
        if i == 0:
            self.temperature = random.randint(-4, 50)
        elif i == 1:
            self.light = random.randint(5, 900)
        elif i == 2:
            self.water = random.randint(0, 1000)
        elif i == 3:
            self.manure = random.randint(0, 1000)
        elif i == 4:
            self.wet = random.randint(0, 100)

        self.reinit()


    def calcBeauty(self):
        if self.light < 0 or self.temperature < -5:
            self.beauty = 0.0000000000001
            return

        tmp1 = math.log(1 + self.light/10, 3)
        tmp2 = 2*(math.log((self.temperature+10)/3, 2) + 1)
        tmp3 = math.log(1 + self.water/10, 3)
        tmp4 = math.log(1 + self.manure/10, 3)
        tmp5 = math.log(1 + self.wet/5, 3)

        self.beauty = tmp1*tmp2 + tmp3 + tmp4 + tmp5

    def calcTempCost(self):
        if self.temperature == -5:
            return
        if self.temperature < -5:
            self.cost += 1000
            return
        tmp = 99999
        if self.temperature <= 10:
            tmp = math.pow(self.temperature + 6, 2) + 100
        elif self.temperature <= 40:
            tmp = math.pow(self.temperature + 10, 2)

        self.cost += tmp

    def calcManureCost(self):
        self.cost += self.manure * 3

    def calcWetCost(self):
        if self.wet > 100:
            self.wet = 100

        if self.wet < 0:
            self.wet = 0

        self.cost += (pow(self.wet - 55, 2) + 300)/1.2


    def calcWaterCount(self):
        self.cost += self.water * 0.3

    def calcLightCost(self):
        tmp = math.fabs(self.light * 2) + 1
        self.cost += tmp

    def resultFun(self):
        res = self.cost / (math.pow(abs(self.beauty), 2) + 0.000001)
        if res <= 0:
            return 99999999
        return res

    def __repr__(self):
        return 'cost = {0}, beauty = {1}, light = {2}, temperature = {3}, result = {4}'.format(
            self.cost, self.beauty, self.light, self.temperature, self.resultFun())


class GeneticAlgo():
    def __init__(self):
        self.currentGenerationResult = 9999999
        self.currentGeneration = [PlantGrowing(1500, 2), PlantGrowing(7000, -5),
                                  PlantGrowing(900, 100), PlantGrowing(8000, 10),
                                  PlantGrowing(10000, 100), PlantGrowing(10, 2), PlantGrowing(4000, 80), PlantGrowing(500, 100)]
        self.nextGeneration = []
        self.iterationCount = 15

    def start(self):
        self.generateGeneration()
        if self.iterationCount > 0:
            self.iterationCount -= 1
            self.selectGeneration()
            self.start()
        else:
            print 'res is {0}, count = {1}'.format(self.currentGeneration[0], self.iterationCount)

    def generateGeneration(self):
        generation = []
        for i in range(0, len(self.currentGeneration)):
            for j in range(i + 1, len(self.currentGeneration)):
                generation.append(self.currentGeneration[i].cross(self.currentGeneration[j]))

        for i in range(0, len(generation)):
            if random.random() < 0.25:
                generation[i].mutate()

        self.nextGeneration = sorted(generation, key=lambda x: x.res)

    def selectGeneration(self):
        count = 5
        randomElementCount = 2
        generation = self.nextGeneration[0:count-randomElementCount]

        i = 0
        numlist = []
        lenNextGen = len(self.nextGeneration)
        while i < randomElementCount:
            num = random.randint(count - randomElementCount, lenNextGen-1)
            if num not in numlist:
                i += 1
                generation.append(self.nextGeneration[num])
                numlist.append(num)

        self.currentGeneration = generation


    def countGenerationResult(self, generation):
        res = 0
        listLen = len(self.currentGeneration)
        for i in range(0, listLen):
            res += self.nextGeneration[i].res

        return res / listLen


    def isNextGenerationCooler(self):
        return self.countGenerationResult(self.currentGeneration) > self.countGenerationResult(self.nextGeneration)


x = minimize(lambda args: (PlantGrowing(args[0], args[1], args[2], args[3], args[4]).resultFun()),
             [100, 40.0, 50, 10, 20], method='nelder-mead', options={'xtol': 1e-8, 'disp': True}).x
print(x[0], x[1], x[2], x[3], x[4])
plant = PlantGrowing(x[0], x[1], x[2], x[3], x[4])
print('plant: %s', plant)

g = GeneticAlgo()
g.start()


