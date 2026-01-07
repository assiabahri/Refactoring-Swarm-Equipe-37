def process_data(data):
    """Function using undefined variables"""
    # 'processed' is not defined before use
    for item in data:
        processed.append(item * 2)  # 'processed' is undefined!
    
    # 'threshold' is undefined
    filtered = [x for x in processed if x > threshold]
    
    # 'result' is defined but 'summary' is not
    result = sum(filtered) / len(filtered)
    final_output = result + summary  # 'summary' is undefined
    
    return final_output

def calculate_stats():
    """Another undefined variables example"""
    numbers = [1, 2, 3, 4, 5]
    
    # Using undefined function
    avg = calculate_average(numbers)  # 'calculate_average' not defined
    
    # Using undefined constant
    normalized = [x / MAX_VALUE for x in numbers]  # 'MAX_VALUE' not defined
    
    return normalized

def handle_user(user_data):
    """Complex undefined variables"""
    # 'user_id' might not exist in user_data
    uid = user_data['user_id']  # KeyError if missing
    
    # 'config' is undefined
    if uid in config['allowed_users']:  # 'config' not defined
        access = True
    else:
        access = False
    
    # 'logger' is undefined
    logger.info(f"User {uid} access: {access}")  # 'logger' not defined
    
    return access

# Global scope undefined variables
def global_issues():
    # Using undefined global variable
    global_value = DEFAULT_SETTING * 2  # 'DEFAULT_SETTING' not defined
    
    # Calling undefined function
    processed = format_output(global_value)  # 'format_output' not defined
    
    return processed

# Test the functions (these will crash)
data = [1, 2, 3]
# print(process_data(data))  # Will crash: NameError

user_info = {"name": "Alice"}  # Missing 'user_id' key
# print(handle_user(user_info))  # Will crash: KeyError

# print(calculate_stats())  # Will crash: NameError
# print(global_issues())   # Will crash: NameError

# This variable is defined too late
LATE_DEFINITION = 100