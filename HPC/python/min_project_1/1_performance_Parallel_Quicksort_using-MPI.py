# Mini Project: Evaluate performance enhancement of parallel Quicksort Algorithm using MPI

from mpi4py import MPI
import numpy as np
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# ----------- GENERATE DATA (only root) -----------
n = int(input("Enter size of array: ")) if rank == 0 else None
n = comm.bcast(n, root=0)

if rank == 0:
    data = np.random.randint(1, 100, n)
    print("Original Array:", data)
else:
    data = None

# ----------- SCATTER DATA -----------
chunk = np.zeros(n // size, dtype=int)
comm.Scatter(data, chunk, root=0)

# ----------- LOCAL QUICK SORT -----------
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr)//2]
    left = arr[arr < pivot]
    middle = arr[arr == pivot]
    right = arr[arr > pivot]
    return np.concatenate((quicksort(left), middle, quicksort(right)))

start = MPI.Wtime()

local_sorted = quicksort(chunk)

# ----------- GATHER RESULTS -----------
gathered = None
if rank == 0:
    gathered = np.zeros(n, dtype=int)

comm.Gather(local_sorted, gathered, root=0)

end = MPI.Wtime()

# ----------- FINAL MERGE (ROOT) -----------
if rank == 0:
    final_sorted = quicksort(gathered)
    print("\nParallel Sorted:", final_sorted)
    print("Parallel Time:", end - start)


# ----------- SEQUENTIAL COMPARISON -----------
if rank == 0:
    start = time.time()
    seq_sorted = quicksort(data)
    end = time.time()
    print("\nSequential Sorted:", seq_sorted)
    print("Sequential Time:", end - start)