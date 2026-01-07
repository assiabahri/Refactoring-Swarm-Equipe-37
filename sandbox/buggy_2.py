def divide_numbers(x, y):
    # This function has division by zero bug
    return x / y

# Test the function
print(divide_numbers(10, 2))
print(divide_numbers(10, 0))  # This will crash!