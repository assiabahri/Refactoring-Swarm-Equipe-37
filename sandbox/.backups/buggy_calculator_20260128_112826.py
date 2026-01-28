# Calculator Module

def add(x: int, y: int) -> int:
    """
    Adds two numbers.

    Args:
        x (int): The first number.
        y (int): The second number.

    Returns:
        int: The sum of x and y.
    """
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        raise TypeError("Both inputs must be numbers")
    return x + y

def subtract(x: int, y: int) -> int:
    """
    Subtracts y from x.

    Args:
        x (int): The first number.
        y (int): The second number.

    Returns:
        int: The difference between x and y.
    """
    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
        raise TypeError("Both inputs must be numbers")
    return x - y

def multiply(a: int, b: int) -> int:
    """
    Multiplies two numbers.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The product of a and b.
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
    def __init__(self, value: int):
        """
        Initializes a Calculator instance.

        Args:
            value (int): The initial value.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Initial value must be a number")
        self.value = value

    def add(self, x: int) -> int:
        """
        Adds x to the current value.

        Args:
            x (int): The number to add.

        Returns:
            int: The new value.
        """
        if not isinstance(x, (int, float)):
            raise TypeError("Input must be a number")
        self.value += x
        return self.value

    def get_value(self) -> int:
        """
        Gets the current value.

        Returns:
            int: The current value.
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

def power(base: int, exp: int) -> int:
    """
    Calculates the power of a number.

    Args:
        base (int): The base number.
        exp (int): The exponent.

    Returns:
        int: The result of base raised to the power of exp.

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