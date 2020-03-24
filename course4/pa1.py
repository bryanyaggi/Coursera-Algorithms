#!/usr/bin/env python3

import numpy as np
import multiprocessing as mp
import time

'''
Programming Assignment 1

In this assignment you will implement one or more algorithms for the all-pairs
shortest-path problem.

Here are data files describing three graphs: g1.txt, g2.txt, g3.txt

The first line indicates the number of vertices and edges, respectively. Each
subsequent line describes an edge (the first two numbers are its tail and head,
respectively) and its length (the third number). NOTE: some of the edge lengths
are negative. NOTE: These graphs may or may not have negative-cost cycles.

Your task is to compute the "shortest shortest path". Precisely, you must first
identify which, if any, of the three graphs have no negative cycles. For each
such graph, you should compute all-pairs shortest paths and remember the
smallest one (i.e., compute min_(u,v ∈ V) d(u,v), where d(u,v) denotes the
shortest-path distance from u to v).

If each of the three graphs has a negative-cost cycle, then enter "NULL" in the
box below. If exactly one graph has no negative-cost cycles, then enter the
length of its shortest shortest path in the box below. If two or more of the
graphs have no negative-cost cycles, then enter the smallest of the lengths of
their shortest shortest paths in the box below.

OPTIONAL: You can use whatever algorithm you like to solve this question. If you
have extra time, try comparing the performance of different all-pairs
shortest-path algorithms!

OPTIONAL: Here is a bigger data set to play with: large.txt
'''

'''
Class for solving all-pairs shortest path problems
'''
class APSP:
    def __init__(self, filename, inf=9999):
        self.filename = filename
        self.inf = inf
        self.readFile(filename)

    def readFile(self, filename):
        with open(filename) as f:
            lines = f.readlines()

        for i in range(len(lines)):
            line = lines[i].split()
            if i == 0:
                self.numVertices = int(line[0])
                self.numEdges = int(line[1])
                self.distanceMatrix = np.full((self.numVertices,
                    self.numVertices), self.inf, dtype='float64')
                for j in range(self.numVertices):
                    self.distanceMatrix[j, j] = 0
            else:
                startVertex = int(line[0]) - 1
                endVertex = int(line[1]) - 1
                length = int(line[2])
                self.distanceMatrix[startVertex, endVertex] = length
    
    def floydWarshall(self):
        A = np.copy(self.distanceMatrix)

        negativeCycle = False
        for k in range(self.numVertices):
            for i in range(self.numVertices):
                for j in range(self.numVertices):
                    A[i, j] = min(A[i, j], A[i, k] + A[k, j])
            if A.diagonal().all() != 0:
                negativeCycle = True
                break

        return negativeCycle, A

    def floydWarshallVectorized(self):
        A = np.copy(self.distanceMatrix)

        negativeCycle = False
        for k in range(self.numVertices):
            A = np.minimum(A, A[np.newaxis, k, :] + A[:, k, np.newaxis])
            if A.diagonal().all() != 0:
                negativeCycle = True
                break

        return negativeCycle, A

    def johnsons(self):
        pass

def runGraph(filename):
    t0 = time.time()
    g = APSP(filename)
    negativeCycle, A = g.floydWarshallVectorized()
    shortestPathLength = A.min()
    print('%s: negative cycle: %s, shortest path length: %s, time: %s'
            %(filename, negativeCycle, shortestPathLength, time.time() - t0))

def runProblem():
    filenames = ['g1.txt', 'g2.txt', 'g3.txt']
    for filename in filenames:
        runGraph(filename)

if __name__ == '__main__':
    runProblem()
