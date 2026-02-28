"""
Buggy Calculator Module Refactored
This module provides basic mathematical operations.
"""

def add(x, y):
    """
    Add two numbers.

    Args:
        x (int or float): The first number.
        y (int or float): The second number.

    Returns:
        int or float: The sum of x and y.
    """
    try:
        return x + y
    except TypeError:
        raise ValueError("Both inputs must be numbers")

def subtract(x, y):
    """
    Subtract two numbers.

    Args:
        x (int or float): The first number.
        y (int or float): The second number.

    Returns:
        int or float: The difference of x and y.
    """
    try:
        return x - y
    except TypeError:
        raise ValueError("Both inputs must be numbers")

def multiply(a, b):
    """
    Multiply two numbers.

    Args:
        a (int or float): The first number.
        b (int or float): The second number.

    Returns:
        int or float: The product of a and b.
    """
    try:
        return a * b
    except TypeError:
        raise ValueError("Both inputs must be numbers")

def divide(x, y):
    """
    Divide two numbers.

    Args:
        x (int or float): The dividend.
        y (int or float): The divisor.

    Returns:
        int or float: The quotient of x and y.

    Raises:
        ZeroDivisionError: If y is zero.
    """
    try:
        if y == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return x / y
    except TypeError:
        raise ValueError("Both inputs must be numbers")

class Calculator:
    """
    A simple calculator class.

    Attributes:
        value (int or float): The current value.
    """

    def __init__(self, value):
        """
        Initialize the calculator with a value.

        Args:
            value (int or float): The initial value.
        """
        self.value = value

    def add(self, x):
        """
        Add a number to the current value.

        Args:
            x (int or float): The number to add.

        Returns:
            int or float: The new value.
        """
        try:
            self.value += x
            return self.value
        except TypeError:
            raise ValueError("Input must be a number")

    def get_value(self):
        """
        Get the current value.

        Returns:
            int or float: The current value.
        """
        return self.value

def factorial(n):
    """
    Calculate the factorial of a number.

    Args:
        n (int): The number.

    Returns:
        int: The factorial of n.

    Raises:
        ValueError: If n is negative.
    """
    if n < 0:
        raise ValueError("Input must be a non-negative integer")
    elif n == 0:
        return 1
    else:
        return n * factorial(n - 1)

def power(base, exp):
    """
    Calculate the power of a number.

    Args:
        base (int or float): The base.
        exp (int): The exponent.

    Returns:
        int or float: The result of base raised to exp.

    Raises:
        TypeError: If exp is not an integer.
    """
    if not isinstance(exp, int):
        raise TypeError("Exponent must be an integer")
    result = 1
    for _ in range(exp):
        result *= base
    return result

# Removed the unused function call