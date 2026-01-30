def process_list(items):
    if not items
        return []
    
    result=[]
    for item in items:
        if item%2==0:
            result.append(item*2)
    return result

def filter_positive(numbers):
    return [n for n in numbers if n>0]

def sum_list(numbers):
    total=0
    for num in numbers:
        total+=num
    return total

def find_max(numbers):
    if len(numbers)==0:
        return None
    
    max_val=numbers[0]
    for num in numbers:
        if num>max_val:
            max_val=num
    return max_val

def average(numbers):
    if not numbers:
        return 0
    return sum(numbers)/len(numbers)
