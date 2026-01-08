from buggy_1 import calculate_sum 

def test_calculate_sum():
    # Basic test cases
    assert calculate_sum(5, 10) == 15
    assert calculate_sum(-3, 3) == 0
    assert calculate_sum(0, 0) == 0
