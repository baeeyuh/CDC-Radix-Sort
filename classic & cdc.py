import random
import time
import heapq

# Classic Radix Sort (Only for integers)
def classic_radix_sort(arr):
    max_val = max(arr)
    exp = 1
    n = len(arr)
    
    output = [0] * n
    count = [0] * 10  # Bucket for digits 0-9
    
    while max_val // exp > 0:
        for i in range(10):
            count[i] = 0
        
        for num in arr:
            index = int(num // exp)  # Make sure index is an integer
            count[index % 10] += 1
        
        for i in range(1, 10):
            count[i] += count[i - 1]
        
        for i in range(n - 1, -1, -1):
            index = int(arr[i] // exp)  # Make sure index is an integer
            output[count[index % 10] - 1] = arr[i]
            count[index % 10] -= 1
        
        for i in range(n):
            arr[i] = output[i]
        
        exp *= 10
    
    return arr

# Enhanced Radix Sort (handles negative numbers and floating-point numbers)
def enhanced_radix_sort(arr):
    # Filter out only numeric types (int and float)
    arr = [x for x in arr if isinstance(x, (int, float))]
    
    if not arr:  # If there's nothing to sort, return empty
        return arr
    
    # Separate negative and positive numbers
    negatives = [x for x in arr if x < 0]
    positives = [x for x in arr if x >= 0]

    arr = positives + [abs(x) for x in negatives]

    scaling_factor = 10**6
    arr = [int(x * scaling_factor) if isinstance(x, float) else x for x in arr]

    max_val = max(arr)
    exp = 1

    n = len(arr)
    output = [0] * n
    count = [0] * 10

    while max_val // exp > 0:
        for i in range(10):
            count[i] = 0

        for i in arr:
            index = i // exp
            count[index % 10] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        for i in range(n - 1, -1, -1):
            index = arr[i] // exp
            output[count[index % 10] - 1] = arr[i]
            count[index % 10] -= 1

        for i in range(n):
            arr[i] = output[i]

        exp *= 10

    arr = [x / scaling_factor if isinstance(x, int) else x for x in arr]
    arr = [x if x >= 0 else -x for x in arr]

    return arr

# Divide and Conquer Radix Sort with Optimized Radix Sort for Each Chunk
def cdc_radix_sort(arr, num_chunks=4):
    chunk_size = len(arr) // num_chunks
    chunks = [arr[i * chunk_size:(i + 1) * chunk_size] for i in range(num_chunks)]
    if len(arr) % num_chunks != 0:
        chunks.append(arr[num_chunks * chunk_size:])

    # Filter out non-numeric types (int and float) in each chunk before sorting
    for i in range(len(chunks)):
        chunks[i] = [x for x in chunks[i] if isinstance(x, (int, float))]  # Only int and float
    
    # Sort each chunk using the enhanced radix sort
    for chunk in chunks:
        enhanced_radix_sort(chunk)

    # Merge sorted chunks (only numeric values in chunks)
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
    # Generate a random array with mixed data types
    arr = [random.uniform(-10000000, 10000000) for _ in range(arr_size)]
    arr_copy = arr[:]  # Mixed data types (int, float, bool, str)
    
    # We need to create copies of the original array for each sorting method
    arr_classic = [x for x in arr if isinstance(x, int)]  # Classic works with integers only
    arr_enhanced = [x for x in arr if isinstance(x, (int, float))]  # Enhanced handles int and float
    arr_cdc = arr  # CDC can handle all data types
    
    print(f"Array size: {arr_size}")

    # Timing Classic Radix Sort
    start_time = time.time()
    if arr_classic:  # Ensure there's something to sort
        classic_radix_sort(arr_classic)  # Classic Radix Sort (works only with integers)
    classic_duration = time.time() - start_time

    # Timing Enhanced Radix Sort (Optimized)
    start_time = time.time()
    if arr_enhanced:  # Ensure there's something to sort
        enhanced_radix_sort(arr_enhanced)  # Enhanced Radix Sort (works with integers and floats)
    enhanced_duration = time.time() - start_time

    # Timing CDC Radix Sort
    start_time = time.time()
    if arr_cdc:  # Ensure there's something to sort
        cdc_radix_sort(arr_cdc, num_chunks=4)  # CDC handles mixed types
    cdc_duration = time.time() - start_time

    # Results
    print(f"Classic Radix Sort Time: {classic_duration:.6f} seconds")
    print(f"Enhanced Radix Sort Time: {enhanced_duration:.6f} seconds")
    print(f"CDC Radix Sort Time: {cdc_duration:.6f} seconds")

# Run the comparison
compare_radix_sort_performance()
