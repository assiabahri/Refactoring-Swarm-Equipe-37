"""
Test suite for buggy_calculator.py
These tests should pass after refactoring
"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent))

from buggy_calculator import add, subtract, multiply, divide, calculator, factorial, power


class TestBasicOperations:
    """Test basic arithmetic operations"""
    
    def test_add_positive_numbers(self):
        """Test adding positive numbers"""
        assert add(2, 3) == 5
        assert add(10, 20) == 30
    
    def test_add_negative_numbers(self):
        """Test adding negative numbers"""
        assert add(-5, -3) == -8
        assert add(-10, 5) == -5
    
    def test_subtract(self):
        """Test subtraction"""
        assert subtract(10, 5) == 5
        assert subtract(0, 5) == -5
    
    def test_multiply(self):
        """Test multiplication"""
        assert multiply(3, 4) == 12
        assert multiply(-2, 5) == -10
        assert multiply(0, 100) == 0
    
    def test_divide(self):
        """Test division"""
        assert divide(10, 2) == 5
        assert divide(9, 3) == 3
    
    def test_divide_by_zero(self):
        """Test division by zero raises error"""
        with pytest.raises(ZeroDivisionError):
            divide(10, 0)


class TestCalculatorClass:
    """Test calculator class"""
    
    def test_calculator_init(self):
        """Test calculator initialization"""
        calc = calculator(10)
        assert calc.get_value() == 10
    
    def test_calculator_add(self):
        """Test calculator add method"""
        calc = calculator(5)
        result = calc.add(3)
        assert result == 8
        assert calc.get_value() == 8
    
    def test_calculator_multiple_operations(self):
        """Test multiple operations"""
        calc = calculator(0)
        calc.add(5)
        calc.add(10)
        assert calc.get_value() == 15


class TestAdvancedFunctions:
    """Test advanced mathematical functions"""
    
    def test_factorial_base_case(self):
        """Test factorial of 0"""
        assert factorial(0) == 1
    
    def test_factorial_positive(self):
        """Test factorial of positive numbers"""
        assert factorial(1) == 1
        assert factorial(5) == 120
        assert factorial(3) == 6
    
    def test_power_basic(self):
        """Test power function"""
        assert power(2, 3) == 8
        assert power(5, 2) == 25
        assert power(10, 0) == 1
    
    def test_power_edge_cases(self):
        """Test power edge cases"""
        assert power(0, 5) == 0
        assert power(1, 100) == 1
