import matplotlib.pyplot as plt
from memory_profiler import memory_usage
import random
import heapq

# Enhanced Radix Sort (handles negative numbers and floating-point numbers)
def enhanced_radix_sort(arr):
    arr = [x for x in arr if isinstance(x, (int, float))]
    if not arr:
        return arr
    
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

# Function to profile memory usage for a sorting algorithm
def profile_sorting_function(sort_func, arr):
    def wrapper():
        sort_func(arr.copy())  # Sort a copy to avoid modifying the original
    # Capture memory usage over time
    mem_profile = memory_usage(wrapper, interval=0.1, retval=False)
    return mem_profile

# Function to compare memory usage of sorting algorithms
def compare_sorting_algorithms_memory(arr):
    algorithms = {
        "Enhanced Radix Sort": enhanced_radix_sort,
        "CDC Radix Sort": cdc_radix_sort
    }

    # Collect memory profiles for each algorithm
    memory_profiles = []
    labels = []
    for name, func in algorithms.items():
        print(f"Profiling {name}...")
        mem_profile = profile_sorting_function(func, arr)
        memory_profiles.append(mem_profile)
        labels.append(name)

    # Plot memory profiles
    for i, mem_profile in enumerate(memory_profiles):
        plt.plot(mem_profile, label=f"{labels[i]} (Peak: {max(mem_profile):.2f} MiB)")

    plt.title("Memory Usage Comparison for Sorting Algorithms")
    plt.xlabel("Time (intervals)")
    plt.ylabel("Memory Usage (MiB)")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

# Example Usage
if __name__ == "__main__":
    arr_size = arr_size=random.randint(1000, 10000000)  # Adjust size as needed
    arr = [1000000 for _ in range(arr_size)]
    arr = [random.uniform(-10000000, 10000000) for _ in range(arr_size)]
    arr_copy = arr[:]
    compare_sorting_algorithms_memory(arr)