from math import factorial as math_factorial

class Calculator:
    """
    A simple calculator class.
    """

    def add(self, a: float, b: float) -> float:
        """
        Adds two numbers.

        Args:
            a (float): The first number.
            b (float): The second number.

        Returns:
            float: The sum of a and b.
        """
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """
        Subtracts two numbers.

        Args:
            a (float): The first number.
            b (float): The second number.

        Returns:
            float: The difference of a and b.
        """
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """
        Multiplies two numbers.

        Args:
            a (float): The first number.
            b (float): The second number.

        Returns:
            float: The product of a and b.
        """
        return a * b

    def divide(self, a: float, b: float) -> float:
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

    def factorial(self, n: int) -> int:
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

    def power(self, a: float, b: float) -> float:
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
    calculator = Calculator()
    return calculator.add(a, b)


def subtract(a: float, b: float) -> float:
    calculator = Calculator()
    return calculator.subtract(a, b)


def multiply(a: float, b: float) -> float:
    calculator = Calculator()
    return calculator.multiply(a, b)


def divide(a: float, b: float) -> float:
    calculator = Calculator()
    return calculator.divide(a, b)


def calculator(initial_value: float = 0) -> Calculator:
    calc = Calculator()
    return calc


def factorial(n: int) -> int:
    calculator = Calculator()
    return calculator.factorial(n)


def power(a: float, b: float) -> float:
    calculator = Calculator()
    return calculator.power(a, b)


def main():
    calculator = Calculator()
    print(calculator.add(5, 3))  # Output: 8
    print(calculator.subtract(5, 3))  # Output: 2
    print(calculator.multiply(5, 3))  # Output: 15
    print(calculator.divide(6, 3))  # Output: 2.0


if __name__ == "__main__":
    main()