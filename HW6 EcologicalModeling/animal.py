"""
Avril Mauro & Katelyn Donn
DS 3500 Homework 5 Rabbit & Fox Animation
animal.py -- Reusable Animal Class
April 14th, 2023
"""

import copy
import random as rnd


class Animal:
    """ A furry creature roaming a field in search of grass to eat.
    Mr. Rabbit must eat enough to reproduce, otherwise he will starve. """

    def __init__(self, m, max_offspring, speed, k_starve, eats, size):
        self.x = rnd.randrange(0, size) # x position in the field
        self.y = rnd.randrange(0, size) # y position in the field
        self.m = m # marker in the field array (1 = grass, 2 = rabbit, 3 = fox)
        self.eaten = 0 # default hungry, >0 if the animal ate
        self.max_offspring = max_offspring # maximum possible offspring per reproduce
        self.speed = speed # maximum distance per move
        self.k_starve = k_starve # num of cycles animal can go w/o starving
        self.eats = eats # what the animal eats
        self.size = size # field size

    def reproduce(self):
        """ Make a new rabbit at the same location.
         Reproduction is hard work! Each reproducing
         rabbit's eaten level is reset to zero. """
        self.eaten = 0
        return copy.deepcopy(self)

    def eat(self, k):
        """ Feed the rabbit 1 grass """
        self.eaten += k

    def move(self):
        """ Move up, down, left, right randomly """
        self.x = min(self.size - 1, max(0, (self.x + rnd.choice(list(range(-self.speed, self.speed+1))))))
        self.y = min(self.size - 1, max(0, (self.y + rnd.choice(list(range(-self.speed, self.speed+1))))))
