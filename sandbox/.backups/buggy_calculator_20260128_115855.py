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


def main():
    calculator = Calculator()
    print(calculator.add(5, 3))  # Output: 8
    print(calculator.subtract(5, 3))  # Output: 2
    print(calculator.multiply(5, 3))  # Output: 15
    print(calculator.divide(6, 3))  # Output: 2.0


if __name__ == "__main__":
    main()