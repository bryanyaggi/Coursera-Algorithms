#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import math
import time

'''
Programming Assignment 2

In this assignment you will implement one or more algorithms for the traveling
salesman problem, such as the dynamic programming algorithm covered in the video
lectures.

Here is a data file describing a TSP instance: tsp.txt

The first line indicates the number of cities. Each city is a point in the
plane, and each subsequent line indicates the x- and y-coordinates of a single
city.

The distance between two cities is defined as the Euclidean distance - that is,
two cities at locations (x,y) and (z,w) have distance sqrt((x-z)^2 + (y-w)^2)
between them.

In the box below, type in the minimum cost of a traveling salesman tour for this
instance, rounded down to the nearest integer.

OPTIONAL: If you want bigger data sets to play with, check out the TSP instances
from around the world here (tsp.gatech.edu/world/countries.html). The smallest
data set (Western Sahara) has 29 cities, and most of the data sets are much
bigger than that. What's the largest of these data sets that you're able to
solve - using dynamic programming or, if you like, a completely different
method?

HINT: You might experiment with ways to reduce the data set size. For example,
trying plotting the points. Can you infer any structure of the optimal solution?
Can you use that structure to speed up your algorithm?
'''

'''
Class for storing city information
'''
class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return ('City(%s, %s)' %(self.x, self.y))

'''
Class for solving travelling salesman problems
'''
class TSP:
    def __init__(self, filename=None, cities=None):
        if filename is None:
            self.cities = cities
            self.numCities = len(cities)
            self._initializeDistanceMatrix()
            self._updateDistanceMatrix()
        else:
            self.cities = []
            self._readFile(filename)

    def _initializeDistanceMatrix(self):
        self.distanceMatrix = np.zeros((self.numCities, self.numCities))

    '''
    Calculates Euclidean distance between cities.
    '''
    def euclideanDistance(self, index1, index2):
        city1 = self.cities[index1]
        city2 = self.cities[index2]
        return math.sqrt((city1.x - city2.x) ** 2 + (city1.y - city2.y) ** 2)

    def _updateDistanceMatrix(self):
        for i in range(len(self.cities)):
            for j in range(i + 1, len(self.cities)):
                distance = self.euclideanDistance(i, j)
                self.distanceMatrix[i, j] = distance
                self.distanceMatrix[j, i] = distance

    '''
    Plots city coordinates.
    '''
    def plotCities(self):
        x = []
        y = []
        labels = []
        for i in range(len(self.cities)):
            city = self.cities[i]
            x.append(city.x)
            y.append(city.y)
            labels.append(i)

        fig, ax = plt.subplots()
        ax.scatter(x, y)
        for i, txt in enumerate(labels):
            ax.annotate(txt, (x[i], y[i]))
        plt.show()

    def _readFile(self, filename):
        with open(filename) as f:
            lines = f.readlines()

        for i in range(len(lines)):
            line = lines[i].split()
            if i == 0:
                self.numCities = int(line[0])
                self._initializeDistanceMatrix()
            else:
                self.cities.append(City(float(line[0]), float(line[1])))
        
        self._updateDistanceMatrix()

    def _citiesToBits(self, cities):
        bits = ['0'] * len(self.cities)
        for city in cities:
            bits[city] = '1'
        
        return ''.join(bits)

    def _bitsToCities(self, bits):
        cities = set()
        for i in range(bits):
            if bits[i] == '1':
                cities.append(i)

        return cities

    def _combinations(self, numCities):
        def recurse(index, numCities, cities):
            if numCities > len(self.cities) - index:
                return
            if index == len(self.cities):
                results.append(cities)
                return

            if numCities >= 1:
                # Add city
                newCities = cities.copy()
                newCities.add(index)
                recurse(index+1, numCities-1, newCities)
            # Don't add city
            recurse(index+1, numCities, cities)

        results = []
        recurse(1, numCities, set())
        return results

    '''
    Solve TSP using Held-Karp algorithm.

    costs dictionary keys are tuples containing binary string representing set
    of cities and end city. Values are tuples containing cost and path. Cost is
    the path cost from City 0 to end, passing through set of cities.
    '''
    def solve(self):
        costs = {} # stores cost and path information

        # Calculate costs for city sets of size 1
        for end in range(1, len(self.cities)):
            citySetBits = self._citiesToBits(set([end]))
            path = [0]
            costs[(citySetBits, end)] = (self.distanceMatrix[0, end], path)

        # Calculate costs for larger city sets
        for citySetSize in range(2, len(self.cities)):
            citySets = self._combinations(citySetSize)
            for citySet in citySets:
                citySetBits = self._citiesToBits(citySet)
                for end in citySet:
                    citySubset = citySet.copy()
                    citySubset.remove(end)
                    citySubsetBits = self._citiesToBits(citySubset)
                    candidates = []
                    for penultimate in citySubset:
                        cost = costs[(citySubsetBits, penultimate)]
                        path = cost[1].copy()
                        path.append(penultimate)
                        candidates.append((cost[0] +
                            self.distanceMatrix[penultimate, end], path))
                    costs[(citySetBits, end)] = min(candidates)

        # Calculate complete tour
        citySet = set(range(1, len(self.cities)))
        citySetBits = self._citiesToBits(citySet)
        candidates = []
        for penultimate in citySet:
            cost = costs[(citySetBits, penultimate)]
            path = cost[1].copy()
            path.append(penultimate)
            candidates.append((cost[0] + self.distanceMatrix[penultimate, 0],
                path))
        
        tour, path = min(candidates)
        return tour, path

def runFinalProblem():
    g = TSP(filename='tsp.txt')
    g.plotCities()

    # Split graph into 2 parts
    t0 = time.time()
    g1 = TSP(cities=g.cities[:13])
    g2 = TSP(cities=g.cities[11:])

    tour1, path1 = g1.solve()
    print('tour 1 = %s, path = %s' %(tour1, path1))
    tour2, path2 = g2.solve()
    path2 = [i + 11 for i in path2]
    print('tour 2 = %s, path = %s' %(tour2, path2))

    commonPath = g1.euclideanDistance(11, 12)
    print('common path (11 to 12) length = %s' %commonPath)
    tour = tour1 + tour2 - (2 * commonPath)
    print('tour = %s, time = %s' %(tour, time.time() - t0))

def runTestProblems():
    filenames = ['tspTest1.txt', 'tspTest2.txt', 'tspTest3.txt']
    for filename in filenames:
        g = TSP(filename=filename)
        g.plotCities()
        tour, path = g.solve()
        print('%s: tour = %s, path = %s' %(filename, tour, path))

if __name__ == '__main__':
    #runTestProblems()
    runFinalProblem()
