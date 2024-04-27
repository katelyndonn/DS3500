from field import Field
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors
import argparse
import numpy as np
from animal import Animal


def animate(i, field, im):
    field.generation()
    # print("AFTER: ", i, np.sum(field.field), len(field.rabbits))
    im.set_array(field.field)
    plt.title("generation = " + str(i))
    return im,


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--k_cycles", help="number of cycles for fox to eat", type=int)
    parser.add_argument("-g", "--grass_growth", help="grass growth rate", type=int)
    parser.add_argument("-s", "--field_size", help="field size", type=int)
    parser.add_argument("-f", "--initial_foxes", help="number of initial foxes", type=int)
    parser.add_argument("-r", "--initial_rabbits", help="number of initial rabbits", type=int)
    args = parser.parse_args()

    GRASS_RATE, SIZE, F_INITIAL, R_INITIAL = .025, 10, 0, 0


    if args.grass_growth:
        GRASS_RATE = args.grass_growth

    if args.field_size:
        SIZE = args.field_size

    if args.initial_foxes:
        F_INITIAL = args.initial_foxes

    if args.initial_rabbits:
        R_INITIAL = args.initial_rabbits

    # Create the ecosystem
    field = Field(SIZE)

    for _ in range(R_INITIAL + 1):
        field.add_animal(Animal(m=2, max_offspring=1, speed=1, k_starve=1, eats=(1,), size=SIZE))

    for _ in range(F_INITIAL + 1):
        field.add_animal(Animal(m=3, max_offspring=2, speed=2, k_starve=10, eats=(2,), size=SIZE))

    # 0 = empty, 1 = grass, 2 = rabbit, 3 = fox
    cvals = [0, 1, 2, 3]
    # fix colors to grass/animal relation
    colors = ["white", "lightgreen", "blue", "red"]

    norm = plt.Normalize(min(cvals), max(cvals))
    tuples = list(zip(map(norm, cvals), colors))
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", tuples)

    array = np.ones(shape=(SIZE, SIZE), dtype=int)
    fig = plt.figure(figsize=(SIZE, SIZE))
    im = plt.imshow(array, cmap=cmap, interpolation=None, aspect='auto', vmin=0, vmax=3)
    anim = animation.FuncAnimation(fig, animate, fargs=(field, im,), frames=1000000, interval=1, repeat=True)
    plt.show()

    #field.history()
    # field.history2()

    # python hw5_main.py


if __name__ == '__main__':
    main()
