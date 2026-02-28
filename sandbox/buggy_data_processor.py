def process_list(items):
    """
    Process a list of integers, doubling the even numbers.

    Args:
        items (list): A list of integers.

    Returns:
        list: A list of integers with even numbers doubled.

    Raises:
        TypeError: If the list contains non-integer items.
    """
    if not items:
        return []
    
    result = []
    for item in items:
        if not isinstance(item, int):
            raise TypeError("The list must only contain integers.")
        if item % 2 == 0:
            result.append(item * 2)
    return result

def filter_positive(numbers):
    """
    Filter a list of numbers, returning only the positive ones.

    Args:
        numbers (list): A list of numbers.

    Returns:
        list: A list of positive numbers.
    """
    return [n for n in numbers if n > 0]

def sum_list(numbers):
    """
    Calculate the sum of a list of numbers.

    Args:
        numbers (list): A list of numbers.

    Returns:
        int: The sum of the numbers.
    """
    return sum(numbers)

def find_max(numbers):
    """
    Find the maximum number in a list.

    Args:
        numbers (list): A list of numbers.

    Returns:
        int: The maximum number, or None if the list is empty.
    """
    if not numbers:
        return None
    return max(numbers)

def average(numbers):
    """
    Calculate the average of a list of numbers.

    Args:
        numbers (list): A list of numbers.

    Returns:
        float: The average of the numbers, or 0 if the list is empty.
    """
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)