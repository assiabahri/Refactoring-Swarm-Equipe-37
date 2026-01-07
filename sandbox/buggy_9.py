def calculate_grade(score):
    """Function missing return in some branches"""
    if score >= 90:
        grade = "A"
        # Oops! Forgot return statement here
    elif score >= 80:
        grade = "B"
        return grade
    elif score >= 70:
        grade = "C"
        # No return here either
    elif score >= 60:
        grade = "D"
        return grade
    else:
        grade = "F"
    # Only returns if score < 60
    
    # This line only runs for scores >= 90 and >= 70
    return f"Grade: {grade}"

def process_user_input(user_input):
    """Another missing return example"""
    if not user_input:
        print("No input provided")
        # Should return None or raise error
    
    cleaned = user_input.strip().lower()
    
    if cleaned == "yes":
        result = True
    elif cleaned == "no":
        result = False
    elif cleaned == "maybe":
        result = None
    else:
        print(f"Unknown input: {cleaned}")
        # Missing return for unknown input
    
    # This might return undefined 'result' for empty input
    return result

def find_maximum(numbers):
    """Edge case missing return"""
    if not numbers:
        print("Empty list provided")
        # Should return None or raise ValueError
    
    max_val = numbers[0]
    for num in numbers[1:]:
        if num > max_val:
            max_val = num
    
    # This line runs even for empty lists
    return max_val

# Test the functions
print(calculate_grade(95))  # Returns None for A grade
print(process_user_input(""))  # Might crash
print(find_maximum([]))  # Will crash with IndexError