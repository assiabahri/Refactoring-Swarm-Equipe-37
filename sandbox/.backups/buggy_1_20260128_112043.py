def calculate_sum(numbers):
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list")
    if not all(isinstance(num, (int, float)) for num in numbers):
        raise ValueError("All elements in the list must be numbers")
    return sum(numbers)

def main():
    numbers = [1, 2, 3, 4, 5]
    result = calculate_sum(numbers)
    print(result)

if __name__ == "__main__":
    main()