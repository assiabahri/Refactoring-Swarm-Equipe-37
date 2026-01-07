import non_existent_module  # This doesn't exist!

def use_json():
    data = json.loads('{"test": "data"}')  # json not imported!
    return data

use_json()