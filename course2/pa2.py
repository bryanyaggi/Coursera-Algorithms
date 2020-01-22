#!/usr/bin/env python3

import time
from heapdict import heapdict

'''
Programming Assignment 2

In this programming problem you'll code up Dijkstra's shortest-path algorithm.

Download the following text file: dijkstraData.txt

The file contains an adjacency list representation of an undirected weighted
graph with 200 vertices labeled 1 to 200. Each row consists of the node tuples
that are adjacent to that particular vertex along with the length of that edge.
For example, the 6th row has 6 as the first entry indicating that this row
corresponds to the vertex labeled 6. The next entry of this row "141,8200"
indicates that there is an edge between vertex 6 and vertex 141 that has length
8200. The rest of the pairs of this row indicate the other vertices adjacent to
vertex 6 and the lengths of the corresponding edges.

Your task is to run Dijkstra's shortest-path algorithm on this graph, using 1
(the first vertex) as the source vertex, and to compute the shortest-path
distances between 1 and every other vertex of the graph. If there is no path
between a vertex v and vertex 1, we'll define the shortest-path distance
between 1 and v to be 1000000.

You should report the shortest-path distances to the following ten vertices, in
order: 7,37,59,82,99,115,133,165,188,197. You should encode the distances as a
comma-separated string of integers. So if you find that all ten of these
vertices except 115 are at distance 1000 away from vertex 1 and 115 is 2000
distance away, then your answer should be 1000,1000,1000,1000,1000,2000,1000,
1000,1000,1000. Remember the order of reporting DOES MATTER, and the string
should be in the same order in which the above ten vertices are given. The
string should not contain any spaces. Please type your answer in the space
provided.

IMPLEMENTATION NOTES: This graph is small enough that the straightforward O(mn)
time implementation of Dijkstra's algorithm should work fine. OPTIONAL: For
those of you seeking an additional challenge, try implementing the heap-based
version. Note this requires a heap that supports deletions, and you'll probably
need to maintain some kind of mapping between vertices and their positions in
the heap.
'''

'''
Class to store graph information.
'''
class Graph:

    def __init__(self, sourceNode=1, maxLength=1000000):
        self.nodes = {}
        self.distances = {}
        self.sourceNode = sourceNode
        self.maxLength = maxLength

    '''
    Adds node to graph.
    node is integer node ID
    '''
    def addNode(self, node):
        if node not in self.nodes:
            self.nodes[node] = {}

    '''
    Adds edge to graph.
    srcNode is integer node ID of source node
    destNode is integer node ID of destination node
    length is length from source to destination nodes
    '''
    def addEdge(self, srcNode, destNode, length):
        self.addNode(srcNode)
        self.addNode(destNode)
        self.nodes[srcNode][destNode] = length

    def dijkstras(self):
        self.distances = {} # reset
        
        hd = heapdict() # initialize heapdict
        for node in self.nodes:
            if node == self.sourceNode:
                hd[node] = 0
            else:
                hd[node] = self.maxLength

        for key in hd:
            print(key)
        
        if self.sourceNode not in hd:
            print('dijkstras error: No source node.')
            return

        distance = 0
        while(hd): # not empty
            node, length = hd.popitem()
            distance += length
            self.distances[node] = distance

            for neighbor in self.nodes[node]:
                if neighbor in hd:
                    if self.nodes[node][neighbor] < hd[neighbor]:
                        hd[neighbor] = self.nodes[node][neighbor]

def readFile(filename):
    graph = Graph()

    with open(filename) as f:
        lines = f.readlines()

    for line in lines:
        line = line.split()
        graph.addNode(int(line[0]))
        for entry in line[1:]:
            entry = entry.split(',')
            if len(entry) == 2:
                graph.addEdge(int(line[0]), int(entry[0]), int(entry[1]))

    return graph

def testGraph():
    graph = Graph()

    graph.addEdge(1, 2, 1)
    graph.addEdge(1, 3, 4)
    graph.addEdge(2, 3, 2)
    graph.addEdge(2, 4, 6)
    graph.addEdge(3, 4, 3)

    return graph

if __name__ == '__main__':
    t0 = time.time()
    #graph = readFile('dijkstraData.txt')
    graph = testGraph()
    print(graph.nodes)
    graph.dijkstras()
    print(graph.distances)
    print('total time = %f' %(time.time() - t0))
