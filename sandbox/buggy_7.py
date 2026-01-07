def calculate_stats(numbers):
    """Function with variable name typos"""
    total_sum = sum(numbers)
    avgrage = total_sum / len(numbers)  # Typo: should be 'average'
    
    maximum = max(numbers)
    minimum = min(numbers)
    
    # More typos
    variance_sum = 0
    for num in numbers:
        diffrence = num - avgrage  # Typo: should be 'difference'
        variance_sum += diffrence ** 2
    
    varience = variance_sum / len(numbers)  # Typo: should be 'variance'
    
    # Using wrong variable names
    return {
        "total": total_sum,
        "average": avgrage,  # Typo persists
        "max_value": maximum,
        "min_value": minmum,  # Typo: should be 'minimum'
        "variance": varience   # Typo persists
    }

data = [1, 2, 3, 4, 5]
stats = calculate_stats(data)
print(f"Statistics: {stats}")