#!/usr/bin/env python3

import time
import random
from heapdict import heapdict

'''
Programming Assignment 1


Problem 1

In this programming problem and the next you'll code up the greedy algorithms
from lecture for minimizing the weighted sum of completion times.

Download the following text file: jobs.txt

This file describes a set of jobs with positive and integral weights and
lengths. It has the format:

[number_of_jobs]

[job_1_weight] [job_1_length]

[job_2_weight] [job_2_length]

...

For example, the third line of the file is "74 59", indicating that the second
job has weight 74 and length 59.

You should NOT assume that edge weights or lengths are distinct.

Your task in this problem is to run the greedy algorithm that schedules jobs in
decreasing order of the difference (weight - length). Recall from lecture that
this algorithm is not always optimal. IMPORTANT: if two jobs have equal
difference (weight - length), you should schedule the job with higher weight
first. Beware: if you break ties in a different way, you are likely to get the
wrong answer. You should report the sum of weighted completion times of the
resulting schedule --- a positive integer --- in the box below.

ADVICE: If you get the wrong answer, try out some small test cases to debug your
algorithm (and post your test cases to the discussion forum).


Problem 2

For this problem, use the same data set as in the previous problem.

Your task now is to run the greedy algorithm that schedules jobs (optimally) in
decreasing order of the ratio (weight/length). In this algorithm, it does not
matter how you break ties. You should report the sum of weighted completion
times of the resulting schedule --- a positive integer --- in the box below. 
'''

'''
Class for scheduling.
'''
class Scheduler:
    def __init__(self, filename):
        self.jobs = self.readFile(filename)

    def readFile(self, filename):
        with open(filename) as f:
            lines = f.readlines()

        jobs = []
        for i in range(len(lines)):
            if i != 0: # skip first line
                line = lines[i].split()
                job = {'jid': i}
                job['weight'] = int(line[0])
                job['length'] = int(line[1])
                jobs.append(job)

        return jobs

    '''
    Calculates Problem 1 score for each job.
    '''
    def calcP1Score(self):
        for job in self.jobs:
            score = job['weight'] - job['length']
            job['p1Score'] = score

    '''
    Calculates Problem 2 score for each job.
    '''
    def calcP2Score(self):
        for job in self.jobs:
            score = job['weight'] / job['length']
            job['p2Score'] = score

    '''
    Calculates sum of weighted completion times for given job order.
    sortedJobs is sorted list of jobs
    '''
    def calcSumWeightedCompletions(self, sortedJobs):
        result = 0
        compTime = 0
        for job in sortedJobs:
            compTime += job['length']
            result += job['weight'] * compTime

        return result

    '''
    Calculates Problem 1 result.
    '''
    def calcP1Result(self):
        self.calcP1Score()
        jobsSorted = sorted(self.jobs,
                key = lambda x: (x['p1Score'], x['weight']), reverse=True)
        return self.calcSumWeightedCompletions(jobsSorted)

    '''
    Calculates Problem 2 result.
    '''
    def calcP2Result(self):
        self.calcP2Score()
        jobsSorted = sorted(self.jobs,
                key = lambda x: x['p2Score'], reverse=True)
        return self.calcSumWeightedCompletions(jobsSorted)

def runSchedulingProblems():
    t0 = time.time()
    scheduler = Scheduler('jobs.txt')
    print('p1 result = %s' %scheduler.calcP1Result())
    print('p2 result = %s' %scheduler.calcP2Result())
    print('p1 and p2 time = %f' %(time.time() - t0))

'''
Problem 3

In this programming problem you'll code up Prim's minimum spanning tree
algorithm.

Download the following text file: edges.txt

This file describes an undirected graph with integer edge costs. It has the
format:

[number_of_nodes] [number_of_edges]

[one_node_of_edge_1] [other_node_of_edge_1] [edge_1_cost]

[one_node_of_edge_2] [other_node_of_edge_2] [edge_2_cost]

...

For example, the third line of the file is "2 3 -8874", indicating that there is
an edge connecting vertex #2 and vertex #3 that has cost -8874.

You should NOT assume that edge costs are positive, nor should you assume that
they are distinct.

Your task is to run Prim's minimum spanning tree algorithm on this graph. You
should report the overall cost of a minimum spanning tree --- an integer, which
may or may not be negative --- in the box below.

IMPLEMENTATION NOTES: This graph is small enough that the straightforward O(mn)
time implementation of Prim's algorithm should work fine. OPTIONAL: For those of
you seeking an additional challenge, try implementing a heap-based version. The
simpler approach, which should already give you a healthy speed-up, is to
maintain relevant edges in a heap (with keys = edge costs). The superior
approach stores the unprocessed vertices in the heap, as described in lecture.
Note this requires a heap that supports deletions, and you'll probably need to
maintain some kind of mapping between vertices and their positions in the heap.
'''

'''
Class for running Prim's algorithm on a graph.
'''
class Graph:
    def __init__(self, filename=None, maxCost=1000000):
        self.nodes = {}
        self.mst = []
        if filename is not None:
            self.readFilename(filename)
        self.maxCost = maxCost

    def readFilename(self, filename):
        with open(filename) as f:
            lines = f.readlines()

        for i in range(len(lines)):
            if i != 0:
                line = lines[i].split()
                self.addEdge(int(line[0]), int(line[1]), int(line[2]))

    '''
    Adds a node to the graph.
    node is new node
    '''
    def addNode(self, node):
        if node not in self.nodes:
            self.nodes[node] = {}

    '''
    Adds an edge to the graph.
    node1 is first node
    node2 is second node
    cost is edge cost
    '''
    def addEdge(self, node1, node2, cost):
        self.addNode(node1)
        self.addNode(node2)
        self.nodes[node1][node2] = cost
        self.nodes[node2][node1] = cost

    '''
    Runs Prim's algorithm to find a MST.
    verbose prints the heap contents on each iteration
    '''
    def prims(self, verbose=False):
        '''
        Prints heapdict contents.
        '''
        def printHeap(heap):
            print('heap contents:')
            for element in heap:
                print(element, heap[element])

        startNode = random.choice(list(self.nodes))
        explored = {startNode}
        self.mst = [(startNode, 0)]
        unexplored = heapdict()
        for node in self.nodes:
            if node not in explored:
                unexplored[node] = self.maxCost
        if verbose:
            printHeap(unexplored)

        newNode = startNode
        while(unexplored): # not empty
            # Update heap
            for uNode in unexplored:
                if newNode in self.nodes[uNode]:
                    newCost = self.nodes[uNode][newNode]
                    if newCost < unexplored[uNode]:
                        unexplored[uNode] = newCost
            if verbose:
                printHeap(unexplored)

            # Extract new node and cost, add to MST
            newNode, cost = unexplored.popitem()
            self.mst.append((node, cost))

    '''
    Calculates MST path cost.
    '''
    def calcMstCost(self):
        totalCost = 0
        for edge in self.mst:
            totalCost += edge[1]
        return totalCost

def runPrimsProblem():
    t0 = time.time()
    graph = Graph('edges.txt')
    graph.prims()
    print('p3 result = %s' %graph.calcMstCost())
    print('p3 time = %f' %(time.time() - t0))

if __name__ == '__main__':
    runSchedulingProblems()
    runPrimsProblem()
