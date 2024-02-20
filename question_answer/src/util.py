import os

def get_absolute_path(relative_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    absolute_path = os.path.join(script_dir, relative_path)
    return os.path.abspath(absolute_path)