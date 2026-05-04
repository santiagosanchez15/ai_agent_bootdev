import os
def write_file(working_directory: str, file_path: str, content: str) -> str:
    '''Write a file by given arguments 
    working_directory: where the file is located
    file_path: file path to the file inside the working directory
    content: content wanted to be added

    updates the file with given content
    '''
    
    absolute_path = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(absolute_path, file_path))
    valid_file = os.path.commonpath([absolute_path, target_path]) == absolute_path
    if not valid_file: return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_path): return f'Error: Cannot write to "{file_path}" as it is a directory'
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    
    #open file and write 
    with open(target_path, "w") as file:
        try: 
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except ValueError: return 'Error: given value is not taken'
        except Exception: return 'Error: given data broke the code, please try again'