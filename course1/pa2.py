#!/usr/bin/env python3

'''
Programming Assignment 2

This file contains all of the 100,000 integers between 1 and 100,000 (inclusive)
in some order, with no integer repeated.

Your task is to compute the number of inversions in the file given, where the
ith row of the file indicates the ith entry of an array.

Because of the large size of this array, you should implement the fast
divide-and-conquer algorithm covered in the video lectures.

The numeric answer for the given input file should be typed in the space below.

So if your answer is 1198233847, then just type 1198233847 in the space
provided without any space / commas / any other punctuation marks. You can make
up to 5 attempts, and we'll use the best one for grading.

(We do not require you to submit your code, so feel free to use any programming
language you want --- just type the final numeric answer in the following
space.)
'''

def readFile(filename):
    with open(filename) as f:
        array = f.readlines()
    array = [int(x) for x in array]
    return array

def sortAndCount(array):
    if len(array) <= 1:
        return array, 0

    mid = len(array) // 2
    left = array[:mid]
    right = array[mid:]
    left, leftCount = sortAndCount(left)
    right, rightCount = sortAndCount(right)
    array, mergeCount = mergeAndCount(left, right)

    return array, leftCount + rightCount + mergeCount

def mergeAndCount(left, right):
    array = [0] * (len(left) + len(right))
    i, j, count = 0, 0, 0
    for k in range(len(array)):
        if i < len(left):
            if j < len(right):
                if left[i] <= right[j]:
                    array[k] = left[i]
                    i += 1
                else:
                    array[k] = right[j]
                    count += (len(left) - i)
                    j += 1
            else:
                array[k] = left[i]
                i += 1
        else:
            array[k] = right[j]
            count += (len(left) - i)
            j += 1

    return array, count

def testResult(array):
    inversions = 0
    for i in range(len(array)):
        for j in range(i + 1, len(array)):
            if array[i] > array[j]:
                inversions += 1
    return inversions

if __name__ == '__main__':
    array = readFile('IntegerArray.txt')
    arrayTest = [9, 8, 7, 6, 5, 4, 3]
    #print(testResult(arrayTest))
    print(sortAndCount(array)[1])
