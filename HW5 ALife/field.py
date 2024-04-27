import matplotlib.pyplot as plt
import numpy as np
import random as rnd
import copy
import seaborn as sns
from animal import Animal

GRASS_RATE, SIZE, F_INITIAL, R_INITIAL = .025, 5, 20, 20
class Field:
    """ A field is a patch of grass with 0 or more animals hopping around
    in search of grass """

    def __init__(self, size):
        """ Create a patch of grass with dimensions SIZE x SIZE
        and initially no animals """
        self.size = size
        self.field = np.ones(shape=(size, size), dtype=int)
        self.animals = [] # list of Animal (a) objects
        self.gen = 0

        # rabbit objects, rabbit positions
        self.rabbits = [a for a in self.animals if a.m == 2]
        self.rabbit_pos = [(a.x, a.y) for a in self.rabbits]

        # fox objects, fox positions
        self.foxes = [a for a in self.animals if a.m == 3]
        self.fox_pos = [(a.x, a.y) for a in self.foxes]

        # history purposes
        self.ngrass = []
        self.nrabbits = []
        self.nfoxes = []

    def add_animal(self, animal):
        """ A new animal is added to the field """
        self.animals.append(animal)

    def update_animals(self):
        self.rabbits = [a for a in self.animals if a.m == 2]
        self.rabbit_pos = [(a.x, a.y) for a in self.rabbits]
        self.foxes = [a for a in self.animals if a.m == 3]
        self.fox_pos = [(a.x, a.y) for a in self.foxes]

    def move(self):
        """ animals move """
        for a in self.animals:
            a.move()
            a.eaten = 0

        self.update_animals()

    def eat(self):
        """ Rabbits eat (if they find grass where they are) """
        self.update_animals()
        same_loc = [pos for pos in self.fox_pos if pos in self.rabbit_pos]

        for r in self.rabbits:
            # rabbits eat if they find grass where they are
            r.eat(1)
            self.field[r.x, r.y] = 0
            # self.reproduce_animal(m=r.m)

            # rabbits die if they run into a fox
            if (r.x, r.y) in same_loc:
                self.rabbits.remove(r)

        for f in self.foxes:
            if (f.x, f.y) in same_loc:
                f.eat(1)
                self.field[f.x, f.y] = 3
                # self.reproduce_animal(m=f.m)

                # FIX NUM FOXES
                # self.nfoxes.append(self.num_foxes())


    def survive(self):
        """ Rabbits who eat some grass live to eat another day """

        survivors = []
        for a in self.animals:

            # check k_starve cycles
            if a.k_starve > 0:
                if (self.gen % a.k_starve == 0) and (a.eaten > 0):
                    survivors.append(a)
            else:
                if a.eaten > 0:
                    survivors.append(a)

        self.animals = survivors
        self.update_animals()

    def reproduce(self):
        f_born = [f.reproduce() for f in self.foxes if (f.eaten > 0)]
        r_born = [r.reproduce() for r in self.rabbits]
        self.animals += f_born
        self.animals += r_born


    # FIX N ANIMALS AND NUMS
        self.nrabbits.append(self.num_rabbits())
        # self.ngrass.append(self.amount_of_grass())
        self.nfoxes.append(self.num_foxes())
    # self.ngrass.append(self.amount_of_grass())

    def grow(self):
        """ Grass grows back with some probability """
        growloc = (np.random.rand(self.size, self.size) < GRASS_RATE) * 1
        self.field = np.maximum(self.field, growloc)

    def get_rabbits(self):
        rabbits = np.zeros(shape=(self.size, self.size), dtype=int)
        for r in self.rabbits:
            rabbits[r.x, r.y] = 2
        return rabbits

    def get_foxes(self):
        foxes = np.zeros(shape=(self.size, self.size), dtype=int)
        for f in self.foxes:
            foxes[f.x, f.y] = 3
        return foxes

    def update_field(self):
        r_array = self.get_rabbits()
        f_array = self.get_foxes()

        self.field += r_array
        self.field += f_array
        # print(self.field)

        for l in self.field:
            for loc in l:
                if loc >= 5:
                    loc = 3

                    print(self.field)

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

        # for fox in self.foxes:
        #     if fox.eaten > 0:
        #         self.reproduce_animal(fox.m)
        #
        # for rabbit in self.rabbits:
        #     self.reproduce_animal(rabbit.m)


        self.ngrass.append(self.amount_of_grass())
        self.update_field()

        self.gen += 1
        if self.gen > 1000:
            exit()


    def history(self, showTrack=True, showPercentage=True, marker='.'):

        plt.figure(figsize=(15, 7))
        plt.xlabel("generation #")
        plt.ylabel("% population")

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

        if showTrack:
            plt.plot(range(self.gen), rs, label='rabbits')
            plt.plot(range(self.gen), fs, label='foxes')
            plt.plot(range(self.gen), gs, label='grass')

        plt.grid()
        plt.legend()
        plt.title("Population vs. TIME: GROWTH RATE =" + str(GRASS_RATE))
        plt.savefig("history.png", bbox_inches='tight')
        plt.show()

    # def history2(self):
    #     xs_r = self.nrabbits[:]
    #     xs_f = self.nfoxes[:]
    #     print(xs_f)
    #     ys = self.ngrass[:]
    #
    #     sns.set_style('dark')
    #     f, ax = plt.subplots(figsize=(7, 6))
    #
    #     #sns.scatterplot(x=xs_r, y=ys, s=5, color=".15")
    #     #sns.histplot(x=xs_r, y=ys, bins=50, pthresh=.1, cmap="mako")
    #     #sns.kdeplot(x=xs_r, y=ys, levels=5, color="r", linewidths=1)
    #
    #     sns.scatterplot(x=xs_f, y=ys, s=5, color="green")
    #     sns.histplot(x=xs_f, y=ys, bins=50, pthresh=.1, cmap="flare")
    #     sns.kdeplot(x=xs_f, y=ys, levels=5, color="yellow", linewidths=1)
    #
    #     plt.grid()
    #     plt.xlim(0, max(max(xs_r), max(xs_f)) * 1.2)
    #
    #     plt.xlabel("# Rabbits")
    #     plt.ylabel("# Grass")
    #     plt.title("Rabbits vs. Grass: GROW_RATE =" + str(GRASS_RATE))
    #     plt.savefig("r_history2.png", bbox_inches='tight')
    #     plt.show()
