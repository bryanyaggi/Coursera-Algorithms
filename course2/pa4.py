#!/usr/bin/env python3

import time
import bisect

'''
Programming Assignment 4

Download the following text file: 2sum.txt

The goal of this problem is to implement a variant of the 2-SUM algorithm
covered in this week's lectures.

The file contains 1 million integers, both positive and negative (there might be
some repetitions!). This is your array of integers, with the ith row of the file
specifying the ith entry of the array.

Your task is to compute the number of target values t in the interval [-10000,
10000] (inclusive) such that there are distinct numbers x, y in the input file
that satisfy x + y = t. (NOTE: ensuring distinctness requires a one-line
addition to the algorithm from lecture.)

Write your numeric answer (an integer between 0 and 20001) in the space
provided.

OPTIONAL CHALLENGE: If this problem is too easy for you, try implementing your
own hash table for it. For example, you could compare performance under the
chaining and open addressing approaches to resolving collisions.
'''

def readFile(filename):
    with open(filename) as f:
        lines = f.readlines()

    integers = set([])
    for line in lines:
        integers.add(int(line))

    return integers

'''
Calculates result for assignment. Uses lecture method.
Note: very slow for default interval

integers is a set of integers
interval is the range of target values
'''
def calcResult(integers, interval=[-10000, 10000], verbose=False):
    total = 0
    for t in range(interval[0], interval[1] + 1):
        if t % 10 == 0:
            print('Progress: target = %d, interval = %s' %(t, interval),
                    end='\r')
        for x in integers:
            y = t - x
            if y in integers and y != x:
                if verbose:
                    print('x = %d, y = %d, t = %d' %(x, y, t))
                total += 1
                break
    return total

'''
Calculates result for assignment. Uses alternate algorithm.

Sorts integers. For each element, finds subset of addends possible. Adds sums
to set of possible sums. Returns length of possible sums.

integers is a set of integers
interval is the range of target values
'''
def calcResultAlt(integers, interval=[-10000, 10000], verbose=False):
    sortedInts = sorted(integers)
    sums = set([])
    for x in sortedInts:
        yMaxVal = interval[1] - x
        yMinVal = interval[0] - x
        yMaxInd = bisect.bisect_right(sortedInts, yMaxVal)
        yMinInd = bisect.bisect_left(sortedInts, yMinVal)
        if verbose:
            print('x = %d, y_min = %d, y_max = %d' %(x, sortedInts[yMinInd],
                sortedInts[yMaxInd-1]))
        for i in range(yMinInd, yMaxInd):
            sums.add(x + sortedInts[i])
    return len(sums)

def testIntegers():
    return set([-3, -1, 1, 2, 9, 11, 7, 6, 2])

def testInterval():
    return [3, 10]

if __name__ == '__main__':
    t0 = time.time()
    integers = readFile('2sum.txt')
    #result = calcResult(testIntegers(), testInterval(), verbose=True)
    #result = calcResultAlt(testIntegers(), testInterval(), verbose=True)
    #result = calcResult(integers)
    result = calcResultAlt(integers)
    print('result = %s' %result)
    print('total time = %f' %(time.time() - t0))
