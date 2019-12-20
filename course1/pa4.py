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

def readFile(filename):
    with open(filename) as f:
        lines = f.readlines()
    edges = 0
    graph = {}
    for line in lines:
        line = line.split()
        vertex = int(line[0])
        adjVerts = [int(x) for x in line[1:]]
        graph[vertex] = adjVerts
        edges += len(adjVerts)
    edges /= 2
    return graph, edges

def contract(graph, edges, verbose=False):
    graph = copy.deepcopy(graph)

    while len(graph) > 2:
        # Select random edge
        edgeIndex = random.randint(0, 2*edges)

        # Find vertices of selected edge
        
        for key in graph.keys():
            if edgeIndex < len(graph[key]):
                break
            edgeIndex -= len(graph[key])
        vertices = [key, graph[key][edgeIndex]]
        

        '''
        vertices = []
        vertices.append(random.choice(list(graph.keys())))
        vertices.append(random.choice(list(graph[vertices[0]])))
        '''

        if verbose:
            print('graph = %s' %graph)
            print('edges = %d' %edges)
            print('edgeIndex = %d' %edgeIndex)
            print('vertices = %s' %vertices)
            print('%s' %(60*'-'))

        # Keep first vertex, remove instances of second vertex in adjacent list
        while vertices[1] in graph[vertices[0]]:
            graph[vertices[0]].remove(vertices[1])
            edges -= 1
        # Merge adjacect vertices of second vertex into first
        for adjVertex in graph[vertices[1]]:
            if adjVertex != vertices[0]:
                graph[vertices[0]].append(adjVertex)
        graph.pop(vertices[1])
        # Replace second vertex with first in graph adjacent lists
        for key in graph.keys():
            for i in range(len(graph[key])):
                if graph[key][i] == vertices[1]:
                    graph[key][i] = vertices[0]

    if verbose:
        print('graph = %s' %graph)
        print('edges = %s' %edges)
    
    return edges

def testResult(graph):
    return 0

if __name__ == '__main__':
    graph, edges = readFile('KargerMinCut.txt')
    '''
    graph = {1:[2,3], 2:[1,3,4], 3:[1,2,4], 4:[2,3]}
    edges = 5
    '''
    results = []
    t0 = time.time()
    for i in range(200):
        results.append(contract(graph, edges))
    t1 = time.time()
    print('results = %s' %results)
    print('min cut = %d' %(min(results)))
    print('total time = %f s' %(t1-t0))
