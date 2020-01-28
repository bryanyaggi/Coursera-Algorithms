#!/usr/bin/env python3

import time
import heapq

'''
Programming Assignment 3

Download the following text file: median.txt

The goal of this problem is to implement the "Median Maintenance" algorithm
(covered in the Week 3 lecture on heap applications). The text file contains a
list of the integers from 1 to 10000 in unsorted order; you should treat this as
a stream of numbers, arriving one by one. Letting x_i denote the ith number of
the file, the kth median m_k is defined as the median of the numbers x_1, ...,
x_k. (So, if k is odd, then m_k is ((k + 1)/2)th smallest number among x1, ...,
x_k; if k is even, then m_k is the (k/2)th smallest number among x1, ..., x_k.)

In the box below you should type the sum of these 10000 medians, modulo 10000
(i.e., only the last 4 digits). That is, you should compute
(m_1 + m_2 + m_3+ ... + m_10000) mod 10000.

OPTIONAL EXERCISE: Compare the performance achieved by heap-based and
search-tree-based implementations of the algorithm.
'''

'''
Class that implements median maintenance algorithm.
'''
class MedianMaintainer:
    def __init__(self, stream):
        self.stream = stream[::-1] # reverse list to pop from end
        self.minHeap = []
        self.maxHeap = []
        self.medians = []

    '''
    Pushes element to min heap.
    '''
    def pushMinHeap(self, element):
        heapq.heappush(self.minHeap, element)

    '''
    Pushes element to max heap.
    '''
    def pushMaxHeap(self, element):
        heapq.heappush(self.maxHeap, -element)

    '''
    Pops min element from min heap.
    '''
    def popMinHeap(self):
        return heapq.heappop(self.minHeap)

    '''
    Pops max element from max heap.
    '''
    def popMaxHeap(self):
        return -heapq.heappop(self.maxHeap)

    '''
    Returns the value of min element in the min heap.
    '''
    def peekMinHeap(self):
        return self.minHeap[0]

    '''
    Returns the value of max element in the max heap.
    '''
    def peekMaxHeap(self):
        return -self.maxHeap[0]

    '''
    Inserts element into data structure.
    '''
    def insertElement(self, element):
        if len(self.maxHeap) == 0:
            self.pushMaxHeap(element)
        elif element <= self.peekMaxHeap():
            self.pushMaxHeap(element)
        else:
            self.pushMinHeap(element)

    '''
    Balances max and min heaps so median can be determined.
    '''
    def balanceHeaps(self):
        balanced = False

        while not balanced:
            maxHeapSize = len(self.maxHeap)
            minHeapSize = len(self.minHeap)

            if (maxHeapSize + minHeapSize) % 2 == 0: # even
                if maxHeapSize - minHeapSize >= 2:
                    element = self.popMaxHeap()
                    self.pushMinHeap(element)
                elif minHeapSize - maxHeapSize >= 3:
                    element = self.popMinHeap()
                    self.pushMaxHeap(element)
                else:
                    balanced = True
            else: # odd
                if maxHeapSize - minHeapSize >= 3:
                    element = self.popMaxHeap()
                    self.pushMinHeap(element)
                elif minHeapSize - maxHeapSize >= 3:
                    element = self.popMinHeap()
                    self.pushMaxHeap(element)
                else:
                    balanced = True

        return maxHeapSize, minHeapSize

    '''
    Returns the median element.
    '''
    def getMedian(self):
        maxHeapSize, minHeapSize = self.balanceHeaps()
        median = 0

        if (maxHeapSize + minHeapSize) % 2 == 0: # even
            if maxHeapSize == minHeapSize:
                median = self.peekMaxHeap()
            elif minHeapSize - maxHeapSize == 2:
                median = self.peekMinHeap()
            else:
                print('Unbalanced heaps!')
        else: # odd
            if maxHeapSize - minHeapSize == 1:
                median = self.peekMaxHeap()
            elif minHeapSize - maxHeapSize == 1:
                median = self.peekMinHeap()
            else:
                print('Unbalanced heaps!')

        return median

    '''
    Processes the next element in the stream.
    '''
    def processNext(self):
        element = self.stream.pop()
        self.insertElement(element)
        return self.getMedian()

    '''
    Processes the complete stream. Prints debugging information if verbose set.
    '''
    def processStream(self, verbose=False):
        if verbose:
            print('stream = %s' %self.stream)

        while len(self.stream):
            self.medians.append(self.processNext())
            if verbose:
                print('min heap: %s' %self.minHeap)
                print('max heap: %s' %self.maxHeap)

        if verbose:
            print('medians = %s' %self.medians)

    '''
    Calculates the last 4 digits of the sum of medians.
    '''
    def calcResult(self):
        summation = 0
        for median in self.medians:
            summation += median
        return summation % 10000

def readFile(filename):
    with open(filename) as f:
        lines = f.readlines()

    stream = []
    for line in lines:
        stream.append(int(line))

    return stream

def testMedianMaintainer():
    #stream = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    #stream = [1, 666, 10, 667, 100, 2, 3]
    stream = [6331, 2793, 1640, 9290, 225, 625, 6195, 2303, 5685, 1354]
    return MedianMaintainer(stream)

if __name__ == '__main__':
    t0 = time.time()
    #mm = testMedianMaintainer()
    stream = readFile('median.txt')
    mm = MedianMaintainer(stream)
    mm.processStream()
    print('result = %s' %mm.calcResult())
    print('total time = %f' %(time.time() - t0))
