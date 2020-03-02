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

class HuffmanCode:
    def __init__(self, filename):
        self.codes = {}
        self.heap = []
        self.readFile(filename)

    def readFile(self, filename):
        with open(filename) as f:
            lines = f.readlines()

        for i in range(len(lines)):
            if i != 0:
                weight = int(lines[i])
                node = Node(weight, symbol=i)
                self.heap.append(node)
        heapq.heapify(self.heap)

    def createTree(self):
        if len(self.heap) < 2:
            print('Symbol list too short.')
            return
        else:
            while len(self.heap) >= 2:
                left = heapq.heappop(self.heap)
                right = heapq.heappop(self.heap)
                weight = left.weight + right.weight
                heapq.heappush(self.heap,
                        Node(weight, leftNode=left, rightNode=right))

    def createCodes(self):
        def recurse(node, code):
            if node.symbol is not None:
                self.codes[code] = node.symbol
            else:
                if node.leftNode is not None:
                    recurse(node.leftNode, code + '0')
                if node.rightNode is not None:
                    recurse(node.rightNode, code + '1')
        
        node = heapq.heappop(self.heap)
        code = ''
        recurse(node, code)
        
    def printResults(self):
        codes = list(self.codes.keys())
        codes = sorted(codes, key=len)
        minBits = len(codes[0])
        maxBits = len(codes[-1])
        print('max length = %s, min length = %s' %(maxBits, minBits))

if __name__ == '__main__':
    huffmanCode = HuffmanCode('huffman.txt')
    huffmanCode.createTree()
    huffmanCode.createCodes()
    huffmanCode.printResults()
