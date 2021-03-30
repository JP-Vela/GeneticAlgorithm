import hashlib
import random as rand
import string
import argparse

#----------------------Full ASCII Table In One String----------------------
characters =  string.punctuation
characters+=string.ascii_letters
characters+=string.digits
characters+=" "

#----------------------Genetic Variables----------------------
popSize = 100
scores = [0]*popSize
population = []

mutationRate = 0.03 # 5% of members are mutated

targetStr = ""
target = ""
individualLength = 0

#----------------------Arguments----------------------

parser = argparse.ArgumentParser()
parser.add_argument('--target', help='foo help')
args = parser.parse_args()


#----------------------MD5 Hashing Algorithm----------------------

def getMD5Hash(psw):
    hash_obj = hashlib.md5( bytes(psw,'utf-8' ) )
    return hash_obj.hexdigest()


targetStr=args.target
target = getMD5Hash(targetStr)
individualLength = len(targetStr)

#----------------------Classes---------------------- 

class Individual:
    def __init__(self):
        self.genes = ""
    
    #@staticmethod
    def setGenes(self,genesString):
        self.genes=genesString

    #@staticmethod
    def getGenes(self):
        return self.genes

#----------------------First Population Funtions---------------------- 

def getRandGene():
    return rand.choice(characters)

def getRandIndividual():
    geneString = ""
    for i in range(individualLength):
        geneString+=getRandGene()

    return geneString

def genBoomers():
    print("Initializing Gen Boomers...")

    for i in range(popSize):
        member = Individual()
        member.setGenes(getRandIndividual())
        population.append(member)

    print("Boomers Initialized")


#----------------------Fitness Functions----------------------

def getFitness(member):
    score=0
    '''member.getGenes()
        targetStr[i]:'''
    genes = member.getGenes()

    for i in range(individualLength):
        if genes[i]==targetStr[i]:#target[i]:
            score+=1

    return score


def setFitnessScores():
    newScores=[0]*popSize
    found=False

    for i in range(popSize):
        newScores[i]=getFitness(population[i])

    if newScores[i]==individualLength:
        found=True

    return found,newScores


def getBestFit():
    highScore = max(scores)

    for i in range(popSize):
        if scores[i]==highScore:
            return i, highScore

    return -1

#----------------------Natural Selection , Crossover, Mutation----------------------

# Selection &  Crossover
def crossover():

    bestFit, highScore = getBestFit()
    parents = []

    print (population[bestFit].getGenes()+""+"\t"+str(highScore))

    scores[bestFit] = 0
    secondBestFit, secondScore = getBestFit()
    scores[bestFit] = highScore

    parents.append(population[bestFit])
    parents.append(population[secondBestFit])

    newGen = []

    #print(parents[0].getGenes())
    #print(parents[1].getGenes())


    for i in range(popSize):
        alpha = Individual()
        alphaGenes = ""

        for j in range(individualLength):
            if rand.random()<0.5:
                alphaGenes+=parents[0].getGenes()[j]
            else:
                alphaGenes+=parents[1].getGenes()[j]

        alpha.setGenes(alphaGenes)
        alphaGenes=""
        newGen.append(alpha)

    newGen[0]=population[bestFit]
    newGen[1]=population[secondBestFit]

    return newGen

# Mutation
def mutate():
    newGen = crossover()

    for i in range(popSize):
        curGenes = newGen[i].getGenes()
        if(i==0 or i==1): continue

        for j in range(individualLength):
            randomNum =rand.random()

            if randomNum<mutationRate:
                index = j
                randomChar = getRandGene()
                curGenes=curGenes[:index]+randomChar+curGenes[index+1:]

        newMember = Individual()
        newMember.setGenes(curGenes)
        newGen[i]=newMember

    newPopulation=newGen

    return newPopulation

genBoomers()


genNum = 0

while True:
    
    #print("---------------------New Generation----------------------")
    found, scores=setFitnessScores()
    if(found):
        print("Found in "+str(genNum))
        break
    population=mutate()
    genNum+=1