import os
from config import MAX_CHARACTERS

def get_file_content(working_directory: str, file_path: str):
    
    absolute_path = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(absolute_path, file_path))
    valid_file = os.path.commonpath([absolute_path, target_path]) == absolute_path
    if not valid_file: return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_path): return f'Error: File not found or is not a regular file: "{file_path}"'

    with open(target_path, "r") as file:
        try: 
            new_file = file.read(MAX_CHARACTERS)
            if file.read(1):
                new_file += f'[...File "{file_path}" truncated at {MAX_CHARACTERS} characters]'
        except ValueError: return 'Error: value given at file path didnt read anything'
        except Exception: return f"Error: {target_path} didnt reach to any value or error was made in the process"
    
    return new_file