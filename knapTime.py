import random
import numpy
from copy import deepcopy

POPULATION_SIZE = 100
MUTATION_RATE = 0.05
CROSSOVER_RATE = 0.1

KNAPSACK_OPTIONS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 25, 36, 51, 87, 129, 301]
KNAPSACK_LIMIT = 44
GENERATION_LIMIT = 50

def getNormalisedCumulativePopulation():
    data = numpy.random.randn(POPULATION_SIZE * 10)
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

        marked = 0
        while marked != POPULATION_SIZE // 2:
            markCutoff = random.random()
            for i in range(POPULATION_SIZE):
                if NORM_CUMULATIVE[i] < markCutoff or self.creatures[i].marked:
                    continue

                self.markForDeath(i)
                marked += 1
                break

        purgedCreatures = [c for c in self.creatures if c.marked is not True]
        mutatedCreatures = [c.mutate() for c in purgedCreatures]

        self.creatures = purgedCreatures + mutatedCreatures
        self.genNumber += 1

    def markForDeath(self, index):
        self.creatures[index].mark()

    def printGenerationStats(self):
        self.sortCreatures()

        creatures = [c.getFitness() for c in self.creatures]
        bestCreature = self.creatures[0].getFitness()
        averageCreature = self.creatures[POPULATION_SIZE // 2].getFitness()
        worstCreature = self.creatures[POPULATION_SIZE - 1].getFitness()

        print(f'Generation {self.genNumber}:')
        print(f'{creatures}\n')
        print(f'Best: {bestCreature}')
        print(f'Average: {averageCreature}')
        print(f'Worst: {worstCreature}\n\n')


class Creature:
    def __init__(self):
        size = random.randrange(1, len(KNAPSACK_OPTIONS))
        self.items = [KNAPSACK_OPTIONS[random.randrange(size)] for _ in range(size)]
        self.marked = False

    def mutate(self):
        mutation = deepcopy(self)

        mutationNumber = random.random()
        if mutationNumber < MUTATION_RATE and len(mutation.items) > 1:
            del mutation.items[random.randrange(len(mutation.items))]

        elif mutationNumber < 3 * MUTATION_RATE and mutationNumber > MUTATION_RATE:
            mutation.items.append(KNAPSACK_OPTIONS[random.randrange(len(KNAPSACK_OPTIONS))])

        else:
            mutation.items[random.randrange(len(mutation.items))] = KNAPSACK_OPTIONS[random.randrange(len(KNAPSACK_OPTIONS))]

        return mutation

    def mark(self):
        self.marked = True

    def getFitness(self):
        return self.getLimit() if self.getLimit() < KNAPSACK_LIMIT else 0

    def getLimit(self):
        return sum(self.items)


NORM_CUMULATIVE = getNormalisedCumulativePopulation()

generation = Generation()
generation.printGenerationStats()
for _ in range(GENERATION_LIMIT):
    generation.mutate()
    generation.printGenerationStats()
