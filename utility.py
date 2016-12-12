#!/usr/bin/env python2.7

import json, random, time, string, inspect
import os, sys, signal, io, operator


'''weights[0] is networkWeight, weights [1] is cpuWeight, weights[2] is memoryWeight, weights[3] is utility weight, weight[4] is reUse weight'''
weights = [random.randint(1,10),random.randint(1,10),random.randint(1,10),random.randint(1,10),random.randint(1,10)]


class Work():
    def __init__(self, wid):
        self.wid = wid
        self.networkCost = 0
        self.cpuCost = 0
        self.memoryCost = 0
        self.utility = 0
        self.workReuse = 0

    def getActualCost(self, weights):
        actualCost = (self.networkCost*weights[0])+(self.cpuCost*weights[1])+(self.memoryCost*weights[2])+(self.utility*weights[3])
        return actualCost

    def getActualUtility(self, weights):
        actualUtility = self.utility+(weights[4]*self.workReuse)
        return actualUtility

    def has_MoreUtility(self, utility):
        if self.utility > utility:
            return True
        return False

    def has_lessUtility(self, utility):
        if self.utility > utility:
            return False
        return True

    def get_wid(self):
        return self.wid

    def get_networkCost(self):
        return self.networkCost

    def get_cpuCost(self):
        return self.cpuCost

    def get_memoryCost(self):
        return self.memoryCost

    def get_utility(self):
        return self.utility

    def printSelf(self):
        print(self.networkCost)
        print(self.cpuCost)
        print(self.memoryCost)
        print(self.utility)
        print(self.workReuse)

################# functions that set passed in list of weights to appropriate values for the domain ######################
def getMobileWeights(weights):
    weights[0] = [5]
    weights[1] = [1]
    weights[2] = [5]
    weights[4] = [10]

'''put a higher price weight on network usage to disincentivize using the battery hungry mobile networks'''
def getLowBatteryWeights(weights):
    weights[0] = [15]
    weights[1] = [5]
    weights[2] = [5]

def getPresentationWeights(weights):
    weights[0] = [1]
    weights[1] = [2]
    weights[2] = [1]
    weights[3] = [15]
    weights[4] = [5]


def genPossibleWork():
    possWorks = []
    for i in range(5):
        workTemp = Work(i)
        workTemp.networkCost = random.randint(1,100)
        workTemp.cpuCost = random.randint(1, 100)
        workTemp.memoryCost = random.randint(1, 100)
        workTemp.utility = random.randint(50, 150)
        workTemp.workReuse = random.randint(1, 25)
        possWorks.append(workTemp)
    return possWorks


################# slide wrapper (execute only in main process) ######################
''' notes:
testing the randomly generated 'work' and each of their attribute values.
'''
def main():
    print(weights)

    genPossibleWork()

    genPossibleWork()[0].printSelf()
 
    return




if __name__ == '__main__':
    #signal.signal(signal.SIGINT, handler)

    #init()
    main()
    # main_job = mp.Process(name='main', target=main)
    # main_job.start()

