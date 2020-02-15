#!/usr/bin/env python3

import time

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

def readFile(filename):
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

def calcP1Score(jobs):
    for job in jobs:
        score = job['weight'] - job['length']
        job['p1Score'] = score

def calcP2Score(jobs):
    for job in jobs:
        score = job['weight'] / job['length']
        job['p2Score'] = score

def calcSumWeightedCompletions(jobs):
    result = 0
    compTime = 0
    for job in jobs:
        compTime += job['length']
        result += job['weight'] * compTime

    return result

def calcP1Result(jobs):
    calcP1Score(jobs)
    jobsSorted = sorted(jobs, key = lambda x: (x['p1Score'], x['weight']),
            reverse=True)
    return calcSumWeightedCompletions(jobsSorted)

def calcP2Result(jobs):
    calcP2Score(jobs)
    jobsSorted = sorted(jobs, key = lambda x: x['p2Score'], reverse=True)
    return calcSumWeightedCompletions(jobsSorted)

if __name__ == '__main__':
    t0 = time.time()
    jobs = readFile('jobs.txt')
    p1Result = calcP1Result(jobs)
    print('p1 result = %s' %calcP1Result(jobs))
    print('p2 result = %s' %calcP2Result(jobs))
    print('total time = %f' %(time.time() - t0))
