import random
import time
import heapq

# Optimized Radix Sort Helper Function for Each Chunk
def optimized_radix_sort(arr):
    # Step 1: Separate negative and positive numbers
    negatives = [x for x in arr if x < 0]
    positives = [x for x in arr if x >= 0]

    # Step 2: Handle negative numbers by negating them temporarily
    arr = positives + [abs(x) for x in negatives]

    # Step 3: Convert floats to integers by scaling them
    scaling_factor = 10**6  # Adjust this value for the desired precision
    arr = [int(x * scaling_factor) if isinstance(x, float) else x for x in arr]

    # Determine the maximum number in the chunk to limit digit passes
    max_val = max(arr)
    exp = 1

    # Preallocate output and count arrays
    n = len(arr)
    output = [0] * n
    count = [0] * 10  # Only 10 buckets for digits 0-9

    # Adaptive loop only for necessary digit places
    while max_val // exp > 0:
        # Reset count array in place
        for i in range(10):
            count[i] = 0

        # Count occurrences of each digit in the current place value
        for i in arr:
            index = i // exp
            count[index % 10] += 1

        # Accumulate counts
        for i in range(1, 10):
            count[i] += count[i - 1]

        # Place elements in the output array based on the current digit
        for i in range(n - 1, -1, -1):
            index = arr[i] // exp
            output[count[index % 10] - 1] = arr[i]
            count[index % 10] -= 1

        # Copy the output back to the original array
        for i in range(n):
            arr[i] = output[i]

        # Move to the next digit place
        exp *= 10

    # Step 4: Scale back floating-point numbers and reattach negative numbers
    arr = [x / scaling_factor if isinstance(x, int) else x for x in arr]
    arr = [x if x >= 0 else -x for x in arr]  # Negate back negative numbers

    return arr

# Divide and Conquer Radix Sort with Optimized Radix Sort for Each Chunk
def radix_sort_chunked(arr, num_chunks=4):
    chunk_size = len(arr) // num_chunks
    chunks = [arr[i * chunk_size:(i + 1) * chunk_size] for i in range(num_chunks)]
    if len(arr) % num_chunks != 0:
        chunks.append(arr[num_chunks * chunk_size:])

    # Sort each chunk sequentially using the optimized radix sort
    for chunk in chunks:
        optimized_radix_sort(chunk)

    # Pairwise merge sorted chunks to reduce merge overhead
    while len(chunks) > 1:
        merged_chunks = []
        for i in range(0, len(chunks), 2):
            if i + 1 < len(chunks):
                merged_chunks.append(list(heapq.merge(chunks[i], chunks[i + 1])))
            else:
                merged_chunks.append(chunks[i])
        chunks = merged_chunks

    return chunks[0] if chunks else []

# Performance Comparison Function
def compare_radix_sort_performance(arr_size=random.randint(1000, 10000000)):
    # Generate a random array with mixed positive, negative, and floating-point values
    arr = [random.uniform(-10000, 10000) for _ in range(arr_size)]
    arr_copy = arr[:]
    print("Array size:", arr_size)
    # Traditional Radix Sort Timing
    start_time = time.time()
    optimized_radix_sort(arr)  # Using optimized radix sort for fair comparison
    traditional_duration = time.time() - start_time

    # Divide-and-Conquer Radix Sort Timing
    start_time = time.time()
    sorted_arr = radix_sort_chunked(arr_copy, num_chunks=4)
    divide_conquer_duration = time.time() - start_time

    # Results
    print("Traditional Radix Sort Time:", traditional_duration)
    print("Divide-and-Conquer Radix Sort Time:", divide_conquer_duration)

# Run the comparison
compare_radix_sort_performance()
