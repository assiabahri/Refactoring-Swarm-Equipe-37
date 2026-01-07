def check_number(num):
if num > 0:  # Missing indentation
    return "Positive"
  elif num < 0:  # Inconsistent indentation
        return "Negative"
    else:  # Wrong indentation level
    return "Zero"

def process_data(data_list):
    result = []
for item in data_list:  # Should be indented
        if item % 2 == 0:
            result.append(item * 2)
        else:
    result.append(item * 3)  # Wrong indentation
            # Extra indented comment
                # Too much indentation here
    return result

def nested_example(x):
    if x > 10:
        print("Greater than 10")
    if x > 20:
            print("Greater than 20")  # Inconsistent
        if x > 30:
        print("Greater than 30")  # Wrong
    else:
    print("30 or less")  # Wrong

# Mixed tabs and spaces (invisible but causes issues)
def tabs_and_spaces():
    if True:
        print("This line uses spaces")  # 4 spaces
    if True:
        print("This might use a tab")    # Tab character (invisible)
    return "Done"