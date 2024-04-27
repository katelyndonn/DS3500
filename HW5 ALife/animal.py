import copy
import random as rnd

SIZE = 500  # The dimensions of the field

class Animal:
    """ A furry creature roaming a field in search of grass to eat.
    Mr. Rabbit must eat enough to reproduce, otherwise he will starve. """

    def __init__(self, m, max_offspring, speed, k_starve, eats, size):
        self.x = rnd.randrange(0, size)
        self.y = rnd.randrange(0, size)
        self.m = m # marker in the field array
        self.eaten = 0
        self.max_offspring = max_offspring
        self.speed = speed
        self.k_starve = k_starve
        self.eats = eats
        self.size = size

    def reproduce(self):
        """ Make a new rabbit at the same location.
         Reproduction is hard work! Each reproducing
         rabbit's eaten level is reset to zero. """
        self.eaten = 0
        return copy.deepcopy(self)


    def eat(self, amount):
        """ Feed the rabbit 1 grass """
        self.eaten += amount

    def move(self):
        """ Move up, down, left, right randomly """

        # self.x += rnd.choice([-1, 0, 1])
        # self.y += rnd.choice([-1, 0, 1])
        self.x = min(self.size - 1, max(0, (self.x + rnd.choice([-self.speed, 0, self.speed]))))
        self.y = min(self.size - 1, max(0, (self.y + rnd.choice([-self.speed, 0, self.speed]))))
