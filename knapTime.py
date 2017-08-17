import random
import numpy
import sys
import matplotlib.pyplot as plot
from copy import deepcopy

POPULATION_SIZE = 10
MUTATION_RATE = 0.8
CROSSOVER_RATE = 0.5

GENERATION_LIMIT = 1000
GENERATION_JUMP = 10

MAX_ITEM_WEIGHT = 10
MAX_ITEM_VALUE = 100
KNAPSACK_ITEMS = 500
KNAPSACK_LIMIT = 341
KNAPSACK_OPTIONS = [[random.randrange(MAX_ITEM_VALUE), random.randrange(1, MAX_ITEM_WEIGHT)] for _ in range(KNAPSACK_ITEMS)]


# Population class holding a generation of creatures
class Population:
    def __init__(self):
        self.genNumber = 0
        self.creatures = [Creature() for _ in range(POPULATION_SIZE)]
        self.bestCreaturePlot, = plot.plot([], [])
        self.averageCreaturePlot, = plot.plot([], [])
        self.worstCreaturePlot, = plot.plot([], [])

    # Sort all the creatures by their fitness (and then by weight)
    def sortCreatures(self):
        self.creatures.sort(key=lambda c: (c.getFitness(), c.getWeight()), reverse=True)

    # Add current generation's best, average and worst creature to the graph
    def updateGraph(self):
        # Add gen number to x axis data
        self.bestCreaturePlot.set_xdata(numpy.append(self.bestCreaturePlot.get_xdata(), self.genNumber))
        self.averageCreaturePlot.set_xdata(numpy.append(self.averageCreaturePlot.get_xdata(), self.genNumber))
        self.worstCreaturePlot.set_xdata(numpy.append(self.worstCreaturePlot.get_xdata(), self.genNumber))

        # Add fitness to y axis data
        self.bestCreaturePlot.set_ydata(numpy.append(self.bestCreaturePlot.get_ydata(), self.creatures[0].getFitness()))
        self.averageCreaturePlot.set_ydata(numpy.append(self.averageCreaturePlot.get_ydata(), self.creatures[POPULATION_SIZE // 2].getFitness()))
        self.worstCreaturePlot.set_ydata(numpy.append(self.worstCreaturePlot.get_ydata(), self.creatures[-1].getFitness()))

        # Rescale graph
        axes = plot.gca()
        axes.relim()
        axes.autoscale_view()
        plot.pause(sys.float_info.epsilon)

    # Mutate the current generation of creatures
    def mutate(self):
        self.sortCreatures()
        self.genNumber += 1

        marked = 0
        # Mark half the creatures for death
        while marked != POPULATION_SIZE // 2:
            for i in range(POPULATION_SIZE):
                if random.random() > NORM_CUMULATIVE[i] or self.creatures[i].marked:
                    continue

                self.markForDeath(i)
                marked += 1
                if marked == POPULATION_SIZE // 2:
                    break

        # Breed and mutate the remaining creatures, performing parent roulette
        purgedCreatures = [c for c in self.creatures if c.marked is not True]
        mutatedCreatures = [c.breed(purgedCreatures[random.randrange(len(purgedCreatures))]) for c in purgedCreatures]
        self.creatures = purgedCreatures + mutatedCreatures

    # Mark a creature for death
    def markForDeath(self, index):
        self.creatures[index].mark()

    # Print out the current generation's stats
    def printGenerationStats(self):
        self.sortCreatures()
        bestCreature = self.creatures[0]
        averageCreature = self.creatures[POPULATION_SIZE // 2]
        worstCreature = self.creatures[-1]

        print(f'Generation {self.genNumber} | Best: {bestCreature} | Average: {averageCreature} | Worst: {worstCreature}')


# Creature class
class Creature:
    def __init__(self):
        # Randomly allocate the creature items from the knapsack options
        self.items = [1 if bool(random.getrandbits(1)) else 0 for _ in range(KNAPSACK_ITEMS)]
        self.marked = False

    # Breed the creature with a partner
    def breed(self, partner):
        offspring = deepcopy(self)
        # Take a random amount of 'genes' (items) from each parent
        offspring.items = [self.items[i] if random.random() < CROSSOVER_RATE else partner.items[i] for i in range(KNAPSACK_ITEMS)]

        # Randomly mutate the offpsring
        if random.random() < MUTATION_RATE:
            offspring.mutate()

        return offspring

    # Mutate the creature by toggling one of its items
    def mutate(self):
        self.items[random.randrange(KNAPSACK_ITEMS)] ^= 1

    # Mark the creature for death
    def mark(self):
        self.marked = True

    # Get a list of the items the creature is holding
    def getItems(self):
        return [KNAPSACK_OPTIONS[item] for item in self.items if item == 1]

    # Get the fitness score for the creature
    def getFitness(self):
        return sum([item[0] for item in self.getItems()]) if self.getWeight() <= KNAPSACK_LIMIT else -self.getWeight() + KNAPSACK_LIMIT

    # Get the weight for the creature
    def getWeight(self):
        return sum([item[1] for item in self.getItems()])

    # Print out the creature prettily
    def __str__(self):
        return str(self.getFitness()) + ' at weight ' + str(self.getWeight())


# Setup interactive plot
plot.ion()

# Generate normalised cumulative distribution of population
data = numpy.random.randn(POPULATION_SIZE)
values, _ = numpy.histogram(data, bins=POPULATION_SIZE)
cumulative = numpy.cumsum(values)
NORM_CUMULATIVE = [float(i) / max(cumulative) for i in cumulative]

# Begin evolutionary process
population = Population()
for _ in range(GENERATION_LIMIT):
    if population.genNumber % GENERATION_JUMP == 0:
        population.printGenerationStats()
        population.updateGraph()

    population.mutate()


# Wait for user input to end program
input('Press any key to exit program')