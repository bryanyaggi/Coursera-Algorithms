#!/usr/bin/env python3

import random
import copy
import time

'''
Programming Assignment 4

The file contains the adjacency list representation of a simple undirected
graph. There are 200 vertices labeled 1 to 200. The first column in the file
represents the vertex label, and the particular row (other entries except the
first column) tells all the vertices that the vertex is adjacent to. So for
example, the 6th row looks like : "6 155 56 52 120 ......". This just means
that the vertex with label 6 is adjacent to (i.e., shares an edge with)
the vertices with labels 155, 56, 52, 120, ..., etc.

Your task is to code up and run the randomized contraction algorithm for the min
cut problem and use it on the above graph to compute the min cut. (HINT: Note
that you'll have to figure out an implementation of edge contractions.
Initially, you might want to do this naively, creating a new graph from the old
every time there's an edge contraction. But you should also think about more
efficient implementations.) (WARNING: As per the video lectures, please make
sure to run the algorithm many times with different random seeds, and remember
the smallest cut that you ever find.) Write your numeric answer in the space
provided. So e.g., if your answer is 5, just type 5 in the space provided.
'''

'''
Class to store parent and rank information for each node. Part of union-find
data structure.
'''
class Subset:
    def __init__(self, parent):
        self.parent = parent
        self.rank = 0

    def __repr__(self):
        return 'Subset(parent: %s, rank: %s)' %(self.parent, self.rank)

'''
Class to store graph information. Implements union-find data structure.
'''
class Graph:
    def __init__(self):
        self.numSubsets = 0
        self.edges = []
        self.subsets = []

    def addNode(self):
        self.subsets.append(Subset(self.numSubsets))
        self.numSubsets += 1

    def addEdge(self, srcNode, destNode):
        self.edges.append((srcNode, destNode))

    '''
    Finds parent of given node.
    '''
    def find(self, node):
        if self.subsets[node].parent != node:
            self.subsets[node].parent = self.find(self.subsets[node].parent)
        return self.subsets[node].parent

    '''
    Unifies 2 nodes by merging them into the same subset.
    '''
    def union(self, nodeA, nodeB):
        parentA = self.find(nodeA)
        parentB = self.find(nodeB)

        if parentA == parentB:
            return
        if self.subsets[parentA].rank >= self.subsets[parentB].rank:
            self.subsets[parentB].parent = parentA
            if self.subsets[parentA].rank == self.subsets[parentB].rank:
                self.subsets[parentA].rank += 1
        else:
            self.subsets[parentA].parent = parentB
        self.numSubsets -= 1

    '''
    Counts cut edges between 2 subsets.
    '''
    def countCutEdges(self):
        if self.numSubsets != 2:
            return -1

        cutEdges = 0
        for i in range(len(graph.edges)):
            if self.find(self.edges[i][0]) != self.find(self.edges[i][1]):
                cutEdges += 1
        return cutEdges / 2

    
    def __repr__(self):
        return ('Graph(numSubsets: %s, edges: %s, subsets: %s)'
                %(self.numSubsets, self.edges, self.subsets))

def readFile(filename):
    graph = Graph()

    with open(filename) as f:
        lines = f.readlines()

    for line in lines:
        line = line.split()
        graph.addNode()
        for node in line[1:]:
            graph.addEdge(graph.numSubsets-1, int(node)-1)

    return graph

'''
Contract random edge until 2 subsets left. Returns number of edges between 2
subsets.

graph is an instance of Graph
verbose prints information for each contract iteration
returns number of edges between 2 subsets
'''
def contract(graph, verbose=False):
    # Create randomly shuffled edge list
    shuffledEdges = copy.deepcopy(graph.edges)
    random.shuffle(shuffledEdges)
    index = 0

    while graph.numSubsets > 2:
        if index >= len(shuffledEdges):
            print('ERROR: Not enough edges; cannot contract further.')
            return -1

        src, dest = shuffledEdges[index] # select random edge
        index += 1

        graph.union(src, dest)

    if verbose:
        print(graph)

    return graph.countCutEdges()

def testGraph():
    graph = Graph()

    for i in range(4):
        graph.addNode()

    graph.addEdge(0,1)
    graph.addEdge(0,2)
    graph.addEdge(1,0)
    graph.addEdge(1,2)
    graph.addEdge(1,3)
    graph.addEdge(2,0)
    graph.addEdge(2,1)
    graph.addEdge(2,3)
    graph.addEdge(3,1)
    graph.addEdge(3,2)

    return graph

if __name__ == '__main__':
    graph = readFile('KargerMinCut.txt')
    #graph = testGraph()
    #print(graph)

    numSubsets = graph.numSubsets
    subsets = copy.deepcopy(graph.subsets)
    results = []
    iterations = 200
    t0 = time.time()
    for i in range(iterations):
        # Reset modified graph data
        graph.numSubsets = numSubsets
        graph.subsets = copy.deepcopy(subsets)

        results.append(contract(graph))

        if i % 100 == 0:
            print('Progress: iteration %d/%d' %(i, iterations), end='\r')

    t1 = time.time()
    print('results = %s' %results)
    print('min cut = %d' %(min(results)))
    print('total time = %f s' %(t1-t0))
