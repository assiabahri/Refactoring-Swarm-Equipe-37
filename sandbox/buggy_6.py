def countdown(n):
    """This function has potential infinite loop"""
    while n > 0:
        print(f"Count: {n}")
        # Oops! Forgot to decrement n
        # n = n - 1  # This line is missing!
    return "Done"

# This will run forever if called
# countdown(5)

def another_infinite():
    i = 0
    while i < 10:
        print(f"i = {i}")
        # Wrong condition - i is never modified
        if i == 5:
            print("Halfway there!")
        # i += 1  # This should be here

another_infinite()