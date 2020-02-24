#!/usr/bin/env python3

import time

'''
Programming Assignment 2


Problem 1

In this programming problem and the next you'll code up the clustering algorithm
from lecture for computing a max-spacing k-clustering.

Download the following text file: clustering1.txt

This file describes a distance function (equivalently, a complete graph with
edge costs). It has the following format:

[number_of_nodes]

[edge 1 node 1] [edge 1 node 2] [edge 1 cost]

[edge 2 node 1] [edge 2 node 2] [edge 2 cost]

...

There is one edge (i,j) for each choice of 1 <= i < j <= n, where n is the
number of nodes.

For example, the third line of the file is "1 3 5250", indicating that the
distance between nodes 1 and 3 (equivalently, the cost of the edge (1,3)) is
5250. You can assume that distances are positive, but you should NOT assume that
they are distinct.

Your task in this problem is to run the clustering algorithm from lecture on
this data set, where the target number k of clusters is set to 4. What is the
maximum spacing of a 4-clustering?

ADVICE: If you're not getting the correct answer, try debugging your algorithm
using some small test cases. And then post them to the discussion forum!


Problem 2

In this question your task is again to run the clustering algorithm from
lecture, but on a MUCH bigger graph. So big, in fact, that the distances (i.e.,
edge costs) are only defined implicitly, rather than being provided as an
explicit list.

Download the following text file: clustering2.txt

The format is:

[# of nodes] [# of bits for each node's label]

[first bit of node 1] ... [last bit of node 1]

[first bit of node 2] ... [last bit of node 2]

...

For example, the third line of the file "0 1 1 0 0 1 1 0 0 1 0 1 1 1 1 1 1 0 1 0
1 1 0 1" denotes the 24 bits associated with node #2.

The distance between two nodes u and v in this problem is defined as the Hamming
distance - the number of differing bits - between the two nodes' labels. For
example, the Hamming distance between the 24-bit label of node #2 above and the
label "0 1 0 0 0 1 0 0 0 1 0 1 1 1 1 1 1 0 1 0 0 1 0 1" is 3 (since they differ
in the 3rd, 7th, and 21st bits).

The question is: what is the largest value of k such that there is a
k-clustering with spacing at least 3? That is, how many clusters are needed to
ensure that no pair of nodes with all but 2 bits in common get split into
different clusters?

NOTE: The graph implicitly defined by the data file is so big that you probably
can't write it out explicitly, let alone sort the edges by cost. So you will
have to be a little creative to complete this part of the question. For example,
is there some way you can identify the smallest distances without explicitly
looking at every pair of nodes?

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
Class that implements union-find data structure.
'''
class UnionFind:
    def __init__(self):
        self.numSubsets = 0
        self.subsets = []

    def __repr__(self):
        return 'UnionFind(subsets: %s)' %self.subsets

    def len(self):
        return len(self.subsets)

    def add(self, parent):
        self.subsets.append(Subset(parent))
        self.numSubsets += 1

    def find(self, node):
        if self.subsets[node].parent != node:
            self.subsets[node].parent = self.find(self.subsets[node].parent)
        return self.subsets[node].parent

    def union(self, node1, node2):
        parent1 = self.find(node1)
        parent2 = self.find(node2)

        if parent1 == parent2:
            return
        if self.subsets[parent1].rank >= self.subsets[parent2].rank:
            self.subsets[parent2].parent = parent1
            if self.subsets[parent1].rank == self.subsets[parent2].rank:
                self.subsets[parent1].rank += 1
        else:
            self.subsets[parent1].parent = parent2
        self.numSubsets -= 1

    def checkSameSubset(self, node1, node2):
        if self.find(node1) == self.find(node2):
            return True
        return False

'''
Class to store graph information. Implements union-find data structure. 
'''
class Graph:
    def __init__(self, filename):
        self.nodes = UnionFind()
        self.edges = {}
        self.readFile(filename)

    def readFile(self, filename):
        with open(filename) as f:
            lines = f.readlines()

        for i in range(len(lines)):
            if i == 0:
                numNodes = int(lines[i])
                for j in range(numNodes):
                    self.nodes.add(j)
            else:
                line = lines[i].split()
                self.addEdge(int(line[0])-1, int(line[1])-1, int(line[2]))

    '''
    Adds an edge to the graph.
    node1 is first node
    node2 is second node
    cost is edge cost
    '''
    def addEdge(self, node1, node2, cost):
        assert node1 != node2, 'Cannot create edge between node and itself.'
        assert node1 < self.nodes.len(), 'First node index too large.'
        assert node2 < self.nodes.len(), 'Second node index too large.'

        nodes = (0, 0)
        if node1 < node2:
            nodes = (node1, node2)
        else:
            nodes = (node2, node1)

        self.edges[nodes] = cost

    def cluster(self, k):
        assert k <= self.nodes.len(), 'k too large.'
        assert k >= 0, 'k must be positive.'

        edgesSorted = sorted(self.edges, key=self.edges.get, reverse=False)

        # Cluster nodes
        i = 0
        while self.nodes.numSubsets > k:
            assert i < len(edgesSorted), 'Not enough edges.'

            edgePair = edgesSorted[i]
            self.nodes.union(edgePair[0], edgePair[1])
            i += 1

        # Find maximum spacing (minimum distance between nodes in different
        # subsets)
        while i < len(edgesSorted):
            edgePair = edgesSorted[i]
            if not self.nodes.checkSameSubset(edgePair[0], edgePair[1]):
                return self.edges[edgePair]
            i += 1
        
        print('No maximum spacing found.')
        return -1

if __name__ == '__main__':
    graph = Graph('clustering1.txt')
    print('p1 result = %s' %graph.cluster(4))
