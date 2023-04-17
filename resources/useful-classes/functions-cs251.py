import json
import os

# ===============================================================================================
def print_dict(dict, title=''):
    """ Display a dictionary in a structured format """
    if title != '':
        print(f'Dictionary: {title}')
    print(json.dumps(dict, indent=3))


# ===============================================================================================
def load_json_file(filename):
    if os.path.exists(filename):
        with open(filename) as json_file: 
            data = json.load(json_file)
        return data
    else:
        return {}
