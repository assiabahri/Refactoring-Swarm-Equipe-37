"""
File with multiple types of bugs
Good for comprehensive testing
"""

import syste  # Typo: should be 'sys'

def complex_function(data):
    # Undefined variable
    results = []
    
    for item in data:
        # Potential division by zero
        processed = item / divisor  # 'divisor' undefined
        
        # Wrong indentation
    if processed > 10:  # Should be inside for loop
            results.append(processed)
        else:
            # Missing return in else branch
            pass
    
    # Infinite loop potential
    counter = 0
    while counter < len(results):
        # Forgot to increment counter
        print(f"Result {counter}: {results[counter]}")
        # counter += 1  # Missing
    
    # Using undefined function
    final = format_output(results)  # 'format_output' undefined
    
    return final

# Syntax error in list comprehension
numbers = [1, 2, 3, 4, 5]
squares = [x**2 for x in numbers  # Missing closing bracket

# Wrong variable name
total_sum = sum(numbers)
average = total_sum / lenght  # Typo: should be 'length'

print("Debug info:")
print(f"Numbers: {numbers}")
print(f"Total: {total_sum}")
print(f"Average: {average}")

# Call the buggy function
# complex_function([1, 2, 3])  # Will crash multiple ways