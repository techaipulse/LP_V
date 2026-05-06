#Title : Implement Min, Max, Sum and Average operations using Parallel Reduction.
import random
import time
from concurrent.futures import ThreadPoolExecutor

# ----------- INPUT -----------
n = int(input("Enter size of array: "))
arr = [random.randint(1, 100) for _ in range(n)]

print("Array:", arr)


# ----------- SEQUENTIAL REDUCTION -----------
def sequential_ops(arr):
    total = sum(arr)
    minimum = min(arr)
    maximum = max(arr)
    average = total / len(arr)
    return total, minimum, maximum, average


# ----------- PARALLEL REDUCTION -----------
def parallel_ops(arr):
    def partial(chunk):
        return sum(chunk), min(chunk), max(chunk)

    # Split array into chunks
    num_threads = 4
    chunk_size = len(arr) // num_threads
    chunks = [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = list(executor.map(partial, chunks))

    total = sum(r[0] for r in results)
    minimum = min(r[1] for r in results)
    maximum = max(r[2] for r in results)
    average = total / len(arr)

    return total, minimum, maximum, average


# ----------- PERFORMANCE COMPARISON -----------

# Sequential
start = time.time()
seq = sequential_ops(arr)
end = time.time()
print("\nSequential Results:", seq)
print("Sequential Time:", end - start)

# Parallel
start = time.time()
par = parallel_ops(arr)
end = time.time()
print("\nParallel Results:", par)
print("Parallel Time:", end - start)