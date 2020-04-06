#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import math
import time

'''
Programming Assignment 3

n this assignment we will revisit an old friend, the traveling salesman problem
(TSP). This week you will implement a heuristic for the TSP, rather than an
exact algorithm, and as a result will be able to handle much larger problem
sizes. Here is a data file describing a TSP instance (original source:
http://www.math.uwaterloo.ca/tsp/world/bm33708.tsp). nn.txt

The first line indicates the number of cities. Each city is a point in the plane
, and each subsequent line indicates the x- and y-coordinates of a single city.

The distance between two cities is defined as the Euclidean distance - that is,
two cities at locations (x,y) and (z,w) have distance sqrt((x-z)^2 + (y-w)^2)
between them.

You should implement the nearest neighbor heuristic:

1. Start the tour at the first city.

2. Repeatedly visit the closest city that the tour hasn't visited yet. In case
of a tie, go to the closest city with the lowest index. For example, if both the
third and fifth cities have the same distance from the first city (and are
closer than any other city), then the tour should begin by going from the first
city to the third city.

3. Once every city has been visited exactly once, return to the first city to
complete the tour.

In the box below, enter the cost of the traveling salesman tour computed by the
nearest neighbor heuristic for this instance, rounded down to the nearest
integer.

[Hint: when constructing the tour, you might find it simpler to work with
squared Euclidean distances (i.e., the formula above but without the square
root) than Euclidean distances. But don't forget to report the length of the
tour in terms of standard Euclidean distance.]
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
Class for approximating travelling salesman solution with nearest neighbor
heuristic.
'''
class TSP:
    def __init__(self, filename=None, cities=None, inf=9999):
        self.inf = inf
        if filename is None:
            self.cities = cities
            self.numCities = len(cities)
            self._initializeDistanceMatrix()
            self._updateDistanceMatrix()
        else:
            self.cities = []
            self._readFile(filename)

    def _initializeDistanceMatrix(self):
        self.distanceMatrix = np.full((self.numCities, self.numCities),
                self.inf, dtype='float64')

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
   
    def _updateDistanceMatrixT(self):
        for i in range(len(self.cities)):
            stop = i + 20
            if stop > len(self.cities):
                stop = len(self.cities)
            for j in range(i + 1, stop):
                distance = self.euclideanDistance(i, j)
                self.distanceMatrix[i, j] = distance
                self.distanceMatrix[j, i] = distance

    '''
    Plots city coordinates.
    '''
    def plotCities(self, showLabels=False):
        x = []
        y = []
        labels = []
        for i in range(len(self.cities)):
            city = self.cities[i]
            x.append(city.x)
            y.append(city.y)
            labels.append(i)

        fig, ax = plt.subplots()
        ax.scatter(x, y, s=1)
        if showLabels:
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
                #self.numCities = 50
                self._initializeDistanceMatrix()
            else:
                self.cities.append(City(float(line[1]), float(line[2])))
        
        self._updateDistanceMatrix()

    '''
    Approximates solution using nearest neighbor heuristic.
    '''
    def solve(self):
        visited = np.ones(self.numCities)
        tour = 0
        
        # Start at City 0
        visited[0] = self.inf
        path = [0]

        while len(path) < self.numCities:
            city = path[-1]
            nextCity = (np.multiply(self.distanceMatrix[city, :],
                visited)).argmin()
            tour += self.distanceMatrix[city, nextCity]
            path.append(nextCity)
            visited[nextCity] = self.inf

        # Return to City 0
        tour += self.euclideanDistance(path[-1], 0)

        return tour, path

def runProblem(filename):
    t0 = time.time()
    g = TSP(filename=filename)
    t1 = time.time()
    print('Updated distance matrix in %s s.' %(t1 - t0))
    #g.plotCities()

    t2 = time.time()
    tour, path = g.solve()
    totalTime = time.time() - t2 + t1 - t0
    print('tour = %s, path = %s, time = %s' %(tour, path, totalTime))

if __name__ == '__main__':
    runProblem('nn.txt')
