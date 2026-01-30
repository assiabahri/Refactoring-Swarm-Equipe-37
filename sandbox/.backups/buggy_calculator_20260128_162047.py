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

    def add(self, a: float) -> None:
        """
        Adds a number to the current value.

        Args:
            a (float): The number to add.
        """
        self.value += a

    def subtract(self, a: float) -> None:
        """
        Subtracts a number from the current value.

        Args:
            a (float): The number to subtract.
        """
        self.value -= a

    def multiply(self, a: float) -> None:
        """
        Multiplies the current value by a number.

        Args:
            a (float): The number to multiply by.
        """
        self.value *= a

    def divide(self, a: float) -> None:
        """
        Divides the current value by a number.

        Args:
            a (float): The number to divide by.

        Raises:
            ZeroDivisionError: If a is zero.
        """
        if a == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        self.value /= a

    @staticmethod
    def add_static(a: float, b: float) -> float:
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
    def subtract_static(a: float, b: float) -> float:
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
    def multiply_static(a: float, b: float) -> float:
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
    def divide_static(a: float, b: float) -> float:
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
    return Calculator.add_static(a, b)


def subtract(a: float, b: float) -> float:
    """
    Subtracts two numbers using the Calculator class.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The difference of a and b.
    """
    return Calculator.subtract_static(a, b)


def multiply(a: float, b: float) -> float:
    """
    Multiplies two numbers using the Calculator class.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The product of a and b.
    """
    return Calculator.multiply_static(a, b)


def divide(a: float, b: float) -> float:
    """
    Divides two numbers using the Calculator class.

    Args:
        a (float): The dividend.
        b (float): The divisor.

    Returns:
        float: The quotient of a and b.
    """
    return Calculator.divide_static(a, b)


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
    calculator_instance.add(5)
    calculator_instance.add(3)
    print(calculator_instance.get_value())  # Output: 8
    calculator_instance = calculator(5)
    calculator_instance.subtract(3)
    print(calculator_instance.get_value())  # Output: 2
    calculator_instance = calculator(5)
    calculator_instance.multiply(3)
    print(calculator_instance.get_value())  # Output: 15
    calculator_instance = calculator(6)
    calculator_instance.divide(3)
    print(calculator_instance.get_value())  # Output: 2.0


if __name__ == "__main__":
    main()