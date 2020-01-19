#!/usr/bin/env python3

import sys
import threading
import time

# Hitting limits if the following are not modified
sys.setrecursionlimit(800000)
threading.stack_size(67108864)

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
        self.sccs = {}

    '''
    Adds node to graph.
    node is integer node ID
    '''
    def addNode(self, node):
        if node not in self.nodes:
            self.nodes[node] = {'in': set(), 'out': set()}

    '''
    Adds edge to graph.
    srcNode is integer node ID of source node
    destNode is integer node ID of destination node
    '''
    def addEdge(self, srcNode, destNode):
        self.addNode(srcNode)
        self.addNode(destNode)
        self.nodes[srcNode]['out'].add(destNode)
        self.nodes[destNode]['in'].add(srcNode)

    '''
    Calculates valid node order for finding SCCs. This function runs the first
    "DFS-Loop" discussed in lecture.
    '''
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

    '''
    Calculates SCCs. This function runs the second "DFS-Loop" discussed in
    lecture.
    '''
    def calcSccs(self):
        self.sccs = {} # reset
        explored = set()
        leader = -1

        def dfs(node):
            explored.add(node)
            if node == leader:
                self.sccs[leader] = set()
            else:
                self.sccs[leader].add(node)
            for destNode in self.nodes[node]['out']:
                if destNode not in explored:
                    dfs(destNode)

        for i in range(len(self.nodeOrder)-1, -1, -1):
            if self.nodeOrder[i] not in explored:
                leader = self.nodeOrder[i]
                dfs(leader)

    '''
    Prints 5 largest SCC sizes.
    '''
    def printSccSizes(self):
        sccSizes = []
        for scc in self.sccs:
            sccSizes.append(len(self.sccs[scc])+1)
        sccSizes.sort(reverse=True)
        for i in range(4):
            sccSizes.append(0)
        print('5 largest SCCs: %s' %(sccSizes[:5]))

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

def main():
    t0 = time.time()
    graph = readFile('SCC.txt')
    #graph = testGraph()
    #print(graph.nodes)
    graph.calcNodeOrder()
    #print(graph.nodeOrder)
    graph.calcSccs()
    #print(graph.sccs)
    graph.printSccSizes()
    print('total time = %f' %(time.time() - t0))

if __name__ == '__main__':
    thread = threading.Thread(target=main)
    thread.start()
