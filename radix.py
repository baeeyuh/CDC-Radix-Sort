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