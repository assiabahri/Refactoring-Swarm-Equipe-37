from math import factorial as math_factorial

"""
A module containing a simple calculator class and functions.
"""


class Calculator:
    """
    A simple calculator class.

    Attributes:
        value (float): The current value of the calculator.
    """

    def __init__(self, initial_value: float = 0):
        """
        Initializes the calculator with an initial value.

        Args:
            initial_value (float): The initial value. Defaults to 0.
        """
        self.value = initial_value

    def get_value(self) -> float:
        """
        Gets the current value of the calculator.

        Returns:
            float: The current value.
        """
        return self.value

    @staticmethod
    def add(a: float, b: float) -> float:
        """
        Adds two numbers.

        Args:
            a (float): The first number.
            b (float): The second number.

        Returns:
            float: The sum of a and b.
        """
        return a + b

    @staticmethod
    def subtract(a: float, b: float) -> float:
        """
        Subtracts two numbers.

        Args:
            a (float): The first number.
            b (float): The second number.

        Returns:
            float: The difference of a and b.
        """
        return a - b

    @staticmethod
    def multiply(a: float, b: float) -> float:
        """
        Multiplies two numbers.

        Args:
            a (float): The first number.
            b (float): The second number.

        Returns:
            float: The product of a and b.
        """
        return a * b

    @staticmethod
    def divide(a: float, b: float) -> float:
        """
        Divides two numbers.

        Args:
            a (float): The dividend.
            b (float): The divisor.

        Returns:
            float: The quotient of a and b.

        Raises:
            ZeroDivisionError: If b is zero.
        """
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return a / b

    @staticmethod
    def factorial(n: int) -> int:
        """
        Calculates the factorial of a number.

        Args:
            n (int): The number.

        Returns:
            int: The factorial of n.

        Raises:
            ValueError: If n is negative.
        """
        if n < 0:
            raise ValueError("n must be a non-negative integer")
        return math_factorial(n)

    @staticmethod
    def power(a: float, b: float) -> float:
        """
        Raises a number to a power.

        Args:
            a (float): The base.
            b (float): The exponent.

        Returns:
            float: a to the power of b.
        """
        return a ** b


def add(a: float, b: float) -> float:
    """
    Adds two numbers using the Calculator class.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The sum of a and b.
    """
    return Calculator.add(a, b)


def subtract(a: float, b: float) -> float:
    """
    Subtracts two numbers using the Calculator class.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The difference of a and b.
    """
    return Calculator.subtract(a, b)


def multiply(a: float, b: float) -> float:
    """
    Multiplies two numbers using the Calculator class.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The product of a and b.
    """
    return Calculator.multiply(a, b)


def divide(a: float, b: float) -> float:
    """
    Divides two numbers using the Calculator class.

    Args:
        a (float): The dividend.
        b (float): The divisor.

    Returns:
        float: The quotient of a and b.
    """
    return Calculator.divide(a, b)


def calculator(initial_value: float = 0) -> Calculator:
    """
    Creates a new Calculator instance.

    Args:
        initial_value (float): The initial value. Defaults to 0.

    Returns:
        Calculator: A new Calculator instance.
    """
    return Calculator(initial_value)


def factorial(n: int) -> int:
    """
    Calculates the factorial of a number using the Calculator class.

    Args:
        n (int): The number.

    Returns:
        int: The factorial of n.
    """
    return Calculator.factorial(n)


def power(a: float, b: float) -> float:
    """
    Raises a number to a power using the Calculator class.

    Args:
        a (float): The base.
        b (float): The exponent.

    Returns:
        float: a to the power of b.
    """
    return Calculator.power(a, b)


def main():
    """
    The main function.
    """
    calculator_instance = calculator()
    print(calculator_instance.add(5, 3))  # Output: 8
    print(calculator_instance.subtract(5, 3))  # Output: 2
    print(calculator_instance.multiply(5, 3))  # Output: 15
    print(calculator_instance.divide(6, 3))  # Output: 2.0


if __name__ == "__main__":
    main()