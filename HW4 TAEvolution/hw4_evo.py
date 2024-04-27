"""
Avril Mauro & Katelyn Donn
DS 3500 Homework 4 Evo TA Schedule
March 28th, 2023
"""

from evo import Evo
import pandas as pd
import numpy as np
import random as rnd


def overallocation(L, crit):
    """ Criteria: calculate and return summed overallocation penalty of tas
        Parameters: L (array) --> matrix of solutions (0 = not assigned, 1 = assigned)
                    crit (int) --> max number of ta's to be assigned to one section
        Returns: overallocation_penalty (int) --> total overallocation penalty score for solution """

    # build a list of overallocation penalties for each section
    overallocation_penalty = []
    # iterate over each section (rows)
    for row in range(L.shape[0]):
        if sum(L[row]) > crit[row]:
            # subtract the max number of ta's from the total ta's assigned
            penalty = sum(L[row]) - crit[row]
            overallocation_penalty.append(penalty)

    # sum the penalties of each row for a total overallocation score for the entire solution
    return sum(overallocation_penalty)


def conflict(L, crit):
    """ Criteria: calculate and return summed time conflicts for each ta
        Parameters: L (array) --> matrix of solutions (0 = not assigned, 1 = assigned)
                    crit (str) --> date and time of section
        Returns: conflict_penalty (int) --> total conflict error score for solution """

    # default conflict score is 0
    conflict_penalty = 0
    # iterate over ta (rows )
    for ta in range(L.shape[0]):
        # build a list of assigned sections (indices) for the ta
        s = []
        for section in range(L.shape[1]):
            if L[ta, section] == 1:
                s.append(section)

        # calculate if any section day/times are repeated (conflict)
        assigned = crit.iloc[s]
        if len(assigned) > len(set(assigned)):
            conflict_penalty += 1

    return conflict_penalty


def undersupport(L, crit):
    """ Criteria: calculate and return summed time conflicts for each ta
        Parameters: L (array) --> matrix of solutions (0 = not assigned, 1 = assigned)
                    crit (int) --> minimum number of ta's to be assigned to a section
        Returns: under_penalty (int) --> total under-support penalty score for solution """

    # default under-support penalty score is 0
    under_penalty = 0
    # iterate over each section (columns)
    for section in range(L.shape[1]):
        # count the amount of ta's assigned for each section
        ta_count = sum(L[:, section])
        # if amount of ta's is less than minimum required, add difference to penalty score
        if ta_count < crit[section]:
            under_penalty += (crit[section] - ta_count)

    return under_penalty


def unwilling(L, crit):
    """ Criteria: calculate and return summed time conflicts for each ta
        Parameters: L (array) --> matrix of solutions (0 = not assigned, 1 = assigned)
                    crit (array) --> array of ta preferences (U='Unwilling')
        Returns: unwilling_penalty (int) --> total unwilling penalty score for solution """

    # default unwilling penalty score is 0
    unwilling_penalty = 0
    # iterate over each ta (rows)
    for ta in range(L.shape[0]):
        # iterate over each section (columns)
        for section in range(L.shape[1]):
            # if a ta is assigned to a section that the ta marked as unwilling, add penalty
            if (L[ta, section] == 1) and (crit.iloc[ta, section] == 'U'):
                unwilling_penalty += 1

    return unwilling_penalty


def unpreferred(L, crit):
    """ Criteria: calculate and return summed time conflicts for each ta
            Parameters: L (array) --> matrix of solutions (0 = not assigned, 1 = assigned)
                        crit (array) --> array of ta preferences (W='Willing', P='Preferred')
            Returns: unpreferred_penalty (int) --> total unwilling penalty score for solution """

    # default unpreferred penalty score is 0
    unpreferred_penalty = 0
    # iterate over each ta (rows)
    for ta in range(L.shape[0]):
        # iterate over each section (columns)
        for section in range(L.shape[1]):
            # if a ta is assigned to a section and they put 'Willing' but not 'Preferred', add penalty
            if (L[ta, section] == 1) and (crit.iloc[ta, section] == 'W'):
                unpreferred_penalty += 1

    return unpreferred_penalty


def swapper(solutions):
    """ Agent: swap two random values """
    L = solutions[-1]
    i = rnd.randrange(0, len(L))
    j = rnd.randrange(0, len(L))
    L[i], L[j] = L[j], L[i]
    return L


def flip(solutions):
    """ Agent: flips a random solution """
    L = solutions[rnd.randrange(0, len(solutions))]
    L = np.fliplr(L)
    return L


def reduce(solutions):
    """ Agent: reduce amount of assignments """
    L = solutions[rnd.randrange(0, len(solutions))]

    for i in range(0, rnd.randint(0, len(L))):
        r = rnd.randrange(0, L.shape[0])
        c = rnd.randrange(0, L.shape[1])
        L[r, c] = 0

    return L


def main():

    # initialize evo framework
    E = Evo()

    # read ta and sections files as dataframes
    ta_df = pd.read_csv('tas.csv')
    sections_df = pd.read_csv('sections.csv')
    sections_df = sections_df[['section', 'daytime', 'min_ta']]

    # start with a base solution
    L = np.array(pd.read_csv('test1.csv', header=None))

    # add fitness criteria to framework
    E.add_fitness_criteria("overallocation", overallocation, c=ta_df['max_assigned'])
    E.add_fitness_criteria("conflict", conflict, c=sections_df['daytime'])
    E.add_fitness_criteria("undersupport", undersupport, c=sections_df['min_ta'])
    E.add_fitness_criteria("unwilling", unwilling, c=ta_df.iloc[:, -17:])
    E.add_fitness_criteria("unpreferred", unpreferred, c=ta_df.iloc[:, -17:])

    # add agents to framework
    E.add_agent("swapper", swapper)
    E.add_agent("flip", flip)
    E.add_agent("reduce", reduce)

    # add solutions to framework
    E.add_solution(L)

    # run the evolver
    E.evolve(100000000, 100, 100, time_limit=600, name='dslayp')


if __name__ == '__main__':
    main()
