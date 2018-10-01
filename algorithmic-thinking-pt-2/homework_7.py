"""
Homework 7
"""

import math

# Question 1
A = [5,4,3,6,7]

def count_inversions(input_list):
    num_inversions = 0
    for idx, first_element in enumerate(input_list):
        if idx == len(input_list) - 1:
            return num_inversions
        else:
            for second_element in input_list[idx+1:]:
                if second_element < first_element:
                    num_inversions += 1
                
print("Q1: There are {} inversions\n".format(count_inversions(A)))

# Question 2-3
# n(n-1)/2

def inverse_seq(n):
    return list(reversed(range(n)))

print("Q2-3")
for number in range(10):
    print('n = {n}, inversions = {i}, guess = {g}'.format(n=number, i=count_inversions(inverse_seq(number)), g=number*(number-1)/2))
print("")

# Question 4

def merge(B, C, A):
    count, i, j, k = 0, 0, 0, 0
    while i < len(B) and j < len(C):
        if B[i] <= C[j]:
            A[k] = B[i]
            i += 1
        else:
            A[k] = C[j]
            j += 1
            count += len(B) - i
        k += 1
    if i == len(B):
        A[k:len(B)+len(C)] = C[j:]
    else:
        A[k:len(B)+len(C)] = B[i:]
    return count

def count_inversions_provided(A):
    if len(A) == 1:
        return 0
    else:
        B = A[0:int(len(A)/2)]
        C = A[int(len(A)/2):]
        il = count_inversions_provided(B)
        ir = count_inversions_provided(C)
        im = merge(B, C, A)
        return il + ir + im

array = [5, 2, 1, 3, 100, 17, 22, 4]
print("Q4 Testing")
print("Array: {}".format(array))
print("Invesions: {}".format(count_inversions_provided(array)))
print("Sorted: {}".format(array))

# Question 8

def mystery(A, l, r):
    """
    A is a sorted array of distinct integers with left/right boundaries l and r
    """
    if l > r:
        return -1
    m = math.floor((l + r)/2)
    if A[m] == m:
        return m
    else:
        if A[m] < m:
            return mystery(A, m+1, r)
        else:
            return mystery(A, l, m-1)

test_ans = mystery([-2, 0, 1, 3, 7, 12, 15],0,6)
print(test_ans) 
