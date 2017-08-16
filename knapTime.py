import random
import numpy
from bisect import bisect_left

POPULATION_SIZE = 100
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.1

KNAPSACK_OPTIONS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 25, 36, 51, 87, 129, 301]
KNAPSACK_LIMIT = 501

def getNormalisedCumulativePopulation():
    data = numpy.random.randn(POPULATION_SIZE)
    values, _ = numpy.histogram(data, bins=POPULATION_SIZE)
    cumulative = numpy.cumsum(values)
    return [float(i) / max(cumulative) for i in cumulative]


def getValidCreature():
    while True:
        creature = Creature()
        if creature.getLimit() <= KNAPSACK_LIMIT:
            break

    return creature


class Generation:
    def __init__(self):
        self.genNumber = 0
        self.creatures = [getValidCreature() for _ in range(POPULATION_SIZE)]

    def sortCreatures(self):
        self.creatures.sort(key=lambda c: c.getFitness(), reverse=True)

    def mutate(self):
        self.sortCreatures()

        mutatedCreatures = set()
        for _ in range(POPULATION_SIZE // 2):

            mutationCutoff = random.random()
            for i in range(POPULATION_SIZE):
                if NORM_CUMULATIVE[i] < mutationCutoff or i in mutatedCreatures:
                    continue

                self.creatures[i].mutate()
                mutatedCreatures.add(i)
                break

        self.genNumber += 1

    # def killCreature(self, index):
    #     self.creatures[index].kill()

    def printGenerationStats(self):
        self.sortCreatures()

        bestCreature = self.creatures[0].getFitness()
        averageCreature = self.creatures[POPULATION_SIZE // 2].getFitness()
        worstCreature = self.creatures[POPULATION_SIZE - 1].getFitness()

        print(f'Generation {self.genNumber}:')
        print(f'Best: {bestCreature}')
        print(f'Average: {averageCreature}')
        print(f'Worst: {worstCreature}')


class Creature:
    def __init__(self):
        size = random.randrange(1, len(KNAPSACK_OPTIONS))
        self.items = [KNAPSACK_OPTIONS[random.randrange(size)] for _ in range(size)]
        # self.alive = True

    def mutate(self):
        self.items[random.randrange(len(self.items))] = KNAPSACK_OPTIONS[random.randrange(len(KNAPSACK_OPTIONS))]

        if random.random() < MUTATION_RATE:
            self.items.append(KNAPSACK_OPTIONS[random.randrange(len(KNAPSACK_OPTIONS))])

        if random.random() < MUTATION_RATE and len(self.items) > 1:
            del self.items[random.randrange(len(self.items))]

    # def kill(self):
    #     self.alive = False

    # def isAlive(self):
    #     return self.alive

    def getFitness(self):
        return self.getLimit() if self.getLimit() < KNAPSACK_LIMIT else 0

    def getLimit(self):
        return sum(self.items)

NORM_CUMULATIVE = getNormalisedCumulativePopulation()

generation = Generation()
for _ in range(10000):
    generation.printGenerationStats()
    generation.mutate()
