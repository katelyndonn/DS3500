"""
Avril Mauro & Katelyn Donn
DS 3500 Homework 5 Rabbit & Fox Animation
field.py
April 14th, 2023
"""

import matplotlib.pyplot as plt
import numpy as np


class Field:
    """ A field is a patch of grass with 0 or more animals hopping around
    in search of grass """

    def __init__(self, size, grassrate):
        """ Create a patch of grass with dimensions SIZE x SIZE
        and initially no animals """
        self.size = size # field size
        self.grassrate = grassrate # rate at which grass grows back
        self.field = np.ones(shape=(size, size), dtype=int) # field of grass
        self.animals = [] # list of Animal (a) objects
        self.gen = 0 # generation counter

        self.rabbits = [] # list of rabbit objects
        self.foxes = [] # list of fox objects
        self.rabbit_pos = [(a.x, a.y) for a in self.rabbits]  # rabbit positions
        self.fox_pos = [(a.x, a.y) for a in self.foxes] # fox positions

        self.ngrass = [] # number of grass positions
        self.nrabbits = [] # number of rabbits
        self.nfoxes = [] # number of foxes

    def add_animal(self, animal):
        """ A new animal is added to the field """
        self.animals.append(animal)
        self.update_animals()

    def update_animals(self):
        """ Updates list of rabbits and list of foxes and their positions """
        self.rabbits = [a for a in self.animals if a.m == 2]
        self.foxes = [a for a in self.animals if a.m == 3]
        self.rabbit_pos = [(a.x, a.y) for a in self.rabbits]
        self.fox_pos = [(a.x, a.y) for a in self.foxes]

    def move(self):
        """ Moves each animal """
        for a in self.animals:
            a.move()
            # every time the animal moves (once per generation),
            # they become hungry again, so eaten resets to 0
            a.eaten = 0

        # update the positions of the animals
        self.update_animals()

    def eat(self):
        """ Each animal eats if they encounter a prey """
        for a in self.animals:
            # check the field to see if an animal runs into a prey
            if self.field[a.x, a.y] in a.eats:
                # eat the prey
                a.eat(1)
                # if the prey is grass, make the spot an empty ground (ex: rabbit vs. grass)
                if self.field[a.x, a.y] == 1:
                    self.field[a.x, a.y] = 0
                else:
                    # else, replace the prey with the predator (ex: fox vs. rabbit)
                    self.field[a.x, a.y] = a.m

    def survive(self):
        """ Rabbits who eat some grass live to eat another day, and
            Foxes who eat some rabbits in k gens live to eat another day """

        # empty list of survivors
        survivors = []
        for a in self.animals:
            # if k generations have passed in a cycle
            if (self.gen+1 % a.k_starve == 0):
                # animal survives if it has eaten
                if a.eaten > 0:
                    survivors.append(a)
            else:
                # animal always survives between k cycle checks
                survivors.append(a)

        # overwrite animal list to be survivors
        self.animals = survivors
        # update rabbit and fox lists and their positions
        self.update_animals()

    def reproduce(self):
        """ Animals reproduce up to their max offspring if they have eaten """
        for a in self.animals:
            # if animal has eaten
            if a.eaten > 0:
                # add a hungry copy of the animal, repeat for multiple offspring
                for _ in range(0, a.max_offspring):
                    self.animals.append(a.reproduce())

        # update rabbit and fox lists and their positions
        self.update_animals()

        # record number of foxes, rabbits, and grass for history records
        self.nrabbits.append(self.num_rabbits())
        self.nfoxes.append(self.num_foxes())
        self.ngrass.append(self.amount_of_grass())

    def grow(self):
        """ Grass grows back with some probability """
        growloc = (np.random.rand(self.size, self.size) < self.grassrate) * 1
        self.field = np.maximum(self.field, growloc)

    def update_field(self):
        """ Updates field positions of rabbits (2's) and foxes (3's) """
        for r in self.rabbit_pos:
            self.field[r] = 2
        for f in self.fox_pos:
            self.field[f] = 3

    def num_rabbits(self):
        """ How many rabbits are there in the field ? """
        return len(self.rabbits)

    def num_foxes(self):
        """ How many foxes are there in the field ? """
        return len(self.foxes)

    def amount_of_grass(self):
        return self.field.sum()

    def generation(self):
        """ Run one generation of rabbits """
        self.move()
        self.eat()
        self.survive()
        self.reproduce()
        self.grow()

        self.update_field()

        self.gen += 1
        if self.gen > 1000:
            self.history()

    def history(self, showTrack=True, showPercentage=True, marker='.'):
        """ Plots % population over generations """

        # initialize figure and graph labels
        plt.figure(figsize=(15, 7))
        plt.xlabel("generation #")
        plt.ylabel("% population")

        # collect population records
        rs = self.nrabbits[:]
        fs = self.nfoxes[:]
        gs = self.ngrass[:]
        if showPercentage:
            maxrabbit = max(rs)
            rs = [r / maxrabbit for r in rs]
            maxfoxes = max(fs)
            fs = [f / maxfoxes for f in fs]
            maxgrass = max(gs)
            gs = [g / maxgrass for g in gs]

        # plot population records over time (generations)
        if showTrack:
            plt.plot(range(self.gen), rs, label='rabbits')
            plt.plot(range(self.gen), fs, label='foxes')
            plt.plot(range(self.gen), gs, label='grass')

        # show grid, legend, title, and save the png of the graph
        plt.grid()
        plt.legend()
        plt.title("Population vs. TIME: GROWTH RATE =" + str(self.grassrate))
        plt.savefig("history.png", bbox_inches='tight')
        plt.show()
