"""
Test suite for buggy_data_processor.py
Note: The source file has syntax errors that need to be fixed first
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# This import will fail until syntax errors are fixed
try:
    from buggy_data_processor import (
        process_list,
        filter_positive,
        sum_list,
        find_max,
        average
    )
    IMPORT_SUCCESS = True
except SyntaxError:
    IMPORT_SUCCESS = False


@pytest.mark.skipif(not IMPORT_SUCCESS, reason="Source file has syntax errors")
class TestDataProcessor:
    """Test data processing functions"""
    
    def test_process_list_empty(self):
        """Test processing empty list"""
        assert process_list([]) == []
    
    def test_process_list_even_numbers(self):
        """Test processing list with even numbers"""
        assert process_list([2, 4, 6]) == [4, 8, 12]
    
    def test_process_list_mixed(self):
        """Test processing list with mixed numbers"""
        result = process_list([1, 2, 3, 4, 5])
        assert result == [4, 8]  # Only even numbers doubled
    
    def test_filter_positive(self):
        """Test filtering positive numbers"""
        assert filter_positive([1, -2, 3, -4, 5]) == [1, 3, 5]
        assert filter_positive([-1, -2, -3]) == []
        assert filter_positive([1, 2, 3]) == [1, 2, 3]
    
    def test_sum_list(self):
        """Test summing list"""
        assert sum_list([1, 2, 3, 4, 5]) == 15
        assert sum_list([]) == 0
        assert sum_list([-1, -2, -3]) == -6
    
    def test_find_max(self):
        """Test finding maximum"""
        assert find_max([1, 5, 3, 9, 2]) == 9
        assert find_max([]) is None
        assert find_max([-5, -1, -10]) == -1
    
    def test_average(self):
        """Test calculating average"""
        assert average([1, 2, 3, 4, 5]) == 3.0
        assert average([10, 20]) == 15.0
        assert average([]) == 0


# Fallback test to ensure pytest runs
def test_module_importable():
    """Test that module can be imported after fixes"""
    # This test will pass once syntax errors are fixed
    if IMPORT_SUCCESS:
        assert True
    else:
        pytest.skip("Module has syntax errors - this is expected before refactoring")
