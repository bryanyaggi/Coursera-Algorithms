#!/usr/bin/env python3

import heapq
import time

'''
Programming Assignment 3


Problem 1

In this programming problem and the next you'll code up the greedy algorithm
from the lectures on Huffman coding.

Download the following text file: huffman.txt

This file describes an instance of the problem. It has the following format:

[number_of_symbols]

[weight of symbol #1]

[weight of symbol #2]

...

For example, the third line of the file is "6852892," indicating that the weight
of the second symbol of the alphabet is 6852892. (We're using weights instead of
frequencies, like in the "A More Complex Example" video.)

Your task in this problem is to run the Huffman coding algorithm from lecture on
this data set. What is the maximum length of a codeword in the resulting Huffman
code?

ADVICE: If you're not getting the correct answer, try debugging your algorithm
using some small test cases. And then post them to the discussion forum!


Problem 2

Continuing the previous problem, what is the minimum length of a codeword in
your Huffman code?

'''

'''
Class to store node information for Huffman Code algorithm.
'''
class Node:
    def __init__(self, weight, symbol=None, leftNode=None, rightNode=None):
        self.weight = weight
        self.symbol = symbol
        self.leftNode = leftNode
        self.rightNode = rightNode

    def __lt__(self, other):
        return self.weight < other.weight

    def __repr__(self):
        return 'Node(weight: %s, symbol: %s)' %(self.weight, self.symbol)

'''
Class that implements Huffman Code algorithm.
'''
class HuffmanCode:
    def __init__(self, filename):
        self.codes = {}
        self.heap = []
        self._readFile(filename)
        self._createTree()
        self._generateCodes()

    def _readFile(self, filename):
        with open(filename) as f:
            lines = f.readlines()

        for i in range(len(lines)):
            if i != 0:
                weight = int(lines[i])
                node = Node(weight, symbol=i)
                self.heap.append(node)
        heapq.heapify(self.heap)

    '''
    Builds Huffman binary tree.
    '''
    def _createTree(self):
        if len(self.heap) < 2:
            print('Symbol list too short.')
            return
        else:
            while len(self.heap) >= 2:
                # Note that left and right ordering does not matter.
                left = heapq.heappop(self.heap)
                right = heapq.heappop(self.heap)
                weight = left.weight + right.weight
                heapq.heappush(self.heap,
                        Node(weight, leftNode=left, rightNode=right))

    '''
    Traverses Huffman binary tree recursively encoding symbols.
    '''
    def _generateCodes(self):
        def recurse(node, code):
            if node.symbol is not None:
                self.codes[code] = node.symbol
            else:
                # Following convention
                if node.leftNode is not None:
                    recurse(node.leftNode, code + '0')
                if node.rightNode is not None:
                    recurse(node.rightNode, code + '1')
        
        node = heapq.heappop(self.heap)
        code = ''
        recurse(node, code)
        
    '''
    Prints range of code bit lengths
    '''
    def printBitLengthRange(self):
        codes = list(self.codes.keys())
        codes = sorted(codes, key=len)
        minBits = len(codes[0])
        maxBits = len(codes[-1])
        print('max length = %s, min length = %s' %(maxBits, minBits))

def runHuffmanProblem():
    t0 = time.time()
    huffmanCode = HuffmanCode('huffman.txt')
    huffmanCode.printBitLengthRange()
    print('huffman problem time = %s' %(time.time() - t0))

'''
Problem 3

In this programming problem you'll code up the dynamic programming algorithm for
computing a maximum-weight independent set of a path graph.

Download the following text file: mwis.txt

This file describes the weights of the vertices in a path graph (with the
weights listed in the order in which vertices appear in the path). It has the
following format:

[number_of_vertices]

[weight of first vertex]

[weight of second vertex]

...

For example, the third line of the file is "6395702," indicating that the weight
of the second vertex of the graph is 6395702.

Your task in this problem is to run the dynamic programming algorithm (and the
reconstruction procedure) from lecture on this data set. The question is: of the
vertices 1, 2, 3, 4, 17, 117, 517, and 997, which ones belong to the
maximum-weight independent set? (By "vertex 1" we mean the first vertex of the
graph---there is no vertex 0.) In the box below, enter a 8-bit string, where the
ith bit should be 1 if the ith of these 8 vertices is in the maximum-weight
independent set, and 0 otherwise. For example, if you think that the vertices 1,
4, 17, and 517 are in the maximum-weight independent set and the other four
vertices are not, then you should enter the string 10011010 in the box below.
'''

'''
Class that implements maximum weight independent set algorithm for path graphs.
'''
class Mwis:
    def __init__(self, filename):
        self._readFile(filename)
        self._calcValue()
        self._findMembers()

    def _readFile(self, filename):
        with open(filename) as f:
            lines = f.readlines()

        for i in range(len(lines)):
            if i == 0:
                numVertices = int(lines[i])
                self.vertices = [0] * (numVertices+1)
                self.A = [0] * (numVertices+1)
                self.members = [0] * (numVertices+1)
            else:
                self.vertices[i] = int(lines[i])
            self.A[1] = self.vertices[1]

    '''
    Uses dynamic programming to calculate MWIS value.
    '''
    def _calcValue(self):
        for i in range(2, len(self.vertices)):
            self.A[i] = max(self.A[i-1], self.A[i-2] + self.vertices[i])
        self.value = self.A[-1]

    '''
    Traverses backwards through stored dynamic programming solutions to find
    members.
    '''
    def _findMembers(self):
        i = len(self.A) - 1
        while i >= 1:
            if self.A[i-1] >= self.A[i-2] + self.vertices[i]:
                i -= 1
            else:
                self.members[i] = 1
                i -= 2

    def printResult(self):
        vertices = [1, 2, 3, 4, 17, 117, 517, 997]
        result = ''
        for vertex in vertices:
            if vertex >= len(self.members):
                result += '0'
            else:
                result += str(self.members[vertex])
        
        print(result)

def runMwisProblem():
    t0 = time.time()
    mwis = Mwis('mwis.txt')
    mwis.printResult()
    print('mwis problem time = %s' %(time.time() - t0))

if __name__ == '__main__':
    runHuffmanProblem()
    runMwisProblem()
