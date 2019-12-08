#!/usr/bin/env python3

import statistics

'''
Programming Assignment 3

The file contains all of the integers between 1 and 10,000 (inclusive, with no
repeats) in unsorted order. The integer in the ith row of the file gives you
the ith entry of an input array.

Your task is to compute the total number of comparisons used to sort the given
input file by QuickSort. As you know, the number of comparisons depends on
which elements are chosen as pivots, so we'll ask you to explore three
different pivoting rules.

You should not count comparisons one-by-one. Rather, when there is a recursive
call on a subarray of length m, you should simply add m−1 to your running
total of comparisons. (This is because the pivot element is compared to
each of the other m−1 elements in the subarray in this recursive call.)

WARNING: The Partition subroutine can be implemented in several different ways,
and different implementations can give you differing numbers of comparisons.
For this problem, you should implement the Partition subroutine exactly as it
is described in the video lectures (otherwise you might get the wrong answer).

HOW TO GIVE US YOUR ANSWER:

Type the numeric answer in the space provided.

So if your answer is 1198233847, then just type 1198233847 in the space
provided without any space / commas / other punctuation marks. You have 5
attempts to get the correct answer.

(We do not require you to submit your code, so feel free to use any programming
language you want --- just type the final numeric answer in the following
space.)
'''

def readFile(filename):
    with open(filename) as f:
        array = f.readlines()
    array = [int(x) for x in array]
    return array

'''
Problem 1

For the first part of the programming assignment, you should always use the
first element of the array as the pivot element.
'''

'''
Chooses pivot element by selecting first element

l is leftmost index
r is rightmost index
returns index of pivot element
'''
def choosePivotFirst(array, l, r):
    return l

'''
Problem 2

Compute the number of comparisons (as in Problem 1), always using the final
element of the given array as the pivot element. Again, be sure to implement
the Partition subroutine exactly as it is described in the video lectures.

Recall from the lectures that, just before the main Partition subroutine, you
should exchange the pivot element (i.e., the last element) with the first
element.
'''

'''
Chooses pivot element by selecting last element

l is leftmost index
r is rightmost index
returns index of pivot element
'''
def choosePivotLast(array, l, r):
    return r

'''
Problem 3

Compute the number of comparisons (as in Problem 1), using the
"median-of-three" pivot rule. [The primary motivation behind this rule is to do
a little bit of extra work to get much better performance on input arrays that
are nearly sorted or reverse sorted.] In more detail, you should choose the
pivot as follows. Consider the first, middle, and final elements of the given
array. (If the array has odd length it should be clear what the "middle"
element is; for an array with even length 2k, use the kth element as the
"middle" element. So for the array 4 5 6 7, the "middle" element is the second
one - 5 and not 6!) Identify which of these three elements is the median (i.e.,
the one whose value is in between the other two), and use this as your pivot.
As discussed in the first and second parts of this programming assignment, be
sure to implement Partition exactly as described in the video lectures
(including exchanging the pivot element with the first element just before the
main Partition subroutine).

EXAMPLE: For the input array 8 2 4 5 7 1 you would consider the first (8),
middle (4), and last (1) elements; since 4 is the median of the set {1,4,8},
you would use 4 as your pivot element.

SUBTLE POINT: A careful analysis would keep track of the comparisons made in
identifying the median of the three candidate elements. You should NOT do this.
That is, as in the previous two problems, you should simply add m-1 to your
running total of comparisons every time you recurse on a subarray with length
m.
'''

'''
Chooses pivot element by selecting the median-of-three element

l is leftmost index
r is rightmost index
returns index of pivot element
'''
def choosePivotMedianOfThree(array, l, r):
    m = l + ((r - l) // 2)
    indices = [l, m, r]
    candidates = []
    for index in indices:
        candidates.append(array[index])
    return indices[candidates.index(statistics.median(candidates))]

'''
Partitions array around the pivot element

array is list to sort
l is leftmost index
r is rightmost index
pivotFun is function used to select pivot
returns index of pivot element
'''
def partition(array, pivotFun, l, r):
    pivot = pivotFun(array, l, r)
    pivotVal = array[pivot]

    # Swap first element to pivot index 
    array[pivot] = array[l]

    i = l + 1
    for j in range(l + 1, r + 1):
        if array[j] < pivotVal:
            tempVal = array[i]
            array[i] = array[j]
            array[j] = tempVal
            i += 1

    array[l] = array[i - 1]
    array[i - 1] = pivotVal

    return i - 1

'''
Performs quick sort algorithm to sort list

array is list to sort
l is leftmost index
r is rightmost index
pivotFun is function used to select pivot
returns number of comparisons made
'''
def quickSort(array, pivotFun, l=0, r=None):
    if r is None:
        r = len(array) - 1
        
    if r - l < 1:
        return 0

    pivot = partition(array, pivotFun, l, r)
    comps = r - l
    comps += quickSort(array, pivotFun, l, pivot - 1)
    comps += quickSort(array, pivotFun, pivot + 1, r)

    return comps

if __name__ == '__main__':
    array1 = readFile('QuickSort.txt')
    array2 = array1.copy()
    array3 = array1.copy()
    '''
    arrayTest = [9, 8, 7, 6, 5, 4, 3]
    print(arrayTest)
    print(quickSort(arrayTest))
    print(arrayTest)
    print(choosePivotMedianOfThree([5, 7, 1, 2], 0, 3))
    '''
    print('P1 comparisons = %d' %quickSort(array1, pivotFun=choosePivotFirst))
    print('P2 comparisons = %d' %quickSort(array2, pivotFun=choosePivotLast))
    print('P3 comparisons = %d' %quickSort(array3, pivotFun=choosePivotMedianOfThree))
