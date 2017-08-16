import random
import numpy
from copy import deepcopy

POPULATION_SIZE = 100
MUTATION_RATE = 0.001
CROSSOVER_RATE = 0.1

KNAPSACK_OPTIONS = [[random.randrange(i*20), random.randrange(i*10)] for i in range(1,301)]
KNAPSACK_LIMIT = 3418
GENERATION_LIMIT = 10000

#TODO(mitch): add values to the weights
#TODO(mitch): incorporate crossover (two parents roulette?)
#TODO(mitch): do better mutation
#TODO(mitch): convert to bit array

def getNormalisedCumulativePopulation():
    data = numpy.random.randn(POPULATION_SIZE * 10)
    values, _ = numpy.histogram(data, bins=POPULATION_SIZE)
    cumulative = numpy.cumsum(values)
    return [float(i) / max(cumulative) for i in cumulative]


def getValidCreature():
    while True:
        creature = Creature()
        if creature.getWeight() <= KNAPSACK_LIMIT:
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
        bestCreature = self.creatures[0]
        averageCreature = self.creatures[POPULATION_SIZE // 2]
        worstCreature = self.creatures[POPULATION_SIZE - 1]

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
        return sum(item[0] for item in self.items) if self.getWeight() < KNAPSACK_LIMIT else 0

    def getWeight(self):
        return sum(item[1] for item in self.items)

    def __str__(self):
        return str(self.getFitness()) + ' at weight ' + str(self.getWeight())


NORM_CUMULATIVE = getNormalisedCumulativePopulation()

generation = Generation()
generation.printGenerationStats()
for _ in range(GENERATION_LIMIT):
    generation.mutate()
    generation.printGenerationStats()
