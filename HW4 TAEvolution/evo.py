
""" reusable evolutionary framework """

import random as rnd
import copy
from functools import reduce
import time
import pandas as pd
import numpy as np


class Evo:

    def __init__(self, timer=20):
        self.pop = {}  # ((eval1, sol1), (eval2, sol2), ...) ==> solution
        self.fitness = {}  # name -> objective func
        self.agents = {}  # name -> (agent operator, # input solutions)
        self.crits = {}  # func --> crit

    def size(self):
        """ The size of the solution population """
        return len(self.pop)

    def add_fitness_criteria(self, name, f, c):
        """ Registering an objective with the Evo framework
        name - The name of the objective (string)
        f    - The objective function:   f(solution)--> a number
        c    - The criteria (part of df we're analyzing)
        """
        self.fitness[name] = f
        self.crits[name] = c

    def add_agent(self, name, op, k=1):
        """ Registering an agent with the Evo framework
        name - The name of the agent
        op   - The operator - the function carried out by the agent  op(*solutions)-> new solution
        k    - The number of input solutions (usually 1) """
        self.agents[name] = (op, k)

    def get_random_solutions(self, k=1):
        """ Pick k random solutions from the population as a list of solutions
            We are returning DEEP copies of these solutions as a list """
        if self.size() == 0:  # No solutions in the populations
            return []
        else:
            popvals = tuple(self.pop.values())
            return [copy.deepcopy(rnd.choice(popvals)) for _ in range(k)]

    def add_solution(self, sol):
        """ Add a new solution to the population """
        eval = tuple([(name, f(sol, crit=self.crits[name])) for name, f in self.fitness.items()])
        self.pop[eval] = sol

    def run_agent(self, name):
        """ Invoke an agent against the current population """
        op, k = self.agents[name]
        picks = self.get_random_solutions(k)
        new_solution = op(picks)
        self.add_solution(new_solution)

    def run_tests(self, tests):
        """ Runs evo framework on test solutions, tests = list of filenames (.csv)
            Returns: dataframe and .csv export of fitness criteria error scores """

        # add each test solution to the evo framework
        for filename in tests:
            L = np.array(pd.read_csv(filename, header=None))
            self.add_solution(L)

        # build the rows of the dataframe (fitness criteria error scores)
        rows = []
        for eval, sol in self.pop.items():
            rows.append(dict(eval))

        # name the columns the filenames without .csv
        # display dataframe transposed so that the criteria are the index
        cols = [i[:-4] for i in tests]
        df = pd.DataFrame(rows, columns=list(self.fitness.keys())).set_index([cols]).T
        print(df)

        # export as a .csv to system's Downloads folder
        df.to_csv("~/Downloads/test_results.csv")

    def display_best(self):
        """ Finds the best solution among all populations (min sum of criteria errors)
            Returns: dataframe and exported .csv of best solution """

        # default min is the size of one solution
        min = list(self.pop.values())[0].size
        solution = ""

        # for each solution in the populations
        for eval, sol in self.pop.items():
            # calculate the sum of criteria errors
            if sum(dict(eval).values()) < min:
                # update minimum value and best solution
                min = sum(dict(eval).values())
                solution = str(dict(eval))

                # display the best solution as a dataframe and export as .csv
                sol_df = pd.DataFrame(sol, columns=range(sol.shape[1]))
                sol_df.to_csv("~/Downloads/best_solution.csv")

        return solution + "\n\n" + str(sol)

    def display_summary(self, name=None):
        """ Displays a dataframe of criteria error scores for every solution in populations """

        # solution name column
        if name is None:
            name = 'dslayp'

        # build rows (scores for each solution) and columns (fitness criteria)
        rows = []
        cols = list(self.fitness.keys())
        for eval, sol in self.pop.items():
            row = dict(eval).values()
            rows.append(row)

        # build a dataframe showing criteria error scores for each solution
        df = pd.DataFrame(rows, columns=cols[::-1]).reset_index(drop=True)
        df['groupname'] = [name for i in range(len(df))]
        df = df.iloc[:, ::-1]

        return df

    def evolve(self, n=1, dom=100, status=100, time_limit=600, name=None):
        """ To run n random agents against the population
        n - # of agent invocations
        dom - # of iterations between discarding the dominated solutions
        time_limit - # of seconds the function runs for
        """
        agent_names = list(self.agents.keys())

        # start timer
        start = time.time()

        for i in range(n):
            # calculate elapsed runtime of evolve function
            elapsed = time.time() - start

            # if elapsed time hits time limit, stop application
            if elapsed >= time_limit:

                # display total runtime, best solution, and summary of criteria error scores
                print("\n ------------------ \nRUNTIME:",
                      round(elapsed/60, 2),
                      "MINUTES\n ------------------ \n")
                print(self.display_best(), '\n')
                print(self.display_summary(name=name))

                # export summary table as a .csv
                self.display_summary().to_csv("~/Downloads/evo_summary.csv")

                # stop the framework
                quit()

            pick = rnd.choice(agent_names)  # pick an agent to run
            self.run_agent(pick)

            if i % dom == 0:
                self.remove_dominated()

            if i % status == 0:  # print the population and iteration
                self.remove_dominated()
                print("Iteration: ", i)
                print("Population Size: ", self.size(), "\n")

            # Clean up population
            self.remove_dominated()



    @staticmethod
    def _dominates(p, q):
        pscores = [score for _, score in p]
        qscores = [score for _, score in q]
        score_diffs = list(map(lambda x, y: y - x, pscores, qscores))
        min_diff = min(score_diffs)
        max_diff = max(score_diffs)
        return min_diff >= 0.0 and max_diff > 0.0

    @staticmethod
    def _reduce_nds(S, p):
        return S - {q for q in S if Evo._dominates(p, q)}

    def remove_dominated(self):
        nds = reduce(Evo._reduce_nds, self.pop.keys(), self.pop.keys())
        self.pop = {k: self.pop[k] for k in nds}

    def __str__(self):
        """ Output the solutions in the population """
        rslt = ""
        for eval, sol in self.pop.items():
            rslt += str(dict(eval)) + ":\t" + str(sol) + "\n" + str(sum(dict(eval).values()))
        return rslt
