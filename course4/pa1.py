#!/usr/bin/env python3

import numpy as np
import multiprocessing as mp
import time
from heapdict import heapdict
import copy

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
Class for storing edge information
'''
class Edge:
    def __init__(self, startVertex, endVertex, length):
        self.startVertex = startVertex
        self.endVertex = endVertex
        self.length = length

    def __repr__(self):
        return ('Edge(start: %s, end: %s, length: %s)'
                %(self.startVertex, self.endVertex, self.length))

'''
Bellman-Ford algorithm used by Johnson's algorithm

vertices is a list of vertices
edges is a list of edges
returns whether negative cycle detected and list of distances to each vertex
'''
def bellmanFord(vertices, edges, sourceVertex, inf=9999):
    distances = [inf] * len(vertices)
    for vertex in vertices:
        if vertex == sourceVertex:
            distances[vertex] = 0
        else:
            distances[vertex] = inf

    # Relax iteratively, last iteration checks for negative cycles
    negativeCycle = False
    for i in range(len(vertices)):
        for edge in edges:
            newDistance = distances[edge.startVertex] + edge.length
            if newDistance < distances[edge.endVertex]:
                if i == len(vertices) - 1:
                    negativeCycle = True
                distances[edge.endVertex] = newDistance

    return negativeCycle, distances

'''
Dijkstra's algorithm used by Johnson's algorithm

vertices is a dictionary with adjacent vertices
returns list of distances to each vertex
'''
def dijkstras(vertices, sourceVertex, inf=9999):
    distances = [inf] * len(vertices)
    distances[sourceVertex] = 0

    hd = heapdict() # initialize heap
    for vertex in vertices:
        if vertex == sourceVertex:
            hd[vertex] = 0
        else:
            hd[vertex] = inf

    while(hd): # not empty
        vertex, distance = hd.popitem()
        distances[vertex] = distance

        # Update frontier vertices
        for neighbor in vertices[vertex]:
            if neighbor in hd:
                newDistance = distance + vertices[vertex][neighbor]
                if newDistance < hd[neighbor]:
                    hd[neighbor] = newDistance

    return distances

'''
Class for solving all-pairs shortest path problems
'''
class APSP:
    def __init__(self, filename, inf=9999):
        self.filename = filename
        self.inf = inf
        self.vertices = {}
        self.edges = []
        self._readFile(filename)

    def _initializeDistanceMatrix(self):
        self.distanceMatrix = np.full((self.numVertices, self.numVertices),
                self.inf, dtype='float64')
        for j in range(self.numVertices):
            self.distanceMatrix[j, j] = 0

    def _addVertex(self, vertex):
        if vertex not in self.vertices:
            self.vertices[vertex] = {}

    def _addEdge(self, startVertex, endVertex, length):
        # Add edge to distance matrix
        self.distanceMatrix[startVertex, endVertex] = length
        
        # Add edge to vertex dictionary
        self._addVertex(startVertex)
        self._addVertex(endVertex)
        self.vertices[startVertex][endVertex] = length

        # Add edge to edge list
        self.edges.append(Edge(startVertex, endVertex, length))

    def _readFile(self, filename):
        with open(filename) as f:
            lines = f.readlines()

        for i in range(len(lines)):
            line = lines[i].split()
            if i == 0:
                self.numVertices = int(line[0])
                self.numEdges = int(line[1])
                self._initializeDistanceMatrix()
            else:
                startVertex = int(line[0]) - 1
                endVertex = int(line[1]) - 1
                length = int(line[2])
                self._addEdge(startVertex, endVertex, length)
    
    '''
    Solves all pairs shortest path using naive Floyd-Warshall algorithm
    '''
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

    '''
    Vectorized, faster Floyd-Warshall algorithm implementation
    '''
    def floydWarshallVectorized(self):
        A = np.copy(self.distanceMatrix)

        negativeCycle = False
        for k in range(self.numVertices):
            A = np.minimum(A, A[np.newaxis, k, :] + A[:, k, np.newaxis])
            if A.diagonal().all() != 0:
                negativeCycle = True
                break

        return negativeCycle, A    
    
    '''
    Solves all pairs shortest path using Johnson's algorithm
    '''
    def johnsons(self):
        vertices = list(self.vertices.keys())
        edges = self.edges.copy()

        # Add vertex to graph and zero-length path to each vertex
        newVertex = -1
        vertices.append(newVertex)
        for vertex in self.vertices:
            edges.append(Edge(newVertex, vertex, 0))

        # Bellman-Ford to find minimum path to each vertex
        negativeCycle, bfDistances = bellmanFord(vertices, edges,
                newVertex, inf=self.inf)
        bfDistances = bfDistances[:-1] # remove element for extra vertex
        
        if negativeCycle:
            return negativeCycle, None

        # Reweigh edges (updating only vertices dictionary)
        for edge in self.edges:
            length = (edge.length + bfDistances[edge.startVertex] -
                    bfDistances[edge.endVertex])
            self.vertices[edge.startVertex][edge.endVertex] = length

        # Dijkstra's from each vertex to find shortest paths
        A = np.zeros((self.numVertices, self.numVertices))
        for sourceVertex in self.vertices:
            A[sourceVertex, :] = dijkstras(self.vertices, sourceVertex,
                    inf=self.inf)

        # Undo edge reweighting to retrieve actual distances (vectorized)
        A = A + np.array(bfDistances) - np.array(bfDistances)[:, np.newaxis]
        
        return negativeCycle, A

def testBellmanFord():
    vertices = ['s', 'v', 'x', 'w', 't']
    edges = []
    edges.append(Edge('s', 'v', 2))
    edges.append(Edge('s', 'x', 4))
    edges.append(Edge('v', 'x', 1))
    edges.append(Edge('v', 'w', 2))
    edges.append(Edge('x', 't', 4))
    edges.append(Edge('w', 't', 2))
    sourceVertex = 's'

    negativeCycle, distances = bellmanFord(vertices, edges, sourceVertex)
    print('negativeCycle: %s, distances: %s' %(negativeCycle, distances))

def runGraphFloydWarshall(filename):
    t0 = time.time()
    g = APSP(filename)
    negativeCycle, A = g.floydWarshallVectorized()
    shortestPathLength = A.min()
    print('%s: negative cycle: %s, shortest path length: %s, time: %s'
            %(filename, negativeCycle, shortestPathLength, time.time() - t0))

def runGraphJohnsons(filename):
    t0 = time.time()
    g = APSP(filename)
    negativeCycle, A = g.johnsons()
    if A is not None:
        shortestPathLength = A.min()
    else:
        shortestPathLength = None
    print('%s: negative cycle: %s, shortest path length: %s, time: %s'
            %(filename, negativeCycle, shortestPathLength, time.time() - t0))

def runProblem():
    filenames = ['g1.txt', 'g2.txt', 'g3.txt']
    print('Floyd-Warshall algorithm')
    for filename in filenames:
        runGraphFloydWarshall(filename)
    print('Johnson\'s algorithm')
    for filename in filenames:
        runGraphJohnsons(filename)

def runOptionalProblem():
    filename = 'large.txt'
    runGraph(filename)

if __name__ == '__main__':
    runProblem()
    #runOptionalProblem()
