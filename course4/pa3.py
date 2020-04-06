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
        self.visited = False

    def __repr__(self):
        return ('City(%s, %s)' %(self.x, self.y))

'''
Class for approximating travelling salesman solution with nearest neighbor
heuristic.
'''
class TSP:
    def __init__(self, filename=None, lines=None, cities=None, inf=9999):
        self.inf = inf
        if filename is None:
            self.cities = cities
            self.numCities = len(cities)
        else:
            self.cities = []
            self.lines = lines
            self._readFile(filename)

    '''
    Calculates Euclidean distance between cities.
    '''
    def euclideanDistance(self, index1, index2):
        city1 = self.cities[index1]
        city2 = self.cities[index2]
        return math.sqrt((city1.x - city2.x) ** 2 + (city1.y - city2.y) ** 2)

    '''
    Calculates X coordinate distance between cities.
    '''
    def xDistance(self, index1, index2):
        city1 = self.cities[index1]
        city2 = self.cities[index2]
        return abs(city1.x - city2.x)

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
            numLines = len(lines)
            if self.lines is not None:
                if self.lines < numLines:
                    numLines = self.lines

        for i in range(numLines):
            line = lines[i].split()
            if i == 0:
                #self.numCities = int(line[0])
                self.numCities = numLines - 1
            else:
                self.cities.append(City(float(line[1]), float(line[2])))
        
    '''
    Approximates solution using nearest neighbor heuristic.
    '''
    def solve(self):
        tour = 0
        path = [0] # start at City 0
        self.cities[0].visited = True

        while len(path) < self.numCities:
            print('Progress: %s/%s' %(len(path), self.numCities), end='\r')

            city = path[-1]

            # Find next city
            minDistance = self.inf
            nextCity = city
            i = 1
            stopForward = False
            stopBackward = False
            while not (stopForward and stopBackward):
                # Search forward along x coordinate
                if city + i > self.numCities - 1:
                    stopForward = True
                elif not self.cities[city + i].visited:
                    distance = self.euclideanDistance(city, city + i)
                    if distance == minDistance and city + i < nextCity:
                        nextCity = city + i
                    elif distance < minDistance:
                        minDistance = distance
                        nextCity = city + i
                    elif self.xDistance(city, city + i) > minDistance:
                        stopForward = True

                # Search backward along x coordinate
                if city - i < 0:
                    stopBackward = True
                elif not self.cities[city - i].visited:
                    distance = self.euclideanDistance(city, city - i)
                    if distance == minDistance and city - i < nextCity:
                        nextCity = city - i
                    elif distance < minDistance:
                        minDistance = distance
                        nextCity = city - i
                    elif self.xDistance(city, city - i) > minDistance:
                        stopBackward = True
                i += 1

            path.append(nextCity)
            self.cities[nextCity].visited = True
            tour += minDistance

        # Return to City 0
        tour += self.euclideanDistance(path[-1], 0)
        print('Progress: %s/%s' %(len(path), self.numCities), end='\r')
        
        print()
        return tour, path

def runProblem(filename, lines=None, printPath=False):
    t0 = time.time()
    g = TSP(filename=filename, lines=lines)
    t1 = time.time()
    g.plotCities()

    t2 = time.time()
    tour, path = g.solve()
    totalTime = time.time() - t2 + t1 - t0
    if printPath:
        print('tour = %s, path = %s, time = %s' %(tour, path, totalTime))
    else:
        print('tour = %s, time = %s' %(tour, totalTime))

if __name__ == '__main__':
    runProblem('nn.txt')
