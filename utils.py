import os

def get_absolute_path(filename):
    # Get the directory of the current .py file
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Build the full path to the file
    file_path = os.path.join(base_dir, filename)

    return file_path
