"""
Avril Mauro & Katelyn Donn
DS 3500 Homework 5 Rabbit & Fox Animation
hw5_main.py
April 14th, 2023
"""


import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors
import argparse
import numpy as np
from animal import Animal
from field import Field


def animate(i, field, im):
    field.generation()
    # print("AFTER: ", i, np.sum(field.field), len(field.rabbits))
    im.set_array(field.field)
    plt.title("generation = " + str(i))
    return im,


def main():
    # Initialize argument parsers for command line use
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--k_cycles", help="number of cycles for fox to eat", type=int)
    parser.add_argument("-g", "--grass_growth", help="grass growth rate", type=float)
    parser.add_argument("-s", "--field_size", help="field size", type=int)
    parser.add_argument("-f", "--initial_foxes", help="number of initial foxes", type=int)
    parser.add_argument("-r", "--initial_rabbits", help="number of initial rabbits", type=int)
    args = parser.parse_args()

    # Set default values
    GRASS_RATE, SIZE, K_CYCLES, F_INITIAL, R_INITIAL = .25, 500, 10, 10, 10

    if args.grass_growth:
        GRASS_RATE = args.grass_growth

    if args.field_size:
        SIZE = args.field_size

    if args.initial_foxes:
        F_INITIAL = args.initial_foxes

    if args.initial_rabbits:
        R_INITIAL = args.initial_rabbits

    if args.k_cycles:
        K_CYCLES = args.k_cycles

    # Create the ecosystem
    field = Field(SIZE, GRASS_RATE)

    # Add initial rabbits
    for _ in range(R_INITIAL + 1):
        field.add_animal(Animal(m=2, max_offspring=1, speed=1, k_starve=1, eats=(1,), size=SIZE))

    # Add initial foxes
    for _ in range(F_INITIAL + 1):
        field.add_animal(Animal(m=3, max_offspring=2, speed=2, k_starve=K_CYCLES, eats=(2,), size=SIZE))

    # 0 = white ground, 1 = green grass, 2 = blue rabbit, 3 = red fox
    cvals = [0, 1, 2, 3]
    colors = ["white", "lightgreen", "blue", "red"]

    # color map
    norm = plt.Normalize(min(cvals), max(cvals))
    tuples = list(zip(map(norm, cvals), colors))
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", tuples)

    # animate field
    array = np.ones(shape=(SIZE, SIZE), dtype=int)
    fig = plt.figure(figsize=(5, 5))
    im = plt.imshow(array, cmap=cmap, interpolation=None, aspect='auto', vmin=0, vmax=3)
    anim = animation.FuncAnimation(fig, animate, fargs=(field, im,), frames=1000000, interval=1, repeat=True)
    plt.show()

    # display population history
    field.history()


if __name__ == '__main__':
    main()
