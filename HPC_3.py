import multiprocessing

# Function to calculate partial sum
def partial_sum(data):
    return sum(data)

# Function to calculate partial minimum
def partial_min(data):
    return min(data)

# Function to calculate partial maximum
def partial_max(data):
    return max(data)

if __name__ == "__main__":

    # Input data
    numbers = [10, 20, 30, 40, 50, 60, 70, 80]

    # Number of processes
    num_processes = 4

    # Divide data into chunks
    chunk_size = len(numbers) // num_processes
    chunks = [numbers[i:i + chunk_size] for i in range(0, len(numbers), chunk_size)]

    # Create process pool
    pool = multiprocessing.Pool(processes=num_processes)

    # Parallel Sum
    partial_sums = pool.map(partial_sum, chunks)
    total_sum = sum(partial_sums)

    # Parallel Minimum
    partial_mins = pool.map(partial_min, chunks)
    minimum = min(partial_mins)

    # Parallel Maximum
    partial_maxs = pool.map(partial_max, chunks)
    maximum = max(partial_maxs)

    # Average
    average = total_sum / len(numbers)

    # Output
    print("Numbers:", numbers)
    print("Sum =", total_sum)
    print("Minimum =", minimum)
    print("Maximum =", maximum)
    print("Average =", average)

    pool.close()
    pool.join()