#!/usr/bin/env python3

import numpy as np
import time

'''
Programming Assignment 4


Problem 1

In this programming problem and the next you'll code up the knapsack algorithm
from lecture. Let's start with a warm-up.

Download following text file: knapsack1.txt

This file describes a knapsack instance, and it has the following format:

[knapsack_size][number_of_items]

[value_1] [weight_1]

[value_2] [weight_2]

...

For example, the third line of the file is "50074 659", indicating that the
second item has value 50074 and size 659, respectively.

You can assume that all numbers are positive. You should assume that item
weights and the knapsack capacity are integers.

In the box below, type in the value of the optimal solution.

ADVICE: If you're not getting the correct answer, try debugging your algorithm
using some small test cases. And then post them to the discussion forum!


Problem 2

This problem also asks you to solve a knapsack instance, but a much bigger one.

Download the following text file: knapsackBig.txt

This file describes a knapsack instance, and it has the following format:

[knapsack_size][number_of_items]

[value_1] [weight_1]

[value_2] [weight_2]

...

For example, the third line of the file is "50074 834558", indicating that the
second item has value 50074 and size 834558, respectively. As before, you should
assume that item weights and the knapsack capacity are integers.

This instance is so big that the straightforward iterative implemetation uses
an infeasible amount of time and space. So you will have to be creative to
compute an optimal solution. One idea is to go back to a recursive
implementation, solving subproblems --- and, of course, caching the results to
avoid redundant work --- only on an "as needed" basis. Also, be sure to think
about appropriate data structures for storing and looking up solutions to
subproblems.

In the box below, type in the value of the optimal solution.

ADVICE: If you're not getting the correct answer, try debugging your algorithm
using some small test cases. And then post them to the discussion forum!
'''

class Item:
    def __init__(self, value, weight):
        self.value = value
        self.weight = weight

    def __repr__(self):
        return 'Item(value: %s, weight: %s)' %(self.value, self.weight)

class Knapsack:
    def __init__(self, filename):
        self.readFile(filename)

    def readFile(self, filename):
        with open(filename) as f:
            lines = f.readlines()

        self.items = [Item(0, 0)]
        for i in range(len(lines)):
            line = lines[i].split()
            if i == 0:
                self.capacity = int(line[0])
                self.numItems = int(line[1])
            else:
                self.items.append(Item(int(line[0]), int(line[1])))

    def solveBottomUp(self, verbose=False):
        # A stores value for give number of items and capacity
        A = np.zeros((self.numItems + 1, self.capacity + 1))
        for i in range(1, A.shape[0]):
            for w in range(A.shape[1]):
                item = self.items[i]
                if w - item.weight < 0: # can't fit item
                    A[i, w] = A[i - 1, w] # don't add item
                else:
                    A[i, w] = max(
                            A[i - 1, w], # don't add item
                            A[i - 1, w - item.weight] + item.value) # add item
        if verbose:
            print(A)
        return A[-1, -1]

    def solveTopDown(self):
        pass

def runProblem1():
    t0 = time.time()
    ks = Knapsack('knapsack1.txt')
    ans = ks.solveBottomUp()
    print('p1 result = %s' %ans)
    print('p1 time = %s' %(time.time() - t0))

def runProblem2():
    pass

if __name__ == '__main__':
    runProblem1()
