import heapq

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
def cdc_radix_sort(arr):
    num_elements = len(arr)
    
    # Set the minimum and maximum chunk size to avoid extremes
    min_chunk_size = 500        # Minimum chunk size (adjustable based on performance)
    max_chunk_size = 10000000       # Maximum chunk size (adjustable based on performance)
    
    # Dynamically calculate optimal chunk size based on the number of elements
    if num_elements < min_chunk_size:
        num_chunks = 1  # No need to chunk if the dataset is small
    else:
        optimal_chunk_size = min(max_chunk_size, num_elements // 10)
        num_chunks = num_elements // optimal_chunk_size
        if num_elements % optimal_chunk_size != 0:
            num_chunks += 1

    # Divide the array into chunks
    chunk_size = num_elements // num_chunks
    chunks = [arr[i * chunk_size:(i + 1) * chunk_size] for i in range(num_chunks)]
    if num_elements % num_chunks != 0:
        chunks.append(arr[num_chunks * chunk_size:])
    
    # Filter out non-numeric types (int and float) in each chunk before sorting
    for i in range(len(chunks)):
        chunks[i] = [x for x in chunks[i] if isinstance(x, (int, float))]
    
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
