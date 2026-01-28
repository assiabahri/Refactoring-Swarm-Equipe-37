# Calculator Module

def add(x: int, y: int) -> float:
    """
    Adds two numbers.

    Args:
        x (int): The first number.
        y (int): The second number.

    Returns:
        float: The sum of x and y.
    """
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        raise TypeError("Both inputs must be numbers")
    return x + y

def subtract(x: int, y: int) -> float:
    """
    Subtracts y from x.

    Args:
        x (int): The first number.
        y (int): The second number.

    Returns:
        float: The difference between x and y.
    """
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        raise TypeError("Both inputs must be numbers")
    return x - y

def multiply(a: int, b: int) -> float:
    """
    Multiplies two numbers.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        float: The product of a and b.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both inputs must be numbers")
    return a * b

def divide(x: int, y: int) -> float:
    """
    Divides x by y.

    Args:
        x (int): The dividend.
        y (int): The divisor.

    Returns:
        float: The quotient of x and y.

    Raises:
        ZeroDivisionError: If y is zero.
    """
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        raise TypeError("Both inputs must be numbers")
    if y == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return x / y

class Calculator:
    def __init__(self, value: float):
        """
        Initializes a Calculator instance.

        Args:
            value (float): The initial value.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Initial value must be a number")
        self.value = value

    def add(self, x: float) -> float:
        """
        Adds x to the current value.

        Args:
            x (float): The number to add.

        Returns:
            float: The new value.
        """
        if not isinstance(x, (int, float)):
            raise TypeError("Input must be a number")
        self.value += x
        return self.value

    def get_value(self) -> float:
        """
        Gets the current value.

        Returns:
            float: The current value.
        """
        return self.value

def factorial(n: int) -> int:
    """
    Calculates the factorial of n.

    Args:
        n (int): The input number.

    Returns:
        int: The factorial of n.

    Raises:
        ValueError: If n is negative.
    """
    if not isinstance(n, int):
        raise TypeError("Input must be an integer")
    if n < 0:
        raise ValueError("Input must be a non-negative integer")
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

def power(base: float, exp: int) -> float:
    """
    Calculates the power of a number.

    Args:
        base (float): The base number.
        exp (int): The exponent.

    Returns:
        float: The result of base raised to the power of exp.

    Raises:
        TypeError: If base or exp is not a number.
    """
    if not isinstance(base, (int, float)) or not isinstance(exp, int):
        raise TypeError("Base must be a number and exponent must be an integer")
    if exp < 0:
        return 1 / power(base, -exp)
    elif exp == 0:
        return 1
    elif exp % 2 == 0:
        return power(base * base, exp // 2)
    else:
        return base * power(base * base, exp // 2)