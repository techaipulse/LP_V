# Title:Write a program to implement Parallel Bubble Sort and Merge sort using OpenMP. Use
# existing algorithms and measure the performance of sequential and parallel algorithms.


import random
import time
from concurrent.futures import ThreadPoolExecutor

# ----------- GENERATE ARRAY -----------
n = int(input("Enter size of array: "))
arr = [random.randint(1, 100) for _ in range(n)]

print("Original Array:", arr)


# ----------- SEQUENTIAL BUBBLE SORT -----------
def bubble_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n):
        for j in range(0, n-i-1):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
    return a


# ----------- PARALLEL BUBBLE SORT (ODD-EVEN) -----------
def parallel_bubble_sort(arr):
    a = arr.copy()
    n = len(a)

    for i in range(n):
        def process(j):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]

        with ThreadPoolExecutor() as executor:
            if i % 2 == 0:
                executor.map(process, range(0, n-1, 2))
            else:
                executor.map(process, range(1, n-1, 2))
    return a


# ----------- SEQUENTIAL MERGE SORT -----------
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ----------- PARALLEL MERGE SORT -----------
def parallel_merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2

    with ThreadPoolExecutor() as executor:
        left_future = executor.submit(parallel_merge_sort, arr[:mid])
        right_future = executor.submit(parallel_merge_sort, arr[mid:])

        left = left_future.result()
        right = right_future.result()

    return merge(left, right)


# ----------- PERFORMANCE COMPARISON -----------

# Bubble Sort
start = time.time()
seq_bubble = bubble_sort(arr)
end = time.time()
print("\nSequential Bubble Sort Time:", end - start)

start = time.time()
par_bubble = parallel_bubble_sort(arr)
end = time.time()
print("Parallel Bubble Sort Time:", end - start)

# Merge Sort
start = time.time()
seq_merge = merge_sort(arr)
end = time.time()
print("\nSequential Merge Sort Time:", end - start)

start = time.time()
par_merge = parallel_merge_sort(arr)
end = time.time()
print("Parallel Merge Sort Time:", end - start)


# ----------- OUTPUT CHECK -----------
print("\nSorted (Merge):", seq_merge)