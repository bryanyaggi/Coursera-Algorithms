#!/usr/bin/env python3

import random
import copy
import time

'''
Programming Assignment 1

The file contains the edges of a directed graph. Vertices are labeled as
positive integers from 1 to 875714. Every row indicates an edge, the vertex
label in first column is the tail and the vertex label in second column is the
head (recall the graph is directed, and the edges are directed from the first
column vertex to the second column vertex). So for example, the 11th row looks
like: "2 47646". This just means that the vertex with label 2 has an outgoing
edge to the vertex with label 47646.

Your task is to code up the algorithm from the video lectures for computing
strongly connected components (SCCs), and to run this algorithm on the given
graph.

Output Format: You should output the sizes of the 5 largest SCCs in the given
graph, in decreasing order of sizes, separated by commas (avoid any spaces). So
if your algorithm computes the sizes of the five largest SCCs to be 500, 400,
300, 200 and 100, then your answer should be "500,400,300,200,100" (without the
quotes). If your algorithm finds less than 5 SCCs, then write 0 for the
remaining terms. Thus, if your algorithm computes only 3 SCCs whose sizes are
400, 300, and 100, then your answer should be "400,300,100,0,0" (without the
quotes). (Note also that your answer should not have any spaces in it.)

WARNING: This is the most challenging programming assignment of the course.
Because of the size of the graph you may have to manage memory carefully. The
best way to do this depends on your programming language and environment, and we
strongly suggest that you exchange tips for doing this on the discussion forums.
'''

'''
Class to store graph information.
'''
class Graph:
    def __init__(self):
        self.nodes = {}
        self.nodeOrder = []

    def addNode(self, node):
        if node not in self.nodes:
            self.nodes[node] = {'in': set(), 'out': set()}

    def addEdge(self, srcNode, destNode):
        self.addNode(srcNode)
        self.addNode(destNode)
        self.nodes[srcNode]['out'].add(destNode)
        self.nodes[destNode]['in'].add(srcNode)

    def calcNodeOrder(self):
        self.nodeOrder = [] # reset
        explored = set()

        def dfs(node):
            explored.add(node)
            for srcNode in self.nodes[node]['in']:
                if srcNode not in explored:
                    dfs(srcNode)
            self.nodeOrder.append(node)

        for node in self.nodes:
            if node not in explored:
                dfs(node)
    
    def __repr__(self):
        return ('Graph(nodes: %s)'
                %(self.nodes))

def readFile(filename):
    graph = Graph()

    with open(filename) as f:
        lines = f.readlines()

    for line in lines:
        line = line.split()
        graph.addEdge(int(line[0]), int(line[1]))

    return graph

def testGraph():
    graph = Graph()

    graph.addEdge(7,1)
    graph.addEdge(5,2)
    graph.addEdge(9,3)
    graph.addEdge(1,4)
    graph.addEdge(8,5)
    graph.addEdge(3,6)
    graph.addEdge(8,6)
    graph.addEdge(4,7)
    graph.addEdge(9,7)
    graph.addEdge(2,8)
    graph.addEdge(6,9)

    return graph

if __name__ == '__main__':
    #graph = readFile('SCC.txt')
    graph = testGraph()
    print(graph)
    graph.calcNodeOrder()
    print(graph.nodeOrder)
