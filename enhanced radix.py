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