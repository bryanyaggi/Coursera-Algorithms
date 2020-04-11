#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import math
import time

'''
Programming Assignment 4

In this assignment you will implement one or more algorithms for the 2SAT
problem.

Here are 6 different 2SAT instances: 2sat*.txt

The file format is as follows. In each instance, the number of variables and the
number of clauses is the same, and this number is specified on the first line of
the file. Each subsequent line specifies a clause via its two literals, with a
number denoting the variable and a "-" sign denoting logical "not". For example,
the second line of the first data file is "-16808 75250", which indicates the
clause not(x_16808) or (x_75250).

Your task is to determine which of the 6 instances are satisfiable, and which
are unsatisfiable. In the box below, enter a 6-bit string, where the ith bit
should be 1 if the ith instance is satisfiable, and 0 otherwise. For example, if
you think that the first 3 instances are satisfiable and the last 3 are not,
then you should enter the string 111000 in the box below.

DISCUSSION: This assignment is deliberately open-ended, and you can implement
whichever 2SAT algorithm you want. For example, 2SAT reduces to computing the
strongly connected components of a suitable graph (with two vertices per
variable and two directed edges per clause, you should think through the
details). This might be an especially attractive option for those of you who
coded up an SCC algorithm in Part 2 of this specialization. Alternatively, you
can use Papadimitriou's randomized local search algorithm. (The algorithm from
lecture is probably too slow as stated, so you might want to make one or more
simple modifications to it - even if this means breaking the analysis given in
lecture - to ensure that it runs in a reasonable amount of time.) A third
approach is via backtracking. In lecture we mentioned this approach only in
passing; see Chapter 9 of the Dasgupta-Papadimitriou-Vazirani book, for example,
for more details.
'''

'''
Class for calculating SCCs
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
    Calculates valid node order for finding SCCs. Run DFS multiple times on
    reversed graph to find all nodes.
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
    Calculates SCCs. Runs DFS multiple times on nodes in specific order to find
    SCCs.
    '''
    def calcSccs(self):
        self.sccs = {}
        explored = set()
        leader = 0

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

    def __repr__(self):
        return 'Graph(%s)' %self.nodes

'''
Class for storing clause literals and producing equivalent implications
'''
class Clause:
    def __init__(self, literal1, literal2):
        self.literals = [literal1, literal2]

    '''
    Returns equivalent implications.
    '''
    def getImplications(self):
        implications = []
        implications.append((-self.literals[0], self.literals[1]))
        implications.append((-self.literals[1], self.literals[0]))
        return implications

'''
Class for 2-SAT problems
'''
class TwoSat:
    def __init__(self, filename):
        self.filename = filename
        self._readFile()

    def _readFile(self):
        with open(self.filename) as f:
            lines = f.readlines()

        for i in range(len(lines)):
            line = lines[i].split()
            if i == 0:
                self.numClauses = int(line[0])
                self.implicationGraph = Graph()
                self.clauses = []
            else:
                literal1 = int(line[0])
                literal2 = int(line[1])
                clause = Clause(literal1, literal2)
                self.clauses.append(clause)
                implications = clause.getImplications()
                for implication in implications:
                    self.implicationGraph.addEdge(implication[0],
                            implication[1])

    '''
    Returns whether 2-SAT is satisfiable.
    '''
    def determineSat(self):
        self.implicationGraph.calcNodeOrder()
        self.implicationGraph.calcSccs()

        for leadNode in self.implicationGraph.sccs:
            scc = self.implicationGraph.sccs[leadNode]
            for node in scc:
                if -node in scc:
                    return False
        return True
        
def runProblem(filename):
    for filename in filenames:
        t0 = time.time()
        twoSat = TwoSat(filename)
        sat = twoSat.determineSat()
        print('%s: satisfiable: %s, time = %s' %(filename, sat,
            time.time() - t0))

if __name__ == '__main__':
    #filenames = ['2satTest.txt']
    filenames = ['2sat1.txt', '2sat2.txt', '2sat3.txt', '2sat4.txt',
            '2sat5.txt', '2sat6.txt']
    runProblem(filenames)
